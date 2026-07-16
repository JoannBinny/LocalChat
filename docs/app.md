# API Reference

## Home Page

```http
GET /
```

Returns the chatbot interface.

---

## Health Check

```http
GET /health
```

Returns backend status and active model.

Example:

```json
{
  "status": "ok",
  "backend": "ollama",
  "model": "phi3"
}
```

---

## Available Models

```http
GET /api/models
```

Returns locally installed Ollama models.

Example:

```json
{
  "models": ["phi3", "llama3"],
  "current": "phi3"
}
```

---

## Clear Chat History

```http
POST /api/chat/clear
```

Clears conversation history for the current session.

Response:

```json
{
  "cleared": true
}
```

---

## Streaming Chat

```http
POST /api/chat/stream
```

Streams responses in real time using Server-Sent Events (SSE).

Request:

```json
{
  "message": "Hello",
  "temperature": 0.7
}
```

---

## Standard Chat

```http
POST /api/chat
```

Non-streaming fallback endpoint.

Request:

```json
{
  "message": "Hello",
  "temperature": 0.7
}
```

Response:

```json
{
  "reply": "Hi! How can I help you?",
  "model_used": "phi3",
  "history": [...]
}
```