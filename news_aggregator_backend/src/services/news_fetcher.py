import requests
from datetime import datetime, timedelta
import os
from typing import List, Dict, Optional

class NewsFetcher:
    """Service to fetch news from various APIs"""
    
    def __init__(self):
        # You'll need to set these environment variables or replace with actual API keys
        self.newsapi_key = os.getenv('NEWSAPI_KEY', 'your_newsapi_key_here')
        self.serpapi_key = os.getenv('SERPAPI_KEY', 'your_serpapi_key_here')
        
    def fetch_from_newsapi(self, query: str = None, category: str = None, 
                          sources: str = None, language: str = 'en', 
                          page_size: int = 20) -> List[Dict]:
        """
        Fetch news from NewsAPI
        
        Args:
            query: Keywords or phrases to search for
            category: News category (business, entertainment, general, health, science, sports, technology)
            sources: Comma-separated string of news sources or blogs
            language: Language code (en, ar, etc.)
            page_size: Number of articles to return (max 100)
        
        Returns:
            List of article dictionaries
        """
        base_url = "https://newsapi.org/v2/top-headlines"
        
        params = {
            'apiKey': self.newsapi_key,
            'language': language,
            'pageSize': page_size
        }
        
        if query:
            params['q'] = query
        if category:
            params['category'] = category
        if sources:
            params['sources'] = sources
            
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            articles = []
            for article in data.get('articles', []):
                # Skip articles with null content
                if not article.get('content') or article.get('content') == '[Removed]':
                    continue
                    
                processed_article = {
                    'title': article.get('title', ''),
                    'url': article.get('url', ''),
                    'source': article.get('source', {}).get('name', 'Unknown'),
                    'author': article.get('author'),
                    'published_date': self._parse_date(article.get('publishedAt')),
                    'content': article.get('content', ''),
                    'image_url': article.get('urlToImage'),
                    'description': article.get('description', '')
                }
                articles.append(processed_article)
                
            return articles
            
        except requests.RequestException as e:
            print(f"Error fetching from NewsAPI: {e}")
            return []
    
    def fetch_everything_newsapi(self, query: str, language: str = 'en', 
                                sort_by: str = 'publishedAt', page_size: int = 20) -> List[Dict]:
        """
        Fetch news from NewsAPI's everything endpoint for more comprehensive search
        
        Args:
            query: Keywords or phrases to search for
            language: Language code
            sort_by: Sort order (relevancy, popularity, publishedAt)
            page_size: Number of articles to return
        
        Returns:
            List of article dictionaries
        """
        base_url = "https://newsapi.org/v2/everything"
        
        # Get articles from the last 7 days
        from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        params = {
            'apiKey': self.newsapi_key,
            'q': query,
            'language': language,
            'sortBy': sort_by,
            'pageSize': page_size,
            'from': from_date
        }
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            articles = []
            for article in data.get('articles', []):
                # Skip articles with null content
                if not article.get('content') or article.get('content') == '[Removed]':
                    continue
                    
                processed_article = {
                    'title': article.get('title', ''),
                    'url': article.get('url', ''),
                    'source': article.get('source', {}).get('name', 'Unknown'),
                    'author': article.get('author'),
                    'published_date': self._parse_date(article.get('publishedAt')),
                    'content': article.get('content', ''),
                    'image_url': article.get('urlToImage'),
                    'description': article.get('description', '')
                }
                articles.append(processed_article)
                
            return articles
            
        except requests.RequestException as e:
            print(f"Error fetching from NewsAPI everything: {e}")
            return []
    
    def fetch_from_serpapi_google_news(self, query: str, gl: str = 'us', 
                                      hl: str = 'en') -> List[Dict]:
        """
        Fetch news from Google News via SerpApi
        
        Args:
            query: Search query
            gl: Country code (us, uk, etc.)
            hl: Language code (en, ar, etc.)
        
        Returns:
            List of article dictionaries
        """
        base_url = "https://serpapi.com/search"
        
        params = {
            'engine': 'google_news',
            'q': query,
            'gl': gl,
            'hl': hl,
            'api_key': self.serpapi_key
        }
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            articles = []
            for article in data.get('news_results', []):
                processed_article = {
                    'title': article.get('title', ''),
                    'url': article.get('link', ''),
                    'source': article.get('source', {}).get('name', 'Unknown') if isinstance(article.get('source'), dict) else article.get('source', 'Unknown'),
                    'author': None,  # Google News doesn't always provide author info
                    'published_date': self._parse_google_news_date(article.get('date')),
                    'content': article.get('snippet', ''),  # Google News provides snippets, not full content
                    'image_url': article.get('thumbnail'),
                    'description': article.get('snippet', '')
                }
                articles.append(processed_article)
                
            return articles
            
        except requests.RequestException as e:
            print(f"Error fetching from SerpApi Google News: {e}")
            return []
    
    def _parse_date(self, date_string: str) -> Optional[datetime]:
        """Parse ISO date string to datetime object"""
        if not date_string:
            return None
        try:
            # Handle different date formats
            if 'T' in date_string:
                return datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            else:
                return datetime.strptime(date_string, '%Y-%m-%d')
        except (ValueError, TypeError):
            return None
    
    def _parse_google_news_date(self, date_string: str) -> Optional[datetime]:
        """Parse Google News date format"""
        if not date_string:
            return None
        try:
            # Google News dates are often relative (e.g., "2 hours ago")
            # For now, return current time - in a real implementation,
            # you'd want to parse relative dates properly
            return datetime.now()
        except (ValueError, TypeError):
            return None
    
    def fetch_trending_topics(self) -> List[str]:
        """
        Fetch trending topics from Google News
        This is a simplified implementation - you might want to enhance it
        """
        try:
            # Fetch general news to identify trending topics
            articles = self.fetch_from_serpapi_google_news("trending")
            
            # Extract keywords from titles (simplified approach)
            topics = []
            for article in articles[:10]:  # Take first 10 articles
                title_words = article['title'].split()
                # Simple keyword extraction - in practice, you'd use NLP
                for word in title_words:
                    if len(word) > 4 and word.lower() not in ['news', 'says', 'after', 'with', 'from']:
                        topics.append(word)
            
            # Return unique topics
            return list(set(topics))[:20]
            
        except Exception as e:
            print(f"Error fetching trending topics: {e}")
            return []

