import React, { useState, useEffect } from 'react';
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
  X,
  Play,
  Pause,
  Clock,
  Database,
  Zap
} from 'lucide-react';
import api from '../services/api';

const BatchScreener = () => {
  // Batch processing state
  const [availableIndices, setAvailableIndices] = useState({});
  const [selectedIndices, setSelectedIndices] = useState(['SP500']);
  const [isProcessing, setBatchProcessing] = useState(false);
  const [currentBatchId, setCurrentBatchId] = useState(null);
  const [batchProgress, setBatchProgress] = useState(null);
  const [batchResults, setBatchResults] = useState([]);
  const [estimatedCompletion, setEstimatedCompletion] = useState(null);
  
  // Filter state (same as regular screener)
  const [priceFilterType, setPriceFilterType] = useState('under');
  const [priceMin, setPriceMin] = useState(10);
  const [priceMax, setPriceMax] = useState(500);
  const [dmiMin, setDmiMin] = useState(20);
  const [dmiMax, setDmiMax] = useState(60);
  const [ppoSlopeThreshold, setPpoSlopeThreshold] = useState(0);
  const [ppoHookFilter, setPpoHookFilter] = useState('all');
  const [sectorFilter, setSectorFilter] = useState('all');
  const [optionableFilter, setOptionableFilter] = useState('all');
  const [earningsFilter, setEarningsFilter] = useState('all');
  
  // UI state
  const [showAdvancedFilters, setShowAdvancedFilters] = useState(false);
  const [lastScanTime, setLastScanTime] = useState(null);
  const [forceRefresh, setForceRefresh] = useState(false);
  const [error, setError] = useState(null);
  const [showTooltip, setShowTooltip] = useState(null);
  
  // Phase 2: Enhanced state for partial results and comprehensive scanning
  const [showPartialResults, setShowPartialResults] = useState(false);
  const [partialResults, setPartialResults] = useState([]);
  const [lastPartialUpdate, setLastPartialUpdate] = useState(null);
  const [scanningMode, setScanningMode] = useState('comprehensive'); // 'comprehensive' or 'fast'

  // Tooltip component for filter explanations
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

  // Load available indices on component mount
  useEffect(() => {
    loadAvailableIndices();
  }, []);

  // Poll batch progress with Phase 2 partial results support
  useEffect(() => {
    let progressInterval;
    let partialResultsInterval;
    
    if (currentBatchId && isProcessing) {
      // Main progress polling (every 2 seconds)
      progressInterval = setInterval(async () => {
        try {
          const progress = await api.getBatchStatus(currentBatchId);
          setBatchProgress(progress);
          
          if (progress.status === 'completed') {
            setBatchProcessing(false);
            await loadBatchResults(currentBatchId);
            setLastScanTime(Date.now());
            setShowPartialResults(false); // Hide partial results when complete
          } else if (progress.status === 'failed') {
            setBatchProcessing(false);
            setError(progress.error || 'Batch processing failed');
            setShowPartialResults(false);
          }
        } catch (error) {
          console.error('Failed to get batch progress:', error);
        }
      }, 2000);

      // Phase 2: Partial results polling (every 5 seconds for real-time feedback)
      if (showPartialResults) {
        partialResultsInterval = setInterval(async () => {
          try {
            const partialData = await api.getBatchPartialResults(currentBatchId);
            if (partialData.partial_results && partialData.partial_results.length > 0) {
              setPartialResults(partialData.partial_results);
              setLastPartialUpdate(partialData.last_update);
            }
          } catch (error) {
            console.error('Failed to get partial results:', error);
          }
        }, 5000);
      }
    }
    
    return () => {
      if (progressInterval) {
        clearInterval(progressInterval);
      }
      if (partialResultsInterval) {
        clearInterval(partialResultsInterval);
      }
    };
  }, [currentBatchId, isProcessing, showPartialResults]);

  const loadAvailableIndices = async () => {
    try {
      const response = await api.getBatchIndices();
      if (response.success) {
        setAvailableIndices(response.indices);
      }
    } catch (error) {
      console.error('Failed to load indices:', error);
      setError('Failed to load available stock indices');
    }
  };

  const loadBatchResults = async (batchId) => {
    try {
      const response = await api.getBatchResults(batchId);
      if (response.status === 'completed') {
        setBatchResults(response.results);
      }
    } catch (error) {
      console.error('Failed to load batch results:', error);
      setError('Failed to load batch results');
    }
  };

  const handleStartBatchScan = async () => {
    try {
      setError(null);
      setBatchProcessing(true);
      setBatchResults([]);
      setBatchProgress(null);
      
      const filterCriteria = {
        indices: selectedIndices,
        filters: {
          price_filter: priceFilterType === 'under' ? 
            { type: 'under', under: priceMax } :
            { type: 'range', min: priceMin, max: priceMax },
          dmi_filter: {
            min: dmiMin,
            max: dmiMax
          },
          ppo_slope_filter: {
            threshold: ppoSlopeThreshold
          },
          ppo_hook_filter: ppoHookFilter,
          sector_filter: sectorFilter,
          optionable_filter: optionableFilter,
          earnings_filter: earningsFilter
        },
        force_refresh: forceRefresh
      };

      const response = await api.startBatchScan(filterCriteria);
      setCurrentBatchId(response.batch_id);
      setEstimatedCompletion(response.estimated_completion_minutes);
      
    } catch (error) {
      console.error('Failed to start batch scan:', error);
      setBatchProcessing(false);
      setError('Failed to start batch scan: ' + error.message);
    }
  };

  const handleCancelBatch = async () => {
    if (currentBatchId) {
      try {
        await api.cancelBatchJob(currentBatchId);
        setBatchProcessing(false);
        setBatchProgress(null);
        setCurrentBatchId(null);
      } catch (error) {
        console.error('Failed to cancel batch:', error);
      }
    }
  };

  const getTotalStocksCount = () => {
    return selectedIndices.reduce((total, index) => {
      const indexData = availableIndices[index];
      return total + (indexData?.stock_count || 0);
    }, 0);
  };

  const getEstimatedScanTime = () => {
    return selectedIndices.reduce((maxTime, index) => {
      const indexData = availableIndices[index];
      return Math.max(maxTime, indexData?.estimated_scan_time_minutes || 0);
    }, 0);
  };

  const exportToCSV = () => {
    if (batchResults.length === 0) return;

    const headers = [
      'Symbol', 'Name', 'Sector', 'Price', 'DMI', 'ADX', 'DI+', 'DI-',
      'PPO Today', 'PPO Yesterday', 'PPO 2-Days-Ago', 'PPO Slope %', 
      'PPO Hook', '1D Return', '5D Return', '1M Return', '1Y Return',
      'Volume Today', 'Volume 3M', 'Data Source'
    ];

    // Function to safely format hook pattern for CSV
    const formatHookPattern = (hookDisplay) => {
      if (!hookDisplay) return 'No Hook';
      
      // Clean the hook pattern and make it Excel-safe
      let cleanHook = String(hookDisplay).trim();
      
      // Replace problematic characters that Excel interprets as formulas
      cleanHook = cleanHook.replace(/^\+/, 'Positive ');  // + Hook -> Positive Hook
      cleanHook = cleanHook.replace(/^-/, 'Negative ');    // - Hook -> Negative Hook
      cleanHook = cleanHook.replace(/^=/, 'Equals ');      // Any = signs
      cleanHook = cleanHook.replace(/^@/, 'At ');          // Any @ signs
      
      return cleanHook || 'No Hook';
    };

    const csvContent = [
      headers.join(','),
      ...batchResults.map(stock => [
        stock.symbol,
        `"${stock.name}"`,
        stock.sector,
        stock.price?.toFixed(2) || '0',
        stock.dmi?.toFixed(2) || '0',
        stock.adx?.toFixed(2) || '0',
        stock.di_plus?.toFixed(2) || '0',
        stock.di_minus?.toFixed(2) || '0',
        stock.ppo_values?.[0]?.toFixed(4) || '0',
        stock.ppo_values?.[1]?.toFixed(4) || '0',
        stock.ppo_values?.[2]?.toFixed(4) || '0',
        stock.ppo_slope_percentage?.toFixed(2) || '0',
        `"${formatHookPattern(stock.ppo_hook_display)}"`, // Excel-safe hook pattern
        stock.returns?.['1d']?.toFixed(2) || '0',
        stock.returns?.['5d']?.toFixed(2) || '0', 
        stock.returns?.['1m']?.toFixed(2) || '0',
        stock.returns?.['1y']?.toFixed(2) || '0',
        stock.volume_today || '0',
        stock.volume_3m || '0',
        stock.data_source || 'unknown'
      ].join(','))
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `batch-screener-results-${new Date().toISOString().split('T')[0]}.csv`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 flex items-center">
                <Database className="h-8 w-8 mr-3 text-blue-600" />
                Batch Stock Screener
              </h1>
              <p className="text-gray-600 mt-2">
                Comprehensive screening across thousands of stocks with advanced batch processing
              </p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-right">
                <div className="text-sm text-gray-500">Total Stocks</div>
                <div className="text-2xl font-bold text-blue-600">
                  {getTotalStocksCount().toLocaleString()}
                </div>
              </div>
              <div className="text-right">
                <div className="text-sm text-gray-500">Est. Scan Time</div>
                <div className="text-2xl font-bold text-green-600">
                  {getEstimatedScanTime().toFixed(1)}min
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Index Selection */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4 flex items-center">
            <Target className="h-5 w-5 mr-2" />
            Stock Universe Selection
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {Object.entries(availableIndices).map(([key, indexData]) => (
              <div key={key} className="border rounded-lg p-4 hover:bg-gray-50 transition-colors">
                <label className="flex items-start space-x-3 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={selectedIndices.includes(key)}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setSelectedIndices([...selectedIndices, key]);
                      } else {
                        setSelectedIndices(selectedIndices.filter(idx => idx !== key));
                      }
                    }}
                    className="mt-1 h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  />
                  <div className="flex-1">
                    <div className="font-medium text-gray-900">{indexData.name}</div>
                    <div className="text-sm text-gray-500">{indexData.description}</div>
                    <div className="text-xs text-gray-400 mt-1">
                      {indexData.stock_count} stocks • ~{indexData.estimated_scan_time_minutes}min
                    </div>
                  </div>
                </label>
              </div>
            ))}
          </div>
        </div>

        {/* Filter Controls */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold flex items-center">
              <Filter className="h-5 w-5 mr-2" />
              Screening Criteria
            </h2>
            <button
              onClick={() => setShowAdvancedFilters(!showAdvancedFilters)}
              className="text-blue-600 hover:text-blue-700 font-medium text-sm"
            >
              {showAdvancedFilters ? 'Hide' : 'Show'} Advanced Filters
            </button>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {/* Price Range */}
            <div>
              <div className="flex items-center mb-2">
                <DollarSign className="h-4 w-4 mr-1 text-green-600" />
                <label className="font-medium text-gray-700">Price Range</label>
              </div>
              <select
                value={priceFilterType}
                onChange={(e) => setPriceFilterType(e.target.value)}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 mb-3"
              >
                <option value="under">Under specific amount</option>
                <option value="range">Within price range</option>
              </select>
              
              {priceFilterType === 'under' ? (
                <input
                  type="number"
                  placeholder="Maximum Price"
                  value={priceMax}
                  onChange={(e) => setPriceMax(Number(e.target.value))}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              ) : (
                <div className="space-y-2">
                  <input
                    type="number"
                    placeholder="Minimum Price"
                    value={priceMin}
                    onChange={(e) => setPriceMin(Number(e.target.value))}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                  <input
                    type="number"
                    placeholder="Maximum Price"
                    value={priceMax}
                    onChange={(e) => setPriceMax(Number(e.target.value))}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              )}
            </div>

            {/* DMI Range */}
            <div>
              <div className="flex items-center mb-2">
                <Activity className="h-4 w-4 mr-1 text-purple-600" />
                <label className="font-medium text-gray-700">DMI Range</label>
                <Tooltip 
                  id="batch-dmi-tooltip"
                  title="Directional Movement Index (DMI)"
                  content="DMI measures trend strength using 14-period calculations. Values above 25 indicate strong trends, while values below 20 suggest sideways movement. ADX shows overall trend strength."
                />
              </div>
              <div className="space-y-2">
                <div>
                  <label className="block text-xs text-gray-500 mb-1">Minimum DMI</label>
                  <input
                    type="number"
                    placeholder="e.g., 20"
                    value={dmiMin}
                    onChange={(e) => setDmiMin(Number(e.target.value))}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-xs text-gray-500 mb-1">Maximum DMI</label>
                  <input
                    type="number"
                    placeholder="e.g., 60"
                    value={dmiMax}
                    onChange={(e) => setDmiMax(Number(e.target.value))}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>
            </div>

            {/* PPO Slope */}
            <div>
              <div className="flex items-center mb-2">
                <TrendingUp className="h-4 w-4 mr-1 text-blue-600" />
                <label className="font-medium text-gray-700">PPO Slope %</label>
                <Tooltip 
                  id="batch-ppo-tooltip"
                  title="PPO Slope Calculation"
                  content="Calculates the 3-day slope of the PPO oscillator using conditional logic. When PPO < 0: (today - yesterday)/yesterday. When PPO > 0: (yesterday - today)/yesterday. Higher values indicate stronger momentum changes."
                />
              </div>
              <div>
                <label className="block text-xs text-gray-500 mb-1">Minimum Slope %</label>
                <input
                  type="number"
                  step="0.1"
                  placeholder="e.g., 5.0"
                  value={ppoSlopeThreshold}
                  onChange={(e) => setPpoSlopeThreshold(Number(e.target.value))}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
            </div>

            {/* PPO Hook Pattern */}
            <div>
              <div className="flex items-center mb-2">
                <BarChart3 className="h-4 w-4 mr-1 text-orange-600" />
                <label className="font-medium text-gray-700">PPO Hook Pattern</label>
                <Tooltip 
                  id="batch-hook-tooltip"
                  title="PPO Hook Patterns"
                  content="Detects reversal patterns in PPO momentum. Positive Hook (+): Today > Yesterday AND Yesterday < Day Before (upward reversal). Negative Hook (-): Today < Yesterday AND Yesterday > Day Before (downward reversal)."
                />
              </div>
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
          </div>

          {/* Advanced Filters */}
          {showAdvancedFilters && (
            <div className="mt-6 pt-6 border-t border-gray-200">
              <h3 className="font-medium text-gray-700 mb-4">Advanced Filters</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <label className="block font-medium text-gray-700 mb-2">Sector</label>
                  <select
                    value={sectorFilter}
                    onChange={(e) => setSectorFilter(e.target.value)}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="all">All Sectors</option>
                    <option value="technology">Technology</option>
                    <option value="healthcare">Healthcare</option>
                    <option value="financials">Financials</option>
                    <option value="energy">Energy</option>
                  </select>
                </div>

                <div>
                  <label className="block font-medium text-gray-700 mb-2">Options Available</label>
                  <select
                    value={optionableFilter}
                    onChange={(e) => setOptionableFilter(e.target.value)}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="all">All Stocks</option>
                    <option value="yes">Options Available</option>
                    <option value="no">No Options</option>
                  </select>
                </div>

                <div>
                  <label className="block font-medium text-gray-700 mb-2">Earnings</label>
                  <select
                    value={earningsFilter}
                    onChange={(e) => setEarningsFilter(e.target.value)}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="all">All Stocks</option>
                    <option value="upcoming">Upcoming Earnings</option>
                    <option value="recent">Recent Earnings</option>
                  </select>
                </div>
              </div>
            </div>
          )}

          {/* Batch Options */}
          <div className="mt-6 pt-6 border-t border-gray-200">
            <h3 className="font-medium text-gray-700 mb-4">Batch Options</h3>
            <div className="flex items-center space-x-6">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={forceRefresh}
                  onChange={(e) => setForceRefresh(e.target.checked)}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <span className="ml-2 text-gray-700">Force fresh data (ignore cache)</span>
              </label>
            </div>
          </div>
        </div>

        {/* Batch Control */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-medium text-gray-900">Batch Processing</h3>
              <p className="text-gray-600 text-sm">
                {isProcessing 
                  ? `Processing ${getTotalStocksCount()} stocks...`
                  : `Ready to scan ${getTotalStocksCount()} stocks from ${selectedIndices.length} indices`
                }
              </p>
            </div>
            
            <div className="flex items-center space-x-4">
              {!isProcessing ? (
                <button
                  onClick={handleStartBatchScan}
                  disabled={selectedIndices.length === 0}
                  className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-semibold py-3 px-6 rounded-lg transition-colors flex items-center space-x-2"
                >
                  <Play className="h-5 w-5" />
                  <span>Start Batch Scan</span>
                </button>
              ) : (
                <button
                  onClick={handleCancelBatch}
                  className="bg-red-600 hover:bg-red-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors flex items-center space-x-2"
                >
                  <X className="h-5 w-5" />
                  <span>Cancel Scan</span>
                </button>
              )}
            </div>
          </div>

          {/* Progress Display */}
          {(isProcessing || batchProgress) && batchProgress && (
            <div className="mt-6 p-4 bg-blue-50 rounded-lg">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-blue-900">
                  Processing: {batchProgress.progress?.current_symbol || 'Initializing...'}
                </span>
                <span className="text-sm text-blue-700">
                  {batchProgress.progress?.percentage.toFixed(1) || 0}%
                </span>
              </div>
              
              <div className="w-full bg-blue-200 rounded-full h-2 mb-3">
                <div 
                  className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${batchProgress.progress?.percentage || 0}%` }}
                ></div>
              </div>
              
              <div className="flex items-center justify-between text-xs text-blue-700">
                <span>
                  {batchProgress.progress?.processed || 0} / {batchProgress.progress?.total || 0} stocks processed
                </span>
                <span>
                  {batchProgress.progress?.api_calls_made || 0} API calls made
                </span>
                {batchProgress.estimated_completion && (
                  <span className="flex items-center">
                    <Clock className="h-3 w-3 mr-1" />
                    ETA: {new Date(batchProgress.estimated_completion).toLocaleTimeString()}
                  </span>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <div className="flex items-start">
              <AlertCircle className="h-5 w-5 text-red-500 mt-0.5 mr-3 flex-shrink-0" />
              <div>
                <h4 className="font-medium text-red-900">Error</h4>
                <p className="text-red-700 text-sm mt-1">{error}</p>
              </div>
              <button
                onClick={() => setError(null)}
                className="ml-auto text-red-500 hover:text-red-700"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
          </div>
        )}

        {/* Results */}
        {batchResults.length > 0 && (
          <div className="bg-white rounded-lg shadow-lg p-6">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h3 className="text-xl font-semibold text-gray-900">Scan Results</h3>
                <p className="text-gray-600 text-sm">
                  Found {batchResults.length} stocks matching your criteria
                  {lastScanTime && (
                    <span className="ml-2">
                      • Last scan: {new Date(lastScanTime).toLocaleTimeString()}
                    </span>
                  )}
                </p>
              </div>
              
              <button
                onClick={exportToCSV}
                className="bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-4 rounded-lg flex items-center space-x-2 transition-colors"
              >
                <Download className="h-4 w-4" />
                <span>Export CSV</span>
              </button>
            </div>

            {/* Results Table */}
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Symbol
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Price
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      DMI/ADX
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      PPO Slope
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Hook Pattern
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Returns
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Source
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {batchResults.map((stock, index) => (
                    <tr key={index} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="font-medium text-gray-900">{stock.symbol}</div>
                        <div className="text-sm text-gray-500">{stock.name}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900">
                          ${stock.price?.toFixed(2) || '0.00'}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900">
                          DMI: {stock.dmi?.toFixed(1) || '0.0'}
                        </div>
                        <div className="text-sm text-gray-500">
                          ADX: {stock.adx?.toFixed(1) || '0.0'}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${
                          (stock.ppo_slope_percentage || 0) > 0 
                            ? 'bg-green-100 text-green-800' 
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {stock.ppo_slope_percentage?.toFixed(2) || '0.00'}%
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {stock.ppo_hook_display ? (
                          <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${
                            stock.ppo_hook_type === 'positive'
                              ? 'bg-green-100 text-green-800'
                              : 'bg-red-100 text-red-800'
                          }`}>
                            {stock.ppo_hook_display}
                          </span>
                        ) : (
                          <span className="text-gray-400 text-sm">No Hook</span>
                        )}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm space-y-1">
                          <div>1D: <span className={(stock.returns?.['1d'] || 0) >= 0 ? 'text-green-600' : 'text-red-600'}>
                            {stock.returns?.['1d']?.toFixed(2) || '0.00'}%
                          </span></div>
                          <div>5D: <span className={(stock.returns?.['5d'] || 0) >= 0 ? 'text-green-600' : 'text-red-600'}>
                            {stock.returns?.['5d']?.toFixed(2) || '0.00'}%
                          </span></div>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="inline-flex items-center px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full">
                          <Zap className="h-3 w-3 mr-1" />
                          {stock.data_source || 'api'}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default BatchScreener;