from datetime import datetime

from yacut import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def from_dict(self, dict):
        self.original = dict.get('url')
        self.short = dict.get('custom_id')

    @classmethod
    def is_exists(cls, custom_id):
        return cls.query.filter_by(short=custom_id).first()