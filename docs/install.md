# Installation Guide

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

# Option A: Ollama (Recommended)

## Install Ollama

Download and install Ollama from:

https://ollama.com

## Pull a Model

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

## Configure Model

Default model:

```python
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi3")
```

Change this value if you want another installed model.

## Start Ollama

```bash
ollama serve
```

## Run the Application

```bash
python app.py
```

Open:

```text
http://localhost:8000
```

---

# Option B: Hugging Face

## Create an Access Token

Generate a free token from:

https://huggingface.co/settings/tokens

## Set Environment Variables

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

## Run the Application

```bash
python app.py
```

Default Hugging Face model:

```python
HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"
```

You may override it through the `HF_MODEL` environment variable.