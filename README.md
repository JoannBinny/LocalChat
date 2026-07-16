# Free LLM Chatbot

A simple chatbot built with **Python, FastAPI, and free LLMs**. It supports both **Ollama** (local models) and **Hugging Face Inference API** (cloud-based free tier).

## Features

* Streaming responses (tokens appear as they are generated)
* Ollama support (offline, free, local inference)
* Hugging Face support (free inference API)
* Conversation memory (last 10 messages)
* Temperature control (0–2)
* Runtime model selection
* List available Ollama models
* Clear conversation history
* Session-based chat support
* Simple HTML + JavaScript frontend

---

## Project Structure

```text
.
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
└── README.md
```

---

## Requirements

* Python 3.9+
* Ollama (for local inference)

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Setup

### Create a Virtual Environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Linux / macOS:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Option A: Ollama (Recommended)

### Install Ollama

Download and install Ollama from:

https://ollama.com

### Pull a Model

Examples:

```bash
ollama pull phi3
```

```bash
ollama pull llama3
```

```bash
ollama pull mistral
```

### Configure Model

Default model:

```python
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi3")
```

Change this value if you want another installed model.

### Start Ollama

```bash
ollama serve
```

### Run the Application

```bash
python app.py
```

Open:

```text
http://localhost:8000
```

---

## Option B: Hugging Face

### Create an Access Token

Generate a free token from:

https://huggingface.co/settings/tokens

### Set Environment Variables

Windows PowerShell:

```powershell
$env:USE_HF="true"
$env:HF_TOKEN="your_token_here"
```

Linux / macOS:

```bash
export USE_HF=true
export HF_TOKEN=your_token_here
```

### Run the Application

```bash
python app.py
```

Default Hugging Face model:

```python
HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"
```

You may override it through the `HF_MODEL` environment variable.

---

## API Endpoints

### Home Page

```http
GET /
```

Returns the chatbot interface.

---

### Health Check

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

### Available Models

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

### Clear Chat History

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

### Streaming Chat

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

### Standard Chat

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

---

## Configuration

| Variable             | Default                            | Description                 |
| -------------------- | ---------------------------------- | --------------------------- |
| USE_HF               | false                              | Enable Hugging Face backend |
| HF_TOKEN             | ""                                 | Hugging Face API token      |
| HF_MODEL             | mistralai/Mistral-7B-Instruct-v0.2 | HF model                    |
| OLLAMA_BASE_URL      | http://localhost:11434             | Ollama server URL           |
| OLLAMA_MODEL         | phi3                               | Local Ollama model          |
| MAX_HISTORY_MESSAGES | 10                                 | Conversation memory size    |

---

## Notes

* Ollama works completely offline after downloading a model.
* Hugging Face requires an internet connection and API token.
* Conversation history is stored in memory and is cleared when the server restarts.
* Streaming mode provides faster user experience because responses appear as they are generated.
* Runtime model selection is supported through the API.
