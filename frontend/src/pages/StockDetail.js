import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { TrendingUp, TrendingDown, Plus, Heart, BarChart3 } from 'lucide-react';
import StockChart from '../components/StockChart';
import api from '../services/api';

const StockDetail = () => {
  const { symbol } = useParams();
  const [selectedPeriod, setSelectedPeriod] = useState('1mo');
  const [showAddToPortfolio, setShowAddToPortfolio] = useState(false);

  const {
    data: stockData,
    isLoading: loadingStock,
    error: stockError
  } = useQuery({
    queryKey: ['stock', symbol],
    queryFn: () => api.getStockDetails(symbol),
    enabled: !!symbol,
  });

  const {
    data: historicalData,
    isLoading: loadingChart,
  } = useQuery({
    queryKey: ['historical', symbol, selectedPeriod],
    queryFn: () => api.getHistoricalData(symbol, selectedPeriod),
    enabled: !!symbol,
  });

  const {
    data: fundamentals,
    isLoading: loadingFundamentals,
  } = useQuery({
    queryKey: ['fundamentals', symbol],
    queryFn: () => api.getStockFundamentals(symbol),
    enabled: !!symbol,
  });

  const {
    data: watchlists,
  } = useQuery({
    queryKey: ['watchlists'],
    queryFn: api.getWatchlists,
  });

  const periods = [
    { label: '1D', value: '1d' },
    { label: '1W', value: '1w' },
    { label: '1M', value: '1mo' },
    { label: '3M', value: '3mo' },
    { label: '1Y', value: '1y' },
  ];

  const addToWatchlist = async (watchlistId) => {
    try {
      await api.addStockToWatchlist(watchlistId, symbol);
      // Could add a toast notification here
    } catch (error) {
      console.error('Failed to add to watchlist:', error);
    }
  };

  if (loadingStock) {
    return (
      <div className="space-y-6">
        <div className="bg-white rounded-lg shadow p-6 animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2 mb-2"></div>
          <div className="h-6 bg-gray-200 rounded w-1/3"></div>
        </div>
        <div className="bg-white rounded-lg shadow p-6 animate-pulse">
          <div className="h-80 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  if (stockError) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-8 text-center">
        <BarChart3 className="h-12 w-12 text-red-400 mx-auto mb-4" />
        <h2 className="text-xl font-semibold text-red-900 mb-2">Stock Not Found</h2>
        <p className="text-red-600">Unable to load data for {symbol}</p>
      </div>
    );
  }

  const isPositive = stockData?.change >= 0;

  return (
    <div className="space-y-6">
      {/* Stock Header */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center space-x-3 mb-2">
              <h1 className="text-3xl font-bold text-gray-900">{stockData?.symbol}</h1>
              {isPositive ? (
                <TrendingUp className="h-6 w-6 text-green-500" />
              ) : (
                <TrendingDown className="h-6 w-6 text-red-500" />
              )}
            </div>
            <p className="text-lg text-gray-600 mb-4">{stockData?.name}</p>
            
            <div className="flex items-center space-x-6">
              <div>
                <p className="text-3xl font-bold text-gray-900">
                  ${stockData?.price?.toFixed(2)}
                </p>
              </div>
              <div className={`text-lg ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
                <div className="flex items-center space-x-1">
                  <span className="font-semibold">
                    {isPositive ? '+' : ''}${stockData?.change?.toFixed(2)}
                  </span>
                  <span>({stockData?.change_percent})</span>
                </div>
                <p className="text-sm text-gray-500">Today</p>
              </div>
            </div>
          </div>
          
          <div className="flex space-x-2">
            <div className="relative">
              <button
                onClick={() => setShowAddToPortfolio(!showAddToPortfolio)}
                className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                <Plus className="h-4 w-4" />
                <span>Add to Portfolio</span>
              </button>
              
              {showAddToPortfolio && (
                <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border z-10">
                  <div className="p-3">
                    <p className="text-sm font-medium text-gray-900 mb-2">Add to Watchlist</p>
                    {watchlists?.map((watchlist) => (
                      <button
                        key={watchlist.id}
                        onClick={() => addToWatchlist(watchlist.id)}
                        className="block w-full text-left px-2 py-1 text-sm text-gray-700 hover:bg-gray-100 rounded"
                      >
                        {watchlist.name}
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>
            
            <button className="flex items-center space-x-2 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors">
              <Heart className="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Chart Controls */}
      <div className="bg-white rounded-lg shadow p-4">
        <div className="flex space-x-2">
          {periods.map((period) => (
            <button
              key={period.value}
              onClick={() => setSelectedPeriod(period.value)}
              className={`px-3 py-2 text-sm font-medium rounded-lg transition-colors ${
                selectedPeriod === period.value
                  ? 'bg-blue-100 text-blue-700'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
              }`}
            >
              {period.label}
            </button>
          ))}
        </div>
      </div>

      {/* Stock Chart */}
      {loadingChart ? (
        <div className="bg-white rounded-lg shadow p-6">
          <div className="h-80 bg-gray-200 animate-pulse rounded"></div>
        </div>
      ) : (
        <StockChart 
          data={historicalData?.data} 
          symbol={stockData?.symbol}
        />
      )}

      {/* Key Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-4">Key Statistics</h3>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-600">Open</span>
              <span className="font-medium">${stockData?.open?.toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">High</span>
              <span className="font-medium">${stockData?.high?.toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Low</span>
              <span className="font-medium">${stockData?.low?.toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Previous Close</span>
              <span className="font-medium">${stockData?.previous_close?.toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Volume</span>
              <span className="font-medium">{stockData?.volume?.toLocaleString()}</span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-4">Company Info</h3>
          {loadingFundamentals ? (
            <div className="space-y-3">
              {[...Array(5)].map((_, i) => (
                <div key={i} className="flex justify-between">
                  <div className="h-4 bg-gray-200 rounded w-1/3"></div>
                  <div className="h-4 bg-gray-200 rounded w-1/4"></div>
                </div>
              ))}
            </div>
          ) : (
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-600">Sector</span>
                <span className="font-medium">{fundamentals?.sector || 'N/A'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Industry</span>
                <span className="font-medium">{fundamentals?.industry || 'N/A'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Market Cap</span>
                <span className="font-medium">
                  {fundamentals?.market_cap ? `$${(fundamentals.market_cap / 1e9).toFixed(1)}B` : 'N/A'}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">P/E Ratio</span>
                <span className="font-medium">{fundamentals?.pe_ratio || 'N/A'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">EPS</span>
                <span className="font-medium">{fundamentals?.eps || 'N/A'}</span>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Company Description */}
      {fundamentals?.description && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-4">About</h3>
          <p className="text-gray-700 leading-relaxed">
            {fundamentals.description}
          </p>
        </div>
      )}
    </div>
  );
};

export default StockDetail;