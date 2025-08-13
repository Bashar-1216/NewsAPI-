from flask import Blueprint, jsonify, request
from src.models.article import Article, db
from datetime import datetime

articles_bp = Blueprint('articles', __name__)

@articles_bp.route('/articles', methods=['GET'])
def get_articles():
    """Get all articles with optional filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    category = request.args.get('category')
    source = request.args.get('source')
    sentiment = request.args.get('sentiment')
    search = request.args.get('search')
    
    query = Article.query
    
    # Apply filters
    if category:
        query = query.filter(Article.category == category)
    if source:
        query = query.filter(Article.source == source)
    if sentiment:
        query = query.filter(Article.sentiment == sentiment)
    if search:
        query = query.filter(Article.title.contains(search) | Article.content.contains(search))
    
    # Order by published date (newest first)
    query = query.order_by(Article.published_date.desc())
    
    # Paginate results
    articles = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'articles': [article.to_dict() for article in articles.items],
        'total': articles.total,
        'pages': articles.pages,
        'current_page': page,
        'per_page': per_page
    })

@articles_bp.route('/articles/<string:article_id>', methods=['GET'])
def get_article(article_id):
    """Get a specific article by ID"""
    article = Article.query.get_or_404(article_id)
    return jsonify(article.to_dict())

@articles_bp.route('/articles', methods=['POST'])
def create_article():
    """Create a new article"""
    data = request.json
    
    # Parse published_date if provided
    published_date = None
    if 'published_date' in data:
        try:
            published_date = datetime.fromisoformat(data['published_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid published_date format'}), 400
    
    article = Article(
        title=data['title'],
        url=data['url'],
        source=data['source'],
        author=data.get('author'),
        published_date=published_date or datetime.utcnow(),
        content=data['content'],
        summary=data.get('summary'),
        category=data.get('category'),
        sentiment=data.get('sentiment'),
        is_fake=data.get('is_fake', False),
        image_url=data.get('image_url')
    )
    
    try:
        db.session.add(article)
        db.session.commit()
        return jsonify(article.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Article with this URL already exists'}), 409

@articles_bp.route('/articles/<string:article_id>', methods=['PUT'])
def update_article(article_id):
    """Update an existing article"""
    article = Article.query.get_or_404(article_id)
    data = request.json
    
    # Update fields if provided
    if 'title' in data:
        article.title = data['title']
    if 'summary' in data:
        article.summary = data['summary']
    if 'category' in data:
        article.category = data['category']
    if 'sentiment' in data:
        article.sentiment = data['sentiment']
    if 'is_fake' in data:
        article.is_fake = data['is_fake']
    
    db.session.commit()
    return jsonify(article.to_dict())

@articles_bp.route('/articles/<string:article_id>', methods=['DELETE'])
def delete_article(article_id):
    """Delete an article"""
    article = Article.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()
    return '', 204

@articles_bp.route('/articles/categories', methods=['GET'])
def get_categories():
    """Get all unique categories"""
    categories = db.session.query(Article.category).distinct().filter(Article.category.isnot(None)).all()
    return jsonify([cat[0] for cat in categories])

@articles_bp.route('/articles/sources', methods=['GET'])
def get_sources():
    """Get all unique sources"""
    sources = db.session.query(Article.source).distinct().all()
    return jsonify([source[0] for source in sources])

