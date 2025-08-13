import nltk
import re
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import pickle
import os
from typing import Dict, List, Optional, Tuple
import logging

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer

class NewsAIAnalyzer:
    """AI service for analyzing news articles"""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()
        self.category_classifier = None
        self.fake_news_classifier = None
        self.model_path = os.path.join(os.path.dirname(__file__), '..', 'models')
        os.makedirs(self.model_path, exist_ok=True)
        
        # Initialize or load models
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize or load pre-trained models"""
        # For now, we'll create simple rule-based classifiers
        # In a production environment, you'd train these on labeled datasets
        
        # Category classification keywords
        self.category_keywords = {
            'technology': ['tech', 'software', 'computer', 'internet', 'digital', 'ai', 'artificial intelligence', 
                          'machine learning', 'blockchain', 'cryptocurrency', 'startup', 'innovation'],
            'business': ['business', 'economy', 'market', 'stock', 'finance', 'company', 'corporate', 
                        'investment', 'profit', 'revenue', 'trade', 'industry'],
            'sports': ['sports', 'football', 'basketball', 'soccer', 'tennis', 'baseball', 'olympics', 
                      'championship', 'team', 'player', 'game', 'match'],
            'health': ['health', 'medical', 'doctor', 'hospital', 'disease', 'treatment', 'medicine', 
                      'vaccine', 'virus', 'pandemic', 'healthcare', 'wellness'],
            'science': ['science', 'research', 'study', 'discovery', 'experiment', 'scientist', 
                       'climate', 'environment', 'space', 'nasa', 'physics', 'chemistry'],
            'entertainment': ['entertainment', 'movie', 'film', 'music', 'celebrity', 'actor', 'actress', 
                             'hollywood', 'concert', 'album', 'show', 'television'],
            'politics': ['politics', 'government', 'president', 'election', 'congress', 'senate', 
                        'policy', 'law', 'vote', 'campaign', 'politician', 'democracy']
        }
        
        # Fake news indicators (simplified approach)
        self.fake_news_indicators = [
            'breaking:', 'shocking:', 'you won\'t believe', 'doctors hate', 'secret', 'exposed',
            'conspiracy', 'cover-up', 'they don\'t want you to know', 'miracle cure',
            'exclusive:', 'leaked', 'insider reveals'
        ]
    
    def preprocess_text(self, text: str) -> str:
        """Preprocess text for analysis"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Tokenize
        words = word_tokenize(text)
        
        # Remove stopwords and stem
        processed_words = [
            self.stemmer.stem(word) for word in words 
            if word not in self.stop_words and len(word) > 2
        ]
        
        return ' '.join(processed_words)
    
    def classify_category(self, title: str, content: str) -> str:
        """Classify news article category using keyword matching"""
        text = f"{title} {content}".lower()
        
        category_scores = {}
        
        for category, keywords in self.category_keywords.items():
            score = 0
            for keyword in keywords:
                # Count occurrences of each keyword
                score += text.count(keyword.lower())
            category_scores[category] = score
        
        # Return category with highest score, or 'general' if no clear category
        if max(category_scores.values()) > 0:
            return max(category_scores, key=category_scores.get)
        else:
            return 'general'
    
    def analyze_sentiment(self, text: str) -> Dict[str, any]:
        """Analyze sentiment of text using TextBlob"""
        if not text:
            return {'sentiment': 'neutral', 'polarity': 0.0, 'subjectivity': 0.0}
        
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Classify sentiment based on polarity
        if polarity > 0.1:
            sentiment = 'positive'
        elif polarity < -0.1:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        return {
            'sentiment': sentiment,
            'polarity': polarity,
            'subjectivity': subjectivity
        }
    
    def detect_fake_news(self, title: str, content: str, source: str) -> Dict[str, any]:
        """Simple fake news detection based on indicators"""
        text = f"{title} {content}".lower()
        
        # Check for fake news indicators
        indicator_count = 0
        found_indicators = []
        
        for indicator in self.fake_news_indicators:
            if indicator in text:
                indicator_count += 1
                found_indicators.append(indicator)
        
        # Simple scoring system
        fake_score = indicator_count / len(self.fake_news_indicators)
        
        # Check source reliability (simplified)
        reliable_sources = [
            'bbc', 'cnn', 'reuters', 'associated press', 'the guardian', 
            'the new york times', 'the washington post', 'npr', 'pbs'
        ]
        
        source_reliable = any(reliable in source.lower() for reliable in reliable_sources)
        
        # Determine if likely fake
        is_fake = fake_score > 0.3 and not source_reliable
        
        return {
            'is_fake': is_fake,
            'fake_score': fake_score,
            'indicators_found': found_indicators,
            'source_reliable': source_reliable
        }
    
    def summarize_text(self, text: str, max_sentences: int = 3) -> str:
        """Simple extractive summarization using sentence ranking"""
        if not text or len(text.strip()) == 0:
            return ""
        
        # Tokenize into sentences
        sentences = sent_tokenize(text)
        
        if len(sentences) <= max_sentences:
            return text
        
        # Simple scoring based on word frequency
        word_freq = {}
        processed_text = self.preprocess_text(text)
        
        for word in processed_text.split():
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Score sentences
        sentence_scores = {}
        for sentence in sentences:
            processed_sentence = self.preprocess_text(sentence)
            score = 0
            word_count = 0
            
            for word in processed_sentence.split():
                if word in word_freq:
                    score += word_freq[word]
                    word_count += 1
            
            if word_count > 0:
                sentence_scores[sentence] = score / word_count
        
        # Get top sentences
        top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:max_sentences]
        
        # Sort by original order
        summary_sentences = []
        for sentence in sentences:
            if any(sentence == s[0] for s in top_sentences):
                summary_sentences.append(sentence)
                if len(summary_sentences) >= max_sentences:
                    break
        
        return ' '.join(summary_sentences)
    
    def analyze_article(self, title: str, content: str, source: str) -> Dict[str, any]:
        """Comprehensive analysis of a news article"""
        
        # Category classification
        category = self.classify_category(title, content)
        
        # Sentiment analysis
        sentiment_data = self.analyze_sentiment(f"{title} {content}")
        
        # Fake news detection
        fake_news_data = self.detect_fake_news(title, content, source)
        
        # Text summarization
        summary = self.summarize_text(content)
        
        return {
            'category': category,
            'sentiment': sentiment_data['sentiment'],
            'sentiment_polarity': sentiment_data['polarity'],
            'sentiment_subjectivity': sentiment_data['subjectivity'],
            'is_fake': fake_news_data['is_fake'],
            'fake_score': fake_news_data['fake_score'],
            'fake_indicators': fake_news_data['indicators_found'],
            'source_reliable': fake_news_data['source_reliable'],
            'summary': summary
        }
    
    def batch_analyze_articles(self, articles: List[Dict]) -> List[Dict]:
        """Analyze multiple articles in batch"""
        analyzed_articles = []
        
        for article in articles:
            try:
                analysis = self.analyze_article(
                    article.get('title', ''),
                    article.get('content', ''),
                    article.get('source', '')
                )
                
                # Update article with analysis results
                article.update(analysis)
                analyzed_articles.append(article)
                
            except Exception as e:
                logging.error(f"Error analyzing article {article.get('title', 'Unknown')}: {e}")
                # Add default values if analysis fails
                article.update({
                    'category': 'general',
                    'sentiment': 'neutral',
                    'sentiment_polarity': 0.0,
                    'sentiment_subjectivity': 0.0,
                    'is_fake': False,
                    'fake_score': 0.0,
                    'fake_indicators': [],
                    'source_reliable': True,
                    'summary': article.get('content', '')[:200] + '...' if len(article.get('content', '')) > 200 else article.get('content', '')
                })
                analyzed_articles.append(article)
        
        return analyzed_articles
    
    def get_trending_keywords(self, articles: List[Dict], top_n: int = 20) -> List[Tuple[str, int]]:
        """Extract trending keywords from a collection of articles"""
        all_text = ""
        for article in articles:
            all_text += f" {article.get('title', '')} {article.get('content', '')}"
        
        processed_text = self.preprocess_text(all_text)
        words = processed_text.split()
        
        # Count word frequencies
        word_freq = {}
        for word in words:
            if len(word) > 3:  # Only consider words longer than 3 characters
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Return top keywords
        return sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:top_n]

