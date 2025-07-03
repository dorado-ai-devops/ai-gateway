#!/bin/bash


MODE=${1:-ollama}
RULESET=${2:-default}

PROJECT_ROOT="/root/devops-ai"
CHART_DIR="$PROJECT_ROOT/chart"
CHART_PACKAGE_DEST="$PROJECT_ROOT/chart_package"

mkdir -p "$CHART_PACKAGE_DEST"


CHART_TGZ=$(helm package "$CHART_DIR" --destination "$CHART_PACKAGE_DEST" | awk '{print $NF}' | tr -d '\n')

if [ ! -f "$CHART_TGZ" ]; then
  echo "❌ No se generó el paquete Helm"
  exit 1
fi

echo "📦 Chart empaquetado: $CHART_TGZ"
echo "📡 Enviando a ai-gateway (modo: $MODE, ruleset: $RULESET)"


curl -X POST http://localhost:5002/lint-chart \
  -F chart=@"$CHART_TGZ" \
  -F mode="$MODE" \
  -F ruleset="$RULESET"

# 🧹 Limpiar temporal
rm -f "$CHART_TGZ"
