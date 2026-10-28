# Free LLM Chatbot

A simple chatbot built with Python, FastAPI, and Ollama.
## Features

- Streaming responses (tokens appear as they are generated)
- Ollama support (offline, free, local inference)
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
├── docs/
    └── app.md
    └── configuration.md
    └── install.md
├── templates/
    └── index.html
├── app.py
├── requirements.txt
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

- [Installation Guide](docs/install.md)
- [API Reference](docs/app.md)
- [Configuration](docs/configuration.md)
