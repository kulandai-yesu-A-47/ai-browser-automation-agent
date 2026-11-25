import json
import requests
from . import browser_tools

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5:3b"

SYSTEM_PROMPT = """
You are a safe browser automation assistant.
Choose exactly one action per response as JSON:
{"action":"search_web","query":"..."}
{"action":"open_page","url":"https://..."}
{"action":"extract_page_text"}
{"action":"fill_form","fields":{"placeholder or label":"value"}}
{"action":"done","message":"..."}
Only use the tools for the user's explicit request. Never submit forms, click purchase/pay/send/delete buttons,
enter passwords, bypass login, or solve CAPTCHAs. If a form is filled, tell the user to review and submit manually.
Return JSON only. Do not invent URLs; use search_web first when needed.
"""

def _ask_ollama(messages):
    response = requests.post(
        OLLAMA_URL,
        json={"model": MODEL, "messages": messages, "stream": False, "format": "json"},
        timeout=120,
    )
    response.raise_for_status()
    return response.json()["message"]["content"]

def run_agent(task: str):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": task},
    ]
    history = []
    for _ in range(5):
        raw = _ask_ollama(messages)
        try:
            plan = json.loads(raw)
        except json.JSONDecodeError:
            return {"reply": raw, "steps": history}
        action = plan.get("action", "done")
        try:
            if action == "search_web":
                result = browser_tools.search_web(plan.get("query", task))
            elif action == "open_page":
                result = browser_tools.open_page(plan.get("url", ""))
            elif action == "extract_page_text":
                result = browser_tools.extract_page_text()
            elif action == "fill_form":
                result = browser_tools.fill_form(plan.get("fields", {}))
            else:
                return {"reply": plan.get("message", "Task finished."), "steps": history}
        except Exception as exc:
            result = {"error": str(exc)}
        history.append({"action": action, "result": result})
        messages.append({"role": "assistant", "content": raw})
        messages.append({
            "role": "user",
            "content": "Tool result:\n" + json.dumps(result, ensure_ascii=False) +
                       "\nContinue if needed. Otherwise return action done with a concise summary."
        })
    return {"reply": "Stopped after 5 safe browser steps. Review the results below.", "steps": history}
