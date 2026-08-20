from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from werkzeug.utils import secure_filename
from app.config import Config
import os

from uuid import uuid4
from app.extensions import db
from app.models import Resume
from app.services import resume_parser

resumes_bp = Blueprint(
    "resumes",
    __name__,
    url_prefix="/resumes"
)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'pdf', 'docx'}
@resumes_bp.post("")
@jwt_required()
def upload_resume():
    user_id = int(get_jwt_identity())

    if "file" not in request.files:
        return jsonify({
            "error": "Resume file is required"
        }), 400

    file = request.files["file"]

    if not file.filename:
        return jsonify({
            "error": "No file selected"
        }), 400

    if not allowed_file(file.filename):
        return jsonify({
            "error": "Invalid file type. Only PDF and DOCX are allowed."
        }), 400

    original_filename = secure_filename(file.filename)

    ext = os.path.splitext(original_filename)[1].lower()

    unique_filename = f"{uuid4().hex}{ext}"
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

    file_path = os.path.join(
        Config.UPLOAD_FOLDER,
        unique_filename,
    )

    file.save(file_path)

    try:
        extracted_text = resume_parser.extract_resume_text(
            file_path,
            ext,
        )
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)

        return jsonify({
            "error": "Failed to parse resume text"
        }), 500

    file_size = os.path.getsize(file_path)

    new_resume = Resume(
        user_id=user_id,
        resume_name=(
            request.form.get("resume_name")
            or original_filename
        ),
        original_file=original_filename,
        extracted_text=extracted_text,
        storage_key=unique_filename,
        m_type=file.mimetype,
        file_size_bytes=file_size,
        version_type=request.form.get("version_type"),
    )

    try:
        db.session.add(new_resume)
        db.session.commit()
    except Exception as e:
        db.session.rollback()

        if os.path.exists(file_path):
            os.remove(file_path)

        return jsonify({
            "error": "Unable to save resume"
        }), 500

    return jsonify({
        "message": "Resume uploaded successfully",
        "resume": new_resume.to_dict(),
        "extracted_text_preview": extracted_text[:500],
    }), 201

@resumes_bp.get("")
@jwt_required()
def get_resume():
    user_id = int(get_jwt_identity())

    query = Resume.query.filter_by(
        user_id=user_id
    )

    resume_name = request.args.get("resume_name")
    version_type = request.args.get("version_type")

    if resume_name:
        query = query.filter(
            Resume.resume_name.ilike(
                f"%{resume_name}%"
            )
        )

    if version_type:
        query = query.filter_by(version_type=version_type)

    resumes = query.order_by(Resume.created_at.desc()
    ).all()

    return jsonify([resume.to_dict() for resume in resumes]), 200

@resumes_bp.delete("/<int:resume_id>")
@jwt_required()
def delete_resume(resume_id):
    user_id = int(get_jwt_identity())

    resume = Resume.query.filter_by(
        resume_id=resume_id,
        user_id=user_id,
    ).first()

    if resume is None:
        return jsonify({"error": "Resume not found"}), 404

    file_path = os.path.join(
        Config.UPLOAD_FOLDER,
        resume.storage_key,
    )

    try:
        db.session.delete(resume)
        db.session.commit()

        if os.path.exists(file_path):
            os.remove(file_path)

    except Exception:
        db.session.rollback()
        return jsonify({"error": "Unable to delete resume"}), 500

    return jsonify({"message": f"Resume {resume_id} successfully deleted"}), 200
