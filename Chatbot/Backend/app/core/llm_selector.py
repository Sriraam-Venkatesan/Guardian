from app.core.config import get_settings
from app.services.gemini_service import GeminiService
from app.services.local_llm_service import LocalLLMService

settings = get_settings()

def get_llm_service():
    """
    Factory function to select the LLM service based on environment configuration.
    """
    provider = settings.LLM_PROVIDER.lower()
    
    if provider == "gemini":
        return GeminiService()
    elif provider == "local":
        return LocalLLMService()
    else:
        # Default fallback or error
        raise ValueError(f"Unsupported LLM provider: {provider}")
