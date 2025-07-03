# routes/lint_chart.py

from flask import Blueprint, request, jsonify
import requests
from config import SERVICES, TIMEOUT

bp = Blueprint('lint_chart', __name__)

@bp.route('/lint-chart', methods=['POST'])
def lint_chart():
    if 'chart' not in request.files or 'mode' not in request.form:
        return jsonify({'error': "Faltan campos requeridos: 'chart' (archivo) y 'mode' (texto)"}), 400

    chart_file = request.files['chart']
    mode = request.form['mode']
    ruleset = request.form.get('ruleset', 'default')

    try:
        files = {'chart': (chart_file.filename, chart_file.stream, chart_file.mimetype)}
        data = {
            'mode': mode,
            'ruleset': ruleset
        }

        response = requests.post(
            SERVICES["lint_chart"],
            files=files,
            data=data,
            timeout=TIMEOUT
        )
        response.raise_for_status()
        return response.json()

    except requests.RequestException as e:
        return jsonify({
            'error': 'Error al contactar con ai-helm-linter',
            'details': str(e)
        }), 500
