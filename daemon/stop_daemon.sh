#!/usr/bin/env bash
# Stop the background Jarvis daemon started by run_daemon.sh

set -e
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PID_FILE="$BASE_DIR/daemon.pid"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    kill "$PID" && rm -f "$PID_FILE"
    echo "Jarvis daemon (PID $PID) stopped."
else
    echo "No daemon.pid file found – daemon may not be running."
fi