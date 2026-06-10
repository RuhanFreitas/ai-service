from enum import Enum

from pydantic import BaseModel, Field


class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class ChatMessage(BaseModel):
    role: MessageRole
    content: str = Field(min_length=1, max_length=8000)


class ChatCompletionRequest(BaseModel):
    messages: list[ChatMessage] = Field(min_length=1, max_length=50)
    system_context: str | None = Field(
        default=None,
        max_length=4000,
        description="Contexto extra enviado pelo backend (leads, imóveis, etc.).",
    )


class AssistantMessage(BaseModel):
    role: MessageRole = MessageRole.ASSISTANT
    content: str


class TokenUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionResponse(BaseModel):
    message: AssistantMessage
    model: str
    provider: str
    usage: TokenUsage


class HealthResponse(BaseModel):
    status: str
    service: str
    provider: str
    model: str


class ProviderInfoResponse(BaseModel):
    provider: str
    model: str
    status: str
