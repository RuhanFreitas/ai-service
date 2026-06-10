from fastapi import APIRouter, Depends

from app.api.deps import get_chat_service
from app.core.config import settings
from app.core.security import verify_internal_api_key
from app.schemas.chat import ChatCompletionRequest, ChatCompletionResponse
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post(
    "/completions",
    response_model=ChatCompletionResponse,
    dependencies=[Depends(verify_internal_api_key)],
    summary="Gera uma resposta do assistente",
)
async def create_chat_completion(
    request: ChatCompletionRequest,
    chat_service: ChatService = Depends(get_chat_service),
) -> ChatCompletionResponse:
    return await chat_service.create_completion(request)


@router.get(
    "/provider",
    dependencies=[Depends(verify_internal_api_key)],
    summary="Retorna informações do provedor de IA ativo",
)
async def get_provider_info(
    chat_service: ChatService = Depends(get_chat_service),
) -> dict[str, str]:
    return chat_service.get_provider_info()
