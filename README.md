# AI Browser Automation Agent

A beginner-friendly AI agent that understands a user's browser task, plans safe browser actions, and reports what it found.

## Features
- Search the web using a browser
- Open a URL and read visible page content
- Extract text from the current page
- Fill simple form fields when matching labels/placeholders are found
- Show each browser action and its result in Streamlit

## Tech stack
Python, FastAPI, Streamlit, Playwright, Ollama (Qwen 2.5 3B).

## Requirements
- Python 3.10+
- Ollama installed and running
- Chromium browser installed through Playwright

## Setup on Windows PowerShell

```powershell
cd D:\AI-Projects\ai-browser-automation-agent
python -m venv env
.\env\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install chromium
ollama pull qwen2.5:3b
```

Make sure Ollama is running. In one terminal:

```powershell
ollama serve
```

If Ollama is already running in the background, do not start another instance.

Terminal 2 (backend):

```powershell
cd D:\AI-Projects\ai-browser-automation-agent
.\env\Scripts\Activate.ps1
python -m uvicorn backend.main:app --reload
```

Terminal 3 (frontend):

```powershell
cd D:\AI-Projects\ai-browser-automation-agent
.\env\Scripts\Activate.ps1
streamlit run frontend/app.py
```

Open the Streamlit URL shown in the terminal, usually http://localhost:8501.

## Example prompts
- Search for Python AI internships in Chennai.
- Open https://www.python.org and summarize the page.
- Search for FastAPI tutorials and extract the useful information.
- Open a website with a contact form and fill the name and email fields (only if matching visible labels/placeholders exist).

## Safety and limitations
This is a learning/demo project. It does not submit forms, make purchases/payments, send messages, delete data, enter passwords, bypass authentication, or solve CAPTCHAs. Always review any filled form yourself and submit manually. Website layouts and bot protections may prevent automation. Search results and extracted website content may be incomplete or change over time.

The demo uses a local Ollama model and runs locally; it is not a production-ready secure browser agent.
