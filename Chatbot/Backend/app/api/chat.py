import re
from fastapi import APIRouter, HTTPException
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.gemini_service import GeminiService
from app.services.local_llm_service import LocalLLMService
from app.core.config import get_settings
from app.utils.prompt_templates import LEGAL_RESTRICTION_MSG, SPECIFY_ACT_MSG, LEGAL_DISCLAIMER
from app.utils.language_utils import detect_language

router = APIRouter()
settings = get_settings()

# Initialize services
gemini_service = GeminiService()
local_llm_service = LocalLLMService()

def is_legal_query(text: str) -> bool:
    """
    STRICT CHECK: Proceed ONLY if the user mentions at least ONE of the following:
    • IPC / ipc / I.P.C
    • Section / Sec / s. + number
    • Act name
    • Case law or court reference
    """
    text_lower = text.lower()
    
    # 1. Section check: "section 302", "sec 302", "s.302"
    if re.search(r'(?:section|sec|s\.|u/s)\s*\d+', text_lower):
        return True
    
    # 2. Specific Act/Legal keywords check (using word boundaries to avoid false positives)
    legal_identifiers = [
        r"\bipc\b", r"\bi\.p\.c\b", r"\bbns\b", r"\bcrpc\b", r"\bbnss\b", r"\bcpc\b", 
        r"\bact\b", r"\bconstitution\b", r"\bcase law\b", r"\bcourt\b", r"\bprovision\b", 
        r"\bbharatiya nyaya\b", r"\bsakshya\b", r"\bnyaya sanhita\b"
    ]
    if any(re.search(pattern, text_lower) for pattern in legal_identifiers):
        return True
        
    return False

def extract_acts_and_sections(text: str):
    """Extraction logic for Acts and Sections."""
    text_lower = text.lower()
    # Matches "302", "302A", etc.
    sections = re.findall(r'(?:section|sec|s\.|u/s)\s*(\d+[A-Z]?)', text_lower)
    acts = re.findall(r'(ipc|bns|crpc|bnss|cpc|evidence act|constitution|nyaya sanhita|sakshya)', text_lower)
    return acts, sections


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Orchestrated chat endpoint with strict legal domain enforcement and fallback.
    """
    question = request.question
    
    # 1. Domain Restriction Check
    if not is_legal_query(question):
        return ChatResponse(
            answer=LEGAL_RESTRICTION_MSG,
            provider="System",
            disclaimer=LEGAL_DISCLAIMER
        )
    
    # 2. Act/Section Specification Check
    acts, sections = extract_acts_and_sections(question)
    if not acts and not sections:
        return ChatResponse(
            answer=SPECIFY_ACT_MSG,
            provider="System",
            disclaimer=LEGAL_DISCLAIMER
        )

    try:
        # 3. Check Local Database (Primary Source)
        # We check if context can be found in the local service
        context = local_llm_service._get_relevant_context(question)
        
        if context:
            # Acts folder found -> Local LLM
            response_text = await local_llm_service.get_response(question, context=context)
            provider = f"Local ({settings.LOCAL_LLM_MODEL})"
        else:
            # Acts folder missing -> Google Gemini Fallback
            response_text = await gemini_service.get_response(question, is_fallback=True)
            provider = "Gemini (Fallback)"
        
        return ChatResponse(
            answer=response_text,
            provider=provider,
            disclaimer=LEGAL_DISCLAIMER
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

