import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Link, useNavigate } from 'react-router-dom';
import { TrendingUp, TrendingDown, BarChart3, Eye, Briefcase, Search, Activity } from 'lucide-react';
import StockCard from '../components/StockCard';
import api from '../services/api';

const Dashboard = () => {
  const [quickAnalysisSymbol, setQuickAnalysisSymbol] = useState('');
  const navigate = useNavigate();

  const handleQuickAnalysis = (e) => {
    e.preventDefault();
    if (quickAnalysisSymbol.trim()) {
      navigate(`/analysis?symbol=${quickAnalysisSymbol.toUpperCase()}`);
    }
  };
  const {
    data: trendingStocks,
    isLoading: loadingTrending,
    error: trendingError
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

  const {
    data: portfolios,
    isLoading: loadingPortfolios,
  } = useQuery({
    queryKey: ['portfolios'],
    queryFn: api.getPortfolios,
  });

  const {
    data: watchlists,
    isLoading: loadingWatchlists,
  } = useQuery({
    queryKey: ['watchlists'],
    queryFn: api.getWatchlists,
  });

  const LoadingGrid = () => (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {[...Array(6)].map((_, i) => (
        <div key={i} className="bg-white rounded-lg shadow p-6 animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-1/4 mb-2"></div>
          <div className="h-3 bg-gray-200 rounded w-3/4 mb-4"></div>
          <div className="h-8 bg-gray-200 rounded w-1/2 mb-2"></div>
          <div className="h-4 bg-gray-200 rounded w-1/3"></div>
        </div>
      ))}
    </div>
  );

  const StatCard = ({ title, value, icon: Icon, color, link }) => (
    <Link to={link} className="block bg-white rounded-lg shadow hover:shadow-md transition-shadow p-6">
      <div className="flex items-center">
        <div className={`p-3 rounded-lg ${color}`}>
          <Icon className="h-6 w-6 text-white" />
        </div>
        <div className="ml-4">
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
        </div>
      </div>
    </Link>
  );

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Welcome to StockWise</h1>
        <p className="text-gray-600 mb-3">Your comprehensive stock analysis platform</p>
        
        {/* Data Source Indicator */}
        <div className="flex items-center justify-center space-x-4 text-sm text-gray-500">
          <span className="flex items-center space-x-1">
            <span className="w-2 h-2 bg-gray-500 rounded-full"></span>
            <span>Market Data: Simulated for Demo</span>
          </span>
          <span>•</span>
          <span>Real-time behavior with demo portfolio data</span>
        </div>
      </div>

      {/* Quick Stock Analysis */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center space-x-2 mb-4">
          <Activity className="h-5 w-5 text-blue-600" />
          <h2 className="text-lg font-semibold text-gray-900">Quick Stock Analysis</h2>
        </div>
        <form onSubmit={handleQuickAnalysis} className="flex gap-3">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
            <input
              type="text"
              value={quickAnalysisSymbol}
              onChange={(e) => setQuickAnalysisSymbol(e.target.value.toUpperCase())}
              placeholder="Enter stock symbol (e.g., AAPL, TSLA)..."
              className="pl-10 pr-4 py-3 w-full border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <button
            type="submit"
            disabled={!quickAnalysisSymbol.trim()}
            className="px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Analyze Stock
          </button>
        </form>
        <p className="text-sm text-gray-500 mt-2">
          Get advanced technical analysis with PPO, DMI, RSI, MACD indicators and AI recommendations
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatCard
          title="Portfolios"
          value={portfolios?.length || 0}
          icon={Briefcase}
          color="bg-blue-500"
          link="/portfolio"
        />
        <StatCard
          title="Watchlists"
          value={watchlists?.length || 0}
          icon={Eye}
          color="bg-green-500"
          link="/watchlist"
        />
        <StatCard
          title="Market Status"
          value="Open"
          icon={BarChart3}
          color="bg-purple-500"
          link="/market"
        />
      </div>

      {/* Top Gainers and Losers */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div>
          <div className="flex items-center space-x-2 mb-4">
            <TrendingUp className="h-5 w-5 text-green-500" />
            <h2 className="text-xl font-bold text-gray-900">Top Gainers</h2>
          </div>
          {loadingGainers ? (
            <div className="space-y-4">
              {[...Array(3)].map((_, i) => (
                <div key={i} className="bg-white rounded-lg shadow p-4 animate-pulse">
                  <div className="h-4 bg-gray-200 rounded w-1/4 mb-2"></div>
                  <div className="h-6 bg-gray-200 rounded w-1/2"></div>
                </div>
              ))}
            </div>
          ) : (
            <div className="space-y-4">
              {gainers?.slice(0, 3).map((stock) => (
                <StockCard key={stock.symbol} stock={stock} />
              ))}
            </div>
          )}
        </div>

        <div>
          <div className="flex items-center space-x-2 mb-4">
            <TrendingDown className="h-5 w-5 text-red-500" />
            <h2 className="text-xl font-bold text-gray-900">Top Losers</h2>
          </div>
          {loadingLosers ? (
            <div className="space-y-4">
              {[...Array(3)].map((_, i) => (
                <div key={i} className="bg-white rounded-lg shadow p-4 animate-pulse">
                  <div className="h-4 bg-gray-200 rounded w-1/4 mb-2"></div>
                  <div className="h-6 bg-gray-200 rounded w-1/2"></div>
                </div>
              ))}
            </div>
          ) : (
            <div className="space-y-4">
              {losers?.slice(0, 3).map((stock) => (
                <StockCard key={stock.symbol} stock={stock} />
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Trending Stocks */}
      <div>
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold text-gray-900">Trending Stocks</h2>
          <Link
            to="/market"
            className="text-blue-600 hover:text-blue-700 font-medium"
          >
            View all →
          </Link>
        </div>

        {loadingTrending ? (
          <LoadingGrid />
        ) : trendingError ? (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <p className="text-red-600">Failed to load trending stocks</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {trendingStocks?.slice(0, 8).map((stock) => (
              <StockCard key={stock.symbol} stock={stock} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;