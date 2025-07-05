from flask import Blueprint, request, jsonify
from clients.service_dispatcher import dispatch  # ✅ Usamos el dispatcher común

bp = Blueprint('generate_pipeline', __name__)

@bp.route('/generate-pipeline', methods=['POST'])
def generate_pipeline():
    if not request.is_json:
        return jsonify({"error": "El cuerpo debe ser JSON"}), 400

    payload = request.get_json()

    description = payload.get("description", "")
    if not description:
        return jsonify({"error": "Falta el campo 'description'"}), 400

    forwarded_payload = {
        "description": description,
        "mode": payload.get("mode", "ollama")
    }

    prompt_path = payload.get("prompt_path")
    response_path = payload.get("response_path")
    llm_used = payload.get("mode", "ollama")

    try:
        result = dispatch(
            service_name="generate_pipeline",
            payload=forwarded_payload,
            prompt_path=prompt_path,
            response_path=response_path,
            llm_used=llm_used
        )
        return result
    except Exception as e:
        return jsonify({
            "error": "Error al contactar con ai-pipeline-gen",
            "details": str(e)
        }), 502
