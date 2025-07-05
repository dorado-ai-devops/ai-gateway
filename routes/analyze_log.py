from flask import Blueprint, request, jsonify
import requests
from config import SERVICES, TIMEOUT

bp = Blueprint('analyze_log', __name__)

@bp.route('/analyze-log', methods=['POST'])
def analyze_log():
    if not request.is_json:
        return jsonify({"error": "El cuerpo debe ser JSON"}), 400

    payload = request.get_json()

    log = payload.get("log", "")
    if not log:
        return jsonify({"error": "Falta el campo 'log'"}), 400

    # Inyectar 'mode' si no viene en el payload
    mode = payload.get("mode", "ollama")

    forwarded_payload = {
        "log": log,
        "mode": mode
    }

    try:
        response = requests.post(
            SERVICES["analyze_log"],
            json=forwarded_payload,
            timeout=TIMEOUT
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Error al contactar con ai-log-analyzer",
            "details": str(e)
        }), 502
