from flask import Flask, jsonify

from app.config import Config
from .extensions import cors, db, migrate, jwt


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    cors.init_app(
        app,
        resources={
            r"/*": {
                "origins": "http://localhost:5173"
            }
        },
    )

    from . import models
    from .routes.auth import auth_bp
    from .routes.applications import applications_bp
    from .routes.resumes import resumes_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(applications_bp)
    app.register_blueprint(resumes_bp)

    @app.get("/")
    def home():
        return {
            "message": "Job Application Tracker API is running"
        }, 200

    return app
