# Jarvis‑Style AI Assistant (Python + FastAPI)

This repository provides a minimal **FastAPI**‑based skeleton for a Jarvis‑like AI
assistant that can:

* Access the filesystem (`read_file`, `write_file`).
* Execute shell commands safely (`run_cmd`).
* Control the mouse and launch applications (`click`, `launch_app`).
* Run continuously as a background daemon.

## Quick Start

```bash
# Clone the repository (or copy the files into a new directory)
git clone <repo‑url>
cd <repo‑dir>

# Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server as a background daemon
cd daemon
./run_daemon.sh

# To stop the daemon later
./stop_daemon.sh
```

The API will be available at `http://127.0.0.1:8000`.
* `GET /health` – health check.
* `POST /chat` – send a message, receive the LLM‑generated reply.

## Extending the Assistant

* **Memory** – integrate a vector store (e.g., ChromaDB) and expose a `recall` tool.
* **Screen sharing** – add a `/screen` endpoint that streams frames captured with `ffmpeg` or `mss`.
* **More UI automation** – add further `pyautogui`‑based tools.
* **Security** – run the daemon inside a Docker container with limited permissions and require explicit approval for destructive commands.

Feel free to fork, modify, and expand this skeleton into a full‑featured Jarvis‑style assistant.