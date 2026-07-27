from flask import Flask, jsonify
from dotenv import load_dotenv

from app.config import Config
from app.extensions import db, migrate, jwt


def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from . import models
    from .routes.auth import auth_bp
    from .routes.applications import applications_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(applications_bp)

    @app.get("/")
    def home():
        return {
            "message": "Job Application Tracker API is running"
        }, 200

    return app
