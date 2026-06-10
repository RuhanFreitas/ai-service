from app.core.config import settings
from app.core.exceptions import AppError
from app.providers.base import LLMProvider
from app.providers.groq import GroqProvider


def get_llm_provider() -> LLMProvider:
    if settings.llm_provider.lower() == "groq":
        return GroqProvider()

    raise AppError(
        message=f"Provedor de IA '{settings.llm_provider}' não suportado.",
        status_code=500,
    )
