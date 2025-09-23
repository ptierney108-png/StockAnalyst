import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { TrendingUp, TrendingDown, Search, BarChart3 } from 'lucide-react';
import StockCard from '../components/StockCard';
import api from '../services/api';

const Market = () => {
  const [activeTab, setActiveTab] = useState('trending');
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);

  const {
    data: trendingStocks,
    isLoading: loadingTrending,
  } = useQuery({
    queryKey: ['trending-stocks'],
    queryFn: api.getTrendingStocks,
  });

  const {
    data: gainers,
    isLoading: loadingGainers,
  } = useQuery({
    queryKey: ['top-gainers'],
    queryFn: api.getTopGainers,
  });

  const {
    data: losers,
    isLoading: loadingLosers,
  } = useQuery({
    queryKey: ['top-losers'],
    queryFn: api.getTopLosers,
  });

  const tabs = [
    { id: 'trending', label: 'Trending', icon: BarChart3 },
    { id: 'gainers', label: 'Top Gainers', icon: TrendingUp },
    { id: 'losers', label: 'Top Losers', icon: TrendingDown },
  ];

  const searchStocks = async (query) => {
    if (query.length < 1) {
      setSearchResults([]);
      return;
    }
    
    try {
      const results = await api.searchStocks(query);
      setSearchResults(results);
    } catch (error) {
      console.error('Search failed:', error);
      setSearchResults([]);
    }
  };

  const LoadingGrid = () => (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      {[...Array(8)].map((_, i) => (
        <div key={i} className="bg-white rounded-lg shadow p-6 animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-1/4 mb-2"></div>
          <div className="h-3 bg-gray-200 rounded w-3/4 mb-4"></div>
          <div className="h-8 bg-gray-200 rounded w-1/2 mb-2"></div>
          <div className="h-4 bg-gray-200 rounded w-1/3"></div>
        </div>
      ))}
    </div>
  );

  const getCurrentData = () => {
    switch (activeTab) {
      case 'gainers':
        return { data: gainers, loading: loadingGainers };
      case 'losers':
        return { data: losers, loading: loadingLosers };
      default:
        return { data: trendingStocks, loading: loadingTrending };
    }
  };

  const { data: currentData, loading: currentLoading } = getCurrentData();

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Market Overview</h1>
          {/* Data Source Indicator */}
          <div className="flex items-center space-x-2 text-sm text-gray-500 mt-1">
            <span className="w-2 h-2 bg-gray-500 rounded-full"></span>
            <span>Market Data: Simulated Demo Environment</span>
          </div>
        </div>
        
        {/* Search */}
        <div className="relative w-full sm:w-96">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => {
              setSearchQuery(e.target.value);
              searchStocks(e.target.value);
            }}
            className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Search stocks..."
          />
          
          {/* Search Results Dropdown */}
          {searchQuery && (
            <div className="absolute top-full left-0 right-0 mt-1 bg-white border border-gray-200 rounded-lg shadow-lg z-10 max-h-60 overflow-y-auto">
              {searchResults.length > 0 ? (
                searchResults.map((stock) => (
                  <div
                    key={stock.symbol}
                    className="p-3 hover:bg-gray-50 cursor-pointer border-b border-gray-100 last:border-b-0"
                    onClick={() => {
                      window.location.href = `/stock/${stock.symbol}`;
                    }}
                  >
                    <div className="font-medium text-gray-900">{stock.symbol}</div>
                    <div className="text-sm text-gray-500">{stock.name}</div>
                  </div>
                ))
              ) : (
                <div className="p-3 text-center text-gray-500">
                  No stocks found for "{searchQuery}"
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Market Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="p-3 rounded-lg bg-green-100">
              <TrendingUp className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Market Status</p>
              <p className="text-2xl font-bold text-gray-900">Open</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="p-3 rounded-lg bg-blue-100">
              <BarChart3 className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">S&P 500</p>
              <p className="text-2xl font-bold text-gray-900">4,567.89</p>
              <p className="text-sm text-green-600">+0.65%</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="p-3 rounded-lg bg-purple-100">
              <TrendingUp className="h-6 w-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">NASDAQ</p>
              <p className="text-2xl font-bold text-gray-900">14,123.45</p>
              <p className="text-sm text-green-600">+1.23%</p>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="flex space-x-8">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <Icon className="h-4 w-4" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Content */}
      <div>
        {currentLoading ? (
          <LoadingGrid />
        ) : !currentData || currentData.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-lg shadow">
            <BarChart3 className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              No data available
            </h3>
            <p className="text-gray-500">
              Unable to load {tabs.find(t => t.id === activeTab)?.label.toLowerCase()} data
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {currentData.map((stock) => (
              <StockCard key={stock.symbol} stock={stock} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Market;