from abc import ABC, abstractmethod

from app.schemas.chat import AssistantMessage, ChatMessage, TokenUsage


class LLMProvider(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def model(self) -> str:
        pass

    @abstractmethod
    async def generate(
        self,
        messages: list[ChatMessage],
        system_prompt: str,
    ) -> tuple[AssistantMessage, TokenUsage]:
        pass
