# Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| OLLAMA_BASE_URL | http://localhost:11434 | Ollama server URL |
| OLLAMA_MODEL | phi3 | Local Ollama model |
| MAX_HISTORY_MESSAGES | 10 | Conversation memory size |

---

## Notes

- Ollama works completely offline after downloading a model.
- Conversation history is stored in memory and is cleared when the server restarts.
- Streaming mode provides faster user experience because responses appear as they are generated.
- Runtime model selection is supported through the API.
