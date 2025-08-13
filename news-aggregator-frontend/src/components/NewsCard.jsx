import { Clock, ExternalLink, Heart, Share2, BookOpen, AlertTriangle } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardFooter, CardHeader } from '@/components/ui/card'

const NewsCard = ({ article, onReadMore }) => {
  const formatDate = (dateString) => {
    const date = new Date(dateString)
    const now = new Date()
    const diffInHours = Math.floor((now - date) / (1000 * 60 * 60))
    
    if (diffInHours < 1) return 'Just now'
    if (diffInHours < 24) return `${diffInHours}h ago`
    if (diffInHours < 48) return 'Yesterday'
    return date.toLocaleDateString()
  }

  const getSentimentColor = (sentiment) => {
    switch (sentiment) {
      case 'positive': return 'bg-green-100 text-green-800'
      case 'negative': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getCategoryColor = (category) => {
    const colors = {
      technology: 'bg-blue-100 text-blue-800',
      business: 'bg-green-100 text-green-800',
      sports: 'bg-orange-100 text-orange-800',
      health: 'bg-pink-100 text-pink-800',
      science: 'bg-purple-100 text-purple-800',
      entertainment: 'bg-yellow-100 text-yellow-800',
      politics: 'bg-red-100 text-red-800',
      general: 'bg-gray-100 text-gray-800'
    }
    return colors[category] || colors.general
  }

  return (
    <Card className="group hover:shadow-lg transition-all duration-300 border border-gray-200 hover:border-blue-300">
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between gap-3">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              {article.category && (
                <Badge className={`text-xs ${getCategoryColor(article.category)}`}>
                  {article.category.charAt(0).toUpperCase() + article.category.slice(1)}
                </Badge>
              )}
              {article.sentiment && (
                <Badge className={`text-xs ${getSentimentColor(article.sentiment)}`}>
                  {article.sentiment}
                </Badge>
              )}
              {article.is_fake && (
                <Badge className="text-xs bg-red-100 text-red-800">
                  <AlertTriangle className="h-3 w-3 mr-1" />
                  Suspicious
                </Badge>
              )}
            </div>
            <h3 className="text-lg font-semibold text-gray-900 group-hover:text-blue-600 transition-colors line-clamp-2">
              {article.title}
            </h3>
          </div>
          {article.image_url && (
            <div className="flex-shrink-0">
              <img
                src={article.image_url}
                alt={article.title}
                className="w-20 h-20 object-cover rounded-lg"
                onError={(e) => {
                  e.target.style.display = 'none'
                }}
              />
            </div>
          )}
        </div>
      </CardHeader>

      <CardContent className="pt-0">
        <p className="text-gray-600 text-sm line-clamp-3 mb-3">
          {article.summary || article.content?.substring(0, 200) + '...'}
        </p>
        
        <div className="flex items-center text-xs text-gray-500 space-x-4">
          <div className="flex items-center">
            <Clock className="h-3 w-3 mr-1" />
            {formatDate(article.published_date || article.created_at)}
          </div>
          <div className="flex items-center">
            <span className="font-medium">{article.source}</span>
          </div>
          {article.author && (
            <div className="flex items-center">
              <span>by {article.author}</span>
            </div>
          )}
        </div>
      </CardContent>

      <CardFooter className="pt-0">
        <div className="flex items-center justify-between w-full">
          <div className="flex items-center space-x-2">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => onReadMore(article)}
              className="text-blue-600 hover:text-blue-700 hover:bg-blue-50"
            >
              <BookOpen className="h-4 w-4 mr-1" />
              Read More
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => window.open(article.url, '_blank')}
              className="text-gray-600 hover:text-gray-700"
            >
              <ExternalLink className="h-4 w-4 mr-1" />
              Source
            </Button>
          </div>
          
          <div className="flex items-center space-x-1">
            <Button variant="ghost" size="sm" className="text-gray-500 hover:text-red-500">
              <Heart className="h-4 w-4" />
            </Button>
            <Button variant="ghost" size="sm" className="text-gray-500 hover:text-blue-500">
              <Share2 className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </CardFooter>
    </Card>
  )
}

export default NewsCard

