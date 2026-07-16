# Free LLM Chatbot

A simple chatbot built with **Python, FastAPI, and free LLMs**. It supports both **Ollama** (local models) and **Hugging Face Inference API** (cloud-based free tier).

## Features

- Streaming responses (tokens appear as they are generated)
- Ollama support (offline, free, local inference)
- Hugging Face support (free inference API)
- Conversation memory (last 10 messages)
- Temperature control (0–2)
- Runtime model selection
- List available Ollama models
- Clear conversation history
- Session-based chat support
- Simple HTML + JavaScript frontend

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

- Python 3.9+
- Ollama (for local inference)

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Documentation

- [Installation Guide](docs/INSTALL.md)
- [API Reference](docs/API.md)
- [Configuration](docs/CONFIGURATION.md)