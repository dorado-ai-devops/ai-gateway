from flask import Blueprint, request, jsonify
from clients.service_dispatcher import dispatch  # ✅ Uso del dispatcher común

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

    forwarded_payload = {
        "log": log,
        "mode": mode
    }

    prompt_path = payload.get("prompt_path")
    response_path = payload.get("response_path")
    llm_used = mode

    try:
        result = dispatch(
            service_name="analyze_log",
            payload=forwarded_payload,
            prompt_path=prompt_path,
            response_path=response_path,
            llm_used=llm_used
        )
        return result
    except Exception as e:
        return jsonify({
            "error": "Error al contactar con ai-log-analyzer",
            "details": str(e)
        }), 502
