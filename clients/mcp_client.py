# clients/mcp_client.py

import requests
from datetime import datetime

MCP_URL = "http://ai-mcp-server.devops-ai.svc.cluster.local:8001/mcp/register"

def send_mcp_message(source, microservice, prompt_path, response_path, llm_used, summary, tags=None):
    payload = {
        "source": source,
        "type": "pipeline-execution",
        "timestamp": datetime.utcnow().isoformat(),
        "microservice": microservice,
        "prompt_path": prompt_path,
        "response_path": response_path,
        "llm_used": llm_used,
        "summary": summary,
        "tags": tags or [],
    }

    try:
        response = requests.post(MCP_URL, json=payload, timeout=3)
        response.raise_for_status()
    except Exception as e:
        print(f"[MCP] Failed to send message: {e}")
