from datetime import datetime, timezone
from app.constants import enums

from app.extensions import db

statuses = enums.status_enum
locations = enums.locations_enum
class ApplicationTrack(db.Model):
    __tablename__ = 'application_track'

    track_id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('job_application.application_id', ondelete="CASCADE"), nullable=False,)
    event_date = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    application = db.relationship(
        "JobApplication",
        back_populates="history",
    )
    notes = db.Column(db.Text)
    status = db.Column(db.Enum(*statuses, name="application_status", ), nullable=False,)

    __table_args__ = (
        db.Index(
            "idx_application_track",
            "application_id",
            db.text("event_date DESC"),
        ),
    )

    def to_dict(self):
        return {
            "id": self.track_id,
            "application_id": self.application_id,
            "event_date": (
                self.event_date.isoformat()
                if self.event_date
                else None
            ),
            "notes": self.notes,
            "status": self.status,
        }