from datetime import datetime, timezone
from app.constants import enums
from app.extensions import db
import sqlalchemy as sa

statuses = enums.status_enum
locations = enums.locations_enum
class JobApplication(db.Model):
    __tablename__ = 'job_application'

    application_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False,)
    user = db.relationship("User", back_populates="applications",)
    history = db.relationship(
        "ApplicationTrack",
        back_populates="application",
        cascade="all, delete-orphan",
        order_by="ApplicationTrack.event_date",
    )
    job_title = db.Column(db.String(255), nullable=False)
    company_name = db.Column(db.String(255), nullable=False)

    salary_min = db.Column(db.Numeric(12, 2))
    salary_max = db.Column(db.Numeric(12, 2))
    date_applied = db.Column(db.Date)
    job_url = db.Column(db.Text)
    currency = db.Column(db.String(3), default='USD', nullable=False)

    status = db.Column(db.Enum(*statuses, name="application_status",), nullable=False, default="Applied",)
    work_location = db.Column(db.Enum(*locations, name="location_type",), nullable=False,)
    job_location = db.Column(db.String(255))
    notes = db.Column(db.Text)
    job_description = db.Column(db.Text)
    last_activity = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

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
        db.Index("idx_job_apps_user_id", "user_id"),
        db.Index("idx_job_apps_date_applied", "user_id", db.text("date_applied DESC")),
        db.Index(
            "idx_job_apps_filters",
            "user_id",
            "status",
            "work_location",
        ),
        db.Index(
            "idx_job_apps_search",
            sa.func.lower(
                sa.text("job_title || ' ' || company_name || ' ' || COALESCE(job_location, '')")
            ).label("job_apps_search_expr"),
            postgresql_ops={
                "job_apps_search_expr": "gin_trgm_ops"
            },
            postgresql_using="gin"
        ),
    )

    def to_dict(self):
        return {
            "application_id": self.application_id,
            "user_id": self.user_id,
            "job_title": self.job_title,
            "company_name": self.company_name,
            "salary_min": (
                str(self.salary_min)
                if self.salary_min is not None
                else None
            ),
            "salary_max": (
                str(self.salary_max)
                if self.salary_max is not None
                else None
            ),
            "date_applied": (
                self.date_applied.isoformat()
                if self.date_applied
                else None
            ),
            "currency": self.currency,
            "job_url": self.job_url,
            "status": self.status,
            "job_location": self.job_location,
            "work_location": self.work_location,
            "notes": self.notes,
            "job_description": self.job_description,
            "last_activity": (
                self.last_activity.isoformat()
                if self.last_activity
                else None
            ),
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }