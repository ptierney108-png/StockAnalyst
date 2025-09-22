import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Plus, Trash2, Eye, X, Search } from 'lucide-react';
import StockCard from '../components/StockCard';
import api from '../services/api';

const Watchlist = () => {
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newWatchlistName, setNewWatchlistName] = useState('');
  const [selectedWatchlist, setSelectedWatchlist] = useState(null);
  const [showAddStock, setShowAddStock] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);

  const queryClient = useQueryClient();

  const {
    data: watchlists,
    isLoading: loadingWatchlists,
  } = useQuery({
    queryKey: ['watchlists'],
    queryFn: api.getWatchlists,
  });

  const {
    data: watchlistStocks,
    isLoading: loadingStocks,
  } = useQuery({
    queryKey: ['watchlist-stocks', selectedWatchlist?.id],
    queryFn: () => api.getWatchlistStocks(selectedWatchlist.id),
    enabled: !!selectedWatchlist,
  });

  const createWatchlistMutation = useMutation({
    mutationFn: api.createWatchlist,
    onSuccess: () => {
      queryClient.invalidateQueries(['watchlists']);
      setShowCreateForm(false);
      setNewWatchlistName('');
    },
  });

  const deleteWatchlistMutation = useMutation({
    mutationFn: api.deleteWatchlist,
    onSuccess: () => {
      queryClient.invalidateQueries(['watchlists']);
      setSelectedWatchlist(null);
    },
  });

  const addStockMutation = useMutation({
    mutationFn: ({ watchlistId, symbol }) => api.addStockToWatchlist(watchlistId, symbol),
    onSuccess: () => {
      queryClient.invalidateQueries(['watchlist-stocks', selectedWatchlist?.id]);
      setShowAddStock(false);
      setSearchQuery('');
      setSearchResults([]);
    },
  });

  const removeStockMutation = useMutation({
    mutationFn: ({ watchlistId, symbol }) => api.removeStockFromWatchlist(watchlistId, symbol),
    onSuccess: () => {
      queryClient.invalidateQueries(['watchlist-stocks', selectedWatchlist?.id]);
    },
  });

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

  const handleCreateWatchlist = (e) => {
    e.preventDefault();
    if (newWatchlistName.trim()) {
      createWatchlistMutation.mutate({ name: newWatchlistName, symbols: [] });
    }
  };

  const handleAddStock = (symbol) => {
    if (selectedWatchlist) {
      addStockMutation.mutate({
        watchlistId: selectedWatchlist.id,
        symbol: symbol
      });
    }
  };

  const handleRemoveStock = (symbol) => {
    if (selectedWatchlist) {
      removeStockMutation.mutate({
        watchlistId: selectedWatchlist.id,
        symbol: symbol
      });
    }
  };

  if (loadingWatchlists) {
    return (
      <div className="space-y-6">
        <div className="h-8 bg-gray-200 animate-pulse rounded w-1/4"></div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="bg-white rounded-lg shadow p-6 animate-pulse">
              <div className="h-6 bg-gray-200 rounded w-3/4 mb-4"></div>
              <div className="h-4 bg-gray-200 rounded w-1/2"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Watchlists</h1>
        <button
          onClick={() => setShowCreateForm(true)}
          className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          <Plus className="h-4 w-4" />
          <span>Create Watchlist</span>
        </button>
      </div>

      {/* Create Watchlist Modal */}
      {showCreateForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-bold mb-4">Create New Watchlist</h2>
            <form onSubmit={handleCreateWatchlist}>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Watchlist Name
                </label>
                <input
                  type="text"
                  value={newWatchlistName}
                  onChange={(e) => setNewWatchlistName(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Tech Stocks"
                  required
                />
              </div>
              <div className="flex space-x-3">
                <button
                  type="button"
                  onClick={() => {
                    setShowCreateForm(false);
                    setNewWatchlistName('');
                  }}
                  className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={createWatchlistMutation.isLoading}
                  className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
                >
                  {createWatchlistMutation.isLoading ? 'Creating...' : 'Create'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Add Stock Modal */}
      {showAddStock && selectedWatchlist && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-bold">Add Stock to {selectedWatchlist.name}</h2>
              <button
                onClick={() => {
                  setShowAddStock(false);
                  setSearchQuery('');
                  setSearchResults([]);
                }}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="h-5 w-5" />
              </button>
            </div>
            
            <div className="mb-4">
              <div className="relative">
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
              </div>
            </div>

            <div className="max-h-60 overflow-y-auto">
              {searchResults.map((stock) => (
                <button
                  key={stock.symbol}
                  onClick={() => handleAddStock(stock.symbol)}
                  className="w-full text-left p-3 hover:bg-gray-50 border-b border-gray-100 last:border-b-0"
                  disabled={addStockMutation.isLoading}
                >
                  <div className="font-medium text-gray-900">{stock.symbol}</div>
                  <div className="text-sm text-gray-500">{stock.name}</div>
                </button>
              ))}
              {searchQuery && searchResults.length === 0 && (
                <div className="p-3 text-center text-gray-500">
                  No stocks found for "{searchQuery}"
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Watchlists Grid */}
      {watchlists?.length === 0 ? (
        <div className="text-center py-12">
          <Eye className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No watchlists yet</h3>
          <p className="text-gray-500 mb-4">Create your first watchlist to track interesting stocks</p>
          <button
            onClick={() => setShowCreateForm(true)}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Create Watchlist
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Watchlists Sidebar */}
          <div className="space-y-4">
            {watchlists?.map((watchlist) => (
              <div
                key={watchlist.id}
                className={`bg-white rounded-lg shadow p-4 cursor-pointer transition-colors ${
                  selectedWatchlist?.id === watchlist.id
                    ? 'ring-2 ring-blue-500 bg-blue-50'
                    : 'hover:bg-gray-50'
                }`}
                onClick={() => setSelectedWatchlist(watchlist)}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-900">{watchlist.name}</h3>
                    <p className="text-sm text-gray-500 mt-1">
                      {watchlist.symbols?.length || 0} stocks
                    </p>
                  </div>
                  <div className="flex space-x-1">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        setShowAddStock(true);
                      }}
                      className="text-blue-600 hover:text-blue-700"
                    >
                      <Plus className="h-4 w-4" />
                    </button>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        deleteWatchlistMutation.mutate(watchlist.id);
                      }}
                      className="text-gray-400 hover:text-red-500"
                      disabled={deleteWatchlistMutation.isLoading}
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Watchlist Stocks */}
          <div className="lg:col-span-2">
            {selectedWatchlist ? (
              <div>
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-xl font-bold text-gray-900">
                    {selectedWatchlist.name}
                  </h2>
                  <button
                    onClick={() => setShowAddStock(true)}
                    className="flex items-center space-x-2 px-3 py-2 text-blue-600 border border-blue-600 rounded-lg hover:bg-blue-50 transition-colors"
                  >
                    <Plus className="h-4 w-4" />
                    <span>Add Stock</span>
                  </button>
                </div>

                {loadingStocks ? (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {[...Array(4)].map((_, i) => (
                      <div key={i} className="bg-white rounded-lg shadow p-6 animate-pulse">
                        <div className="h-4 bg-gray-200 rounded w-1/4 mb-2"></div>
                        <div className="h-3 bg-gray-200 rounded w-3/4 mb-4"></div>
                        <div className="h-8 bg-gray-200 rounded w-1/2"></div>
                      </div>
                    ))}
                  </div>
                ) : watchlistStocks?.length === 0 ? (
                  <div className="text-center py-12 bg-white rounded-lg shadow">
                    <Eye className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-lg font-medium text-gray-900 mb-2">
                      No stocks in this watchlist
                    </h3>
                    <p className="text-gray-500 mb-4">
                      Add stocks to track their performance
                    </p>
                    <button
                      onClick={() => setShowAddStock(true)}
                      className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                    >
                      Add First Stock
                    </button>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {watchlistStocks?.map((stock) => (
                      <div key={stock.symbol} className="relative">
                        <StockCard stock={stock} />
                        <button
                          onClick={() => handleRemoveStock(stock.symbol)}
                          className="absolute top-2 right-2 p-1 bg-white rounded-full shadow-sm text-gray-400 hover:text-red-500 transition-colors"
                          disabled={removeStockMutation.isLoading}
                        >
                          <X className="h-4 w-4" />
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ) : (
              <div className="text-center py-12 bg-white rounded-lg shadow">
                <Eye className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  Select a watchlist
                </h3>
                <p className="text-gray-500">
                  Choose a watchlist from the left to view its stocks
                </p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default Watchlist;