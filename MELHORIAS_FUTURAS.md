# Melhorias futuras — AI Service

Ideias visando melhorias futuras e escalabilidade.

---

## Curto prazo

- **Streaming** — resposta aparecendo aos poucos no chat, como no ChatGPT
- **Rate limiting** — limitar mensagens por minuto para evitar abuso e controlar custo
- **Cache** — guardar respostas de perguntas frequentes por alguns minutos
- **Logs estruturados** — registrar tempo de resposta, tokens usados e erros em JSON

---

## Médio prazo

- **Mais provedores** — OpenAI como fallback, Ollama para rodar local
- **Fallback automático** — se Groq falhar, tentar outro provedor antes de dar erro
- **Métricas** — tempo médio de resposta, tokens/dia, taxa de erro (Prometheus, Datadog)
- **Fila com Redis** — enfileirar mensagens em pico de uso e responder via WebSocket

---

## Longo prazo

- **Escalar horizontalmente** — várias instâncias atrás de um load balancer (serviço não guarda estado)
- **Function calling** — assistente executar ações reais: "mostre meus leads novos", "agende visita"
- **RAG** — buscar em manuais e FAQs internos antes de responder
- **Deploy em nuvem** — Railway, Render, Cloud Run ou Kubernetes conforme o volume

---

## Segurança

| Hoje | Futuro |
|---|---|
| Chave interna fixa | Rotação automática de chaves |
| Sem rate limit | Limite por usuário/IP |
| CORS básico | Restringir origens só ao backend em produção |

---

## Prioridade sugerida

1. Integrar com o `server` e validar fluxo completo no `web`
2. Streaming e rate limiting, se sobrar tempo
3. Demais itens conforme necessidade real de escala
