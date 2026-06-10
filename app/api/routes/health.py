from fastapi import APIRouter

from app.core.config import settings
from app.schemas.chat import HealthResponse

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse, summary="Verifica se o serviço está no ar")
async def health_check() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service=settings.app_name,
        provider=settings.llm_provider,
        model=settings.groq_model,
    )
