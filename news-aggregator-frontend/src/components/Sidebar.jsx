import { TrendingUp, BarChart3, Filter, Settings, User, Bookmark } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

const Sidebar = ({ trendingKeywords, categoryStats, onFilterChange }) => {
  const sidebarItems = [
    { icon: User, label: 'Profile', active: false },
    { icon: Bookmark, label: 'Saved Articles', active: false },
    { icon: Filter, label: 'Filters', active: true },
    { icon: BarChart3, label: 'Analytics', active: false },
    { icon: Settings, label: 'Settings', active: false },
  ]

  return (
    <aside className="w-80 bg-gray-50 border-r border-gray-200 h-screen overflow-y-auto">
      <div className="p-6 space-y-6">
        {/* Navigation */}
        <div>
          <h2 className="text-sm font-semibold text-gray-900 mb-3">Navigation</h2>
          <nav className="space-y-1">
            {sidebarItems.map((item) => (
              <Button
                key={item.label}
                variant={item.active ? "default" : "ghost"}
                className={`w-full justify-start ${
                  item.active 
                    ? 'bg-blue-600 text-white hover:bg-blue-700' 
                    : 'text-gray-700 hover:text-blue-600 hover:bg-blue-50'
                }`}
              >
                <item.icon className="h-4 w-4 mr-3" />
                {item.label}
              </Button>
            ))}
          </nav>
        </div>

        {/* Trending Keywords */}
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-semibold text-gray-900 flex items-center">
              <TrendingUp className="h-4 w-4 mr-2 text-green-600" />
              Trending Now
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-0">
            <div className="space-y-2">
              {trendingKeywords && trendingKeywords.length > 0 ? (
                trendingKeywords.slice(0, 10).map((keyword, index) => (
                  <div key={index} className="flex items-center justify-between">
                    <Badge 
                      variant="secondary" 
                      className="text-xs cursor-pointer hover:bg-blue-100 hover:text-blue-800"
                      onClick={() => onFilterChange('search', keyword.keyword)}
                    >
                      {keyword.keyword}
                    </Badge>
                    <span className="text-xs text-gray-500">{keyword.frequency}</span>
                  </div>
                ))
              ) : (
                <p className="text-xs text-gray-500">No trending keywords available</p>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Category Statistics */}
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-semibold text-gray-900 flex items-center">
              <BarChart3 className="h-4 w-4 mr-2 text-blue-600" />
              Categories
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-0">
            <div className="space-y-3">
              {categoryStats && categoryStats.length > 0 ? (
                categoryStats.map((stat, index) => (
                  <div key={index} className="space-y-1">
                    <div className="flex items-center justify-between">
                      <span 
                        className="text-sm text-gray-700 cursor-pointer hover:text-blue-600"
                        onClick={() => onFilterChange('category', stat.category)}
                      >
                        {stat.category.charAt(0).toUpperCase() + stat.category.slice(1)}
                      </span>
                      <span className="text-xs text-gray-500">{stat.count}</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-1">
                      <div 
                        className="bg-blue-600 h-1 rounded-full transition-all duration-300"
                        style={{ 
                          width: `${Math.min((stat.count / Math.max(...categoryStats.map(s => s.count))) * 100, 100)}%` 
                        }}
                      ></div>
                    </div>
                  </div>
                ))
              ) : (
                <p className="text-xs text-gray-500">No category data available</p>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Quick Filters */}
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-semibold text-gray-900 flex items-center">
              <Filter className="h-4 w-4 mr-2 text-purple-600" />
              Quick Filters
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-0">
            <div className="space-y-2">
              <Button 
                variant="outline" 
                size="sm" 
                className="w-full justify-start text-xs"
                onClick={() => onFilterChange('sentiment', 'positive')}
              >
                <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                Positive News
              </Button>
              <Button 
                variant="outline" 
                size="sm" 
                className="w-full justify-start text-xs"
                onClick={() => onFilterChange('sentiment', 'negative')}
              >
                <div className="w-2 h-2 bg-red-500 rounded-full mr-2"></div>
                Negative News
              </Button>
              <Button 
                variant="outline" 
                size="sm" 
                className="w-full justify-start text-xs"
                onClick={() => onFilterChange('fake', 'false')}
              >
                <div className="w-2 h-2 bg-blue-500 rounded-full mr-2"></div>
                Verified Only
              </Button>
              <Button 
                variant="outline" 
                size="sm" 
                className="w-full justify-start text-xs"
                onClick={() => onFilterChange('recent', 'today')}
              >
                <div className="w-2 h-2 bg-orange-500 rounded-full mr-2"></div>
                Today's News
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </aside>
  )
}

export default Sidebar

