from .lint_chart import bp as lint_chart_bp
from .analyze_log import bp as analyze_log_bp
from .generate_pipeline import bp as generate_pipeline_bp

def register_routes(app):
    app.register_blueprint(lint_chart_bp)
    app.register_blueprint(analyze_log_bp)
    app.register_blueprint(generate_pipeline_bp)
