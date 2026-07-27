from datetime import datetime, timezone

from app.extensions import db

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)
    google_id = db.Column(db.String(255), unique=True, nullable=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    applications = db.relationship("JobApplication", back_populates="user", cascade="all, delete-orphan",)
    resumes = db.relationship("Resume", back_populates="user", cascade="all, delete-orphan")
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    __table_args__ = (
        db.CheckConstraint(
            "password_hash IS NOT NULL OR google_id IS NOT NULL",
            name="valid_authentication",
        ),
    )

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "email": self.email,
            "google_id": self.google_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }