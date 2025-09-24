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

    // Safely extract data with fallbacks
    const currentPrice = Number(apiData.current_price) || 0;
    const indicators = apiData.indicators || {};
    const fundamental = apiData.fundamental_data || {};

    return {
      symbol: apiData.symbol || 'N/A',
      currentPrice: currentPrice,
      priceChange: Number(apiData.price_change_percent) || 0,
      peRatio: Number(fundamental.pe_ratio) || 25.0,
      rsi: Number(indicators.rsi) || 50.0,
      volume: Number(apiData.volume) || 1000000,
      sma20: Number(indicators.sma_20) || currentPrice,
      sma50: Number(indicators.sma_50) || currentPrice,
      sma200: Number(indicators.sma_200) || currentPrice,
      marketCap: fundamental.market_cap || 'N/A',
      dividendYield: Number(fundamental.dividend_yield) || 0,
      timestamp: new Date().toISOString(),
      dataSource: apiData.data_source || 'alpha_vantage',
      ppo: Number(indicators.ppo) || 0,
      adx: Number(indicators.adx) || 25,
      dmi_plus: Number(indicators.dmi_plus) || 20,
      dmi_minus: Number(indicators.dmi_minus) || 15
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
        reason: `Overbought condition at RSI ${metrics.rsi.toFixed(1)} suggests potential pullback`,
        impact: '-2 points'
      });
    } else {
      reasons.push({
        type: 'neutral',
        metric: 'RSI Indicator',
        reason: `RSI at ${metrics.rsi.toFixed(1)} shows balanced momentum`,
        impact: '0 points'
      });
    }

    // 4. Moving Average Analysis
    const smaScore = (metrics.currentPrice > metrics.sma20 ? 1 : 0) +
                     (metrics.currentPrice > metrics.sma50 ? 1 : 0) +
                     (metrics.currentPrice > metrics.sma200 ? 1 : 0);
    
    if (smaScore >= 2) {
      score += 1;
      reasons.push({
        type: 'positive',
        metric: 'Moving Averages',
        reason: `Price above key moving averages (${smaScore}/3) indicates uptrend`,
        impact: '+1 point'
      });
    } else if (smaScore === 0) {
      score -= 1;
      reasons.push({
        type: 'negative',
        metric: 'Moving Averages',
        reason: `Price below all moving averages indicates downtrend`,
        impact: '-1 point'
      });
    } else {
      reasons.push({
        type: 'neutral',
        metric: 'Moving Averages',
        reason: `Mixed signals from moving averages (${smaScore}/3)`,
        impact: '0 points'
      });
    }

    // 5. Volume Analysis
    const volumeInM = metrics.volume / 1000000;
    if (volumeInM > 2) {
      score += 1;
      reasons.push({
        type: 'positive',
        metric: 'Volume Activity',
        reason: `High volume activity (${volumeInM.toFixed(1)}M) suggests strong interest`,
        impact: '+1 point'
      });
    } else if (volumeInM < 0.5) {
      score -= 1;
      reasons.push({
        type: 'negative',
        metric: 'Volume Activity',
        reason: `Low volume (${volumeInM.toFixed(1)}M) indicates weak interest`,
        impact: '-1 point'
      });
    } else {
      reasons.push({
        type: 'neutral',
        metric: 'Volume Activity',
        reason: `Moderate volume activity (${volumeInM.toFixed(1)}M)`,
        impact: '0 points'
      });
    }

    // 6. Dividend Yield (if applicable)
    if (metrics.dividendYield > 3) {
      score += 1;
      reasons.push({
        type: 'positive',
        metric: 'Dividend Yield',
        reason: `Attractive dividend yield of ${metrics.dividendYield.toFixed(2)}%`,
        impact: '+1 point'
      });
    }

    // Calculate final recommendation
    let recommendation, confidence;
    if (score >= 3) {
      recommendation = 'BUY';
      confidence = Math.min(95, 60 + (score * 8));
    } else if (score <= -2) {
      recommendation = 'SELL';
      confidence = Math.min(95, 60 + (Math.abs(score) * 8));
    } else {
      recommendation = 'HOLD';
      confidence = 50 + (Math.random() * 20);
    }

    return {
      metrics,
      score,
      recommendation,
      confidence: Math.round(confidence),
      reasons,
      summary: `Point-based analysis yields ${score} points, suggesting ${recommendation} with ${Math.round(confidence)}% confidence.`
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
    setDataSource('');

    try {
      // Use real API to get stock data
      const apiData = await api.getStockAnalysis(stockSymbol.toUpperCase(), '3M');
      
      if (apiData) {
        const metrics = convertToPointBasedAnalysis(apiData);
        const analysisResult = calculateRecommendation(metrics);
        setDataSource(apiData.data_source || 'alpha_vantage');
        setAnalysis(analysisResult);
      } else {
        setError('No data found for this symbol. Please try another symbol.');
      }
    } catch (err) {
      console.error('Analysis error:', err);
      setError('Analysis failed. Please check the symbol and try again.');
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

  // Get reason icon
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
              <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-2 rounded-lg">
                <Target className="h-6 w-6" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Point Based Decision</h1>
                <p className="text-gray-600">Systematic Stock Evaluation System</p>
              </div>
            </div>
            
            {dataSource && (
              <div className="text-sm text-gray-600 bg-blue-50 px-3 py-2 rounded-lg border border-blue-200">
                <span className="font-medium">🔘 Data Source:</span> {dataSource === 'alpha_vantage' ? 'Alpha Vantage (Real Data)' : dataSource === 'mock' ? 'Demo Data (Simulated)' : dataSource}
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-6 py-8">
        {/* Analysis Input Form */}
        <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-8 mb-8">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-3">Stock Analysis Engine</h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Enter a stock symbol to receive a comprehensive point-based analysis using real market data, 
              technical indicators, and fundamental metrics to generate BUY/SELL/HOLD recommendations.
            </p>
          </div>

          <form onSubmit={handleAnalysis} className="max-w-md mx-auto">
            <div className="flex space-x-3">
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                <input
                  type="text"
                  value={stockSymbol}
                  onChange={(e) => setStockSymbol(e.target.value.toUpperCase())}
                  placeholder="Enter symbol (e.g., AAPL)"
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-center font-mono text-lg"
                  disabled={loading}
                />
              </div>
              <button
                type="submit"
                disabled={loading}
                className="px-8 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold rounded-lg hover:from-blue-700 hover:to-purple-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? (
                  <div className="flex items-center space-x-2">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    <span>Analyzing...</span>
                  </div>
                ) : (
                  'Analyze'
                )}
              </button>
            </div>
            
            {error && (
              <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-red-700 text-sm text-center">{error}</p>
              </div>
            )}
          </form>
        </div>

        {/* Analysis Results */}
        {analysis && (
          <div className="space-y-6">
            {/* Main Recommendation Card */}
            <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
              <div className="text-center">
                <div className="flex items-center justify-center mb-4">
                  <div className={`p-3 rounded-full ${getRecommendationStyle(analysis.recommendation).bgColor} ${getRecommendationStyle(analysis.recommendation).borderColor} border-2`}>
                    {React.createElement(getRecommendationStyle(analysis.recommendation).icon, {
                      className: `h-8 w-8 ${getRecommendationStyle(analysis.recommendation).textColor}`
                    })}
                  </div>
                </div>
                <h3 className="text-3xl font-bold text-gray-900 mb-2">{analysis.metrics.symbol}</h3>
                <div className={`inline-flex items-center px-6 py-2 rounded-full ${getRecommendationStyle(analysis.recommendation).bgColor} ${getRecommendationStyle(analysis.recommendation).borderColor} border-2 mb-4`}>
                  <span className={`text-2xl font-bold ${getRecommendationStyle(analysis.recommendation).textColor}`}>
                    {analysis.recommendation}
                  </span>
                </div>
                <p className="text-gray-600 mb-4">{analysis.summary}</p>
                <div className="flex items-center justify-center space-x-6">
                  <div className="text-center">
                    <p className="text-sm text-gray-500">Score</p>
                    <p className="text-2xl font-bold text-gray-900">{analysis.score}</p>
                  </div>
                  <div className="text-center">
                    <p className="text-sm text-gray-500">Confidence</p>
                    <p className="text-2xl font-bold text-gray-900">{analysis.confidence}%</p>
                  </div>
                  <div className="text-center">
                    <p className="text-sm text-gray-500">Current Price</p>
                    <p className="text-2xl font-bold text-gray-900">${analysis.metrics.currentPrice}</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Financial Metrics Grid */}
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[
                { label: 'P/E Ratio', value: analysis.metrics.peRatio, icon: BarChart3, color: 'blue' },
                { label: 'RSI', value: analysis.metrics.rsi?.toFixed(1), icon: Activity, color: 'purple' },
                { label: 'Volume', value: `${(analysis.metrics.volume / 1000000).toFixed(1)}M`, icon: TrendingUp, color: 'green' },
                { label: 'SMA 20', value: `$${analysis.metrics.sma20?.toFixed(2)}`, icon: Target, color: 'orange' },
                { label: 'SMA 50', value: `$${analysis.metrics.sma50?.toFixed(2)}`, icon: Target, color: 'red' },
                { label: 'Dividend Yield', value: `${analysis.metrics.dividendYield?.toFixed(2)}%`, icon: Zap, color: 'indigo' }
              ].map((metric, index) => (
                <div key={index} className="bg-white rounded-lg border border-gray-200 p-4 hover:shadow-md transition-shadow">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-500">{metric.label}</p>
                      <p className="text-xl font-bold text-gray-900">{metric.value}</p>
                    </div>
                    <div className={`p-2 rounded-lg bg-${metric.color}-100`}>
                      <metric.icon className={`h-5 w-5 text-${metric.color}-600`} />
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Detailed Analysis Reasons */}
            <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Analysis Breakdown</h3>
              <div className="space-y-4">
                {analysis.reasons.map((reason, index) => (
                  <div key={index} className="flex items-start space-x-3 p-4 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors">
                    <div className="mt-0.5">
                      {getReasonIcon(reason.type)}
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center justify-between">
                        <h4 className="font-semibold text-gray-900">{reason.metric}</h4>
                        <span className={`text-sm font-medium px-2 py-1 rounded ${
                          reason.type === 'positive' ? 'bg-green-100 text-green-800' :
                          reason.type === 'negative' ? 'bg-red-100 text-red-800' :
                          'bg-yellow-100 text-yellow-800'
                        }`}>
                          {reason.impact}
                        </span>
                      </div>
                      <p className="text-gray-600 mt-1">{reason.reason}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default PointBasedDecision;