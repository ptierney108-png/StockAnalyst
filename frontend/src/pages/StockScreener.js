import React, { useState } from 'react';
import { 
  Search, 
  Filter, 
  TrendingUp, 
  TrendingDown, 
  BarChart3, 
  Activity,
  DollarSign,
  Volume2,
  Calendar,
  Target,
  Info,
  Download,
  RefreshCw,
  AlertCircle,
  CheckCircle,
  X
} from 'lucide-react';
import StockDataGenerator from '../utils/stockDataGenerator';
import { TechnicalAnalysisEngine } from '../utils/technicalAnalysis';

const StockScreener = () => {
  // State for filtering criteria
  const [priceFilterType, setPriceFilterType] = useState('under'); // 'under' or 'range'
  const [priceUnder, setPriceUnder] = useState(50);
  const [priceMin, setPriceMin] = useState(10);
  const [priceMax, setPriceMax] = useState(100);
  
  // DMI filter states
  const [dmiMin, setDmiMin] = useState(20);
  const [dmiMax, setDmiMax] = useState(60);
  
  // PPO slope filter
  const [ppoSlopeThreshold, setPpoSlopeThreshold] = useState(5);
  
  // Advanced filters
  const [sectorFilter, setSectorFilter] = useState('all');
  const [optionableFilter, setOptionableFilter] = useState('all');
  const [earningsFilter, setEarningsFilter] = useState('all');
  
  // UI states
  const [isLoading, setIsLoading] = useState(false);
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [results, setResults] = useState([]);
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });
  const [validationErrors, setValidationErrors] = useState([]);

  // Enhanced screening function with real technical analysis
  const handleScan = async () => {
    // Validate inputs
    const priceValidation = TechnicalAnalysisEngine.validatePriceRange({
      type: priceFilterType,
      under: priceUnder,
      min: priceMin,
      max: priceMax
    });

    if (!priceValidation.isValid) {
      setValidationErrors(priceValidation.errors);
      return;
    }

    // Validate DMI range
    if (dmiMin >= dmiMax) {
      setValidationErrors(['DMI minimum must be less than maximum']);
      return;
    }

    if (dmiMin < 0 || dmiMax > 100) {
      setValidationErrors(['DMI values must be between 0 and 100']);
      return;
    }

    setValidationErrors([]);
    setIsLoading(true);
    
    try {
      // Simulate API delay for realistic experience
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Create filter criteria object
      const filterCriteria = {
        priceFilter: {
          type: priceFilterType,
          under: priceUnder,
          min: priceMin,
          max: priceMax
        },
        dmiFilter: {
          min: dmiMin,
          max: dmiMax
        },
        ppoSlopeFilter: {
          threshold: Math.abs(ppoSlopeThreshold)
        },
        sectorFilter,
        optionableFilter,
        earningsFilter
      };

      // Generate filtered stocks using sophisticated data generator
      const filteredStocks = StockDataGenerator.generateFilteredStocks(filterCriteria);
      setResults(filteredStocks);
      
    } catch (error) {
      console.error('Screening error:', error);
      setValidationErrors(['An error occurred during screening. Please try again.']);
    } finally {
      setIsLoading(false);
    }
  };

  // Generate mock results for demonstration
  const generateMockResults = () => {
    const sectors = ['Technology', 'Healthcare', 'Finance', 'Energy', 'Consumer Goods'];
    const companies = [
      { symbol: 'AAPL', name: 'Apple Inc.', sector: 'Technology' },
      { symbol: 'MSFT', name: 'Microsoft Corporation', sector: 'Technology' },
      { symbol: 'GOOGL', name: 'Alphabet Inc.', sector: 'Technology' },
      { symbol: 'JNJ', name: 'Johnson & Johnson', sector: 'Healthcare' },
      { symbol: 'JPM', name: 'JPMorgan Chase & Co.', sector: 'Finance' },
      { symbol: 'XOM', name: 'Exxon Mobil Corporation', sector: 'Energy' },
      { symbol: 'PG', name: 'Procter & Gamble Co.', sector: 'Consumer Goods' },
      { symbol: 'NVDA', name: 'NVIDIA Corporation', sector: 'Technology' },
      { symbol: 'UNH', name: 'UnitedHealth Group Inc.', sector: 'Healthcare' },
      { symbol: 'HD', name: 'The Home Depot Inc.', sector: 'Consumer Goods' }
    ];

    return companies.map(company => ({
      ...company,
      price: Math.random() * (priceMax - priceMin) + priceMin,
      volume: Math.floor(Math.random() * 50000000) + 1000000,
      volume3m: Math.floor(Math.random() * 45000000) + 2000000,
      volumeYear: Math.floor(Math.random() * 40000000) + 3000000,
      return1d: (Math.random() - 0.5) * 10,
      return5d: (Math.random() - 0.5) * 20,
      return2w: (Math.random() - 0.5) * 30,
      return1m: (Math.random() - 0.5) * 40,
      return1y: (Math.random() - 0.5) * 100,
      dmi: Math.random() * (dmiMax - dmiMin) + dmiMin,
      ppoValues: [
        Math.random() * 4 - 2,
        Math.random() * 4 - 2,
        Math.random() * 4 - 2
      ],
      ppoSlope: (Math.random() - 0.5) * 20,
      industry: 'Software',
      optionable: Math.random() > 0.3,
      callBid: Math.random() * 5 + 0.5,
      callAsk: Math.random() * 5 + 1,
      putBid: Math.random() * 5 + 0.5,
      putAsk: Math.random() * 5 + 1,
      lastEarnings: new Date(Date.now() - Math.random() * 120 * 24 * 60 * 60 * 1000),
      nextEarnings: new Date(Date.now() + Math.random() * 120 * 24 * 60 * 60 * 1000),
      daysToEarnings: Math.floor(Math.random() * 120)
    }));
  };

  // Sorting function
  const handleSort = (key) => {
    let direction = 'asc';
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });

    const sortedData = [...results].sort((a, b) => {
      if (a[key] < b[key]) return direction === 'asc' ? -1 : 1;
      if (a[key] > b[key]) return direction === 'asc' ? 1 : -1;
      return 0;
    });
    setResults(sortedData);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Advanced Stock Screener</h1>
          <p className="text-gray-600">
            Filter stocks using technical indicators including DMI and PPO slope analysis. 
            Discover opportunities with precise momentum and directional movement criteria.
          </p>
        </div>

        {/* Filtering Panel */}
        <div className="bg-white rounded-2xl shadow-lg p-6 mb-6 border border-gray-100">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center space-x-2">
              <Filter className="h-5 w-5 text-blue-600" />
              <h2 className="text-xl font-bold text-gray-900">Screening Criteria</h2>
            </div>
            <button
              onClick={() => setShowAdvanced(!showAdvanced)}
              className="text-blue-600 hover:text-blue-700 text-sm font-medium"
            >
              {showAdvanced ? 'Hide Advanced' : 'Show Advanced Filters'}
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {/* Price Filter */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                <DollarSign className="h-4 w-4 inline mr-1" />
                Price Range
              </label>
              <select
                value={priceFilterType}
                onChange={(e) => setPriceFilterType(e.target.value)}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 mb-2"
              >
                <option value="under">Under specific amount</option>
                <option value="range">Within price range</option>
              </select>
              
              {priceFilterType === 'under' ? (
                <div>
                  <label className="block text-xs text-gray-500 mb-1">Maximum Price</label>
                  <input
                    type="number"
                    value={priceUnder}
                    onChange={(e) => setPriceUnder(Number(e.target.value))}
                    min="1"
                    max="1000"
                    className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    placeholder="e.g., 50"
                  />
                </div>
              ) : (
                <div className="space-y-2">
                  <div>
                    <label className="block text-xs text-gray-500 mb-1">Minimum Price</label>
                    <input
                      type="number"
                      value={priceMin}
                      onChange={(e) => setPriceMin(Number(e.target.value))}
                      min="1"
                      max="999"
                      className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                      placeholder="e.g., 10"
                    />
                  </div>
                  <div>
                    <label className="block text-xs text-gray-500 mb-1">Maximum Price</label>
                    <input
                      type="number"
                      value={priceMax}
                      onChange={(e) => setPriceMax(Number(e.target.value))}
                      min={priceMin + 1}
                      max="1000"
                      className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                      placeholder="e.g., 100"
                    />
                  </div>
                </div>
              )}
            </div>

            {/* DMI Filter */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                <Activity className="h-4 w-4 inline mr-1" />
                DMI Range
                <button className="ml-1 text-gray-400 hover:text-gray-600">
                  <Info className="h-3 w-3" title="Directional Movement Index (14-period)" />
                </button>
              </label>
              <div className="space-y-2">
                <div>
                  <label className="block text-xs text-gray-500 mb-1">Minimum DMI</label>
                  <input
                    type="number"
                    value={dmiMin}
                    onChange={(e) => setDmiMin(Number(e.target.value))}
                    min="0"
                    max="100"
                    className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    placeholder="e.g., 20"
                  />
                </div>
                <div>
                  <label className="block text-xs text-gray-500 mb-1">Maximum DMI</label>
                  <input
                    type="number"
                    value={dmiMax}
                    onChange={(e) => setDmiMax(Number(e.target.value))}
                    min={dmiMin + 1}
                    max="100"
                    className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    placeholder="e.g., 60"
                  />
                </div>
              </div>
            </div>

            {/* PPO Slope Filter */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                <BarChart3 className="h-4 w-4 inline mr-1" />
                PPO Slope %
                <button className="ml-1 text-gray-400 hover:text-gray-600">
                  <Info className="h-3 w-3" title="3-day PPO slope threshold percentage" />
                </button>
              </label>
              <div>
                <label className="block text-xs text-gray-500 mb-1">Minimum Slope %</label>
                <input
                  type="number"
                  value={ppoSlopeThreshold}
                  onChange={(e) => setPpoSlopeThreshold(Number(e.target.value))}
                  min="-50"
                  max="50"
                  step="0.1"
                  className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  placeholder="e.g., 5.0"
                />
              </div>
            </div>

            {/* Scan Button */}
            <div className="flex items-end">
              <button
                onClick={handleScan}
                disabled={isLoading}
                className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-semibold py-3 px-4 rounded-lg transition-colors flex items-center justify-center space-x-2"
              >
                {isLoading ? (
                  <>
                    <RefreshCw className="h-4 w-4 animate-spin" />
                    <span>Scanning...</span>
                  </>
                ) : (
                  <>
                    <Search className="h-4 w-4" />
                    <span>Scan Stocks</span>
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Advanced Filters - Progressive Disclosure */}
          {showAdvanced && (
            <div className="mt-6 pt-6 border-t border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Advanced Filters</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Sector</label>
                  <select className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
                    <option value="">All Sectors</option>
                    <option value="technology">Technology</option>
                    <option value="healthcare">Healthcare</option>
                    <option value="finance">Finance</option>
                    <option value="energy">Energy</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Optionable</label>
                  <select className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
                    <option value="">All Stocks</option>
                    <option value="yes">Optionable Only</option>
                    <option value="no">Non-Optionable Only</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Earnings</label>
                  <select className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
                    <option value="">All Stocks</option>
                    <option value="within7">Within 7 Days</option>
                    <option value="after7">After 7 Days</option>
                  </select>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Results Section */}
        {results.length > 0 && (
          <div className="bg-white rounded-2xl shadow-lg border border-gray-100">
            <div className="p-6 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Target className="h-5 w-5 text-green-600" />
                  <h2 className="text-xl font-bold text-gray-900">
                    Screening Results ({results.length} stocks found)
                  </h2>
                </div>
                <button className="flex items-center space-x-2 text-blue-600 hover:text-blue-700 font-medium">
                  <Download className="h-4 w-4" />
                  <span>Export Results</span>
                </button>
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                        onClick={() => handleSort('symbol')}>
                      Symbol
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Company
                    </th>
                    <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                        onClick={() => handleSort('price')}>
                      Price
                    </th>
                    <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                        onClick={() => handleSort('return1d')}>
                      1D Return
                    </th>
                    <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                        onClick={() => handleSort('return5d')}>
                      5D Return
                    </th>
                    <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                        onClick={() => handleSort('dmi')}>
                      DMI
                    </th>
                    <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                        onClick={() => handleSort('ppoSlope')}>
                      PPO Slope %
                    </th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Earnings
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {results.map((stock, index) => (
                    <tr key={stock.symbol} className="hover:bg-gray-50">
                      <td className="px-4 py-4 whitespace-nowrap">
                        <div className="font-bold text-blue-600">{stock.symbol}</div>
                        <div className="text-xs text-gray-500">{stock.sector}</div>
                      </td>
                      <td className="px-4 py-4">
                        <div className="text-sm font-medium text-gray-900">{stock.name}</div>
                        <div className="text-xs text-gray-500">{stock.industry}</div>
                      </td>
                      <td className="px-4 py-4 whitespace-nowrap text-right">
                        <div className="text-sm font-bold text-gray-900">${stock.price.toFixed(2)}</div>
                        <div className="text-xs text-gray-500">Vol: {(stock.volume / 1000000).toFixed(1)}M</div>
                      </td>
                      <td className="px-4 py-4 whitespace-nowrap text-right">
                        <span className={`inline-flex items-center px-2 py-1 rounded text-xs font-semibold ${
                          stock.return1d >= 0 
                            ? 'bg-green-100 text-green-800' 
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {stock.return1d >= 0 ? '+' : ''}{stock.return1d.toFixed(2)}%
                        </span>
                      </td>
                      <td className="px-4 py-4 whitespace-nowrap text-right">
                        <span className={`inline-flex items-center px-2 py-1 rounded text-xs font-semibold ${
                          stock.return5d >= 0 
                            ? 'bg-green-100 text-green-800' 
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {stock.return5d >= 0 ? '+' : ''}{stock.return5d.toFixed(2)}%
                        </span>
                      </td>
                      <td className="px-4 py-4 whitespace-nowrap text-right">
                        <div className="text-sm font-semibold text-gray-900">{stock.dmi.toFixed(1)}</div>
                      </td>
                      <td className="px-4 py-4 whitespace-nowrap text-right">
                        <span className={`inline-flex items-center px-2 py-1 rounded text-xs font-semibold ${
                          stock.ppoSlope >= 0 
                            ? 'bg-blue-100 text-blue-800' 
                            : 'bg-orange-100 text-orange-800'
                        }`}>
                          {stock.ppoSlope >= 0 ? '+' : ''}{stock.ppoSlope.toFixed(2)}%
                        </span>
                      </td>
                      <td className="px-4 py-4 whitespace-nowrap text-center">
                        <div className={`inline-flex items-center px-2 py-1 rounded text-xs font-medium ${
                          stock.daysToEarnings <= 7 
                            ? 'bg-yellow-100 text-yellow-800' 
                            : 'bg-gray-100 text-gray-800'
                        }`}>
                          {stock.daysToEarnings <= 7 && (
                            <AlertCircle className="h-3 w-3 mr-1" />
                          )}
                          {stock.daysToEarnings}d
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Educational Panel */}
        <div className="mt-6 bg-blue-50 rounded-2xl p-6 border border-blue-100">
          <h3 className="text-lg font-bold text-blue-900 mb-3">Technical Indicator Guide</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div>
              <h4 className="font-semibold text-blue-800 mb-2">DMI (Directional Movement Index)</h4>
              <p className="text-blue-700">
                Measures trend strength using DI+ and DI- values. Higher DMI values (above 25) indicate stronger trends, 
                while lower values suggest sideways movement.
              </p>
            </div>
            <div>
              <h4 className="font-semibold text-blue-800 mb-2">PPO Slope</h4>
              <p className="text-blue-700">
                Calculates the 3-day slope of the PPO oscillator. Positive slopes suggest increasing momentum, 
                while negative slopes indicate weakening momentum.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StockScreener;