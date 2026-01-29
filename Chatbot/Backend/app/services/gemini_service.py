import google.generativeai as genai
from app.core.config import get_settings
from app.utils.prompt_templates import format_prompt

settings = get_settings()

class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')

    async def get_response(self, question: str, is_fallback: bool = False) -> str:
        prompt = format_prompt(question, is_fallback=is_fallback)
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error connecting to Gemini API: {str(e)}"

