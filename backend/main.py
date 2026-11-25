from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from .agent import run_agent
from .browser_tools import close_browser

app = FastAPI(title="AI Browser Automation Agent", version="1.0.0")

class TaskRequest(BaseModel):
    task: str = Field(min_length=3, max_length=1000)

@app.get("/")
def home():
    return {"message": "AI Browser Automation Agent API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/agent/run")
def run_task(request: TaskRequest):
    try:
        return run_agent(request.task)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@app.post("/browser/close")
def stop_browser():
    close_browser()
    return {"message": "Browser closed"}
