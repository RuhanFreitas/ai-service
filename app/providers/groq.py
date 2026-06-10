from groq import AsyncGroq, GroqError

from app.core.config import settings
from app.core.exceptions import ProviderError
from app.providers.base import LLMProvider
from app.schemas.chat import AssistantMessage, ChatMessage, MessageRole, TokenUsage


class GroqProvider(LLMProvider):
    def __init__(self) -> None:
        self._client = AsyncGroq(api_key=settings.groq_api_key)

    @property
    def name(self) -> str:
        return "groq"

    @property
    def model(self) -> str:
        return settings.groq_model

    async def generate(
        self,
        messages: list[ChatMessage],
        system_prompt: str,
    ) -> tuple[AssistantMessage, TokenUsage]:
        payload = [{"role": MessageRole.SYSTEM.value, "content": system_prompt}]
        payload.extend({"role": message.role.value, "content": message.content} for message in messages)

        try:
            response = await self._client.chat.completions.create(
                model=self.model,
                messages=payload,
                temperature=settings.llm_temperature,
                max_tokens=settings.llm_max_tokens,
            )
        except GroqError as error:
            raise ProviderError(f"Falha na comunicação com a Groq: {error}") from error

        choice = response.choices[0]
        content = choice.message.content or ""

        usage = response.usage
        token_usage = TokenUsage(
            prompt_tokens=usage.prompt_tokens if usage else 0,
            completion_tokens=usage.completion_tokens if usage else 0,
            total_tokens=usage.total_tokens if usage else 0,
        )

        return AssistantMessage(content=content.strip()), token_usage
