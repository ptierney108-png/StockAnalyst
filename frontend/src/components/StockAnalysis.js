import React, { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import Chart from 'react-apexcharts';
import { Search, TrendingUp, TrendingDown, Brain, BarChart3, Activity, Target } from 'lucide-react';
import api from '../services/api';

const StockAnalysis = () => {
  const [symbol, setSymbol] = useState('AAPL');
  const [inputSymbol, setInputSymbol] = useState('');
  const [timeframe, setTimeframe] = useState('1D');

  const {
    data: analysisData,
    isLoading,
    error,
    refetch
  } = useQuery({
    queryKey: ['stock-analysis', symbol],
    queryFn: () => api.getStockAnalysis(symbol),
    enabled: !!symbol,
    refetchInterval: 30000, // Refresh every 30 seconds
  });

  const handleAnalyze = () => {
    if (inputSymbol.trim()) {
      setSymbol(inputSymbol.toUpperCase());
      setInputSymbol('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleAnalyze();
    }
  };

  // Prepare candlestick chart data
  const candlestickData = analysisData?.chart_data?.map(item => ({
    x: new Date(item.date),
    y: [item.open, item.high, item.low, item.close]
  })) || [];

  // Prepare PPO chart data
  const ppoData = analysisData?.chart_data?.map(item => ({
    x: new Date(item.date),
    y: item.ppo || 0
  })) || [];

  // Candlestick chart options
  const candlestickOptions = {
    chart: {
      type: 'candlestick',
      height: 400,
      toolbar: {
        show: true,
        tools: {
          download: true,
          selection: true,
          zoom: true,
          zoomin: true,
          zoomout: true,
          pan: true,
          reset: true
        }
      }
    },
    title: {
      text: `${symbol} - ${timeframe} Chart`,
      align: 'left',
      style: {
        fontSize: '16px',
        fontWeight: 'bold'
      }
    },
    xaxis: {
      type: 'datetime',
      labels: {
        format: 'MMM dd'
      }
    },
    yaxis: {
      tooltip: {
        enabled: true
      },
      labels: {
        formatter: (value) => `$${value?.toFixed(2)}`
      }
    },
    plotOptions: {
      candlestick: {
        colors: {
          upward: '#00b746',
          downward: '#ef403c'
        },
        wick: {
          useFillColor: true
        }
      }
    },
    grid: {
      show: true,
      borderColor: '#e0e0e0',
      strokeDashArray: 1
    },
    tooltip: {
      shared: false,
      y: {
        formatter: (value) => `$${value?.toFixed(2)}`
      }
    }
  };

  // PPO chart options
  const ppoOptions = {
    chart: {
      type: 'line',
      height: 200,
      toolbar: {
        show: false
      }
    },
    title: {
      text: 'PPO Indicator',
      align: 'left',
      style: {
        fontSize: '14px',
        fontWeight: 'bold'
      }
    },
    xaxis: {
      type: 'datetime',
      labels: {
        format: 'MMM dd'
      }
    },
    yaxis: {
      labels: {
        formatter: (value) => `${value?.toFixed(2)}%`
      }
    },
    stroke: {
      curve: 'smooth',
      width: 2
    },
    colors: ['#2563eb'],
    grid: {
      show: true,
      borderColor: '#e0e0e0',
      strokeDashArray: 1
    },
    markers: {
      size: 0
    },
    tooltip: {
      y: {
        formatter: (value) => `${value?.toFixed(2)}%`
      }
    }
  };

  const getRecommendationColor = (recommendation) => {
    switch (recommendation) {
      case 'BUY': return 'text-green-600 bg-green-100';
      case 'SELL': return 'text-red-600 bg-red-100';
      default: return 'text-yellow-600 bg-yellow-100';
    }
  };

  const getSentimentColor = (sentiment) => {
    switch (sentiment) {
      case 'Positive': return 'text-green-600 bg-green-100';
      case 'Negative': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  if (error) {
    return (
      <div className="max-w-6xl mx-auto p-6">
        <div className="bg-red-50 border border-red-200 rounded-lg p-8 text-center">
          <BarChart3 className="h-12 w-12 text-red-400 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-red-900 mb-2">Analysis Error</h2>
          <p className="text-red-600">Unable to load analysis for {symbol}</p>
          <button
            onClick={() => refetch()}
            className="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
          >
            Retry Analysis
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-6">
      {/* Header & Stock Input */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
              <Activity className="h-6 w-6 text-blue-600" />
              Stock Technical Analysis
            </h1>
            <p className="text-gray-600">Advanced technical indicators and AI-powered insights</p>
          </div>
          
          <div className="flex gap-2">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
              <input
                type="text"
                value={inputSymbol}
                onChange={(e) => setInputSymbol(e.target.value.toUpperCase())}
                onKeyPress={handleKeyPress}
                placeholder="Enter stock symbol..."
                className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 w-48"
              />
            </div>
            <button
              onClick={handleAnalyze}
              disabled={!inputSymbol.trim() || isLoading}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Analyzing...' : 'Analyze'}
            </button>
          </div>
        </div>
      </div>

      {isLoading ? (
        <div className="space-y-6">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="bg-white rounded-lg shadow p-6 animate-pulse">
              <div className="h-6 bg-gray-200 rounded w-1/4 mb-4"></div>
              <div className="h-64 bg-gray-200 rounded"></div>
            </div>
          ))}
        </div>
      ) : analysisData && (
        <>
          {/* Stock Overview */}
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-start justify-between mb-4">
              <div>
                <h2 className="text-xl font-bold text-gray-900">{analysisData.symbol}</h2>
                <p className="text-3xl font-bold text-gray-900 mt-1">
                  ${analysisData.current_price?.toFixed(2)}
                </p>
              </div>
              <div className="text-right">
                <div className={`flex items-center space-x-1 ${
                  analysisData.price_change >= 0 ? 'text-green-600' : 'text-red-600'
                }`}>
                  {analysisData.price_change >= 0 ? (
                    <TrendingUp className="h-4 w-4" />
                  ) : (
                    <TrendingDown className="h-4 w-4" />
                  )}
                  <span className="font-semibold">
                    {analysisData.price_change >= 0 ? '+' : ''}${analysisData.price_change?.toFixed(2)}
                  </span>
                  <span>({analysisData.price_change_percent?.toFixed(2)}%)</span>
                </div>
                <p className="text-sm text-gray-500 mt-1">
                  Volume: {analysisData.volume?.toLocaleString()}
                </p>
              </div>
            </div>

            {/* AI Recommendation & Sentiment */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
              <div className="border rounded-lg p-4">
                <div className="flex items-center space-x-2 mb-2">
                  <Brain className="h-5 w-5 text-purple-600" />
                  <h3 className="font-semibold text-gray-900">AI Recommendation</h3>
                </div>
                <div className="flex items-center justify-between">
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${getRecommendationColor(analysisData.ai_recommendation)}`}>
                    {analysisData.ai_recommendation}
                  </span>
                  <span className="text-sm text-gray-600">
                    Confidence: {(analysisData.ai_confidence * 100)?.toFixed(1)}%
                  </span>
                </div>
              </div>

              <div className="border rounded-lg p-4">
                <div className="flex items-center space-x-2 mb-2">
                  <Target className="h-5 w-5 text-orange-600" />
                  <h3 className="font-semibold text-gray-900">Market Sentiment</h3>
                </div>
                <div className="flex items-center justify-between">
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${getSentimentColor(analysisData.sentiment_analysis)}`}>
                    {analysisData.sentiment_analysis}
                  </span>
                  <span className="text-sm text-gray-600">
                    Score: {analysisData.sentiment_score?.toFixed(2)}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Charts */}
          <div className="bg-white rounded-lg shadow p-6">
            <div className="mb-4">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Price Chart</h3>
              <div className="flex space-x-2">
                {['1D', '1W', '1M', '3M', '1Y'].map((tf) => (
                  <button
                    key={tf}
                    onClick={() => setTimeframe(tf)}
                    className={`px-3 py-1 text-sm rounded ${
                      timeframe === tf
                        ? 'bg-blue-100 text-blue-700'
                        : 'text-gray-600 hover:text-gray-900'
                    }`}
                  >
                    {tf}
                  </button>
                ))}
              </div>
            </div>
            
            <Chart
              options={candlestickOptions}
              series={[{ data: candlestickData }]}
              type="candlestick"
              height={400}
            />
          </div>

          {/* PPO Indicator Chart */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">PPO Indicator</h3>
            <Chart
              options={ppoOptions}
              series={[{ name: 'PPO', data: ppoData }]}
              type="line"
              height={200}
            />
          </div>

          {/* Technical Indicators */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* PPO & DMI Data Display */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">PPO Data (Last 3 Days)</h3>
              <div className="space-y-3">
                {analysisData.ppo_history?.map((item, index) => (
                  <div key={index} className="flex justify-between items-center p-3 bg-gray-50 rounded">
                    <span className="text-sm font-medium text-gray-700">{item.date}</span>
                    <span className={`font-bold ${item.ppo >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                      {item.ppo?.toFixed(3)}%
                    </span>
                  </div>
                ))}
              </div>
              
              {/* PPO Slope */}
              <div className="mt-4 p-3 bg-blue-50 rounded">
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium text-gray-700">PPO Slope</span>
                  <span className={`font-bold ${analysisData.indicators?.ppo_slope_percentage >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                    {analysisData.indicators?.ppo_slope_percentage?.toFixed(2)}%
                  </span>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">DMI Data (Last 3 Days)</h3>
              <div className="space-y-3">
                {analysisData.dmi_history?.map((item, index) => (
                  <div key={index} className="p-3 bg-gray-50 rounded">
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-sm font-medium text-gray-700">{item.date}</span>
                    </div>
                    <div className="grid grid-cols-3 gap-2 text-xs">
                      <div>DMI+: <span className="font-bold text-green-600">{item.dmi_plus?.toFixed(1)}</span></div>
                      <div>DMI-: <span className="font-bold text-red-600">{item.dmi_minus?.toFixed(1)}</span></div>
                      <div>ADX: <span className="font-bold text-blue-600">{item.adx?.toFixed(1)}</span></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* All Technical Indicators */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Technical Indicators</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              <div className="p-3 border rounded">
                <div className="text-xs text-gray-500">PPO</div>
                <div className="font-bold text-blue-600">{analysisData.indicators?.ppo?.toFixed(3)}%</div>
              </div>
              <div className="p-3 border rounded">
                <div className="text-xs text-gray-500">PPO Signal</div>
                <div className="font-bold text-blue-600">{analysisData.indicators?.ppo_signal?.toFixed(3)}%</div>
              </div>
              <div className="p-3 border rounded">
                <div className="text-xs text-gray-500">RSI</div>
                <div className={`font-bold ${analysisData.indicators?.rsi > 70 ? 'text-red-600' : analysisData.indicators?.rsi < 30 ? 'text-green-600' : 'text-gray-600'}`}>
                  {analysisData.indicators?.rsi?.toFixed(1)}
                </div>
              </div>
              <div className="p-3 border rounded">
                <div className="text-xs text-gray-500">MACD</div>
                <div className={`font-bold ${analysisData.indicators?.macd >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {analysisData.indicators?.macd?.toFixed(3)}
                </div>
              </div>
              <div className="p-3 border rounded">
                <div className="text-xs text-gray-500">SMA 20</div>
                <div className="font-bold text-gray-600">${analysisData.indicators?.sma_20?.toFixed(2)}</div>
              </div>
              <div className="p-3 border rounded">
                <div className="text-xs text-gray-500">SMA 50</div>
                <div className="font-bold text-gray-600">${analysisData.indicators?.sma_50?.toFixed(2)}</div>
              </div>
              <div className="p-3 border rounded">
                <div className="text-xs text-gray-500">SMA 200</div>
                <div className="font-bold text-gray-600">${analysisData.indicators?.sma_200?.toFixed(2)}</div>
              </div>
              <div className="p-3 border rounded">
                <div className="text-xs text-gray-500">ADX</div>
                <div className={`font-bold ${analysisData.indicators?.adx > 25 ? 'text-green-600' : 'text-gray-600'}`}>
                  {analysisData.indicators?.adx?.toFixed(1)}
                </div>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default StockAnalysis;