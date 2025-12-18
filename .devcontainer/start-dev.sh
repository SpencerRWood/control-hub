#!/usr/bin/env bash
set -euo pipefail

LOG_DIR="/workspace/.devcontainer"
LOG_FILE="$LOG_DIR/start-dev.log"
mkdir -p "$LOG_DIR"

# Log *everything* this script does
exec >>"$LOG_FILE" 2>&1

echo "========================================"
echo "start-dev.sh invoked at $(date -Is)"
echo "PWD=$(pwd)"
id
echo "========================================"

# ---- Backend ----
if pgrep -fa "uvicorn.*8000" >/dev/null; then
  echo "[backend] already running"
else
  echo "[backend] starting uvicorn"
  cd /workspace/backend
  nohup uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --reload \
    > "$LOG_DIR/uvicorn.log" 2>&1 &
fi

# ---- Frontend ----
if pgrep -fa "vite.*5173" >/dev/null; then
  echo "[frontend] already running"
else
  echo "[frontend] starting vite"
  cd /workspace/frontend
  nohup npm run dev -- \
    --host 0.0.0.0 \
    --port 5173 \
    > "$LOG_DIR/vite.log" 2>&1 &
fi

echo "start-dev.sh completed at $(date -Is)"
