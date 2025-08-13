from flask import Blueprint, jsonify, request
from src.services.news_fetcher import NewsFetcher
from src.services.sample_news_generator import SampleNewsGenerator
from src.models.article import Article, db
from datetime import datetime

news_bp = Blueprint('news', __name__)
news_fetcher = NewsFetcher()
sample_generator = SampleNewsGenerator()

@news_bp.route('/news/fetch', methods=['POST'])
def fetch_news():
    """Fetch news from external APIs and store in database"""
    data = request.json or {}
    
    query = data.get('query')
    category = data.get('category')
    source_api = data.get('source_api', 'newsapi')  # 'newsapi' or 'serpapi'
    language = data.get('language', 'en')
    
    articles = []
    
    try:
        if source_api == 'newsapi':
            if query:
                # Use everything endpoint for search queries
                articles = news_fetcher.fetch_everything_newsapi(
                    query=query, 
                    language=language
                )
            else:
                # Use top headlines for category-based fetching
                articles = news_fetcher.fetch_from_newsapi(
                    category=category,
                    language=language
                )
        elif source_api == 'serpapi':
            if query:
                articles = news_fetcher.fetch_from_serpapi_google_news(
                    query=query,
                    hl=language
                )
        
        # Store articles in database
        stored_count = 0
        skipped_count = 0
        
        for article_data in articles:
            # Check if article already exists
            existing_article = Article.query.filter_by(url=article_data['url']).first()
            if existing_article:
                skipped_count += 1
                continue
            
            # Create new article
            article = Article(
                title=article_data['title'],
                url=article_data['url'],
                source=article_data['source'],
                author=article_data.get('author'),
                published_date=article_data.get('published_date') or datetime.utcnow(),
                content=article_data.get('content', article_data.get('description', '')),
                image_url=article_data.get('image_url')
            )
            
            db.session.add(article)
            stored_count += 1
        
        db.session.commit()
        
        return jsonify({
            'message': f'Successfully fetched and stored {stored_count} articles',
            'stored': stored_count,
            'skipped': skipped_count,
            'total_fetched': len(articles)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to fetch news: {str(e)}'}), 500

@news_bp.route('/news/trending', methods=['GET'])
def get_trending_topics():
    """Get trending topics from Google News"""
    try:
        topics = news_fetcher.fetch_trending_topics()
        return jsonify({'trending_topics': topics})
    except Exception as e:
        return jsonify({'error': f'Failed to fetch trending topics: {str(e)}'}), 500

@news_bp.route('/news/sources', methods=['GET'])
def get_available_sources():
    """Get available news sources"""
    # This is a simplified list - in practice, you'd fetch from NewsAPI sources endpoint
    sources = [
        'BBC News', 'CNN', 'Reuters', 'Associated Press', 'The Guardian',
        'The New York Times', 'The Washington Post', 'Al Jazeera English',
        'TechCrunch', 'Ars Technica', 'The Verge', 'Wired'
    ]
    return jsonify({'sources': sources})

@news_bp.route('/news/categories', methods=['GET'])
def get_available_categories():
    """Get available news categories"""
    categories = [
        'business', 'entertainment', 'general', 'health', 
        'science', 'sports', 'technology'
    ]
    return jsonify({'categories': categories})

@news_bp.route('/news/bulk-fetch', methods=['POST'])
def bulk_fetch_news():
    """Fetch news from multiple sources and categories"""
    try:
        # Try to fetch from real APIs first, but fall back to sample data
        total_stored = 0
        total_skipped = 0
        
        # Check if we have valid API keys
        if news_fetcher.newsapi_key == 'your_newsapi_key_here':
            # Use sample data instead
            print("Using sample data since API keys are not configured")
            sample_articles = sample_generator.generate_sample_articles(10)
            
            for article_data in sample_articles:
                # Check if article already exists
                existing_article = Article.query.filter_by(url=article_data['url']).first()
                if existing_article:
                    total_skipped += 1
                    continue
                
                # Create new article
                article = Article(
                    title=article_data['title'],
                    url=article_data['url'],
                    source=article_data['source'],
                    author=article_data.get('author'),
                    published_date=article_data.get('published_date') or datetime.utcnow(),
                    content=article_data.get('content', ''),
                    category=article_data.get('category'),
                    image_url=article_data.get('image_url')
                )
                
                db.session.add(article)
                total_stored += 1
        else:
            # Use real API data
            categories = ['business', 'technology', 'science', 'health', 'sports']
            
            for category in categories:
                # Fetch from NewsAPI
                articles = news_fetcher.fetch_from_newsapi(category=category)
                
                for article_data in articles:
                    # Check if article already exists
                    existing_article = Article.query.filter_by(url=article_data['url']).first()
                    if existing_article:
                        total_skipped += 1
                        continue
                    
                    # Create new article
                    article = Article(
                        title=article_data['title'],
                        url=article_data['url'],
                        source=article_data['source'],
                        author=article_data.get('author'),
                        published_date=article_data.get('published_date') or datetime.utcnow(),
                        content=article_data.get('content', article_data.get('description', '')),
                        category=category,  # Set the category
                        image_url=article_data.get('image_url')
                    )
                    
                    db.session.add(article)
                    total_stored += 1
        
        db.session.commit()
        
        return jsonify({
            'message': f'Bulk fetch completed. Stored {total_stored} articles',
            'stored': total_stored,
            'skipped': total_skipped
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Bulk fetch failed: {str(e)}'}), 500


@news_bp.route('/news/sample-trending', methods=['GET'])
def get_sample_trending():
    """Get sample trending keywords for testing"""
    try:
        trending = sample_generator.get_sample_trending_keywords()
        return jsonify({'trending_keywords': trending})
    except Exception as e:
        return jsonify({'error': f'Failed to get sample trending: {str(e)}'}), 500

@news_bp.route('/news/sample-stats', methods=['GET'])
def get_sample_stats():
    """Get sample category statistics for testing"""
    try:
        stats = sample_generator.get_sample_category_stats()
        return jsonify({'category_distribution': stats})
    except Exception as e:
        return jsonify({'error': f'Failed to get sample stats: {str(e)}'}), 500

