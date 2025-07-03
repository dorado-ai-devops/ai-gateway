from flask import Blueprint, request, jsonify
import requests
import os

lint_chart_bp = Blueprint('lint_chart', __name__)

HELM_LINTER_URL = os.getenv("HELM_LINTER_URL", "http://ai-helm-linter.devops-ai.svc.cluster.local:80/lint-chart")

@lint_chart_bp.route('/lint-chart', methods=['POST'])
def lint_chart():
    if not request.is_json:
        return jsonify({"error": "El cuerpo debe ser JSON"}), 400

    payload = request.get_json()

    try:
        response = requests.post(HELM_LINTER_URL, json=payload)
        response.raise_for_status()
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Error al contactar con ai-helm-linter", "details": str(e)}), 502
