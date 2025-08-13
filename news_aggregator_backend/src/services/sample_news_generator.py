from datetime import datetime, timedelta
import random
import uuid

class SampleNewsGenerator:
    """Generate sample news articles for testing purposes"""
    
    def __init__(self):
        self.sample_articles = [
            {
                'title': 'Breakthrough in Quantum Computing Achieved by Tech Giants',
                'content': 'Scientists at leading technology companies have announced a major breakthrough in quantum computing that could revolutionize data processing. The new quantum processor demonstrates unprecedented stability and computational power, potentially solving complex problems that are currently impossible for classical computers. This advancement brings us closer to practical quantum computing applications in cryptography, drug discovery, and artificial intelligence. The research team spent over five years developing the technology, overcoming significant technical challenges related to quantum decoherence and error correction.',
                'source': 'TechCrunch',
                'author': 'Sarah Johnson',
                'category': 'technology',
                'image_url': 'https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=400'
            },
            {
                'title': 'Global Markets Rally as Economic Indicators Show Strong Growth',
                'content': 'Stock markets worldwide experienced significant gains today following the release of positive economic indicators. GDP growth exceeded expectations in major economies, while unemployment rates continued to decline. Analysts attribute the positive trends to increased consumer spending and business investment. The technology sector led the rally, with several companies reporting record quarterly earnings. However, some economists warn that inflation concerns remain a potential risk factor for sustained growth.',
                'source': 'Reuters',
                'author': 'Michael Chen',
                'category': 'business',
                'image_url': 'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=400'
            },
            {
                'title': 'Revolutionary Gene Therapy Shows Promise in Cancer Treatment',
                'content': 'A groundbreaking gene therapy treatment has shown remarkable success in clinical trials for treating aggressive forms of cancer. The therapy works by modifying patients\' immune cells to better recognize and attack cancer cells. Early results indicate a 70% success rate in patients who had not responded to traditional treatments. The FDA is fast-tracking the approval process due to the therapy\'s potential to save lives. Medical experts believe this could represent a paradigm shift in cancer treatment approaches.',
                'source': 'Medical News Today',
                'author': 'Dr. Emily Rodriguez',
                'category': 'health',
                'image_url': 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=400'
            },
            {
                'title': 'Climate Scientists Discover New Method to Capture Carbon from Atmosphere',
                'content': 'Researchers have developed an innovative technology that can efficiently capture carbon dioxide directly from the atmosphere at a fraction of the current cost. The new method uses specially designed materials that can absorb CO2 and convert it into useful products. This breakthrough could play a crucial role in combating climate change by removing excess carbon from the atmosphere. The technology is scalable and could be deployed globally within the next decade if funding and regulatory approval are secured.',
                'source': 'Nature',
                'author': 'Prof. David Thompson',
                'category': 'science',
                'image_url': 'https://images.unsplash.com/photo-1569163139394-de4e4f43e4e3?w=400'
            },
            {
                'title': 'Championship Finals Set as Underdog Team Advances',
                'content': 'In a stunning upset, the underdog team defeated the defending champions to secure their place in the championship finals. The match was decided in the final minutes with a spectacular performance that left fans and analysts amazed. This marks the first time in the team\'s history that they have reached the finals. The victory was attributed to exceptional teamwork and strategic gameplay that caught their opponents off guard. Ticket sales for the finals have already broken records.',
                'source': 'ESPN',
                'author': 'James Wilson',
                'category': 'sports',
                'image_url': 'https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=400'
            },
            {
                'title': 'Streaming Platform Announces Massive Investment in Original Content',
                'content': 'A major streaming platform has announced a $10 billion investment in original content production over the next three years. The investment will fund hundreds of new series, movies, and documentaries across multiple genres and languages. The company aims to compete more effectively with established entertainment giants and attract subscribers globally. Several high-profile directors and actors have already signed exclusive deals. Industry analysts predict this could reshape the entertainment landscape significantly.',
                'source': 'Variety',
                'author': 'Lisa Martinez',
                'category': 'entertainment',
                'image_url': 'https://images.unsplash.com/photo-1489599735188-900b2b7c2e8e?w=400'
            },
            {
                'title': 'New Environmental Protection Bill Passes with Bipartisan Support',
                'content': 'Congress has passed comprehensive environmental protection legislation with rare bipartisan support. The bill includes provisions for renewable energy incentives, stricter pollution controls, and funding for environmental restoration projects. Environmental groups have praised the legislation as a significant step forward in addressing climate change. The bill also creates thousands of jobs in the green energy sector. President is expected to sign the bill into law next week.',
                'source': 'Associated Press',
                'author': 'Robert Davis',
                'category': 'politics',
                'image_url': 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=400'
            },
            {
                'title': 'Artificial Intelligence Helps Doctors Diagnose Rare Diseases',
                'content': 'A new AI system has demonstrated remarkable accuracy in diagnosing rare diseases that often stump medical professionals. The system analyzes patient symptoms, medical history, and test results to suggest potential diagnoses. In clinical trials, the AI correctly identified rare conditions 85% of the time, compared to 65% for human doctors alone. The technology could be particularly valuable in areas with limited access to specialist physicians. Several hospitals are already implementing the system.',
                'source': 'BBC Health',
                'author': 'Dr. Amanda Foster',
                'category': 'health',
                'image_url': 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1f?w=400'
            },
            {
                'title': 'Space Mission Successfully Lands on Mars, Begins Scientific Research',
                'content': 'The latest Mars mission has successfully landed on the red planet and begun its scientific research operations. The rover is equipped with advanced instruments to search for signs of past or present life and analyze the planet\'s geology. Initial images and data have already provided new insights into Mars\' atmospheric conditions and surface composition. The mission is expected to operate for at least two years, with the possibility of extension. Scientists worldwide are eagerly awaiting the discoveries that may reshape our understanding of Mars.',
                'source': 'NASA News',
                'author': 'Dr. Jennifer Kim',
                'category': 'science',
                'image_url': 'https://images.unsplash.com/photo-1446776877081-d282a0f896e2?w=400'
            },
            {
                'title': 'Cybersecurity Experts Warn of New Sophisticated Threat',
                'content': 'Cybersecurity researchers have identified a new type of malware that poses significant risks to both individual users and organizations. The malware uses advanced techniques to avoid detection and can steal sensitive information without users\' knowledge. Security experts recommend updating all software immediately and implementing additional security measures. The threat appears to be state-sponsored and targets critical infrastructure. Government agencies are working with private companies to develop countermeasures.',
                'source': 'CyberSecurity Today',
                'author': 'Alex Thompson',
                'category': 'technology',
                'image_url': 'https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=400'
            }
        ]
    
    def generate_sample_articles(self, count=10):
        """Generate sample articles with realistic data"""
        articles = []
        
        for i in range(min(count, len(self.sample_articles))):
            article = self.sample_articles[i].copy()
            
            # Add realistic timestamps
            days_ago = random.randint(0, 7)
            hours_ago = random.randint(0, 23)
            published_date = datetime.utcnow() - timedelta(days=days_ago, hours=hours_ago)
            
            article.update({
                'url': f'https://example.com/article-{uuid.uuid4().hex[:8]}',
                'published_date': published_date,
                'created_at': datetime.utcnow()
            })
            
            articles.append(article)
        
        return articles
    
    def get_sample_trending_keywords(self):
        """Generate sample trending keywords"""
        keywords = [
            {'keyword': 'quantum computing', 'frequency': 45},
            {'keyword': 'artificial intelligence', 'frequency': 38},
            {'keyword': 'climate change', 'frequency': 32},
            {'keyword': 'gene therapy', 'frequency': 28},
            {'keyword': 'cybersecurity', 'frequency': 25},
            {'keyword': 'space exploration', 'frequency': 22},
            {'keyword': 'renewable energy', 'frequency': 20},
            {'keyword': 'machine learning', 'frequency': 18},
            {'keyword': 'biotechnology', 'frequency': 15},
            {'keyword': 'blockchain', 'frequency': 12}
        ]
        return keywords
    
    def get_sample_category_stats(self):
        """Generate sample category statistics"""
        stats = [
            {'category': 'technology', 'count': 25},
            {'category': 'health', 'count': 18},
            {'category': 'science', 'count': 15},
            {'category': 'business', 'count': 12},
            {'category': 'politics', 'count': 10},
            {'category': 'sports', 'count': 8},
            {'category': 'entertainment', 'count': 6},
            {'category': 'general', 'count': 4}
        ]
        return stats

