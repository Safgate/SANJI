 #!/usr/bin/env python3
"""
FastAPI entry point for the Jarvis‑style AI assistant.
It exposes:
* POST /chat   – receive a user message, run the LangChain agent, and return the response.
* GET  /health – simple health check.
* (Future) /screen – live screen stream endpoint.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# ----------------------------------------------------------------------
# Agent setup (LangChain + tools).  This is a minimal version; you can
# extend it with memory, screen‑capture, etc.  The code mirrors the
# standalone REPL example but is callable from the API.
# ----------------------------------------------------------------------
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI   # replace with local LLM wrapper if desired
import pathlib, subprocess

def read_file(path: str) -> str:
    """Read a text file and return its contents."""
    try:
        return pathlib.Path(path).read_text()
    except Exception as e:
        return f"Error reading {path}: {e}"

def write_file(path: str, content: str) -> str:
    """Write content to a file, overwriting if it exists."""
    try:
        pathlib.Path(path).write_text(content)
        return f"Wrote {len(content)} characters to {path}"
    except Exception as e:
        return f"Error writing {path}: {e}"

def run_cmd(cmd: str) -> str:
    """Execute a shell command safely."""
    dangerous = ["rm -rf", "dd if=", "mkfs", ":(){ :|:& };:"]
    if any(d in cmd for d in dangerous):
        return "⚠️ Blocked dangerous command. Ask for explicit approval."
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=30
        )
        return result.stdout + ("\n" if result.stderr else "") + result.stderr
    except subprocess.TimeoutExpired:
        return "Command timed out."
    except Exception as e:
        return f"Command execution error: {e}"

tools = [
    Tool(name="read_file", func=read_file,
         description="Read a text file and return its contents."),
    Tool(name="write_file", func=write_file,
         description="Write content to a file, overwriting if it exists."),
    Tool(name="run_cmd", func=run_cmd,
         description="Execute a shell command and return its output."),
]

llm = OpenAI(model="gpt-4o")
agent = initialize_agent(
    tools, llm, agent_type="openai-functions", verbose=False
)

app = FastAPI(title="Jarvis Assistant API")

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    try:
        reply = agent.run(req.message)
        return ChatResponse(reply=reply)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)