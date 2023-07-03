from datetime import datetime as dt

from . import db
from .settings import CUSTOM_ID_MAX_LENGTH, LINK_SIZE_MAX


class URLMap(db.Model):
    """Класс для создания модели URLMap."""
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    original = db.Column(
        db.String(CUSTOM_ID_MAX_LENGTH),
        nullable=False
    )
    short = db.Column(
        db.String(LINK_SIZE_MAX),
        unique=True,
        nullable=False,
        index=True
    )
    timestamp = db.Column(
        db.DateTime,
        default=dt.utcnow
    )

    def __repr__(self) -> str:
        return (
            f'id: {self.id}\n'
            f'original: {self.original}\n'
            f'short: {self.short}\n'
            f'timestamp: {self.timestamp}\n'
        )

    def to_dict(self):
        return dict(
            id=self.id,
            original=self.original,
            short=self.short,
            timestamp=self.timestamp
        )

    def from_dict(self, data):
        for field in ['original', 'short']:
            if field in data:
                setattr(self, field, data[field])
