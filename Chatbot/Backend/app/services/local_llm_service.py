import httpx
import json
import re
import os
from app.core.config import get_settings
from app.utils.prompt_templates import format_prompt

settings = get_settings()

class LocalLLMService:
    def __init__(self):
        self.url = settings.LOCAL_LLM_URL
        self.model = settings.LOCAL_LLM_MODEL
        self.ipc_data = self._load_ipc_data()

    def _load_ipc_data(self):
        """Loads IPC data from JSON files."""
        data = {}
        paths = [
            "d:/Anti/Hackathon/Chatbot/acts/ipc.json",
            "d:/Anti/Hackathon/Chatbot/acts/ipc_extension_part1.json",
            "d:/Anti/Hackathon/Chatbot/acts/ipc_extension_part2.json",
            "d:/Anti/Hackathon/Chatbot/acts/ipc_extension_part3.json"
        ]
        for path in paths:
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        data.update(json.load(f))
                except Exception:
                    pass
        return data

    def _get_relevant_context(self, question: str) -> str:
        """Simple retrieval: find IPC section numbers in the question."""
        # Find numbers like "302", "Section 302", "Sec 302"
        found_sections = re.findall(r'(?:section|sec|u/s)?\s*(\d+[A-Z]?)', question.lower())
        
        context_parts = []
        for sec in found_sections:
            if sec in self.ipc_data:
                item = self.ipc_data[sec]
                context_parts.append(
                    f"IPC Section {sec}: {item.get('title', '')}\n"
                    f"Legal Text: {item.get('legal_text', '')}\n"
                    f"Explanation: {item.get('practical_explanation', '')}"
                )
        
        if context_parts:
            return "\n\nRelevant IPC Provisions:\n" + "\n---\n".join(context_parts)
        return ""

    async def get_response(self, question: str, context: str = "") -> str:
        # Prompt formatted with verified context from local database
        prompt = format_prompt(question, context=context)
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            async with httpx.AsyncClient(timeout=90.0) as client:
                response = await client.post(self.url, json=payload)
                response.raise_for_status()
                data = response.json()
                return data.get("response", "No response from local LLM.")
        except httpx.HTTPError as e:
            return f"Error connecting to local LLM (Ollama): {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"


