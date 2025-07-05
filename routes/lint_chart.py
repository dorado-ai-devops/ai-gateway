from flask import Blueprint, request, jsonify
from clients.service_dispatcher import dispatch
import os
from datetime import datetime, timezone
import tempfile
import json

bp = Blueprint('lint_chart', __name__)

@bp.route('/lint-chart', methods=['POST'])
def lint_chart():
    if 'chart' not in request.files:
        return jsonify({"error": "Falta el archivo 'chart' (.tgz)"}), 400

    chart_file = request.files['chart']
    mode = request.form.get("mode", "ollama")
    chart_name = request.form.get("chart_name", "unknown")

    # 🕒 Timestamp único con zona horaria UTC
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    base_filename = f"chart_{ts}"
    save_dir = "/app/outputs/charts"
    os.makedirs(save_dir, exist_ok=True)

    # ⚠️ Guardar .tgz temporal para procesar
    with tempfile.NamedTemporaryFile(delete=False, suffix=".tgz") as tmp:
        chart_file.save(tmp.name)
        chart_path = tmp.name

    prompt_path = os.path.join(save_dir, f"{base_filename}.path.json")
    response_path = os.path.join(save_dir, f"{base_filename}.lint")

    # 📝 Guardar metadata como .json
    try:
        metadata = {
            "chart_name": chart_name,
            "chart_temp_path": chart_path
        }
        with open(prompt_path, "w") as f:
            json.dump(metadata, f, indent=2)
    except Exception as e:
        return jsonify({"error": f"No se pudo guardar el archivo .path.json: {e}"}), 500

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

        try:
            with open(response_path, "w") as f:
                f.write(str(result))
        except Exception as e:
            return jsonify({"error": f"No se pudo guardar el resultado .lint: {e}"}), 500

        return result

    except Exception as e:
        return jsonify({
            "error": "Error al contactar con ai-helm-linter",
            "details": str(e)
        }), 502

    finally:
        # 🧹 Eliminar el .tgz temporal
        try:
            os.remove(chart_path)
        except Exception:
            pass
