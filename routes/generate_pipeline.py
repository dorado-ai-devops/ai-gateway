from flask import Blueprint, request, jsonify
from clients.service_dispatcher import dispatch
import os
from datetime import datetime, timezone  # ✅ Añadido timezone

bp = Blueprint('generate_pipeline', __name__)

@bp.route('/generate-pipeline', methods=['POST'])
def generate_pipeline():
    if not request.is_json:
        return jsonify({"error": "El cuerpo debe ser JSON"}), 400

    payload = request.get_json()

    description = payload.get("description", "")
    if not description:
        return jsonify({"error": "Falta el campo 'description'"}), 400

    mode = payload.get("mode", "ollama")

    # ✅ Timestamp con zona horaria UTC
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    base_filename = f"pipeline_{ts}"
    prompt_path = f"/app/outputs/pipelines/{base_filename}.prompt"
    response_path = f"/app/outputs/pipelines/{base_filename}.jenkinsfile"

    # 💾 Guardar prompt (descripción)
    try:
        os.makedirs(os.path.dirname(prompt_path), exist_ok=True)
        with open(prompt_path, "w") as f:
            f.write(description)
    except Exception as e:
        return jsonify({"error": f"No se pudo guardar el prompt: {e}"}), 500

    # 🔁 Payload para el microservicio real
    forwarded_payload = {
        "description": description,
        "mode": mode
    }

    try:
        result = dispatch(
            service_name="generate_pipeline",
            payload=forwarded_payload,
            prompt_path=prompt_path,
            response_path=response_path,
            llm_used=mode
        )
        return result
    except Exception as e:
        return jsonify({
            "error": "Error al contactar con ai-pipeline-gen",
            "details": str(e)
        }), 502
