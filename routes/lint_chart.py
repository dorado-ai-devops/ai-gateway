from flask import Blueprint, request, jsonify
from clients.service_dispatcher import dispatch  # ✅ Nuevo import

bp = Blueprint('lint_chart', __name__)

@bp.route('/lint-chart', methods=['POST'])
def lint_chart():
    if not request.is_json:
        return jsonify({"error": "El cuerpo debe ser JSON"}), 400

    payload = request.get_json()

    chart_path = payload.get("chart_path", "")
    if not chart_path:
        return jsonify({"error": "Falta el campo 'chart_path'"}), 400

    forwarded_payload = {
        "chart_path": chart_path,
        "mode": payload.get("mode", "ollama")
    }

    prompt_path = payload.get("prompt_path")
    response_path = payload.get("response_path")
    llm_used = payload.get("mode", "ollama")

    try:
        result = dispatch(
            service_name="lint_chart",
            payload=forwarded_payload,
            prompt_path=prompt_path,
            response_path=response_path,
            llm_used=llm_used
        )
        return result
    except Exception as e:
        return jsonify({
            "error": "Error al contactar con ai-helm-linter",
            "details": str(e)
        }), 502
