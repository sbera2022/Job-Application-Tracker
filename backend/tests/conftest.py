import pytest
from werkzeug.security import generate_password_hash
from app import create_app
from app.extensions import db
from app.models import User
from flask_jwt_extended import (
    get_jwt_identity,
    create_access_token,
)
@pytest.fixture()
def app():
    config_override = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "JWT_SECRET_KEY": "test-secret-key",
    }

    app = create_app(config_override)

    with app.app_context():
        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture
def auth_user_a(app):
    user = User(
        email="user_a@tracker.com",
        first_name="User",
        last_name="A",
        password_hash=generate_password_hash("Password123"),
    )

    db.session.add(user)
    db.session.commit()

    token = create_access_token(
        identity=str(user.user_id),
    )

    return {"headers": {
        "Authorization": f"Bearer {token}"
    },
    "user_id": user.user_id,
    }


@pytest.fixture
def auth_user_b(app):
    user = User(
        email="user_b@tracker.com",
        first_name="User",
        last_name="B",
        password_hash=generate_password_hash("Password123"),
    )

    db.session.add(user)
    db.session.commit()

    token = create_access_token(
        identity=str(user.user_id)
    )

    return {"headers": {
        "Authorization": f"Bearer {token}"
    },
    "user_id": user.user_id,
    }
