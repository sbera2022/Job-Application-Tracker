from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from werkzeug.security import (
    check_password_hash,
    generate_password_hash,
)

from app.extensions import db
from app.models import User


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth",
)

@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must contain JSON"}), 400

    required = ["email", "password", "first_name", "last_name"]

    missing = [field for field in required if not data.get(field)]

    if missing:
        return jsonify({
            "error": "Missing required fields",
            "fields": missing
        }), 400

    existing_user = User.query.filter_by(
        email=data["email"]
    ).first()

    if existing_user:
        return jsonify({
            "error": "Email already registered"
        }), 409

    new_user = User(
        email=data["email"].strip().lower(),
        password_hash=generate_password_hash(
            data["password"]
        ),
        first_name=data["first_name"].strip(),
        last_name=data["last_name"].strip(),
    )

    try:
        db.session.add(new_user)
        db.session.commit()

    except Exception:
        db.session.rollback()

        return jsonify({"error": "Unable to register user"}), 500

    return jsonify(new_user.to_dict()), 201

@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must contain JSON"}), 400

    required = ["email", "password"]

    missing = [field for field in required if not data.get(field)]

    if missing:
        return jsonify({
            "error": "Missing required fields",
            "fields": missing
        }), 400

    email = data["email"].strip().lower()
    password = data["password"]

    user = User.query.filter_by(email=email).first()
    access_token = create_access_token(identity=str(user.user_id))

    if user is None:
        return jsonify({
            "error": "Invalid email or password"
        }), 401

    if user.password_hash is None:
        return jsonify({
            "error": "This account does not use password login"
        }), 401

    if not check_password_hash(user.password_hash, password):
        return jsonify({
            "error": "Invalid email or password"
        }), 401

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "user": user.to_dict()
    }), 200