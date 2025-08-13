from flask import Blueprint, jsonify, request
from src.services.ai_analyzer import NewsAIAnalyzer
from src.models.article import Article, db
from datetime import datetime

ai_bp = Blueprint('ai', __name__)
ai_analyzer = NewsAIAnalyzer()

@ai_bp.route('/ai/analyze-article', methods=['POST'])
def analyze_single_article():
    """Analyze a single article with AI"""
    data = request.json
    
    if not data or not all(key in data for key in ['title', 'content', 'source']):
        return jsonify({'error': 'Missing required fields: title, content, source'}), 400
    
    try:
        analysis = ai_analyzer.analyze_article(
            title=data['title'],
            content=data['content'],
            source=data['source']
        )
        
        return jsonify({
            'message': 'Article analyzed successfully',
            'analysis': analysis
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@ai_bp.route('/ai/analyze-stored-articles', methods=['POST'])
def analyze_stored_articles():
    """Analyze all stored articles that haven't been analyzed yet"""
    try:
        # Get articles that haven't been analyzed (no category or sentiment)
        unanalyzed_articles = Article.query.filter(
            (Article.category.is_(None)) | (Article.sentiment.is_(None))
        ).all()
        
        if not unanalyzed_articles:
            return jsonify({
                'message': 'No unanalyzed articles found',
                'analyzed_count': 0
            }), 200
        
        analyzed_count = 0
        
        for article in unanalyzed_articles:
            try:
                analysis = ai_analyzer.analyze_article(
                    title=article.title,
                    content=article.content,
                    source=article.source
                )
                
                # Update article with analysis results
                article.category = analysis['category']
                article.sentiment = analysis['sentiment']
                article.is_fake = analysis['is_fake']
                article.summary = analysis['summary']
                
                analyzed_count += 1
                
            except Exception as e:
                print(f"Error analyzing article {article.id}: {e}")
                continue
        
        # Commit all changes
        db.session.commit()
        
        return jsonify({
            'message': f'Successfully analyzed {analyzed_count} articles',
            'analyzed_count': analyzed_count,
            'total_unanalyzed': len(unanalyzed_articles)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Batch analysis failed: {str(e)}'}), 500

@ai_bp.route('/ai/analyze-article/<string:article_id>', methods=['POST'])
def analyze_article_by_id(article_id):
    """Analyze a specific stored article by ID"""
    try:
        article = Article.query.get_or_404(article_id)
        
        analysis = ai_analyzer.analyze_article(
            title=article.title,
            content=article.content,
            source=article.source
        )
        
        # Update article with analysis results
        article.category = analysis['category']
        article.sentiment = analysis['sentiment']
        article.is_fake = analysis['is_fake']
        article.summary = analysis['summary']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Article analyzed and updated successfully',
            'article_id': article_id,
            'analysis': analysis
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@ai_bp.route('/ai/sentiment-analysis', methods=['POST'])
def sentiment_analysis():
    """Perform sentiment analysis on provided text"""
    data = request.json
    
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing required field: text'}), 400
    
    try:
        sentiment_data = ai_analyzer.analyze_sentiment(data['text'])
        
        return jsonify({
            'message': 'Sentiment analysis completed',
            'sentiment': sentiment_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Sentiment analysis failed: {str(e)}'}), 500

@ai_bp.route('/ai/summarize', methods=['POST'])
def summarize_text():
    """Summarize provided text"""
    data = request.json
    
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing required field: text'}), 400
    
    max_sentences = data.get('max_sentences', 3)
    
    try:
        summary = ai_analyzer.summarize_text(data['text'], max_sentences)
        
        return jsonify({
            'message': 'Text summarized successfully',
            'summary': summary,
            'original_length': len(data['text']),
            'summary_length': len(summary)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Summarization failed: {str(e)}'}), 500

@ai_bp.route('/ai/detect-fake-news', methods=['POST'])
def detect_fake_news():
    """Detect if news content might be fake"""
    data = request.json
    
    if not data or not all(key in data for key in ['title', 'content', 'source']):
        return jsonify({'error': 'Missing required fields: title, content, source'}), 400
    
    try:
        fake_news_data = ai_analyzer.detect_fake_news(
            title=data['title'],
            content=data['content'],
            source=data['source']
        )
        
        return jsonify({
            'message': 'Fake news detection completed',
            'fake_news_analysis': fake_news_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Fake news detection failed: {str(e)}'}), 500

@ai_bp.route('/ai/trending-keywords', methods=['GET'])
def get_trending_keywords():
    """Get trending keywords from recent articles"""
    try:
        # Get recent articles (last 7 days)
        from datetime import datetime, timedelta
        week_ago = datetime.utcnow() - timedelta(days=7)
        
        recent_articles = Article.query.filter(
            Article.created_at >= week_ago
        ).all()
        
        if not recent_articles:
            return jsonify({
                'message': 'No recent articles found',
                'trending_keywords': []
            }), 200
        
        # Convert to dict format for analyzer
        articles_data = [
            {
                'title': article.title,
                'content': article.content
            }
            for article in recent_articles
        ]
        
        trending_keywords = ai_analyzer.get_trending_keywords(articles_data)
        
        return jsonify({
            'message': f'Found trending keywords from {len(recent_articles)} recent articles',
            'trending_keywords': [
                {'keyword': keyword, 'frequency': freq}
                for keyword, freq in trending_keywords
            ],
            'articles_analyzed': len(recent_articles)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Trending keywords analysis failed: {str(e)}'}), 500

@ai_bp.route('/ai/category-stats', methods=['GET'])
def get_category_statistics():
    """Get statistics about article categories"""
    try:
        # Get category distribution
        category_stats = db.session.query(
            Article.category,
            db.func.count(Article.id).label('count')
        ).filter(
            Article.category.isnot(None)
        ).group_by(Article.category).all()
        
        # Get sentiment distribution
        sentiment_stats = db.session.query(
            Article.sentiment,
            db.func.count(Article.id).label('count')
        ).filter(
            Article.sentiment.isnot(None)
        ).group_by(Article.sentiment).all()
        
        # Get fake news statistics
        fake_news_count = Article.query.filter(Article.is_fake == True).count()
        total_articles = Article.query.count()
        
        return jsonify({
            'category_distribution': [
                {'category': cat, 'count': count}
                for cat, count in category_stats
            ],
            'sentiment_distribution': [
                {'sentiment': sent, 'count': count}
                for sent, count in sentiment_stats
            ],
            'fake_news_stats': {
                'fake_count': fake_news_count,
                'total_articles': total_articles,
                'fake_percentage': (fake_news_count / total_articles * 100) if total_articles > 0 else 0
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Statistics retrieval failed: {str(e)}'}), 500

