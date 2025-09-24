import React, { useState } from 'react';
import { Search, TrendingUp, TrendingDown, Minus, BarChart3, Activity, Target, Zap, CheckCircle, XCircle, AlertTriangle } from 'lucide-react';
import api from '../services/api';

const PointBasedDecision = () => {
  const [stockSymbol, setStockSymbol] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [dataSource, setDataSource] = useState('');

  // Convert real API data to point-based analysis format
  const convertToPointBasedAnalysis = (apiData) => {
    if (!apiData) return null;

    return {
      symbol: apiData.symbol,
      currentPrice: apiData.current_price,
      priceChange: apiData.price_change_percent,
      peRatio: apiData.fundamental_data?.pe_ratio || 25.0,
      rsi: apiData.indicators?.rsi || 50.0,
      volume: apiData.volume,
      sma20: apiData.indicators?.sma_20 || apiData.current_price,
      sma50: apiData.indicators?.sma_50 || apiData.current_price,
      sma200: apiData.indicators?.sma_200 || apiData.current_price,
      marketCap: apiData.fundamental_data?.market_cap || 'N/A',
      dividendYield: apiData.fundamental_data?.dividend_yield || 0,
      timestamp: new Date().toISOString(),
      dataSource: apiData.data_source || 'alpha_vantage',
      ppo: apiData.indicators?.ppo || 0,
      adx: apiData.indicators?.adx || 25,
      dmi_plus: apiData.indicators?.dmi_plus || 20,
      dmi_minus: apiData.indicators?.dmi_minus || 15
    };
  };
  };

  // Comprehensive scoring algorithm
  const calculateRecommendation = (metrics) => {
    let score = 0;
    const reasons = [];

    // 1. Price Momentum Analysis
    if (metrics.priceChange > 5) {
      score += 2;
      reasons.push({
        type: 'positive',
        metric: 'Price Momentum',
        reason: `Strong upward momentum with ${metrics.priceChange.toFixed(1)}% gain`,
        impact: '+2 points'
      });
    } else if (metrics.priceChange < -5) {
      score -= 2;
      reasons.push({
        type: 'negative',
        metric: 'Price Momentum',
        reason: `Significant downward pressure with ${Math.abs(metrics.priceChange).toFixed(1)}% decline`,
        impact: '-2 points'
      });
    } else {
      reasons.push({
        type: 'neutral',
        metric: 'Price Momentum',
        reason: `Moderate price movement at ${metrics.priceChange.toFixed(1)}%`,
        impact: '0 points'
      });
    }

    // 2. P/E Ratio Valuation
    if (metrics.peRatio < 15) {
      score += 2;
      reasons.push({
        type: 'positive',
        metric: 'P/E Valuation',
        reason: `Attractive valuation with P/E ratio of ${metrics.peRatio}`,
        impact: '+2 points'
      });
    } else if (metrics.peRatio > 30) {
      score -= 1;
      reasons.push({
        type: 'negative',
        metric: 'P/E Valuation',
        reason: `High valuation concern with P/E ratio of ${metrics.peRatio}`,
        impact: '-1 point'
      });
    } else {
      reasons.push({
        type: 'neutral',
        metric: 'P/E Valuation',
        reason: `Fair valuation with P/E ratio of ${metrics.peRatio}`,
        impact: '0 points'
      });
    }

    // 3. RSI Technical Indicator
    if (metrics.rsi < 30) {
      score += 2;
      reasons.push({
        type: 'positive',
        metric: 'RSI Indicator',
        reason: `Oversold condition at RSI ${metrics.rsi.toFixed(1)} suggests potential upside`,
        impact: '+2 points'
      });
    } else if (metrics.rsi > 70) {
      score -= 2;
      reasons.push({
        type: 'negative',
        metric: 'RSI Indicator',
        reason: `Overbought condition at RSI ${metrics.rsi.toFixed(1)} suggests potential correction`,
        impact: '-2 points'
      });
    } else {
      reasons.push({
        type: 'neutral',
        metric: 'RSI Indicator',
        reason: `Neutral RSI at ${metrics.rsi.toFixed(1)} indicates balanced momentum`,
        impact: '0 points'
      });
    }

    // 4. Moving Average Trend
    const aboveMA = metrics.currentPrice > metrics.sma20 && metrics.currentPrice > metrics.sma50;
    if (aboveMA) {
      score += 1;
      reasons.push({
        type: 'positive',
        metric: 'Moving Average Trend',
        reason: `Price above key moving averages indicates uptrend`,
        impact: '+1 point'
      });
    } else {
      score -= 1;
      reasons.push({
        type: 'negative',
        metric: 'Moving Average Trend',
        reason: `Price below moving averages suggests downtrend`,
        impact: '-1 point'
      });
    }

    // 5. Volume Analysis (additional insight)
    const volumeLevel = metrics.volume > 1000000 ? 'High' : metrics.volume > 500000 ? 'Moderate' : 'Low';
    reasons.push({
      type: 'neutral',
      metric: 'Volume Analysis',
      reason: `${volumeLevel} trading volume of ${metrics.volume.toLocaleString()} shares`,
      impact: 'Informational'
    });

    // Generate final recommendation
    let recommendation, confidence, description;
    
    if (score >= 3) {
      recommendation = 'BUY';
      confidence = Math.min(95, 70 + (score - 3) * 5);
      description = 'Strong positive indicators suggest good buying opportunity';
    } else if (score <= -2) {
      recommendation = 'SELL';
      confidence = Math.min(95, 70 + Math.abs(score + 2) * 5);
      description = 'Multiple negative factors indicate selling pressure';
    } else {
      recommendation = 'HOLD';
      confidence = 60 + Math.abs(score) * 5;
      description = 'Mixed signals suggest maintaining current position';
    }

    return {
      recommendation,
      score,
      confidence,
      description,
      reasons,
      metrics
    };
  };

  // Form submission handler
  const handleAnalysis = async (e) => {
    e.preventDefault();
    
    if (!stockSymbol.trim()) {
      setError('Please enter a stock symbol');
      return;
    }

    if (stockSymbol.length > 5) {
      setError('Stock symbol should be 5 characters or less');
      return;
    }

    setError('');
    setLoading(true);
    setAnalysis(null);

    try {
      // Simulate API delay for realistic experience
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      const metrics = generateFinancialMetrics(stockSymbol);
      const analysisResult = calculateRecommendation(metrics);
      
      setAnalysis(analysisResult);
    } catch (err) {
      setError('Analysis failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Get recommendation styling
  const getRecommendationStyle = (recommendation) => {
    switch (recommendation) {
      case 'BUY':
        return {
          bgColor: 'bg-green-100',
          textColor: 'text-green-800',
          borderColor: 'border-green-200',
          icon: TrendingUp
        };
      case 'SELL':
        return {
          bgColor: 'bg-red-100',
          textColor: 'text-red-800',
          borderColor: 'border-red-200',
          icon: TrendingDown
        };
      default:
        return {
          bgColor: 'bg-yellow-100',
          textColor: 'text-yellow-800',
          borderColor: 'border-yellow-200',
          icon: Minus
        };
    }
  };

  const getReasonIcon = (type) => {
    switch (type) {
      case 'positive':
        return <CheckCircle className="h-4 w-4 text-green-600" />;
      case 'negative':
        return <XCircle className="h-4 w-4 text-red-600" />;
      default:
        return <AlertTriangle className="h-4 w-4 text-yellow-600" />;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Professional Header */}
      <div className="bg-white shadow-lg border-b border-gray-200">
        <div className="max-w-6xl mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="p-3 bg-gradient-to-r from-green-500 to-blue-600 rounded-xl shadow-lg">
                <Target className="h-7 w-7 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-green-600 to-blue-600 bg-clip-text text-transparent">
                  Point-Based Decision System
                </h1>
                <p className="text-sm text-gray-600">Quantitative Stock Analysis with Transparent Scoring</p>
                {/* Data Source Indicator */}
                <div className="flex items-center space-x-2 text-xs text-gray-500 mt-1">
                  <span className="w-2 h-2 bg-gray-500 rounded-full"></span>
                  <span>Analysis Data: Deterministic Demo Simulation</span>
                </div>
              </div>
            </div>
            <div className="flex items-center space-x-2 text-sm text-gray-500">
              <Activity className="h-4 w-4" />
              <span>Multi-Factor Analysis Engine</span>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-6 py-8">
        {/* Stock Input Form */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-8 border border-gray-100">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-3">Quantitative Stock Recommendation</h2>
            <p className="text-gray-600 text-lg max-w-2xl mx-auto">
              Get transparent buy, sell, or hold recommendations based on systematic point-based scoring
            </p>
          </div>

          <form onSubmit={handleAnalysis} className="max-w-md mx-auto">
            <div className="relative">
              <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
              <input
                type="text"
                value={stockSymbol}
                onChange={(e) => setStockSymbol(e.target.value.toUpperCase())}
                placeholder="Enter stock symbol (e.g., AAPL, TSLA)"
                className="w-full pl-12 pr-4 py-4 text-lg border-2 border-gray-300 rounded-xl focus:outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-100 transition-all"
                disabled={loading}
                maxLength={5}
              />
            </div>
            
            {error && (
              <div className="mt-3 p-3 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-red-600 text-sm font-medium">{error}</p>
              </div>
            )}

            <button
              type="submit"
              disabled={loading || !stockSymbol.trim()}
              className="w-full mt-6 px-6 py-4 bg-gradient-to-r from-green-500 to-blue-600 text-white font-semibold rounded-xl hover:from-green-600 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all text-lg shadow-lg"
            >
              {loading ? (
                <div className="flex items-center justify-center space-x-2">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                  <span>Analyzing...</span>
                </div>
              ) : (
                'Analyze Stock'
              )}
            </button>
          </form>
        </div>

        {/* Analysis Results */}
        {analysis && (
          <div className="space-y-6">
            {/* Recommendation Card */}
            <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
              <div className="text-center mb-8">
                <h3 className="text-2xl font-bold text-gray-900 mb-4">
                  Analysis Results for {analysis.metrics.symbol}
                </h3>
                
                {(() => {
                  const style = getRecommendationStyle(analysis.recommendation);
                  const RecommendationIcon = style.icon;
                  
                  return (
                    <div className="flex items-center justify-center space-x-4 mb-6">
                      <div className={`${style.bgColor} ${style.textColor} ${style.borderColor} border-2 px-8 py-4 rounded-2xl flex items-center space-x-3 shadow-lg`}>
                        <RecommendationIcon className="h-8 w-8" />
                        <span className="text-3xl font-bold">{analysis.recommendation}</span>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-gray-900">{analysis.confidence}%</div>
                        <div className="text-sm text-gray-600">Confidence</div>
                      </div>
                    </div>
                  );
                })()}
                
                <p className="text-lg text-gray-700 max-w-2xl mx-auto">{analysis.description}</p>
                <div className="mt-4 inline-flex items-center space-x-2 bg-gray-100 px-4 py-2 rounded-full">
                  <Target className="h-4 w-4 text-gray-600" />
                  <span className="text-sm font-medium text-gray-700">
                    Score: {analysis.score > 0 ? '+' : ''}{analysis.score} points
                  </span>
                </div>
              </div>

              {/* Financial Metrics Grid */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-8">
                <div className="text-center p-4 bg-gray-50 rounded-xl border border-gray-200">
                  <div className="text-2xl font-bold text-gray-900">${analysis.metrics.currentPrice}</div>
                  <div className="text-sm text-gray-600">Current Price</div>
                  <div className={`text-sm font-medium mt-1 ${analysis.metrics.priceChange >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                    {analysis.metrics.priceChange >= 0 ? '+' : ''}{analysis.metrics.priceChange}%
                  </div>
                </div>
                
                <div className="text-center p-4 bg-gray-50 rounded-xl border border-gray-200">
                  <div className="text-2xl font-bold text-gray-900">{analysis.metrics.peRatio}</div>
                  <div className="text-sm text-gray-600">P/E Ratio</div>
                  <div className={`text-sm font-medium mt-1 ${analysis.metrics.peRatio < 15 ? 'text-green-600' : analysis.metrics.peRatio > 30 ? 'text-red-600' : 'text-yellow-600'}`}>
                    {analysis.metrics.peRatio < 15 ? 'Attractive' : analysis.metrics.peRatio > 30 ? 'Expensive' : 'Fair'}
                  </div>
                </div>
                
                <div className="text-center p-4 bg-gray-50 rounded-xl border border-gray-200">
                  <div className="text-2xl font-bold text-gray-900">{analysis.metrics.rsi}</div>
                  <div className="text-sm text-gray-600">RSI</div>
                  <div className={`text-sm font-medium mt-1 ${analysis.metrics.rsi < 30 ? 'text-green-600' : analysis.metrics.rsi > 70 ? 'text-red-600' : 'text-yellow-600'}`}>
                    {analysis.metrics.rsi < 30 ? 'Oversold' : analysis.metrics.rsi > 70 ? 'Overbought' : 'Neutral'}
                  </div>
                </div>
                
                <div className="text-center p-4 bg-gray-50 rounded-xl border border-gray-200">
                  <div className="text-2xl font-bold text-gray-900">{analysis.metrics.volume.toLocaleString()}</div>
                  <div className="text-sm text-gray-600">Volume</div>
                  <div className="text-sm font-medium mt-1 text-blue-600">
                    {analysis.metrics.volume > 1000000 ? 'High' : 'Moderate'}
                  </div>
                </div>
              </div>

              {/* Additional Metrics */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="p-4 bg-blue-50 rounded-xl border border-blue-200">
                  <h4 className="font-semibold text-gray-900 mb-2">Moving Averages</h4>
                  <div className="space-y-1 text-sm">
                    <div className="flex justify-between">
                      <span>SMA 20:</span>
                      <span className="font-medium">${analysis.metrics.sma20}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>SMA 50:</span>
                      <span className="font-medium">${analysis.metrics.sma50}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>SMA 200:</span>
                      <span className="font-medium">${analysis.metrics.sma200}</span>
                    </div>
                  </div>
                </div>
                
                <div className="p-4 bg-green-50 rounded-xl border border-green-200">
                  <h4 className="font-semibold text-gray-900 mb-2">Valuation</h4>
                  <div className="space-y-1 text-sm">
                    <div className="flex justify-between">
                      <span>Market Cap:</span>
                      <span className="font-medium">${(analysis.metrics.marketCap / 1000000).toFixed(0)}M</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Dividend Yield:</span>
                      <span className="font-medium">{analysis.metrics.dividendYield}%</span>
                    </div>
                  </div>
                </div>
                
                <div className="p-4 bg-purple-50 rounded-xl border border-purple-200">
                  <h4 className="font-semibold text-gray-900 mb-2">Technical Status</h4>
                  <div className="space-y-1 text-sm">
                    <div className="flex justify-between">
                      <span>Trend:</span>
                      <span className={`font-medium ${analysis.metrics.currentPrice > analysis.metrics.sma50 ? 'text-green-600' : 'text-red-600'}`}>
                        {analysis.metrics.currentPrice > analysis.metrics.sma50 ? 'Uptrend' : 'Downtrend'}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span>Momentum:</span>
                      <span className={`font-medium ${Math.abs(analysis.metrics.priceChange) > 2 ? 'text-blue-600' : 'text-gray-600'}`}>
                        {Math.abs(analysis.metrics.priceChange) > 2 ? 'Strong' : 'Weak'}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Intelligent Explanation System */}
            <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
              <h3 className="text-2xl font-bold text-gray-900 mb-6 flex items-center space-x-2">
                <Zap className="h-6 w-6 text-blue-600" />
                <span>Decision Analysis</span>
              </h3>
              
              <div className="space-y-4">
                {analysis.reasons.map((reason, index) => (
                  <div key={index} className={`p-4 rounded-xl border-2 ${
                    reason.type === 'positive' ? 'bg-green-50 border-green-200' :
                    reason.type === 'negative' ? 'bg-red-50 border-red-200' :
                    'bg-yellow-50 border-yellow-200'
                  }`}>
                    <div className="flex items-start space-x-3">
                      {getReasonIcon(reason.type)}
                      <div className="flex-1">
                        <div className="flex items-center justify-between mb-2">
                          <h4 className="font-semibold text-gray-900">{reason.metric}</h4>
                          <span className={`text-sm font-medium px-2 py-1 rounded-full ${
                            reason.type === 'positive' ? 'bg-green-100 text-green-800' :
                            reason.type === 'negative' ? 'bg-red-100 text-red-800' :
                            'bg-yellow-100 text-yellow-800'
                          }`}>
                            {reason.impact}
                          </span>
                        </div>
                        <p className="text-gray-700">{reason.reason}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              <div className="mt-6 p-4 bg-gray-100 rounded-xl border border-gray-200">
                <h4 className="font-semibold text-gray-900 mb-2">Scoring Summary</h4>
                <p className="text-sm text-gray-700">
                  <strong>Recommendation Logic:</strong> BUY (≥3 points) | HOLD (-1 to 2 points) | SELL (≤-2 points)
                </p>
                <p className="text-sm text-gray-600 mt-1">
                  Final Score: <strong>{analysis.score > 0 ? '+' : ''}{analysis.score} points</strong> → 
                  <strong className={`ml-1 ${
                    analysis.recommendation === 'BUY' ? 'text-green-600' :
                    analysis.recommendation === 'SELL' ? 'text-red-600' :
                    'text-yellow-600'
                  }`}>
                    {analysis.recommendation}
                  </strong>
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default PointBasedDecision;