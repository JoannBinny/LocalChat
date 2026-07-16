"""
Chatbot Backend - FastAPI + Ollama / Hugging Face
Improvements over original:
  - Streaming responses (fixes lag — tokens appear as generated)
  - /api/models endpoint (list available Ollama models)
  - /api/chat/clear endpoint (reset session history)
  - Session ID passed as query param (multi-tab safe)
  - Cleaner error messages
"""

import json
import os
from collections import deque
from typing import Optional, AsyncIterator

import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse, StreamingResponse
from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel, Field


# ── Configuration ────────────────────────────────────────────────────────────


OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL    = os.getenv("OLLAMA_MODEL", "phi3")

MAX_HISTORY_MESSAGES = 10   # increased from 5

SYSTEM_PROMPT = (
    "You are a helpful, friendly assistant. "
    "Answer concisely and clearly. "
    "If you don't know something, say so honestly."
)

# ── App setup ─────────────────────────────────────────────────────────────────

app = FastAPI(title="LLM Chatbot", version="2.0.0")

_BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
template_env = Environment(loader=FileSystemLoader(os.path.join(_BASE_DIR, "templates")))

# ── Conversation store ────────────────────────────────────────────────────────

conversation_store: dict[str, deque] = {}


def get_history(session_id: str) -> deque:
    if session_id not in conversation_store:
        conversation_store[session_id] = deque(maxlen=MAX_HISTORY_MESSAGES)
    return conversation_store[session_id]


# ── Request / Response models ─────────────────────────────────────────────────

class ChatRequest(BaseModel):
    message:     str            = Field(..., min_length=1)
    temperature: float          = Field(default=0.7, ge=0.0, le=2.0)
    history:     Optional[list[dict]] = None
    model:       Optional[str]  = None   # override model at runtime


class ChatResponse(BaseModel):
    reply:      str
    model_used: str
    history:    list[dict]


# ── Message builder ───────────────────────────────────────────────────────────

def build_messages(history: deque, new_user_message: str) -> list[dict]:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": new_user_message})
    return messages


# ── Ollama helpers ────────────────────────────────────────────────────────────

async def stream_ollama(messages: list[dict], temperature: float, model: str) -> AsyncIterator[str]:
    """Yield text chunks from Ollama's streaming /api/chat."""
    async with httpx.AsyncClient(timeout=120.0) as client:
        async with client.stream(
            "POST",
            f"{OLLAMA_BASE_URL}/api/chat",
            json={
                "model":   model,
                "messages": messages,
                "stream":  True,
                "options": {"temperature": temperature},
            },
        ) as resp:
            resp.raise_for_status()
            async for line in resp.aiter_lines():
                if not line:
                    continue
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue
                chunk = (data.get("message", {}) or {}).get("content", "")
                if chunk:
                    yield chunk
                if data.get("done"):
                    break


async def call_ollama(messages: list[dict], temperature: float, model: str) -> str:
    """Non-streaming Ollama call (used internally when we need the full reply at once)."""
    chunks = []
    async for chunk in stream_ollama(messages, temperature, model):
        chunks.append(chunk)
    return "".join(chunks)


async def get_ollama_models() -> list[str]:
    """Return list of locally available Ollama model names."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
            r.raise_for_status()
            return [m["name"] for m in r.json().get("models", [])]
    except Exception:
        return []


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def index():
    return template_env.get_template("index.html").render()


@app.get("/health")
async def health():
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            r = await client.get(f"{OLLAMA_BASE_URL}/api/tags")

            if r.status_code != 200:
                return {"status": "degraded", "ollama": "unreachable"}

            return {
                "status": "ok",
                "backend": "ollama",
                "model": OLLAMA_MODEL
            }

    except Exception as e:
        return {"status": "degraded", "ollama": str(e)}


@app.get("/api/models")
async def list_models():
    models = await get_ollama_models()
    return {
        "models": models,
        "current": OLLAMA_MODEL
    }

@app.post("/api/chat/clear")
async def clear_history(session_id: str = "default"):
    """Wipe conversation history for a session."""
    if session_id in conversation_store:
        conversation_store[session_id].clear()
    return {"cleared": True, "session_id": session_id}


@app.post("/api/chat/stream")
async def chat_stream(
    request: ChatRequest,
    session_id: str = Query(default="default"),
):
    """
    Streaming chat endpoint.
    Returns a text/event-stream where each event is a JSON object:
      { "chunk": "..." }        — partial text
      { "done": true, "model_used": "...", "history": [...] }  — final frame
    """
    user_message = request.message.strip()
    temperature  = request.temperature
    history      = get_history(session_id)

    if request.history:
        history.clear()
        for m in request.history[-MAX_HISTORY_MESSAGES:]:
            if m.get("role") in ("user", "assistant") and m.get("content"):
                history.append({"role": m["role"], "content": m["content"]})

    messages = build_messages(history, user_message)

    
    model = request.model or OLLAMA_MODEL
    print("USING MODEL:", model)
    async def event_generator():
        collected = []
        try:
            
            async for chunk in stream_ollama(messages, temperature, model):
                collected.append(chunk)
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"

            full_reply = "".join(collected).strip()
            history.append({"role": "user",      "content": user_message})
            history.append({"role": "assistant", "content": full_reply})

            final = {
                "done":       True,
                "model_used": model,
                "history":    [{"role": m["role"], "content": m["content"]} for m in history],
            }
            yield f"data: {json.dumps(final)}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


# ── Non-streaming fallback ────────────────────────────────────────────────────

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, session_id: str = Query(default="default")):
    """Non-streaming endpoint (kept for compatibility)."""
    user_message = request.message.strip()
    temperature  = request.temperature
    history      = get_history(session_id)

    if request.history:
        history.clear()
        for m in request.history[-MAX_HISTORY_MESSAGES:]:
            if m.get("role") in ("user", "assistant") and m.get("content"):
                history.append({"role": m["role"], "content": m["content"]})

    messages = build_messages(history, user_message)
    model = request.model or OLLAMA_MODEL
    print("Using model:", model)

    reply = await call_ollama(messages, temperature, model)

    history.append({"role": "user",      "content": user_message})
    history.append({"role": "assistant", "content": reply})

    return ChatResponse(
        reply=reply,
        model_used=model,
        history=[{"role": m["role"], "content": m["content"]} for m in history],
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)