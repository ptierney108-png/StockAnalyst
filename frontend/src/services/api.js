import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API_BASE = `${BACKEND_URL}/api`;

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 30000, // Increased timeout for analysis
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

const api = {
  // Health check
  health: async () => {
    const response = await apiClient.get('/');
    return response.data;
  },

  // Advanced Stock Analysis - NEW
  getStockAnalysis: async (symbol, timeframe = '1D') => {
    const response = await apiClient.get(`/analyze/${symbol}?timeframe=${timeframe}`);
    return response.data;
  },

  performStockAnalysis: async (symbol, timeframe = 'daily') => {
    const response = await apiClient.post('/analyze', { symbol, timeframe });
    return response.data;
  },

  // Stock search and data
  searchStocks: async (query) => {
    const response = await apiClient.get(`/stocks/search?q=${encodeURIComponent(query)}`);
    return response.data;
  },

  getStockDetails: async (symbol) => {
    const response = await apiClient.get(`/stocks/${symbol}`);
    return response.data;
  },

  getHistoricalData: async (symbol, period = '1mo') => {
    const response = await apiClient.get(`/stocks/${symbol}/historical?period=${period}`);
    return response.data;
  },

  getStockFundamentals: async (symbol) => {
    const response = await apiClient.get(`/stocks/${symbol}/fundamentals`);
    return response.data;
  },

  // Market data
  getTrendingStocks: async () => {
    const response = await apiClient.get('/market/trending');
    return response.data;
  },

  getTopGainers: async () => {
    const response = await apiClient.get('/market/gainers');
    return response.data;
  },

  getTopLosers: async () => {
    const response = await apiClient.get('/market/losers');
    return response.data;
  },

  // Portfolio management
  getPortfolios: async () => {
    const response = await apiClient.get('/portfolios');
    return response.data;
  },

  getPortfolio: async (portfolioId) => {
    const response = await apiClient.get(`/portfolios/${portfolioId}`);
    return response.data;
  },

  createPortfolio: async (portfolioData) => {
    const response = await apiClient.post('/portfolios', portfolioData);
    return response.data;
  },

  deletePortfolio: async (portfolioId) => {
    const response = await apiClient.delete(`/portfolios/${portfolioId}`);
    return response.data;
  },

  addStockToPortfolio: async (portfolioId, stockData) => {
    const response = await apiClient.post(`/portfolios/${portfolioId}/stocks`, stockData);
    return response.data;
  },

  // Watchlist management
  getWatchlists: async () => {
    const response = await apiClient.get('/watchlists');
    return response.data;
  },

  getWatchlistStocks: async (watchlistId) => {
    const response = await apiClient.get(`/watchlists/${watchlistId}/stocks`);
    return response.data;
  },

  createWatchlist: async (watchlistData) => {
    const response = await apiClient.post('/watchlists', watchlistData);
    return response.data;
  },

  deleteWatchlist: async (watchlistId) => {
    const response = await apiClient.delete(`/watchlists/${watchlistId}`);
    return response.data;
  },

  addStockToWatchlist: async (watchlistId, symbol) => {
    const response = await apiClient.post(`/watchlists/${watchlistId}/stocks/${symbol}`);
    return response.data;
  },

  removeStockFromWatchlist: async (watchlistId, symbol) => {
    const response = await apiClient.delete(`/watchlists/${watchlistId}/stocks/${symbol}`);
    return response.data;
  },

  // Stock screening
  screenStocks: async (filters) => {
    const response = await apiClient.post('/screener/scan', filters);
    return response.data;
  },

  // Batch Processing APIs
  getBatchIndices: async () => {
    const response = await apiClient.get('/batch/indices');
    return response.data;
  },

  startBatchScan: async (scanRequest) => {
    const response = await apiClient.post('/batch/scan', scanRequest, {
      timeout: 60000 // Longer timeout for batch start
    });
    return response.data;
  },

  getBatchStatus: async (batchId) => {
    const response = await apiClient.get(`/batch/status/${batchId}`);
    return response.data;
  },

  getBatchResults: async (batchId) => {
    const response = await apiClient.get(`/batch/results/${batchId}`, {
      timeout: 60000 // Longer timeout for large result sets
    });
    return response.data;
  },

  cancelBatchJob: async (batchId) => {
    const response = await apiClient.delete(`/batch/cancel/${batchId}`);
    return response.data;
  },

  getBatchStats: async () => {
    const response = await apiClient.get('/batch/stats');
    return response.data;
  },

  // Phase 2: Partial Results API
  getBatchPartialResults: async (batchId) => {
    const response = await apiClient.get(`/batch/partial-results/${batchId}`);
    return response.data;
  },

  // CSV Export API
  exportBatchResultsToCSV: async (batchId) => {
    const response = await apiClient.get(`/batch/export/${batchId}`, {
      responseType: 'blob', // Important for file download
      timeout: 60000 // Longer timeout for large datasets
    });
    return response;
  },

  // AI Insights API
  getBatchAiInsights: async (batchId) => {
    const response = await apiClient.get(`/batch/insights/${batchId}`, {
      timeout: 30000 // Longer timeout for AI processing
    });
    return response.data;
  },
};

export default api;