from flask import Blueprint, request, jsonify
from clients.service_dispatcher import dispatch
import os
from datetime import datetime, timezone

bp = Blueprint('lint_chart', __name__)

@bp.route('/lint-chart', methods=['POST'])
def lint_chart():
    if 'chart' not in request.files:
        return jsonify({"error": "Falta el archivo 'chart' (.tgz)"}), 400

    chart_file = request.files['chart']
    mode = request.form.get("mode", "ollama")

    # 🕒 Timestamp único con zona horaria UTC
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    base_filename = f"chart_{ts}"
    save_dir = "/app/outputs/charts"
    os.makedirs(save_dir, exist_ok=True)

    chart_path = os.path.join(save_dir, f"{base_filename}.tgz")
    prompt_path = os.path.join(save_dir, f"{base_filename}.path")
    response_path = os.path.join(save_dir, f"{base_filename}.lint")

    # 💾 Guardar el archivo del Chart
    try:
        chart_file.save(chart_path)
        with open(prompt_path, "w") as f:
            f.write(chart_path)
    except Exception as e:
        return jsonify({"error": f"No se pudo guardar el Chart: {e}"}), 500

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
