from datetime import datetime, timezone

from app.extensions import db

class ApplicationResume(db.Model):
    __tablename__ = 'application_resumes'

    application_id = db.Column(
        db.Integer,
        db.ForeignKey('job_application.application_id', ondelete='CASCADE'),
        primary_key=True,
    )
    resume_id = db.Column(
        db.Integer,
        db.ForeignKey('resumes.resume_id', ondelete='CASCADE'),
        primary_key=True,
    )
    attached_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def to_dict(self):
        return {
            "application_id": self.application_id,
            "resume_id": self.resume_id,
            "attached_at": self.attached_at
        }