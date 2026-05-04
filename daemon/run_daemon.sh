#!/usr/bin/env bash
# Start the FastAPI Jarvis assistant as a background daemon.
# Activates a virtual environment if present, then launches uvicorn.

set -e
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$BASE_DIR"

# Activate virtual environment if it exists
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

# Ensure a logs directory exists
mkdir -p logs

# Start uvicorn in the background, redirect output to logs/daemon.log
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > logs/daemon.log 2>&1 &
echo $! > daemon.pid
echo "Jarvis daemon started (PID $(cat daemon.pid)). Logs: $BASE_DIR/logs/daemon.log"