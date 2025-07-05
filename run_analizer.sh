#!/bin/bash

MODE=${1:-ollama}

LOG_FILE="./sample_log.txt"
if [ ! -f "$LOG_FILE" ]; then
  echo "❌ No se encontró el archivo $LOG_FILE"
  exit 1
fi

echo "📡 Enviando log a ai-gateway (modo: $MODE)"

curl -X POST http://localhost:5002/analyze-log \
  -F log=@"$LOG_FILE" \
  -F mode="$MODE"
