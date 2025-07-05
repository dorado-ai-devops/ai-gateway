# clients/service_dispatcher.py

import requests
from datetime import datetime
from config import SERVICES, TIMEOUT, DEBUG
from clients.mcp_client import send_mcp_message
import os

def dispatch(service_name, payload, headers=None, prompt_path=None, response_path=None, llm_used="ollama"):
    """
    Redirige la petición al microservicio correspondiente usando configuración centralizada.
    Además, registra un mensaje MCP si la ejecución es exitosa.
    """
    if service_name not in SERVICES:
        raise ValueError(f"Servicio no reconocido: {service_name}")

    url = SERVICES[service_name]

    try:
        if service_name == "lint_chart":
            chart_path = payload.get("chart_path")
            if not chart_path or not os.path.isfile(chart_path):
                raise FileNotFoundError(f"Archivo de Chart no encontrado: {chart_path}")

            with open(chart_path, "rb") as f:
                files = {"chart": f}
                data = {"mode": payload.get("mode", "ollama")}
                response = requests.post(url, files=files, data=data, timeout=TIMEOUT)

        else:
            response = requests.post(url, json=payload, headers=headers or {}, timeout=TIMEOUT)

        response.raise_for_status()
        result = response.json()

        if prompt_path and response_path:
            summary = f"Respuesta del microservicio '{service_name}' registrada correctamente."
            tags = [service_name, "ai", "pipeline"]

            send_mcp_message(
                source="ai-gateway",
                microservice=service_name,
                prompt_path=prompt_path,
                response_path=response_path,
                llm_used=llm_used,
                summary=summary,
                tags=tags,
            )

        return result

    except requests.exceptions.RequestException as e:
        if DEBUG:
            print(f"[ERROR] Fallo al contactar con {service_name} en {url}: {e}")
        raise RuntimeError(f"Fallo en la redirección al microservicio {service_name}")

    except Exception as e:
        if DEBUG:
            print(f"[ERROR] {e}")
        raise RuntimeError(f"Fallo inesperado en dispatch: {e}")
