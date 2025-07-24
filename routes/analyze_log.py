from flask import Blueprint, request, jsonify
from clients.service_dispatcher import dispatch
import os
from datetime import datetime, timezone

bp = Blueprint('analyze_log', __name__)

@bp.route('/analyze-log', methods=['POST'])
def analyze_log():
    if not request.is_json:
        return jsonify({"error": "El cuerpo debe ser JSON"}), 400

    payload = request.get_json()
    log = payload.get("log", "")
    if not log:
        return jsonify({"error": "Falta el campo 'log'"}), 400

    mode = payload.get("mode", "ollama")

    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    base_filename = f"log_{ts}"
    prompt_path = f"/app/outputs/logs/{base_filename}.log"
    response_path = f"/app/outputs/logs/{base_filename}.analysis"

    try:
        os.makedirs(os.path.dirname(prompt_path), exist_ok=True)
        with open(prompt_path, "w") as f:
            f.write(log)
    except Exception as e:
        return jsonify({"error": f"No se pudo guardar el log: {e}"}), 500

    forwarded_payload = {
        "log": log,
        "mode": mode
    }

    try:
        result = dispatch(
            service_name="analyze_log",
            payload=forwarded_payload,
            prompt_path=prompt_path,
            response_path=response_path,
            llm_used=mode
        )

        #  Guardar resultado en response_path
        os.makedirs(os.path.dirname(response_path), exist_ok=True)
        with open(response_path, "w") as f:
            f.write(result if isinstance(result, str) else str(result))

        return jsonify({"result": result})
    except Exception as e:
        return jsonify({
            "error": "Error al contactar con ai-log-analyzer",
            "details": str(e)
        }), 502
