# routes/generate_pipeline.py

from flask import Blueprint, request, jsonify
from clients.service_dispatcher import dispatch

generate_pipeline_bp = Blueprint('generate_pipeline', __name__)

@generate_pipeline_bp.route('/', methods=['POST'])
def generate_pipeline():
    try:
        data = request.get_json(force=True)

        if 'description' not in data or 'target' not in data:
            return jsonify({'error': 'Campos "description" y "target" requeridos'}), 400

        result = dispatch('pipeline', data)
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
