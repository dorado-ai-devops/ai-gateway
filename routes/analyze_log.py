from flask import Blueprint, request, jsonify
import requests
import os

analyze_log_bp = Blueprint('analyze_log', __name__)

LOG_ANALYZER_URL = os.getenv("LOG_ANALYZER_URL", "http://ai-log-analyzer.devops-ai.svc.cluster.local:80/analyze")

@analyze_log_bp.route('/analyze-log', methods=['POST'])
def analyze_log():
    if not request.is_json:
        return jsonify({"error": "El cuerpo debe ser JSON"}), 400

    payload = request.get_json()

    try:
        response = requests.post(LOG_ANALYZER_URL, json=payload)
        response.raise_for_status()
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Error al contactar con ai-log-analyzer", "details": str(e)}), 502
