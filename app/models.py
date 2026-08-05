from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from app.extensions import db
from app.extensions import login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class ContentVersion(db.Model):
    """
    Represents a snapshot of the help content at a specific point in time.
    """
    __bind_key__ = 'help_system'
    __tablename__ = 'content_versions'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    comment = db.Column(db.String(500))
    manifest_hash = db.Column(db.String(64), nullable=False)  # SHA-256 hash of the manifest file
    is_published = db.Column(db.Boolean, default=False, index=True)

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "comment": self.comment,
            "manifest_hash": self.manifest_hash,
            "is_published": self.is_published
        }


class BlobMetadata(db.Model):
    """
    Metadata for blobs stored in Content-Addressable Storage (CAS).
    """
    __bind_key__ = 'help_system'
    __tablename__ = 'blob_metadata'

    sha256 = db.Column(db.String(64), primary_key=True)
    filename = db.Column(db.String(255))  # Original filename or hint
    mime_type = db.Column(db.String(100))
    size = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
