import { useState, useEffect } from 'react'
import Header from './components/Header'
import Sidebar from './components/Sidebar'
import NewsCard from './components/NewsCard'
import ArticleModal from './components/ArticleModal'
import LoadingSpinner from './components/LoadingSpinner'
import { Button } from '@/components/ui/button'
import { RefreshCw, AlertCircle } from 'lucide-react'
import './App.css'

function App() {
  const [articles, setArticles] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [selectedArticle, setSelectedArticle] = useState(null)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [trendingKeywords, setTrendingKeywords] = useState([])
  const [categoryStats, setCategoryStats] = useState([])
  const [filters, setFilters] = useState({
    search: '',
    category: '',
    sentiment: '',
    source: ''
  })

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';

  // Fetch articles
  const fetchArticles = async () => {
    try {
      setLoading(true)
      setError(null)
      
      const params = new URLSearchParams()
      if (filters.search) params.append('search', filters.search)
      if (filters.category && filters.category !== 'all') params.append('category', filters.category)
      if (filters.sentiment) params.append('sentiment', filters.sentiment)
      if (filters.source) params.append('source', filters.source)
      
      const response = await fetch(`${API_BASE_URL}/articles?${params}`)
      if (!response.ok) throw new Error('Failed to fetch articles')
      
      const data = await response.json()
      setArticles(data.articles || [])
    } catch (err) {
      setError(err.message)
      console.error('Error fetching articles:', err)
    } finally {
      setLoading(false)
    }
  }

  // Fetch trending keywords
  const fetchTrendingKeywords = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/ai/trending-keywords`)
      if (response.ok) {
        const data = await response.json()
        setTrendingKeywords(data.trending_keywords || [])
      }
    } catch (err) {
      console.error('Error fetching trending keywords:', err)
    }
  }

  // Fetch category statistics
  const fetchCategoryStats = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/ai/category-stats`)
      if (response.ok) {
        const data = await response.json()
        setCategoryStats(data.category_distribution || [])
      }
    } catch (err) {
      console.error('Error fetching category stats:', err)
    }
  }

  // Fetch sample news data
  const fetchSampleNews = async () => {
    try {
      setLoading(true)
      const response = await fetch(`${API_BASE_URL}/news/bulk-fetch`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      })
      
      if (response.ok) {
        // After fetching, analyze the articles
        await fetch(`${API_BASE_URL}/ai/analyze-stored-articles`, {
          method: 'POST'
        })
        
        // Refresh the articles list
        await fetchArticles()
        await fetchTrendingKeywords()
        await fetchCategoryStats()
      }
    } catch (err) {
      console.error('Error fetching sample news:', err)
      setError('Failed to fetch sample news')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchArticles()
    fetchTrendingKeywords()
    fetchCategoryStats()
  }, [filters])

  const handleSearch = (query) => {
    setFilters(prev => ({ ...prev, search: query }))
  }

  const handleCategoryFilter = (category) => {
    setFilters(prev => ({ ...prev, category }))
  }

  const handleFilterChange = (type, value) => {
    setFilters(prev => ({ ...prev, [type]: value }))
  }

  const handleReadMore = (article) => {
    setSelectedArticle(article)
    setIsModalOpen(true)
  }

  const handleRefresh = () => {
    fetchArticles()
    fetchTrendingKeywords()
    fetchCategoryStats()
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header 
        onSearch={handleSearch}
        onCategoryFilter={handleCategoryFilter}
      />
      
      <div className="flex">
        <Sidebar 
          trendingKeywords={trendingKeywords}
          categoryStats={categoryStats}
          onFilterChange={handleFilterChange}
        />
        
        <main className="flex-1 p-6">
          <div className="max-w-6xl mx-auto">
            {/* Header Actions */}
            <div className="flex items-center justify-between mb-6">
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Latest News</h1>
                <p className="text-gray-600 mt-1">
                  {articles.length} articles found
                  {filters.search && ` for "${filters.search}"`}
                  {filters.category && filters.category !== 'all' && ` in ${filters.category}`}
                </p>
              </div>
              <div className="flex items-center space-x-3">
                <Button
                  variant="outline"
                  onClick={handleRefresh}
                  disabled={loading}
                  className="border-blue-600 text-blue-600 hover:bg-blue-50"
                >
                  <RefreshCw className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
                  Refresh
                </Button>
                <Button
                  onClick={fetchSampleNews}
                  disabled={loading}
                  className="bg-blue-600 hover:bg-blue-700 text-white"
                >
                  Fetch Sample News
                </Button>
              </div>
            </div>

            {/* Content */}
            {loading ? (
              <LoadingSpinner text="Loading news articles..." />
            ) : error ? (
              <div className="text-center py-12">
                <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Error Loading Articles</h3>
                <p className="text-gray-600 mb-4">{error}</p>
                <Button onClick={handleRefresh} variant="outline">
                  Try Again
                </Button>
              </div>
            ) : articles.length === 0 ? (
              <div className="text-center py-12">
                <div className="text-gray-400 mb-4">
                  <svg className="h-16 w-16 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z" />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">No Articles Found</h3>
                <p className="text-gray-600 mb-4">
                  Try adjusting your filters or fetch some sample news to get started.
                </p>
                <Button onClick={fetchSampleNews} className="bg-blue-600 hover:bg-blue-700 text-white">
                  Fetch Sample News
                </Button>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {articles.map((article) => (
                  <NewsCard
                    key={article.id}
                    article={article}
                    onReadMore={handleReadMore}
                  />
                ))}
              </div>
            )}
          </div>
        </main>
      </div>

      {/* Article Modal */}
      <ArticleModal
        article={selectedArticle}
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
      />
    </div>
  )
}

export default App
