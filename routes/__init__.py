from .lint_chart import lint_chart_bp
from .analyze_log import analyze_log_bp
# from .generate_pipeline import generate_pipeline_bp  # cuando lo tengas

def register_routes(app):
    app.register_blueprint(lint_chart_bp)
    app.register_blueprint(analyze_log_bp)
    # app.register_blueprint(generate_pipeline_bp)  # descomenta cuando esté
