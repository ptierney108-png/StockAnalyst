import React, { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useSearchParams } from 'react-router-dom';
import Chart from 'react-apexcharts';
import { Search, TrendingUp, TrendingDown, Brain, BarChart3, Activity, Target, Zap } from 'lucide-react';
import api from '../services/api';

const StockAnalysis = () => {
  const [searchParams] = useSearchParams();
  const urlSymbol = searchParams.get('symbol');
  
  const [symbol, setSymbol] = useState(urlSymbol || 'AAPL');
  const [inputSymbol, setInputSymbol] = useState('');

  // Update symbol when URL parameter changes
  useEffect(() => {
    if (urlSymbol && urlSymbol !== symbol) {
      setSymbol(urlSymbol.toUpperCase());
    }
  }, [urlSymbol, symbol]);

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

  // Prepare sophisticated candlestick chart data
  const candlestickData = analysisData?.chart_data?.map(item => ({
    x: new Date(item.date).getTime(),
    y: [item.open, item.high, item.low, item.close]
  })) || [];

  // Prepare PPO data for the bottom chart  
  const ppoData = analysisData?.chart_data?.map(item => ({
    x: new Date(item.date).getTime(),
    y: item.ppo || 0
  })) || [];

  // Advanced Candlestick Chart Configuration
  const chartOptions = {
    chart: {
      type: 'candlestick',
      height: 400,
      id: 'candlestick-chart',
      toolbar: {
        show: true,
        autoSelected: 'pan',
        tools: {
          download: true,
          selection: true,
          zoom: true,
          zoomin: true,
          zoomout: true,
          pan: true,
          reset: true
        }
      },
      background: '#ffffff',
      foreColor: '#333'
    },
    title: {
      text: `${symbol} - Stock Analysis`,
      align: 'left',
      style: {
        fontSize: '18px',
        fontWeight: 'bold',
        color: '#1f2937'
      }
    },
    xaxis: {
      type: 'datetime',
      labels: {
        format: 'MMM dd',
        style: {
          colors: '#6b7280',
          fontSize: '12px'
        }
      },
      axisBorder: {
        show: true,
        color: '#e5e7eb'
      },
      axisTicks: {
        show: true,
        color: '#e5e7eb'
      }
    },
    yaxis: {
      tooltip: {
        enabled: true
      },
      labels: {
        formatter: (value) => `$${value?.toFixed(2)}`,
        style: {
          colors: '#6b7280',
          fontSize: '12px'
        }
      },
      title: {
        text: 'Price ($)',
        style: {
          color: '#6b7280',
          fontSize: '12px',
          fontWeight: 600
        }
      }
    },
    plotOptions: {
      candlestick: {
        colors: {
          upward: '#10b981',
          downward: '#ef4444'
        },
        wick: {
          useFillColor: true
        }
      }
    },
    grid: {
      show: true,
      borderColor: '#f3f4f6',
      strokeDashArray: 1,
      position: 'back',
      xaxis: {
        lines: {
          show: false
        }
      },
      yaxis: {
        lines: {
          show: true
        }
      }
    },
    tooltip: {
      shared: false,
      custom: function({ seriesIndex, dataPointIndex, w }) {
        const o = w.globals.seriesCandleO[seriesIndex][dataPointIndex];
        const h = w.globals.seriesCandleH[seriesIndex][dataPointIndex];
        const l = w.globals.seriesCandleL[seriesIndex][dataPointIndex];
        const c = w.globals.seriesCandleC[seriesIndex][dataPointIndex];
        return `
          <div class="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
            <div class="font-semibold text-gray-900 mb-2">${symbol}</div>
            <div class="space-y-1 text-sm">
              <div>Open: <span class="font-medium">$${o?.toFixed(2)}</span></div>
              <div>High: <span class="font-medium text-green-600">$${h?.toFixed(2)}</span></div>
              <div>Low: <span class="font-medium text-red-600">$${l?.toFixed(2)}</span></div>
              <div>Close: <span class="font-medium">$${c?.toFixed(2)}</span></div>
            </div>
          </div>
        `;
      }
    },
    responsive: [{
      breakpoint: 768,
      options: {
        chart: {
          height: 300
        }
      }
    }]
  };

  // PPO Indicator Chart with Histogram (like MACD)
  const ppoChartOptions = {
    chart: {
      type: 'line',
      height: 200,
      id: 'ppo-chart',
      toolbar: {
        show: false
      },
      background: '#ffffff'
    },
    title: {
      text: 'PPO Indicator with Histogram',
      align: 'left',
      style: {
        fontSize: '14px',
        fontWeight: 'bold',
        color: '#1f2937'
      }
    },
    xaxis: {
      type: 'datetime',
      labels: {
        show: false
      },
      axisBorder: {
        show: false
      },
      axisTicks: {
        show: false
      }
    },
    yaxis: [
      {
        seriesName: 'PPO',
        labels: {
          formatter: (value) => `${value?.toFixed(2)}%`,
          style: {
            colors: '#6b7280',
            fontSize: '10px'
          }
        },
        title: {
          text: 'PPO (%)',
          style: {
            color: '#6b7280',
            fontSize: '10px',
            fontWeight: 600
          }
        }
      },
      {
        seriesName: 'Histogram',
        opposite: true,
        labels: {
          formatter: (value) => `${value?.toFixed(3)}`,
          style: {
            colors: '#6b7280',
            fontSize: '10px'
          }
        },
        title: {
          text: 'Histogram',
          style: {
            color: '#6b7280',
            fontSize: '10px',
            fontWeight: 600
          }
        }
      }
    ],
    stroke: {
      curve: 'smooth',
      width: [2, 2, 0] // PPO, Signal, Histogram (no stroke for bars)
    },
    colors: ['#3b82f6', '#f59e0b', '#10b981'],
    grid: {
      show: true,
      borderColor: '#f3f4f6',
      strokeDashArray: 1,
      yaxis: {
        lines: {
          show: true
        }
      }
    },
    markers: {
      size: 0
    },
    tooltip: {
      y: {
        formatter: (value, { seriesIndex }) => {
          if (seriesIndex === 2) return `${value?.toFixed(3)}`;
          return `${value?.toFixed(3)}%`;
        }
      }
    },
    dataLabels: {
      enabled: false
    },
    legend: {
      show: true,
      position: 'top',
      horizontalAlign: 'right',
      fontSize: '12px'
    },
    plotOptions: {
      bar: {
        columnWidth: '50%'
      }
    }
  };

  // Prepare PPO chart series data
  const ppoChartSeries = [
    {
      name: 'PPO Line',
      type: 'line',
      data: analysisData?.chart_data?.map(item => ({
        x: new Date(item.date).getTime(),
        y: item.ppo || 0
      })) || []
    },
    {
      name: 'PPO Signal',
      type: 'line', 
      data: analysisData?.chart_data?.map(item => ({
        x: new Date(item.date).getTime(),
        y: (item.ppo || 0) * 0.85 // Signal line approximation
      })) || []
    },
    {
      name: 'Histogram',
      type: 'column',
      yAxisIndex: 1,
      data: analysisData?.chart_data?.map(item => ({
        x: new Date(item.date).getTime(),
        y: ((item.ppo || 0) - (item.ppo || 0) * 0.85) // Histogram = PPO - Signal
      })) || []
    }
  ];

  const getRecommendationColor = (recommendation) => {
    switch (recommendation) {
      case 'BUY': return 'text-green-700 bg-green-100 border-green-200';
      case 'SELL': return 'text-red-700 bg-red-100 border-red-200';
      default: return 'text-yellow-700 bg-yellow-100 border-yellow-200';
    }
  };

  const getSentimentColor = (sentiment) => {
    switch (sentiment) {
      case 'Positive': return 'text-green-700 bg-green-100 border-green-200';
      case 'Negative': return 'text-red-700 bg-red-100 border-red-200';
      default: return 'text-gray-700 bg-gray-100 border-gray-200';
    }
  };

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <div className="max-w-4xl mx-auto">
          <div className="bg-red-50 border border-red-200 rounded-xl p-8 text-center">
            <BarChart3 className="h-12 w-12 text-red-400 mx-auto mb-4" />
            <h2 className="text-xl font-semibold text-red-900 mb-2">Analysis Error</h2>
            <p className="text-red-600">Unable to load analysis for {symbol}</p>
            <button
              onClick={() => refetch()}
              className="mt-4 px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
            >
              Retry Analysis
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-blue-100 rounded-lg">
                <Zap className="h-6 w-6 text-blue-600" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">FinanceAI</h1>
                <p className="text-sm text-gray-600">AI-Powered Stock Trading Platform</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-3">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                <input
                  type="text"
                  value={inputSymbol}
                  onChange={(e) => setInputSymbol(e.target.value.toUpperCase())}
                  onKeyPress={handleKeyPress}
                  placeholder="Enter stock symbol..."
                  className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent w-64"
                />
              </div>
              <button
                onClick={handleAnalyze}
                disabled={!inputSymbol.trim() || isLoading}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
              >
                {isLoading ? 'Analyzing...' : 'Start Analyzing'}
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8 space-y-8">
        {isLoading ? (
          <div className="space-y-6">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="bg-white rounded-xl shadow-sm p-6 animate-pulse">
                <div className="h-6 bg-gray-200 rounded w-1/4 mb-4"></div>
                <div className="h-64 bg-gray-200 rounded"></div>
              </div>
            ))}
          </div>
        ) : analysisData && (
          <>
            {/* Market Overview Section */}
            <div className="bg-white rounded-xl shadow-sm p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Market Overview</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="p-6 bg-gray-50 rounded-lg">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="text-lg font-semibold text-gray-900">{analysisData.symbol}</h3>
                    <div className={`flex items-center space-x-1 ${analysisData.price_change >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                      {analysisData.price_change >= 0 ? (
                        <TrendingUp className="h-4 w-4" />
                      ) : (
                        <TrendingDown className="h-4 w-4" />
                      )}
                      <span className="font-semibold">
                        {analysisData.price_change_percent?.toFixed(2)}%
                      </span>
                    </div>
                  </div>
                  <div className="text-3xl font-bold text-gray-900 mb-4">
                    ${analysisData.current_price?.toFixed(2)}
                  </div>
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-gray-500">Volume:</span>
                      <span className="ml-2 font-medium">{analysisData.volume?.toLocaleString()}</span>
                    </div>
                    <div>
                      <span className="text-gray-500">Change:</span>
                      <span className={`ml-2 font-medium ${analysisData.price_change >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                        {analysisData.price_change >= 0 ? '+' : ''}${analysisData.price_change?.toFixed(2)}
                      </span>
                    </div>
                  </div>
                </div>

                {/* AI Recommendations */}
                <div className="space-y-4">
                  <div className="p-4 border rounded-lg">
                    <div className="flex items-center space-x-2 mb-3">
                      <Brain className="h-5 w-5 text-purple-600" />
                      <h3 className="font-semibold text-gray-900">AI Recommendation</h3>
                    </div>
                    <div className="flex items-center justify-between mb-3">
                      <span className={`px-4 py-2 rounded-full text-sm font-bold border ${getRecommendationColor(analysisData.ai_recommendation)}`}>
                        {analysisData.ai_recommendation}
                      </span>
                      <span className="text-sm text-gray-600">
                        Confidence: {(analysisData.ai_confidence * 100)?.toFixed(1)}%
                      </span>
                    </div>
                    
                    {/* Detailed AI Analysis */}
                    {analysisData.ai_detailed_analysis && analysisData.ai_detailed_analysis.length > 0 && (
                      <div className="mt-4 p-3 bg-gray-50 rounded-lg">
                        <div className="text-sm font-medium text-gray-900 mb-2">Technical Analysis:</div>
                        <div className="space-y-1">
                          {analysisData.ai_detailed_analysis.map((analysis, index) => (
                            <div key={index} className="text-sm text-gray-700">
                              {analysis}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                    
                    {analysisData.ai_reasoning && (
                      <div className="mt-2 text-sm text-gray-600 italic">
                        {analysisData.ai_reasoning}
                      </div>
                    )}
                  </div>

                  <div className="p-4 border rounded-lg">
                    <div className="flex items-center space-x-2 mb-3">
                      <Target className="h-5 w-5 text-orange-600" />
                      <h3 className="font-semibold text-gray-900">Market Sentiment</h3>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className={`px-4 py-2 rounded-full text-sm font-bold border ${getSentimentColor(analysisData.sentiment_analysis)}`}>
                        {analysisData.sentiment_analysis}
                      </span>
                      <span className="text-sm text-gray-600">
                        Score: {analysisData.sentiment_score?.toFixed(2)}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Advanced Charts Section */}
            <div className="bg-white rounded-xl shadow-sm p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-6">Technical Chart Analysis</h3>
              
              {/* Main Candlestick Chart */}
              <div className="mb-4">
                <Chart
                  options={chartOptions}
                  series={[{ name: symbol, data: candlestickData }]}
                  type="candlestick"
                  height={400}
                />
              </div>

              {/* PPO Indicator Chart with Histogram */}
              <div>
                <Chart
                  options={ppoChartOptions}
                  series={ppoChartSeries}
                  type="line"
                  height={200}
                />
              </div>
            </div>

            {/* PPO Components Analysis */}
            <div className="bg-white rounded-xl shadow-sm p-6">
              <div className="flex items-center space-x-2 mb-6">
                <BarChart3 className="h-5 w-5 text-blue-600" />
                <h3 className="text-lg font-semibold text-gray-900">Past 3 Days PPO Components</h3>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {analysisData.ppo_history?.map((item, index) => (
                  <div key={index} className="p-6 bg-gray-50 rounded-lg">
                    <div className="text-center mb-4">
                      <div className="text-sm text-gray-500 mb-2">{item.date}</div>
                    </div>
                    
                    <div className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-blue-600 font-medium">PPO Line:</span>
                        <span className="font-bold text-green-600">{item.ppo?.toFixed(2)}%</span>
                      </div>
                      
                      <div className="flex justify-between items-center">
                        <span className="text-orange-600 font-medium">Signal:</span>
                        <span className="font-bold text-green-600">
                          {(item.ppo * 0.9)?.toFixed(2)}%
                        </span>
                      </div>
                      
                      <div className="flex justify-between items-center">
                        <span className="text-purple-600 font-medium">Histogram:</span>
                        <span className={`font-bold ${item.ppo >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                          {(item.ppo * 0.1)?.toFixed(2)}%
                        </span>
                      </div>
                      
                      <div className="mt-4">
                        <div className="text-xs text-gray-500 mb-2">Histogram Bar</div>
                        <div className="w-full h-2 bg-gray-200 rounded">
                          <div 
                            className={`h-2 rounded ${item.ppo >= 0 ? 'bg-green-500' : 'bg-red-500'}`}
                            style={{ width: `${Math.min(Math.abs(item.ppo) * 10, 100)}%` }}
                          ></div>
                        </div>
                        <div className="text-xs text-center mt-1 font-medium">
                          {item.ppo >= 0 ? 'Bullish' : 'Bearish'}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* PPO Slope Trend Analysis */}
            <div className="bg-gradient-to-r from-green-50 to-blue-50 rounded-xl p-6 border border-green-200">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900">PPO Slope Trend</h3>
                <div className={`text-2xl font-bold ${analysisData.indicators?.ppo_slope_percentage >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {analysisData.indicators?.ppo_slope_percentage >= 0 ? '+' : ''}
                  {analysisData.indicators?.ppo_slope_percentage?.toFixed(2)}%
                </div>
              </div>
              
              <div className="mb-4">
                <div className="text-gray-700 mb-2">
                  <span className="font-semibold">Trend Analysis:</span> 
                  {analysisData.indicators?.ppo_slope_percentage > 5 ? 
                    ' Bullish momentum accelerating - strong upward trend.' :
                    analysisData.indicators?.ppo_slope_percentage < -5 ?
                    ' Bearish momentum accelerating - strong downward trend.' :
                    ' Neutral momentum - watch for potential trend changes.'
                  }
                </div>
                <div className="text-sm text-gray-600">
                  <span className="font-medium">Formula:</span> 
                  {analysisData.indicators?.ppo > 0 ? 
                    ' Positive PPO: (Yesterday - Today) / Yesterday × 100' :
                    ' Negative PPO: (Today - Yesterday) / Yesterday × 100'
                  }
                </div>
              </div>
            </div>

            {/* PPO Analysis Summary */}
            <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-6">
              <div className="flex items-start space-x-3">
                <div className="p-2 bg-yellow-100 rounded-lg">
                  <Brain className="h-5 w-5 text-yellow-600" />
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900 mb-2">PPO Analysis:</h3>
                  <p className="text-gray-700">
                    {analysisData.indicators?.ppo > 0 ?
                      `Positive momentum with PPO at ${analysisData.indicators?.ppo?.toFixed(2)}%. Watch histogram for potential trend changes.` :
                      `Neutral momentum with PPO at ${analysisData.indicators?.ppo?.toFixed(2)}%. Watch histogram for potential trend changes.`
                    }
                  </p>
                </div>
              </div>
            </div>

            {/* Technical Indicators Grid */}
            <div className="bg-white rounded-xl shadow-sm p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-6">Technical Indicators</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
                {[
                  { label: 'PPO', value: analysisData.indicators?.ppo, suffix: '%', color: 'blue' },
                  { label: 'RSI', value: analysisData.indicators?.rsi, suffix: '', color: analysisData.indicators?.rsi > 70 ? 'red' : analysisData.indicators?.rsi < 30 ? 'green' : 'gray' },
                  { label: 'MACD', value: analysisData.indicators?.macd, suffix: '', color: analysisData.indicators?.macd >= 0 ? 'green' : 'red' },
                  { label: 'DMI+', value: analysisData.indicators?.dmi_plus, suffix: '', color: 'green' },
                  { label: 'DMI-', value: analysisData.indicators?.dmi_minus, suffix: '', color: 'red' },
                  { label: 'ADX', value: analysisData.indicators?.adx, suffix: '', color: analysisData.indicators?.adx > 25 ? 'green' : 'gray' },
                  { label: 'SMA 20', value: analysisData.indicators?.sma_20, suffix: '', color: 'gray', prefix: '$' },
                  { label: 'SMA 50', value: analysisData.indicators?.sma_50, suffix: '', color: 'gray', prefix: '$' },
                  { label: 'SMA 200', value: analysisData.indicators?.sma_200, suffix: '', color: 'gray', prefix: '$' }
                ].map((indicator, index) => (
                  <div key={index} className="p-4 border border-gray-200 rounded-lg text-center">
                    <div className="text-xs text-gray-500 mb-1">{indicator.label}</div>
                    <div className={`font-bold text-${indicator.color}-600`}>
                      {indicator.prefix || ''}{indicator.value?.toFixed(indicator.prefix ? 2 : 1)}{indicator.suffix}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default StockAnalysis;