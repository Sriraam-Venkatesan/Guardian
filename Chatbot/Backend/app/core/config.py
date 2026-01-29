from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "Guardian Legal API"
    DEBUG: bool = True
    
    # LLM Provider: "gemini" or "local"
    LLM_PROVIDER: str = "gemini"
    
    # Google Gemini
    GEMINI_API_KEY: str = ""
    
    # Local LLM (Ollama)
    LOCAL_LLM_URL: str = "http://localhost:11434/api/generate"
    LOCAL_LLM_MODEL: str = "llama2"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
