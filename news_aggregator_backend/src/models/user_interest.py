from src.models.user import db
from datetime import datetime
import uuid

class UserInterest(db.Model):
    __tablename__ = 'user_interests'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    keyword = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=True)
    source = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<UserInterest {self.keyword}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'keyword': self.keyword,
            'category': self.category,
            'source': self.source,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

