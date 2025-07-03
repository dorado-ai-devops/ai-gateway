# clients/service_dispatcher.py

import requests
from config import SERVICES, TIMEOUT, DEBUG

def dispatch(service_name, payload, headers=None):
    """
    Redirige la petición al microservicio correspondiente usando configuración centralizada.
    """
    if service_name not in SERVICES:
        raise ValueError(f"Servicio no reconocido: {service_name}")

    url = SERVICES[service_name]

    try:
        response = requests.post(url, json=payload, headers=headers or {}, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        if DEBUG:
            print(f"[ERROR] Fallo al contactar con {service_name} en {url}: {e}")
        raise RuntimeError(f"Fallo en la redirección al microservicio {service_name}")
