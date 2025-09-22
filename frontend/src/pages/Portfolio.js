import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Plus, Trash2, TrendingUp, TrendingDown, Briefcase } from 'lucide-react';
import api from '../services/api';

const Portfolio = () => {
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newPortfolioName, setNewPortfolioName] = useState('');
  const [selectedPortfolio, setSelectedPortfolio] = useState(null);
  const [showAddStock, setShowAddStock] = useState(false);
  const [newStock, setNewStock] = useState({
    symbol: '',
    quantity: '',
    avg_price: ''
  });

  const queryClient = useQueryClient();

  const {
    data: portfolios,
    isLoading: loadingPortfolios,
  } = useQuery({
    queryKey: ['portfolios'],
    queryFn: api.getPortfolios,
  });

  const createPortfolioMutation = useMutation({
    mutationFn: api.createPortfolio,
    onSuccess: () => {
      queryClient.invalidateQueries(['portfolios']);
      setShowCreateForm(false);
      setNewPortfolioName('');
    },
  });

  const deletePortfolioMutation = useMutation({
    mutationFn: api.deletePortfolio,
    onSuccess: () => {
      queryClient.invalidateQueries(['portfolios']);
      setSelectedPortfolio(null);
    },
  });

  const addStockMutation = useMutation({
    mutationFn: ({ portfolioId, stock }) => api.addStockToPortfolio(portfolioId, stock),
    onSuccess: () => {
      queryClient.invalidateQueries(['portfolios']);
      setShowAddStock(false);
      setNewStock({ symbol: '', quantity: '', avg_price: '' });
    },
  });

  const handleCreatePortfolio = (e) => {
    e.preventDefault();
    if (newPortfolioName.trim()) {
      createPortfolioMutation.mutate({ name: newPortfolioName });
    }
  };

  const handleAddStock = (e) => {
    e.preventDefault();
    if (selectedPortfolio && newStock.symbol && newStock.quantity && newStock.avg_price) {
      addStockMutation.mutate({
        portfolioId: selectedPortfolio.id,
        stock: {
          symbol: newStock.symbol.toUpperCase(),
          quantity: parseInt(newStock.quantity),
          avg_price: parseFloat(newStock.avg_price)
        }
      });
    }
  };

  const calculatePortfolioValue = (portfolio) => {
    return portfolio.stocks?.reduce((total, stock) => total + (stock.value || 0), 0) || 0;
  };

  const calculatePortfolioChange = (portfolio) => {
    return portfolio.stocks?.reduce((total, stock) => total + (stock.change || 0), 0) || 0;
  };

  if (loadingPortfolios) {
    return (
      <div className="space-y-6">
        <div className="h-8 bg-gray-200 animate-pulse rounded w-1/4"></div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="bg-white rounded-lg shadow p-6 animate-pulse">
              <div className="h-6 bg-gray-200 rounded w-3/4 mb-4"></div>
              <div className="h-8 bg-gray-200 rounded w-1/2 mb-2"></div>
              <div className="h-4 bg-gray-200 rounded w-1/3"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Portfolio Management</h1>
        <button
          onClick={() => setShowCreateForm(true)}
          className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          <Plus className="h-4 w-4" />
          <span>Create Portfolio</span>
        </button>
      </div>

      {/* Create Portfolio Modal */}
      {showCreateForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-bold mb-4">Create New Portfolio</h2>
            <form onSubmit={handleCreatePortfolio}>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Portfolio Name
                </label>
                <input
                  type="text"
                  value={newPortfolioName}
                  onChange={(e) => setNewPortfolioName(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="My Portfolio"
                  required
                />
              </div>
              <div className="flex space-x-3">
                <button
                  type="button"
                  onClick={() => {
                    setShowCreateForm(false);
                    setNewPortfolioName('');
                  }}
                  className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={createPortfolioMutation.isLoading}
                  className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
                >
                  {createPortfolioMutation.isLoading ? 'Creating...' : 'Create'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Add Stock Modal */}
      {showAddStock && selectedPortfolio && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-bold mb-4">Add Stock to {selectedPortfolio.name}</h2>
            <form onSubmit={handleAddStock}>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Stock Symbol
                  </label>
                  <input
                    type="text"
                    value={newStock.symbol}
                    onChange={(e) => setNewStock({ ...newStock, symbol: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="AAPL"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Quantity
                  </label>
                  <input
                    type="number"
                    value={newStock.quantity}
                    onChange={(e) => setNewStock({ ...newStock, quantity: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="10"
                    min="1"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Average Price
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    value={newStock.avg_price}
                    onChange={(e) => setNewStock({ ...newStock, avg_price: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="150.00"
                    min="0"
                    required
                  />
                </div>
              </div>
              <div className="flex space-x-3 mt-6">
                <button
                  type="button"
                  onClick={() => {
                    setShowAddStock(false);
                    setNewStock({ symbol: '', quantity: '', avg_price: '' });
                  }}
                  className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={addStockMutation.isLoading}
                  className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
                >
                  {addStockMutation.isLoading ? 'Adding...' : 'Add Stock'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Portfolios Grid */}
      {portfolios?.length === 0 ? (
        <div className="text-center py-12">
          <Briefcase className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No portfolios yet</h3>
          <p className="text-gray-500 mb-4">Create your first portfolio to start tracking your investments</p>
          <button
            onClick={() => setShowCreateForm(true)}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Create Portfolio
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {portfolios?.map((portfolio) => {
            const totalValue = calculatePortfolioValue(portfolio);
            const totalChange = calculatePortfolioChange(portfolio);
            const isPositive = totalChange >= 0;

            return (
              <div key={portfolio.id} className="bg-white rounded-lg shadow hover:shadow-md transition-shadow">
                <div className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <h3 className="text-lg font-semibold text-gray-900">{portfolio.name}</h3>
                    <button
                      onClick={() => deletePortfolioMutation.mutate(portfolio.id)}
                      className="text-gray-400 hover:text-red-500 transition-colors"
                      disabled={deletePortfolioMutation.isLoading}
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>

                  <div className="space-y-2 mb-4">
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">Total Value</span>
                      <span className="text-lg font-bold text-gray-900">
                        ${totalValue.toFixed(2)}
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">Total Change</span>
                      <div className={`flex items-center space-x-1 ${
                        isPositive ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {isPositive ? (
                          <TrendingUp className="h-3 w-3" />
                        ) : (
                          <TrendingDown className="h-3 w-3" />
                        )}
                        <span className="text-sm font-medium">
                          {isPositive ? '+' : ''}${totalChange.toFixed(2)}
                        </span>
                      </div>
                    </div>
                    <div className="text-sm text-gray-500">
                      {portfolio.stocks?.length || 0} stocks
                    </div>
                  </div>

                  <div className="space-y-2 mb-4">
                    {portfolio.stocks?.slice(0, 3).map((stock, index) => (
                      <div key={index} className="flex justify-between text-sm">
                        <span className="text-gray-600">{stock.symbol}</span>
                        <span className="font-medium">
                          {stock.quantity} @ ${stock.current_price?.toFixed(2)}
                        </span>
                      </div>
                    ))}
                    {portfolio.stocks?.length > 3 && (
                      <div className="text-sm text-gray-500">
                        +{portfolio.stocks.length - 3} more stocks
                      </div>
                    )}
                  </div>

                  <button
                    onClick={() => {
                      setSelectedPortfolio(portfolio);
                      setShowAddStock(true);
                    }}
                    className="w-full px-4 py-2 border border-blue-600 text-blue-600 rounded-lg hover:bg-blue-50 transition-colors"
                  >
                    Add Stock
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default Portfolio;