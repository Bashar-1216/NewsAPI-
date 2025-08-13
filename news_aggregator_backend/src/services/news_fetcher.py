import requests
from datetime import datetime, timedelta
import os
from typing import List, Dict, Optional

class NewsFetcher:
    """Service to fetch news from various APIs"""
    
    def __init__(self):
        # Use environment variables for API keys
        self.newsapi_key = os.getenv('NEWSAPI_KEY')
        self.serpapi_key = os.getenv('SERPAPI_KEY')
        
        if not self.newsapi_key or not self.serpapi_key:
            raise ValueError("Please set NEWSAPI_KEY and SERPAPI_KEY in environment variables.")

        # Optional: allow overriding backend base URL
        self.base_url_override = os.getenv('BASE_API_URL')

    def fetch_from_newsapi(self, query: str = None, category: str = None, 
                          sources: str = None, language: str = 'en', 
                          page_size: int = 20) -> List[Dict]:
        """Fetch top headlines from NewsAPI"""
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
                if not article.get('content') or article.get('content') == '[Removed]':
                    continue
                articles.append({
                    'title': article.get('title', ''),
                    'url': article.get('url', ''),
                    'source': article.get('source', {}).get('name', 'Unknown'),
                    'author': article.get('author'),
                    'published_date': self._parse_date(article.get('publishedAt')),
                    'content': article.get('content', ''),
                    'image_url': article.get('urlToImage'),
                    'description': article.get('description', '')
                })
            return articles
        except requests.RequestException as e:
            print(f"Error fetching from NewsAPI: {e}")
            return []

    def fetch_everything_newsapi(self, query: str, language: str = 'en', 
                                sort_by: str = 'publishedAt', page_size: int = 20) -> List[Dict]:
        """Fetch news from NewsAPI's everything endpoint"""
        base_url = "https://newsapi.org/v2/everything"
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
                if not article.get('content') or article.get('content') == '[Removed]':
                    continue
                articles.append({
                    'title': article.get('title', ''),
                    'url': article.get('url', ''),
                    'source': article.get('source', {}).get('name', 'Unknown'),
                    'author': article.get('author'),
                    'published_date': self._parse_date(article.get('publishedAt')),
                    'content': article.get('content', ''),
                    'image_url': article.get('urlToImage'),
                    'description': article.get('description', '')
                })
            return articles
        except requests.RequestException as e:
            print(f"Error fetching from NewsAPI everything: {e}")
            return []

    def fetch_from_serpapi_google_news(self, query: str, gl: str = 'us', hl: str = 'en') -> List[Dict]:
        """Fetch news from Google News via SerpApi"""
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
                articles.append({
                    'title': article.get('title', ''),
                    'url': article.get('link', ''),
                    'source': article.get('source', {}).get('name', 'Unknown') if isinstance(article.get('source'), dict) else article.get('source', 'Unknown'),
                    'author': None,
                    'published_date': self._parse_google_news_date(article.get('date')),
                    'content': article.get('snippet', ''),
                    'image_url': article.get('thumbnail'),
                    'description': article.get('snippet', '')
                })
            return articles
        except requests.RequestException as e:
            print(f"Error fetching from SerpApi Google News: {e}")
            return []

    def _parse_date(self, date_string: str) -> Optional[datetime]:
        """Parse ISO date string to datetime object"""
        if not date_string:
            return None
        try:
            if 'T' in date_string:
                return datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            return datetime.strptime(date_string, '%Y-%m-%d')
        except (ValueError, TypeError):
            return None

    def _parse_google_news_date(self, date_string: str) -> Optional[datetime]:
        """Parse Google News date string (simplified)"""
        if not date_string:
            return None
        try:
            # For simplicity, return current time (can enhance to parse relative dates)
            return datetime.now()
        except Exception:
            return None

    def fetch_trending_topics(self) -> List[str]:
        """Fetch trending topics from Google News (simplified)"""
        try:
            articles = self.fetch_from_serpapi_google_news("trending")
            topics = []
            for article in articles[:10]:
                for word in article['title'].split():
                    if len(word) > 4 and word.lower() not in ['news', 'says', 'after', 'with', 'from']:
                        topics.append(word)
            return list(set(topics))[:20]
        except Exception as e:
            print(f"Error fetching trending topics: {e}")
            return []
