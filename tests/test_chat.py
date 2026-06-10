from httpx import ASGITransport, AsyncClient
import pytest

from app.api.deps import get_chat_service
from app.main import app
from app.providers.base import LLMProvider
from app.schemas.chat import AssistantMessage, ChatCompletionRequest, ChatMessage, MessageRole, TokenUsage
from app.services.chat_service import ChatService


class FakeProvider(LLMProvider):
    @property
    def name(self) -> str:
        return "groq"

    @property
    def model(self) -> str:
        return "fake-model"

    async def generate(self, messages, system_prompt):
        last_message = messages[-1].content
        return (
            AssistantMessage(content=f"Resposta simulada para: {last_message}"),
            TokenUsage(prompt_tokens=10, completion_tokens=20, total_tokens=30),
        )


@pytest.fixture
def client():
    app.dependency_overrides[get_chat_service] = lambda: ChatService(provider=FakeProvider())
    transport = ASGITransport(app=app)
    yield AsyncClient(transport=transport, base_url="http://test")
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_chat_completion_requires_api_key(client):
    response = await client.post(
        "/api/v1/chat/completions",
        json={
            "messages": [{"role": "user", "content": "Olá"}],
        },
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_chat_completion_rejects_invalid_api_key(client):
    response = await client.post(
        "/api/v1/chat/completions",
        headers={"X-API-Key": "chave-errada"},
        json={
            "messages": [{"role": "user", "content": "Olá"}],
        },
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_chat_completion_returns_assistant_message(client):
    response = await client.post(
        "/api/v1/chat/completions",
        headers={"X-API-Key": "test-internal-key"},
        json={
            "messages": [{"role": "user", "content": "Como organizo meus leads?"}],
            "system_context": "Usuário possui 3 leads no status NOVO.",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["message"]["role"] == "assistant"
    assert "Resposta simulada" in data["message"]["content"]
    assert data["provider"] == "groq"
    assert data["usage"]["total_tokens"] == 30


@pytest.mark.asyncio
async def test_get_provider_info(client):
    response = await client.get(
        "/api/v1/chat/provider",
        headers={"X-API-Key": "test-internal-key"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["provider"] == "groq"
    assert data["status"] == "ativo"


@pytest.mark.asyncio
async def test_chat_service_builds_system_prompt_with_context():
    service = ChatService(provider=FakeProvider())
    prompt = service._build_system_prompt("Lead: João Silva")

    assert "SI Soluções Imobiliárias" in prompt
    assert "João Silva" in prompt


@pytest.mark.asyncio
async def test_chat_service_create_completion():
    service = ChatService(provider=FakeProvider())
    request = ChatCompletionRequest(
        messages=[ChatMessage(role=MessageRole.USER, content="Oi")],
    )

    response = await service.create_completion(request)

    assert response.message.content.startswith("Resposta simulada")
    assert response.model == "fake-model"
