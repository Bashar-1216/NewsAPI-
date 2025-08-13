from src.models.user import db
from datetime import datetime
import uuid

class ReadingHistory(db.Model):
    __tablename__ = 'reading_history'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    article_id = db.Column(db.String(36), db.ForeignKey('articles.id'), nullable=False)
    read_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<ReadingHistory User:{self.user_id} Article:{self.article_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'article_id': self.article_id,
            'read_at': self.read_at.isoformat() if self.read_at else None
        }

