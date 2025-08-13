from src.models.user import db
from datetime import datetime
import uuid

class Article(db.Model):
    __tablename__ = 'articles'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False, unique=True)
    source = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=True)
    published_date = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=True)
    sentiment = db.Column(db.String(20), nullable=True)
    is_fake = db.Column(db.Boolean, nullable=False, default=False)
    image_url = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Article {self.title[:50]}...>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'url': self.url,
            'source': self.source,
            'author': self.author,
            'published_date': self.published_date.isoformat() if self.published_date else None,
            'content': self.content,
            'summary': self.summary,
            'category': self.category,
            'sentiment': self.sentiment,
            'is_fake': self.is_fake,
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

