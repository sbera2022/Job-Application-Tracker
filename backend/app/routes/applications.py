from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)

from app.extensions import db
from app.models import ApplicationTrack, JobApplication
from app.utils.validators import validate_application
from datetime import datetime, timezone

applications_bp = Blueprint(
    "applications",
    __name__,
    url_prefix="/applications",
)

@applications_bp.get("")
@jwt_required()
def get_applications():
    user_id = int(get_jwt_identity())

    query = JobApplication.query.filter_by(user_id=user_id)

    status = request.args.get("status")
    work_location = request.args.get("work_location")
    company = request.args.get("company")
    search = request.args.get("search")

    if status:
        query = query.filter_by(status=status)

    if work_location:
        query = query.filter_by(work_location=work_location)

    if company:
        query = query.filter(
            JobApplication.company_name.ilike(f"%{company}%")
        )

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            db.or_(
                JobApplication.job_title.ilike(search_term),
                JobApplication.company_name.ilike(search_term),
                JobApplication.job_location.ilike(search_term),
            )
        )

    apps = query.order_by(
        JobApplication.created_at.desc()
    ).all()

    return jsonify([a.to_dict() for a in apps]), 200

@applications_bp.post("")
@jwt_required()
def create_application():
    data = request.get_json(silent=True)
    required = ['job_title', 'company_name', 'work_location']
    user_id = int(get_jwt_identity())

    if not data:
        return jsonify({"error": "Request body must contain JSON"}), 400

    missing = [field for field in required if not data.get(field)]
    if missing:
        return jsonify({"error": "Missing required fields", "field": missing, }), 400

    if user_id is None:
        return jsonify({"error": "User not found"}), 404

    valid_error = validate_application(data)
    if valid_error:
        return jsonify(valid_error), 400

    new_app = JobApplication(
        user_id=user_id,
        job_title=data['job_title'].strip(),
        company_name=data['company_name'].strip(),
        job_url=data.get('job_url'),
        salary_min=data.get('salary_min'),
        salary_max=data.get('salary_max'),
        currency=data.get("currency", "USD"),
        job_location=data.get('job_location'),
        work_location=data['work_location'],
        status=data.get('status', 'Applied'),
        notes=data.get('notes'),
        job_description=data.get('job_description')
    )

    history = ApplicationTrack(application=new_app, status=new_app.status, notes="Application record created", )

    try:
        db.session.add(new_app)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Unable to create application"}), 500

    return jsonify(new_app.to_dict()), 201

@applications_bp.get("/<int:application_id>")
@jwt_required()
def get_application_by_id(application_id):
    user_id = int(get_jwt_identity())

    applicant = JobApplication.query.filter_by(
        application_id=application_id,
        user_id=user_id,
    ).first()

    if applicant is None:
        return jsonify({
            "error": "Application not found"
        }), 404

    return jsonify(applicant.to_dict()), 200

@applications_bp.patch("/<int:application_id>")
@jwt_required()
def update_application(application_id):
    user_id = int(get_jwt_identity())

    applicant = JobApplication.query.filter_by(
        application_id=application_id,
        user_id=user_id,
    ).first()

    data = request.get_json(silent=True)

    if applicant is None:
        return jsonify({"error": "Application not found"}), 404

    if not data:
        return jsonify({"error": "Request body must contain JSON"}), 400

    editable = [
        "job_title",
        "company_name",
        "job_url",
        "salary_min",
        "salary_max",
        "currency",
        "status",
        "work_location",
        "job_location",
        "date_applied",
        "notes",
        "job_description",
    ]

    old_status = applicant.status

    valid_error = validate_application(data)
    if valid_error:
        return jsonify(valid_error), 400

    for field in editable:
        if field in data:
            setattr(applicant, field, data[field])

    applicant.last_activity = datetime.now(timezone.utc)

    try:
        if "status" in data and data["status"] != old_status:
            history = ApplicationTrack(
                application=applicant,
                status=data["status"],
                notes=data.get("status_note"),
            )
            db.session.add(history)
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Unable to update application"}), 500

    return jsonify(applicant.to_dict()), 200

@applications_bp.delete("/<int:application_id>")
@jwt_required()
def delete_application(application_id):
    user_id = int(get_jwt_identity())

    applicant = JobApplication.query.filter_by(
        application_id=application_id,
        user_id=user_id,
    ).first()

    if applicant is None:
        return jsonify({"error": "Application not found"})

    try:
        db.session.delete(applicant)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Unable to delete application"}), 500

    return jsonify({"message": f"Application {application_id} successfully deleted"}), 200

@applications_bp.get("/<int:application_id>/history")
@jwt_required()
def get_application_history(application_id):
    user_id = int(get_jwt_identity())

    applicant = JobApplication.query.filter_by(
        application_id=application_id,
        user_id=user_id,
    ).first()

    if applicant is None:
        return jsonify({"error": "Application not found"}), 404

    history = (
        ApplicationTrack.query
        .filter_by(application_id=application_id)
        .order_by(ApplicationTrack.event_date.desc())
        .all()
    )

    return jsonify([record.to_dict() for record in history]), 200