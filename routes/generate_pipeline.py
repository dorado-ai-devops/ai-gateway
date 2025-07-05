from flask import Blueprint, request, jsonify
from clients.service_dispatcher import dispatch

bp = Blueprint('generate_pipeline', __name__)

@bp.route('/generate', methods=['POST'])
def generate_pipeline():
    try:
        data = request.get_json(force=True)

        if 'description' not in data:
            return jsonify({'error': 'Campo "description" requerido'}), 400

        mode = data.get("mode", "ollama")

        forwarded_payload = {
            "description": data["description"],
            "mode": mode
        }

        result = dispatch('generate_pipeline', forwarded_payload)
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
