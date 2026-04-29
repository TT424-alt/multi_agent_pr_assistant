import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # LLM backend selection
    LLM_BACKEND = os.getenv("LLM_BACKEND", "deepseek").lower()

    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

    # Anthropic
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

    # DeepSeek
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")


    # GitHub
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

    # Model names
    MODEL_MAP = {
        "openai": "gpt-5.5",
        "anthropic": "claude-opus-4.6",
        "deepseek": "deepseek-chat",
    }
