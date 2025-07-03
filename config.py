# config.py

import os

# Configuraciones de redirección
SERVICES = {
    "lint_chart": os.getenv("SERVICE_LINT_CHART", "http://ai-helm-linter.devops-ai.svc.cluster.local:80/lint_chart"),
    "analyze_log": os.getenv("SERVICE_ANALYZE_LOG", "http://ai-log-analyzer.devops-ai.svc.cluster.local:80/analyze"),
    "generate_pipeline": os.getenv("SERVICE_GENERATE_PIPELINE", "http://ai-pipeline-gen.devops-ai.svc.cluster.local:80/generate")
}

# Configuraciones globales
TIMEOUT = int(os.getenv("GATEWAY_TIMEOUT", 20))
DEBUG = os.getenv("GATEWAY_DEBUG", "false").lower() == "true"
