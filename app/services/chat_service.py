from app.providers import get_llm_provider
from app.providers.base import LLMProvider
from app.schemas.chat import ChatCompletionRequest, ChatCompletionResponse
from app.services.prompts import SYSTEM_PROMPT


class ChatService:
    def __init__(self, provider: LLMProvider | None = None) -> None:
        self._provider = provider or get_llm_provider()

    def _build_system_prompt(self, system_context: str | None) -> str:
        if not system_context:
            return SYSTEM_PROMPT

        return f"{SYSTEM_PROMPT}\n\nContexto atual do usuário no sistema:\n{system_context.strip()}"

    async def create_completion(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        system_prompt = self._build_system_prompt(request.system_context)
        message, usage = await self._provider.generate(
            messages=request.messages,
            system_prompt=system_prompt,
        )

        return ChatCompletionResponse(
            message=message,
            model=self._provider.model,
            provider=self._provider.name,
            usage=usage,
        )

    def get_provider_info(self) -> dict[str, str]:
        return {
            "provider": self._provider.name,
            "model": self._provider.model,
            "status": "ativo",
        }
