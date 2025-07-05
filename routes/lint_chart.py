from flask import Blueprint, request, jsonify
from clients.service_dispatcher import dispatch
import os
from datetime import datetime, timezone

bp = Blueprint('lint_chart', __name__)

@bp.route('/lint-chart', methods=['POST'])
def lint_chart():
    if not request.is_json:
        return jsonify({"error": "El cuerpo debe ser JSON"}), 400

    payload = request.get_json()
    chart_path = payload.get("chart_path", "")
    if not chart_path:
        return jsonify({"error": "Falta el campo 'chart_path'"}), 400

    mode = payload.get("mode", "ollama")

    # 🕒 Timestamp único con zona horaria UTC
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    base_filename = f"chart_{ts}"
    prompt_path = f"/app/outputs/charts/{base_filename}.path"
    response_path = f"/app/outputs/charts/{base_filename}.lint"

    # 💾 Guardar ruta del chart como pseudo-prompt
    try:
        os.makedirs(os.path.dirname(prompt_path), exist_ok=True)
        with open(prompt_path, "w") as f:
            f.write(chart_path)
    except Exception as e:
        return jsonify({"error": f"No se pudo guardar el path del Chart: {e}"}), 500

    forwarded_payload = {
        "chart_path": chart_path,
        "mode": mode
    }

    try:
        result = dispatch(
            service_name="lint_chart",
            payload=forwarded_payload,
            prompt_path=prompt_path,
            response_path=response_path,
            llm_used=mode
        )
        return result
    except Exception as e:
        return jsonify({
            "error": "Error al contactar con ai-helm-linter",
            "details": str(e)
        }), 502
