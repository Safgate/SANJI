#!/usr/bin/env python3
"""Tiny native GUI wrapper for the Jarvis FastAPI assistant.
It starts the daemon, opens a webview pointing to the local API UI, and
shuts the daemon down when the window is closed.
"""
import os
import signal
import subprocess
import sys
import time

import webview

# Resolve the absolute path to the daemon start script
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DAEMON_SCRIPT = os.path.join(BASE_DIR, "daemon", "run_daemon.sh")

def start_daemon():
    """Launch the FastAPI daemon in its own process group."""
    proc = subprocess.Popen(["bash", DAEMON_SCRIPT],
                            preexec_fn=os.setsid,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
    return proc

def stop_daemon(proc):
    """Terminate the daemon process group cleanly."""
    try:
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
    except Exception:
        pass

if __name__ == "__main__":
    daemon = start_daemon()
    # Give the server a moment to start up
    time.sleep(2)

    # Open a native window that loads the FastAPI Swagger UI (or any front‑end you add)
    webview.create_window("Jarvis Assistant", "http://127.0.0.1:8000/docs")
    webview.start()

    # When the window closes, stop the daemon
    stop_daemon(daemon)
    sys.exit(0)