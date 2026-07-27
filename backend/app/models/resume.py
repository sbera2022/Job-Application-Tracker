from datetime import datetime, timezone

from app.extensions import db

class Resume(db.Model):
    __tablename__ = 'resumes'

    resume_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False,)
    user = db.relationship("User", back_populates="resumes")
    resume_name = db.Column(db.String(255), nullable=False)
    version_type = db.Column(db.String(50))
    original_file = db.Column(db.String(255), nullable=False)
    storage_key = db.Column(db.Text, nullable=False)
    m_type = db.Column(db.String(100), nullable=False)
    file_size_bytes = db.Column(db.BigInteger)
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
        db.Index("idx_resumes_user_id", "user_id"),
    )
    def to_dict(self):
        return {
            "id": self.resume_id,
            "user_id": self.user_id,
            "resume_name": self.resume_name,
            "version_type": self.version_type,
            "original_file": self.original_file,
            "storage_key": self.storage_key,
            "m_type": self.m_type,
            "file_size_type": self.file_size_bytes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }