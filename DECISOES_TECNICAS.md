# Decisões técnicas — AI Service

Por que escolhi cada tecnologia e abordagem neste microsserviço.

---

## Groq

Rápida, com plano gratuito generoso e boa resposta em português. OpenAI tem qualidade similar, mas custo maior. Ollama roda local, mas complica a avaliação do case. A pasta `providers/` permite trocar o provedor depois sem reescrever tudo.

---

## Sem banco de dados

Este serviço só transforma mensagens em respostas. Quem guarda histórico é o backend, que já usa PostgreSQL. Menos complexidade e mais fácil de escalar. Dá para subir várias instâncias sem compartilhar estado.

---

## Backend como gateway

O frontend nunca fala com a IA direto. O backend valida o login, monta o contexto com dados reais do banco e protege a chave da Groq.

---

## Autenticação com X-API-Key

Comunicação serviço-a-serviço, não usuário-a-serviço. Simples e suficiente para o case. Em produção, poderia evoluir para mTLS ou tokens rotativos.

---

## System prompt + contexto dinâmico

O comportamento fixo do assistente (tom, idioma, limites) fica em `prompts.py`. O contexto que muda a cada conversa (leads, imóveis) vem do backend via campo `system_context`.

---

## Testes com provedor simulado

Os testes usam um `FakeProvider` em vez de chamar a Groq de verdade. Rápido, gratuito e funciona no CI sem API key.

---

## Docker no próprio repositório

Cada serviço tem seu `Dockerfile` e `docker-compose.yml`. Quem clona só o ai-service consegue rodar com um comando, sem depender de uma pasta central.

---

## Limites nos schemas

| Limite | Valor |
|---|---|
| Tamanho de uma mensagem | 8.000 caracteres |
| Mensagens por requisição | 50 |
| Contexto extra | 4.000 caracteres |

Evita payloads abusivos e controla custo de tokens na Groq.

---

## Temperatura 0.4

Assistente de CRM precisa ser consistente, não criativo demais. Ajustável via `.env` se quiser testar outros valores.