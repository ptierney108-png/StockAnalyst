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
import { TableSkeleton } from '../components/LoadingSkeleton';
import { StockScreenerErrorBoundary } from '../components/ErrorBoundary';
import api from '../services/api';


const StockScreener = () => {
  // Helper function to detect PPO hooks
  const detectPPOHook = (ppoValues) => {
    if (!ppoValues || ppoValues.length < 3) return null;
    
    const today = ppoValues[0];      // Today (index 0)
    const yesterday = ppoValues[1];   // Yesterday (index 1) 
    const dayBefore = ppoValues[2];   // Day before yesterday (index 2)
    
    // Positive hook: TODAY > YESTERDAY AND YESTERDAY < PRIOR DAY
    if (today > yesterday && yesterday < dayBefore) {
      return 'positive';
    }
    
    // Negative hook: TODAY < YESTERDAY AND YESTERDAY > PRIOR DAY  
    if (today < yesterday && yesterday > dayBefore) {
      return 'negative';
    }
    
    return null;
  };

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
  
  // PPO Hook filter - NEW
  const [ppoHookFilter, setPpoHookFilter] = useState('all'); // 'all', 'positive', 'negative', 'both'
  
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
  const [showTooltip, setShowTooltip] = useState(null);
  const [scanProgress, setScanProgress] = useState(0);
  const [lastScanTime, setLastScanTime] = useState(null);

  // Export functionality
  const exportResults = () => {
    if (results.length === 0) {
      alert('No results to export. Please run a scan first.');
      return;
    }

    // Create CSV content
    const headers = [
      'Symbol', 'Company Name', 'Sector', 'Industry', 'Price', 
      'Volume Today', 'Volume Avg 3M', 'Volume Year',
      '1D Return %', '5D Return %', '2W Return %', '1M Return %', '1Y Return %',
      'DMI', 'ADX', 'DI+', 'DI-', 
      'PPO Day 1', 'PPO Day 2', 'PPO Day 3', 'PPO Slope %', 'PPO Hook',
      'Optionable', 'Call Bid', 'Call Ask', 'Put Bid', 'Put Ask', 'Options Expiration',
      'Last Earnings', 'Next Earnings', 'Days to Earnings'
    ];

    const csvContent = [
      headers.join(','),
      ...results.map(stock => {
        const hook = detectPPOHook(stock.ppoValues);
        return [
          stock.symbol,
          `"${stock.name}"`,
          stock.sector,
          stock.industry,
          stock.price.toFixed(2),
          stock.volume,
          stock.volume3m,
          stock.volumeYear,
          stock.return1d.toFixed(2),
          stock.return5d.toFixed(2),
          stock.return2w.toFixed(2),
          stock.return1m.toFixed(2),
          stock.return1y.toFixed(2),
          stock.dmi.toFixed(2),
          stock.adx?.toFixed(2) || 'N/A',
          stock.diPlus?.toFixed(2) || 'N/A',
          stock.diMinus?.toFixed(2) || 'N/A',
          stock.ppoValues?.[0]?.toFixed(4) || 'N/A',
          stock.ppoValues?.[1]?.toFixed(4) || 'N/A',
          stock.ppoValues?.[2]?.toFixed(4) || 'N/A',
          stock.ppoSlope.toFixed(2),
          hook || 'None',
          stock.optionable ? 'Yes' : 'No',
          stock.callBid?.toFixed(2) || 'N/A',
          stock.callAsk?.toFixed(2) || 'N/A',
          stock.putBid?.toFixed(2) || 'N/A',
          stock.putAsk?.toFixed(2) || 'N/A',
          stock.optionsExpiration || 'N/A',
          stock.lastEarnings?.toLocaleDateString() || 'N/A',
          stock.nextEarnings?.toLocaleDateString() || 'N/A',
          stock.daysToEarnings || 'N/A'
        ].join(',');
      })
    ].join('\n');

    // Create and download file
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `stock_screener_results_${new Date().toISOString().split('T')[0]}.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // Tooltip component
  const Tooltip = ({ id, title, content }) => (
    <div className="relative inline-block">
      <button
        className="ml-1 text-gray-400 hover:text-gray-600"
        onMouseEnter={() => setShowTooltip(id)}
        onMouseLeave={() => setShowTooltip(null)}
      >
        <Info className="h-3 w-3" />
      </button>
      {showTooltip === id && (
        <div className="absolute z-10 w-64 p-3 text-sm bg-gray-900 text-white rounded-lg shadow-lg -top-2 left-6">
          <div className="font-semibold mb-1">{title}</div>
          <div className="text-gray-300">{content}</div>
          <div className="absolute top-2 -left-1 w-2 h-2 bg-gray-900 transform rotate-45"></div>
        </div>
      )}
    </div>
  );

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
    setScanProgress(0);
    const startTime = Date.now();
    
    try {
      // Simulate progressive loading with realistic feedback
      const progressSteps = [
        { progress: 20, message: 'Validating criteria...' },
        { progress: 40, message: 'Fetching market data...' },
        { progress: 60, message: 'Calculating technical indicators...' },
        { progress: 80, message: 'Applying filters...' },
        { progress: 95, message: 'Finalizing results...' },
      ];

      for (const step of progressSteps) {
        setScanProgress(step.progress);
        await new Promise(resolve => setTimeout(resolve, 300));
      }
      
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
        ppoHookFilter: ppoHookFilter, // NEW: PPO hook filtering
        sectorFilter,
        optionableFilter,
        earningsFilter
      };

      // Generate filtered stocks using sophisticated data generator
      const filteredStocks = StockDataGenerator.generateFilteredStocks(filterCriteria);
      
      setScanProgress(100);
      await new Promise(resolve => setTimeout(resolve, 200));
      
      setResults(filteredStocks);
      setLastScanTime(Date.now() - startTime);
      
    } catch (error) {
      console.error('Screening error:', error);
      setValidationErrors(['An error occurred during screening. Please try again.']);
    } finally {
      setIsLoading(false);
      setScanProgress(0);
    }
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
          <p className="text-gray-600 mb-3">
            Filter stocks using technical indicators including DMI and PPO slope analysis. 
            Discover opportunities with precise momentum and directional movement criteria.
          </p>
          
          {/* Data Source Indicator */}
          <div className="flex items-center space-x-4 text-sm text-gray-500">
            <span className="flex items-center space-x-1">
              <span className="w-2 h-2 bg-gray-500 rounded-full"></span>
              <span>Data Source: Simulated Market Data</span>
            </span>
            <span>•</span>
            <span>Realistic technical indicators and market behavior</span>
          </div>
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
            {/* Validation Errors */}
            {validationErrors.length > 0 && (
              <div className="col-span-full bg-red-50 border border-red-200 rounded-lg p-4">
                <div className="flex items-center space-x-2 mb-2">
                  <X className="h-4 w-4 text-red-600" />
                  <span className="font-semibold text-red-800">Validation Errors:</span>
                </div>
                <ul className="list-disc list-inside text-sm text-red-700 space-y-1">
                  {validationErrors.map((error, index) => (
                    <li key={index}>{error}</li>
                  ))}
                </ul>
              </div>
            )}
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
                <Tooltip 
                  id="dmi-tooltip"
                  title="Directional Movement Index (DMI)"
                  content="DMI measures trend strength using 14-period calculations. Values above 25 indicate strong trends, while values below 20 suggest sideways movement. ADX shows overall trend strength."
                />
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
                <Tooltip 
                  id="ppo-tooltip"
                  title="PPO Slope Calculation"
                  content="Calculates the 3-day slope of the PPO oscillator using conditional logic. When PPO < 0: (today - yesterday)/yesterday. When PPO > 0: (yesterday - today)/yesterday. Higher values indicate stronger momentum changes."
                />
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

            {/* PPO Hook Filter - NEW */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                <Target className="h-4 w-4 inline mr-1" />
                PPO Hook Pattern
                <Tooltip 
                  id="hook-tooltip"
                  title="PPO Hook Detection"
                  content="Positive Hook (+): TODAY > YESTERDAY AND YESTERDAY < PRIOR DAY indicates upward momentum reversal. Negative Hook (-): TODAY < YESTERDAY AND YESTERDAY > PRIOR DAY indicates downward momentum reversal."
                />
              </label>
              <select
                value={ppoHookFilter}
                onChange={(e) => setPpoHookFilter(e.target.value)}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="all">All Stocks</option>
                <option value="positive">Positive Hook (+HOOK) Only</option>
                <option value="negative">Negative Hook (-HOOK) Only</option>
                <option value="both">Both Hooks (+HOOK or -HOOK)</option>
              </select>
            </div>

            {/* Scan Button */}
            <div className="flex items-end">
              <button
                onClick={handleScan}
                disabled={isLoading}
                className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-semibold py-3 px-4 rounded-lg transition-colors flex items-center justify-center space-x-2"
              >
                {isLoading ? (
                  <div className="flex flex-col items-center space-y-1 w-full">
                    <div className="flex items-center space-x-2">
                      <RefreshCw className="h-4 w-4 animate-spin" />
                      <span>Scanning...</span>
                    </div>
                    <div className="w-full bg-blue-300 rounded-full h-1">
                      <div 
                        className="bg-white h-1 rounded-full transition-all duration-300"
                        style={{ width: `${scanProgress}%` }}
                      ></div>
                    </div>
                    <span className="text-xs">{scanProgress}%</span>
                  </div>
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
                  <select 
                    value={sectorFilter}
                    onChange={(e) => setSectorFilter(e.target.value)}
                    className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="all">All Sectors</option>
                    <option value="technology">Technology</option>
                    <option value="healthcare">Healthcare</option>
                    <option value="finance">Finance</option>
                    <option value="energy">Energy</option>
                    <option value="consumer goods">Consumer Goods</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Optionable</label>
                  <select 
                    value={optionableFilter}
                    onChange={(e) => setOptionableFilter(e.target.value)}
                    className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="all">All Stocks</option>
                    <option value="yes">Optionable Only</option>
                    <option value="no">Non-Optionable Only</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Earnings</label>
                  <select 
                    value={earningsFilter}
                    onChange={(e) => setEarningsFilter(e.target.value)}
                    className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="all">All Stocks</option>
                    <option value="within7">Within 7 Days</option>
                    <option value="after7">After 7 Days</option>
                  </select>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Results Section */}
        {scanProgress > 0 && scanProgress < 100 ? (
          <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-6">
            <div className="flex items-center space-x-2 mb-4">
              <Target className="h-5 w-5 text-blue-600" />
              <h2 className="text-xl font-bold text-gray-900">Scanning Stocks...</h2>
            </div>
            <TableSkeleton rows={8} cols={6} />
          </div>
        ) : results.length > 0 && (
          <div className="bg-white rounded-2xl shadow-lg border border-gray-100">
            <div className="p-6 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Target className="h-5 w-5 text-green-600" />
                  <h2 className="text-xl font-bold text-gray-900">
                    Screening Results ({results.length} stocks found)
                  </h2>
                  {lastScanTime && (
                    <div className="text-sm text-gray-500">
                      Scan completed in {(lastScanTime / 1000).toFixed(1)}s
                    </div>
                  )}
                </div>
                
                {/* Data Source Indicator for Screener */}
                <div className="flex items-center space-x-4 text-sm text-gray-600 mt-2">
                  <span className="flex items-center space-x-1">
                    <span className="w-2 h-2 bg-gray-500 rounded-full"></span>
                    <span>Source: Demo Data (Simulated)</span>
                  </span>
                  <span>•</span>
                  <span>Enhanced with realistic market indicators</span>
                </div>
                <button 
                  onClick={exportResults}
                  className="flex items-center space-x-2 text-blue-600 hover:text-blue-700 font-medium transition-colors"
                >
                  <Download className="h-4 w-4" />
                  <span>Export Results</span>
                </button>
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                        onClick={() => handleSort('symbol')}>
                      Symbol
                    </th>
                    <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Company
                    </th>
                    <th className="px-3 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                        onClick={() => handleSort('price')}>
                      Price
                    </th>
                    <th className="px-3 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Volume Today
                    </th>
                    <th className="px-3 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Volume Avg 3M
                    </th>
                    <th className="px-3 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Volume Year
                    </th>
                    <th className="px-3 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                        onClick={() => handleSort('return1d')}>
                      1D
                    </th>
                    <th className="px-3 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                        onClick={() => handleSort('return5d')}>
                      5D
                    </th>
                    <th className="px-3 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                        onClick={() => handleSort('return2w')}>
                      2W
                    </th>
                    <th className="px-3 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                        onClick={() => handleSort('return1m')}>
                      1M
                    </th>
                    <th className="px-3 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                        onClick={() => handleSort('return1y')}>
                      1Y
                    </th>
                    <th className="px-3 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                        onClick={() => handleSort('dmi')}>
                      DMI/ADX
                    </th>
                    <th className="px-3 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                      PPO (3 Days)
                    </th>
                    <th className="px-3 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                        onClick={() => handleSort('ppoSlope')}>
                      PPO Slope
                    </th>
                    <th className="px-3 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Options
                    </th>
                    <th className="px-3 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Earnings
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {results.map((stock, index) => (
                    <tr key={stock.symbol} className={`hover:bg-gray-50 ${
                      stock.daysToEarnings <= 7 ? 'bg-yellow-50' : ''
                    }`}>
                      <td className="px-3 py-3 whitespace-nowrap">
                        <div className="font-bold text-blue-600 text-sm">{stock.symbol}</div>
                        <div className="text-xs text-gray-500">{stock.sector}</div>
                      </td>
                      <td className="px-3 py-3 min-w-0">
                        <div className="text-sm font-medium text-gray-900 truncate">{stock.name}</div>
                        <div className="text-xs text-gray-500">{stock.industry}</div>
                      </td>
                      <td className="px-3 py-3 whitespace-nowrap text-right">
                        <div className="text-sm font-bold text-gray-900">${stock.price.toFixed(2)}</div>
                        <div className="text-xs text-gray-500">
                          {stock.optionable ? (
                            <span className="inline-flex items-center px-1 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800">
                              <CheckCircle className="w-3 h-3 mr-1" />
                              OPT
                            </span>
                          ) : (
                            <span className="text-gray-400">N/A</span>
                          )}
                        </div>
                      </td>
                      <td className="px-3 py-3 whitespace-nowrap text-right">
                        <div className="text-sm font-semibold text-gray-900">
                          {(stock.volume / 1000000).toFixed(1)}M
                        </div>
                      </td>
                      <td className="px-3 py-3 whitespace-nowrap text-right">
                        <div className="text-sm text-gray-700">
                          {(stock.volume3m / 1000000).toFixed(1)}M
                        </div>
                      </td>
                      <td className="px-3 py-3 whitespace-nowrap text-right">
                        <div className="text-sm text-gray-700">
                          {(stock.volumeYear / 1000000).toFixed(1)}M
                        </div>
                      </td>
                      <td className="px-3 py-3 whitespace-nowrap text-right">
                        <span className={`inline-flex items-center px-2 py-1 rounded text-xs font-semibold ${
                          stock.return1d >= 0 
                            ? 'bg-green-100 text-green-800' 
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {stock.return1d >= 0 ? '+' : ''}{stock.return1d.toFixed(1)}%
                        </span>
                      </td>
                      <td className="px-3 py-3 whitespace-nowrap text-right">
                        <span className={`inline-flex items-center px-2 py-1 rounded text-xs font-semibold ${
                          stock.return5d >= 0 
                            ? 'bg-green-100 text-green-800' 
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {stock.return5d >= 0 ? '+' : ''}{stock.return5d.toFixed(1)}%
                        </span>
                      </td>
                      <td className="px-3 py-3 whitespace-nowrap text-right">
                        <span className={`inline-flex items-center px-2 py-1 rounded text-xs font-semibold ${
                          stock.return2w >= 0 
                            ? 'bg-green-100 text-green-800' 
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {stock.return2w >= 0 ? '+' : ''}{stock.return2w.toFixed(1)}%
                        </span>
                      </td>
                      <td className="px-3 py-3 whitespace-nowrap text-right">
                        <span className={`inline-flex items-center px-2 py-1 rounded text-xs font-semibold ${
                          stock.return1m >= 0 
                            ? 'bg-green-100 text-green-800' 
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {stock.return1m >= 0 ? '+' : ''}{stock.return1m.toFixed(1)}%
                        </span>
                      </td>
                      <td className="px-3 py-3 whitespace-nowrap text-right">
                        <span className={`inline-flex items-center px-2 py-1 rounded text-xs font-semibold ${
                          stock.return1y >= 0 
                            ? 'bg-green-100 text-green-800' 
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {stock.return1y >= 0 ? '+' : ''}{stock.return1y.toFixed(0)}%
                        </span>
                      </td>
                      <td className="px-3 py-3 whitespace-nowrap text-right">
                        <div className="text-sm font-semibold text-gray-900">
                          {stock.dmi.toFixed(1)}
                        </div>
                        <div className="text-xs text-gray-500">
                          ADX: {stock.adx?.toFixed(1) || 'N/A'}
                        </div>
                        <div className="text-xs space-x-1">
                          <span className="text-green-600">+{stock.diPlus?.toFixed(1) || 'N/A'}</span>
                          <span className="text-red-600">-{stock.diMinus?.toFixed(1) || 'N/A'}</span>
                        </div>
                      </td>
                      <td className="px-3 py-3 whitespace-nowrap text-center">
                        <div className="space-y-1">
                          {stock.ppoValues?.map((ppo, idx) => {
                            const dayLabels = ['Today', 'Yesterday', '2 Days Ago'];
                            return (
                              <div key={idx} className={`text-xs px-1 py-0.5 rounded font-medium ${
                                ppo >= 0 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                              }`}>
                                <div className="text-xs text-gray-500">{dayLabels[idx]}({idx})</div>
                                {ppo >= 0 ? '+' : ''}{ppo.toFixed(3)}
                              </div>
                            );
                          }) || 'N/A'}
                        </div>
                      </td>
                      <td className="px-3 py-3 whitespace-nowrap text-right">
                        {(() => {
                          const hook = detectPPOHook(stock.ppoValues);
                          return (
                            <div className="space-y-1">
                              <span className={`inline-flex items-center px-2 py-1 rounded text-xs font-semibold ${
                                stock.ppoSlope >= 0 
                                  ? 'bg-blue-100 text-blue-800' 
                                  : 'bg-orange-100 text-orange-800'
                              }`}>
                                {hook === 'positive' && <span className="mr-1">⭐</span>}
                                {hook === 'negative' && <span className="mr-1">⚠️</span>}
                                {stock.ppoSlope >= 0 ? '+' : ''}{stock.ppoSlope.toFixed(2)}%
                              </span>
                              {hook && (
                                <div className={`text-xs font-medium ${
                                  hook === 'positive' ? 'text-green-700' : 'text-red-700'
                                }`}>
                                  {hook === 'positive' ? '+ Hook' : '- Hook'}
                                </div>
                              )}
                            </div>
                          );
                        })()}
                      </td>
                      <td className="px-3 py-3 whitespace-nowrap text-center">
                        <div className="space-y-1">
                          {stock.optionable ? (
                            <>
                              <div className="text-xs">
                                <span className="text-green-600 font-medium">C: {stock.callBid?.toFixed(2)}-{stock.callAsk?.toFixed(2)}</span>
                              </div>
                              <div className="text-xs">
                                <span className="text-red-600 font-medium">P: {stock.putBid?.toFixed(2)}-{stock.putAsk?.toFixed(2)}</span>
                              </div>
                              <div className="text-xs text-gray-500 font-medium">
                                Exp: {stock.optionsExpiration || 'N/A'}
                              </div>
                            </>
                          ) : (
                            <span className="text-xs text-gray-500">N/A</span>
                          )}
                        </div>
                      </td>
                      <td className="px-3 py-3 whitespace-nowrap text-center">
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
                        <div className="text-xs text-gray-500 mt-1">
                          {stock.nextEarnings?.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                        </div>
                        <div className="text-xs text-gray-400">
                          Last: {stock.lastEarnings?.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Enhanced Educational Panel */}
        <div className="mt-6 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-2xl p-6 border border-blue-100">
          <h3 className="text-lg font-bold text-blue-900 mb-4 flex items-center">
            <Info className="h-5 w-5 mr-2" />
            Technical Analysis Guide & Performance Tips
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 text-sm">
            <div>
              <h4 className="font-semibold text-blue-800 mb-2">DMI (Directional Movement Index)</h4>
              <p className="text-blue-700 mb-2">
                Measures trend strength using DI+ (bullish) and DI- (bearish) values with ADX for overall trend strength.
              </p>
              <ul className="text-blue-600 text-xs space-y-1">
                <li>• ADX &gt; 25: Strong trend</li>
                <li>• ADX 20-25: Moderate trend</li>
                <li>• ADX &lt; 20: Weak/sideways</li>
                <li>• DI+ &gt; DI-: Bullish bias</li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-blue-800 mb-2">PPO Slope Analysis</h4>
              <p className="text-blue-700 mb-2">
                Calculates momentum acceleration using 3-day PPO slope with conditional logic based on oscillator position.
              </p>
              <ul className="text-blue-600 text-xs space-y-1">
                <li>• Positive slope: Increasing momentum</li>
                <li>• Negative slope: Decreasing momentum</li>
                <li>• Higher threshold: More selective</li>
                <li>• Use with price confirmation</li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-blue-800 mb-2">Screening Best Practices</h4>
              <p className="text-blue-700 mb-2">
                Optimize your screening strategy for better results and faster processing.
              </p>
              <ul className="text-blue-600 text-xs space-y-1">
                <li>• Start with broad criteria</li>
                <li>• Narrow down gradually</li>
                <li>• Consider earnings dates</li>
                <li>• Verify options availability</li>
              </ul>
            </div>
          </div>
          
          {/* Advanced Tips */}
          <div className="mt-6 pt-4 border-t border-blue-200">
            <h4 className="font-semibold text-blue-800 mb-3">Advanced Filtering Strategies</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs text-blue-700">
              <div>
                <span className="font-medium">For Momentum Trading:</span> Use DMI &gt; 30 with PPO slope &gt; 5% and recent earnings data.
              </div>
              <div>
                <span className="font-medium">For Options Strategy:</span> Filter by optionable stocks with tight bid-ask spreads and upcoming earnings.
              </div>
              <div>
                <span className="font-medium">For Value Screening:</span> Combine price ranges with sector filtering for systematic opportunities.
              </div>
              <div>
                <span className="font-medium">For Risk Management:</span> Check volume patterns and recent return volatility across timeframes.
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StockScreener;