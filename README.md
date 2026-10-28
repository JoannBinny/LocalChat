<div align="center">

# Free LLM Chatbot

A simple chatbot that runs fully on your own machine. No API keys, no cost.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-local_inference-black)

</div>

<!-- Add a screenshot or demo GIF here, for example: ![Chatbot demo](docs/demo.gif) -->

## Features

Responses stream in token by token, so you see the answer as it is generated.

It runs on Ollama, which means inference is local, offline, and free.

The bot remembers the last 10 messages of the conversation, and each browser session keeps its own chat.

You can change the model while the app is running, see which Ollama models you have installed, adjust the temperature (0 to 2), and clear the conversation at any time.

The frontend is plain HTML and JavaScript, so there is nothing to build.

## Getting started

You'll need Python 3.9+ and [Ollama](https://ollama.com) installed.

**1. Clone the repo**

```bash
git clone https://github.com/JoannBinny/LLM-ChatBot.git
cd LLM-ChatBot
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Pull a model**

```bash
ollama pull llama3
```

Any model from the Ollama library works. You can switch between installed models from the app.

**4. Run the app**

```bash
uvicorn app:app --reload
```

Then open `http://localhost:8000` in your browser.

## Project structure

```
.
├── app.py              FastAPI app and chat logic
├── templates/
│   └── index.html      Chat interface
├── docs/               Install, API, and configuration guides
├── requirements.txt
└── README.md
```

## Documentation

[Installation guide](docs/install.md)

[API reference](docs/app.md)

[Configuration](docs/configuration.md)

## Built with

Python, FastAPI, Ollama, and vanilla JavaScript.
