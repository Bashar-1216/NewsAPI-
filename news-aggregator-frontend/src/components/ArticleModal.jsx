import { X, ExternalLink, Clock, User, Tag, Heart, Share2 } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog'

const ArticleModal = ({ article, isOpen, onClose }) => {
  if (!article) return null

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
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
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <div className="flex items-start justify-between">
            <div className="flex-1 pr-4">
              <div className="flex items-center gap-2 mb-3">
                {article.category && (
                  <Badge className={`text-xs ${getCategoryColor(article.category)}`}>
                    <Tag className="h-3 w-3 mr-1" />
                    {article.category.charAt(0).toUpperCase() + article.category.slice(1)}
                  </Badge>
                )}
                {article.sentiment && (
                  <Badge className={`text-xs ${getSentimentColor(article.sentiment)}`}>
                    {article.sentiment}
                  </Badge>
                )}
              </div>
              <DialogTitle className="text-2xl font-bold text-gray-900 leading-tight">
                {article.title}
              </DialogTitle>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={onClose}
              className="text-gray-500 hover:text-gray-700"
            >
              <X className="h-5 w-5" />
            </Button>
          </div>
        </DialogHeader>

        <div className="space-y-6">
          {/* Article Meta */}
          <div className="flex items-center text-sm text-gray-600 space-x-4 border-b border-gray-200 pb-4">
            <div className="flex items-center">
              <Clock className="h-4 w-4 mr-1" />
              {formatDate(article.published_date || article.created_at)}
            </div>
            <div className="flex items-center font-medium">
              {article.source}
            </div>
            {article.author && (
              <div className="flex items-center">
                <User className="h-4 w-4 mr-1" />
                {article.author}
              </div>
            )}
          </div>

          {/* Article Image */}
          {article.image_url && (
            <div className="w-full">
              <img
                src={article.image_url}
                alt={article.title}
                className="w-full h-64 object-cover rounded-lg"
                onError={(e) => {
                  e.target.style.display = 'none'
                }}
              />
            </div>
          )}

          {/* Article Summary */}
          {article.summary && (
            <div className="bg-blue-50 border-l-4 border-blue-400 p-4 rounded-r-lg">
              <h3 className="text-sm font-semibold text-blue-900 mb-2">AI Summary</h3>
              <p className="text-blue-800 text-sm leading-relaxed">{article.summary}</p>
            </div>
          )}

          {/* Article Content */}
          <div className="prose max-w-none">
            <div className="text-gray-800 leading-relaxed whitespace-pre-wrap">
              {article.content}
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex items-center justify-between pt-6 border-t border-gray-200">
            <div className="flex items-center space-x-3">
              <Button
                variant="outline"
                onClick={() => window.open(article.url, '_blank')}
                className="border-blue-600 text-blue-600 hover:bg-blue-50"
              >
                <ExternalLink className="h-4 w-4 mr-2" />
                Read Original
              </Button>
            </div>
            
            <div className="flex items-center space-x-2">
              <Button variant="ghost" size="sm" className="text-gray-500 hover:text-red-500">
                <Heart className="h-4 w-4 mr-1" />
                Save
              </Button>
              <Button variant="ghost" size="sm" className="text-gray-500 hover:text-blue-500">
                <Share2 className="h-4 w-4 mr-1" />
                Share
              </Button>
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}

export default ArticleModal

