from datetime import datetime

from app import db


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(2048), unique=True, nullable=False)
    interval = db.Column(db.Integer, nullable=False)
    next_runtime = db.Column(db.DateTime, default=datetime.utcnow)
    replies = db.relationship('Reply', backref='link', lazy='dynamic')

    def __repr__(self):
        return f'<Link {self.url}>'

    def to_dict(self, keys_to_include=None):
        as_dict = {
            'id': self.id,
            'url': self.url,
            'interval': self.interval,
        }
        if keys_to_include:
            return {k: v for k, v in as_dict.items() if k in keys_to_include}
        return as_dict


class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    response = db.Column(db.String(2048))
    duration = db.Column(db.Numeric(1, 3), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    link_id = db.Column(db.Integer, db.ForeignKey('link.id'), nullable=False)

    def __repr__(self):
        return f'<Reply for url: {self.url.url}>'

    def to_dict(self):
        return {
            'response': self.response,
            'duration': str(self.duration),
            'created_at': self.created_at,
        }
