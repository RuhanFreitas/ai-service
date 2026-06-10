# SI AI Service

Microsserviço de IA da SI Soluções Imobiliárias. Ele roda o ChatBot que ajuda usuários com dúvidas sobre leads, imóveis e o fluxo de vendas.

O frontend não acessa este serviço diretamente. Quem chama a IA é o backend (`server`), que valida o usuário logado e envia o contexto da conversa.

Repositórios relacionados:
- [web](https://github.com/RuhanFreitas/web) — frontend
- [server](https://github.com/RuhanFreitas/server) — backend

---

## Tecnologias

| Tecnologia | Uso |
|---|---|
| Python 3.12+ | Linguagem |
| FastAPI | API REST |
| Uvicorn | Servidor |
| Pydantic | Validação de dados |
| Groq SDK | Integração com a IA |
| Pytest | Testes |
| Docker | Container |

---

## Arquitetura

```
web (frontend) → server (backend) → ai-service → Groq API
```

1. Usuário envia mensagem no chat do frontend
2. Backend valida o login e monta o contexto (leads, imóveis)
3. Backend chama este serviço com `X-API-Key`
4. Serviço consulta a Groq e devolve a resposta
5. Backend salva o histórico e repassa ao frontend

A chave da Groq fica só aqui e no backend — nunca no navegador.

---

## Estrutura

```
ai-service/
├── app/
│   ├── main.py                 # Entrada da aplicação
│   ├── api/
│   │   ├── deps.py             # Dependências injetadas
│   │   └── routes/
│   │       ├── chat.py         # Rotas do chat
│   │       └── health.py       # Saúde do serviço
│   ├── core/
│   │   ├── config.py           # Variáveis de ambiente
│   │   ├── exceptions.py       # Erros da aplicação
│   │   └── security.py         # Validação da X-API-Key
│   ├── providers/
│   │   ├── base.py             # Interface do provedor de IA
│   │   ├── groq.py             # Implementação Groq
│   │   └── __init__.py
│   ├── schemas/
│   │   └── chat.py             # Modelos de entrada/saída
│   └── services/
│       ├── chat_service.py     # Lógica do chat
│       └── prompts.py          # Texto base do assistente
├── tests/
│   ├── conftest.py
│   ├── test_chat.py
│   └── test_health.py
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── requirements-dev.txt
```

---

## Rotas

Prefixo: `/api/v1`

| Método | Rota | Auth | Descrição |
|---|---|---|---|
| `GET` | `/health` | Não | Verifica se o serviço está no ar |
| `POST` | `/chat/completions` | Sim | Envia mensagens e recebe resposta do assistente |
| `GET` | `/chat/provider` | Sim | Mostra provedor e modelo ativos |

Rotas protegidas exigem o header:
```
X-API-Key: sua-chave-interna
```

**Exemplo de requisição (`POST /chat/completions`):**
```json
{
  "messages": [
    { "role": "user", "content": "Quantos leads novos eu tenho?" }
  ],
  "system_context": "Usuário possui 3 leads no status NOVO."
}
```

Docs interativas: [http://localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs)

---

## Banco de dados

Este serviço não tem banco próprio. Ele recebe a requisição, gera a resposta e devolve.

O histórico de chat fica no backend (PostgreSQL):

```
ChatSession          ChatMessage
├── id               ├── id
├── userId           ├── sessionId
└── createdAt        ├── role (user | assistant)
                     ├── content
                     └── createdAt
```

---

## Como rodar

### Pré-requisitos
- Python 3.12+
- Chave da [Groq](https://console.groq.com/)
- (Opcional) Docker

### Local

```bash
git clone https://github.com/RuhanFreitas/ai-service.git
cd ai-service
python -m venv .venv

# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements-dev.txt
cp .env.example .env   # **preencha GROQ_API_KEY e INTERNAL_API_KEY**
uvicorn app.main:app --reload --port 8000
```

Testes: `pytest`  
Health check: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)

### Docker

```bash
cp .env.example .env   # preencha as chaves
docker compose up --build
```

---

## Variáveis de ambiente

| Variável | Obrigatória | Descrição |
|---|---|---|
| `INTERNAL_API_KEY` | Sim | Chave que o backend envia no header |
| `GROQ_API_KEY` | Sim | Chave da Groq |
| `GROQ_MODEL` | Não | Modelo (padrão: `llama-3.3-70b-versatile`) |
| `LLM_PROVIDER` | Não | Provedor (padrão: `groq`) |
| `LLM_MAX_TOKENS` | Não | Limite de tokens (padrão: `1024`) |
| `LLM_TEMPERATURE` | Não | Criatividade 0–1 (padrão: `0.4`) |
| `CORS_ORIGINS` | Não | URLs permitidas, separadas por vírgula |


---

## Integração

| Serviço | Papel |
|---|---|
| **server** | Chama `/chat/completions` com `X-API-Key` e contexto do usuário |
| **web** | Não se comunica com este serviço |

O backend deve usar a mesma `INTERNAL_API_KEY` configurada aqui.

---

## Outros documentos

- [Decisões técnicas](./DECISOES_TECNICAS.md)
- [Melhorias futuras](./MELHORIAS_FUTURAS.md)
