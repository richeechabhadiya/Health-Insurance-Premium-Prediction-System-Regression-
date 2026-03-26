#!/usr/bin/env bash
set -e
ROOT=$(cd "$(dirname "$0")" && pwd)
PY="$ROOT/venv/bin/python"
if [ ! -x "$PY" ]; then
  echo "venv python not found at $PY" >&2
  exit 1
fi
echo "Starting streamlit with $PY"
nohup "$PY" -m streamlit run "$ROOT/app/app.py" --server.port 8501 > /tmp/streamlit.log 2>&1 & echo $! > /tmp/streamlit.pid
echo "Started. PID: $(cat /tmp/streamlit.pid)"
