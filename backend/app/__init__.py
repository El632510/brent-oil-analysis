"""
Flask app factory. Kept small on purpose: routes are registered as
blueprints in app/routes/, and all data loading lives in app/services.py
so the route functions stay thin.
"""
from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)  # dashboard runs on a different port during development

    from app.routes.prices import prices_bp
    from app.routes.change_points import change_points_bp
    from app.routes.events import events_bp
    from app.routes.summary import summary_bp

    app.register_blueprint(prices_bp, url_prefix="/api/prices")
    app.register_blueprint(change_points_bp, url_prefix="/api/change-points")
    app.register_blueprint(events_bp, url_prefix="/api/events")
    app.register_blueprint(summary_bp, url_prefix="/api/summary")

    @app.route("/api/health")
    def health_check():
        return {"status": "ok"}

    return app
