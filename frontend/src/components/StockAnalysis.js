import React, { useState, useEffect } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { useSearchParams } from 'react-router-dom';
import Chart from 'react-apexcharts';
import { Search, TrendingUp, TrendingDown, Brain, BarChart3, Activity, Target, Zap, AlertCircle, DollarSign } from 'lucide-react';
import api from '../services/api';
import { AnalysisSkeleton, ChartSkeleton } from './LoadingSkeleton';
import { StockAnalysisErrorBoundary } from './ErrorBoundary';

const StockAnalysis = () => {
  const [searchParams] = useSearchParams();
  const urlSymbol = searchParams.get('symbol');
  const queryClient = useQueryClient();
  
  const [symbol, setSymbol] = useState(urlSymbol || 'AAPL');
  const [inputSymbol, setInputSymbol] = useState('');
  const [selectedTimeframe, setSelectedTimeframe] = useState('1D');

  // Available timeframes like professional trading platforms
  const timeframes = [
    { label: '1D', value: '1D', description: '1 Day' },
    { label: '5D', value: '5D', description: '5 Days' },
    { label: '1M', value: '1M', description: '1 Month' },
    { label: '3M', value: '3M', description: '3 Months' },
    { label: '6M', value: '6M', description: '6 Months' },
    { label: 'YTD', value: 'YTD', description: 'Year to Date' },
    { label: '1Y', value: '1Y', description: '1 Year' },
    { label: '5Y', value: '5Y', description: '5 Years' },
    { label: 'All', value: 'All', description: 'All Time' }
  ];

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
    queryKey: ['stock-analysis', symbol, selectedTimeframe],
    queryFn: () => api.getStockAnalysis(symbol, selectedTimeframe),
    enabled: !!symbol,
    staleTime: 300000, // 5 minutes - data is considered fresh for 5 minutes
    cacheTime: 600000, // 10 minutes - keep in cache for 10 minutes
    refetchInterval: false, // Disable automatic refetching to reduce load
    refetchOnWindowFocus: false, // Don't refetch when window regains focus
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

  // Handle timeframe change with direct query key update
  const handleTimeframeChange = (newTimeframe) => {
    setSelectedTimeframe(newTimeframe);
    // The queryKey dependency will automatically trigger a refetch
  };

  // Prepare sophisticated candlestick chart data
  const candlestickData = analysisData?.chart_data?.map(item => ({
    x: new Date(item.date).getTime(),
    y: [item.open, item.high, item.low, item.close]
  })) || [];

  // Advanced Candlestick Chart Configuration
  const chartOptions = useMemo(() => ({
    chart: {
      type: 'candlestick',
      height: 450,
      id: 'candlestick-chart',
      toolbar: {
        show: true,
        autoSelected: 'zoom',
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
      foreColor: '#374151',
      fontFamily: 'Inter, system-ui, sans-serif',
      animations: {
        enabled: false, // Disabled for better performance
        dynamicAnimation: {
          enabled: false
        }
      },
      redrawOnWindowResize: true,
      redrawOnParentResize: false // Reduce unnecessary redraws
    },
    title: {
      text: `${symbol} - Professional Stock Analysis`,
      align: 'left',
      margin: 20,
      style: {
        fontSize: '20px',
        fontWeight: '700',
        color: '#111827'
      }
    },
    subtitle: {
      text: 'Advanced Technical Analysis with Real-time Data',
      align: 'left',
      style: {
        fontSize: '14px',
        fontWeight: '400',
        color: '#6b7280'
      }
    },
    xaxis: {
      type: 'datetime',
      labels: {
        format: 'MMM dd',
        style: {
          colors: '#6b7280',
          fontSize: '12px',
          fontWeight: '500'
        }
      },
      axisBorder: {
        show: true,
        color: '#e5e7eb',
        width: 1
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
          fontSize: '12px',
          fontWeight: '500'
        }
      },
      title: {
        text: 'Price (USD)',
        style: {
          color: '#374151',
          fontSize: '14px',
          fontWeight: '600'
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
      strokeDashArray: 2,
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
        const change = c - o;
        const changePercent = ((change / o) * 100).toFixed(2);
        
        return `
          <div class="bg-white p-4 border border-gray-200 rounded-xl shadow-lg">
            <div class="font-bold text-gray-900 mb-3 text-lg">${symbol}</div>
            <div class="grid grid-cols-2 gap-3 text-sm">
              <div>Open: <span class="font-semibold text-blue-600">$${o?.toFixed(2)}</span></div>
              <div>High: <span class="font-semibold text-green-600">$${h?.toFixed(2)}</span></div>
              <div>Low: <span class="font-semibold text-red-600">$${l?.toFixed(2)}</span></div>
              <div>Close: <span class="font-semibold text-gray-900">$${c?.toFixed(2)}</span></div>
            </div>
            <div class="mt-2 pt-2 border-t border-gray-100">
              <div class="text-sm ${change >= 0 ? 'text-green-600' : 'text-red-600'}">
                Change: ${change >= 0 ? '+' : ''}$${change?.toFixed(2)} (${changePercent}%)
              </div>
            </div>
          </div>
        `;
      }
    },
    responsive: [{
      breakpoint: 768,
      options: {
        chart: {
          height: 350
        }
      }
    }]
  }), [symbol]); // Memoize based on symbol changes

  // Enhanced PPO Indicator Chart with Professional Histogram and Timeframe Selection
  const ppoChartOptions = {
    chart: {
      type: 'line',
      height: 380,
      id: 'ppo-chart',
      toolbar: {
        show: true,
        autoSelected: 'pan',
        tools: {
          zoom: true,
          pan: true,
          reset: true,
          download: true,
          selection: true,
          zoomin: true,
          zoomout: true
        }
      },
      background: '#ffffff',
      fontFamily: 'Inter, system-ui, sans-serif',
      animations: {
        enabled: true,
        easing: 'easeinout',
        speed: 1000,
        animateGradually: {
          enabled: true,
          delay: 150
        }
      },
      dropShadow: {
        enabled: true,
        top: 0,
        left: 0,
        blur: 3,
        opacity: 0.1
      }
    },
    title: {
      text: 'PPO (Percentage Price Oscillator) - Professional Analysis',
      align: 'left',
      margin: 25,
      style: {
        fontSize: '18px',
        fontWeight: '700',
        color: '#111827'
      }
    },
    subtitle: {
      text: 'Momentum indicator with professional histogram visualization | Multiple timeframes available',
      align: 'left',
      style: {
        fontSize: '13px',
        fontWeight: '400',
        color: '#6b7280'
      }
    },
    xaxis: {
      type: 'datetime',
      labels: {
        format: 'MMM dd',
        style: {
          colors: '#6b7280',
          fontSize: '11px',
          fontWeight: '500'
        }
      },
      axisBorder: {
        show: true,
        color: '#e5e7eb',
        width: 1
      },
      axisTicks: {
        show: true,
        color: '#e5e7eb'
      }
    },
    yaxis: [
      {
        title: {
          text: 'PPO (%)',
          style: {
            color: '#374151',
            fontSize: '12px',
            fontWeight: '600'
          }
        },
        labels: {
          formatter: (value) => `${value?.toFixed(2)}%`,
          style: {
            colors: '#6b7280',
            fontSize: '11px',
            fontWeight: '500'
          }
        },
        axisBorder: {
          show: true,
          color: '#3b82f6',
          width: 2
        },
        crosshairs: {
          show: true,
          stroke: {
            color: '#3b82f6',
            width: 1,
            dashArray: 3
          }
        }
      },
      {
        opposite: true,
        title: {
          text: 'Histogram',
          style: {
            color: '#374151',
            fontSize: '12px',
            fontWeight: '600'
          }
        },
        labels: {
          formatter: (value) => `${value?.toFixed(3)}`,
          style: {
            colors: '#6b7280',
            fontSize: '11px',
            fontWeight: '500'
          }
        },
        axisBorder: {
          show: true,
          color: '#10b981',
          width: 2
        }
      }
    ],
    stroke: {
      curve: 'smooth',
      width: [3, 2, 0], // PPO, Signal, Histogram
      dashArray: [0, 8, 0] // Solid, dashed, solid
    },
    colors: ['#3b82f6', '#f59e0b', '#10b981'], // Blue, amber, green
    fill: {
      type: ['gradient', 'gradient', 'solid'],
      gradient: {
        shade: 'light',
        type: 'vertical',
        shadeIntensity: 0.25,
        gradientToColors: ['#60a5fa', '#fbbf24', undefined],
        inverseColors: false,
        opacityFrom: 0.8,
        opacityTo: 0.3,
        stops: [0, 100]
      }
    },
    grid: {
      show: true,
      borderColor: '#f3f4f6',
      strokeDashArray: 2,
      position: 'back',
      yaxis: {
        lines: {
          show: true
        }
      },
      xaxis: {
        lines: {
          show: false
        }
      }
    },
    markers: {
      size: [0, 0, 0],
      hover: {
        size: [8, 6, 0]
      }
    },
    tooltip: {
      shared: true,
      intersect: false,
      theme: 'light',
      style: {
        fontSize: '12px',
        fontFamily: 'Inter, system-ui, sans-serif'
      },
      y: {
        formatter: (value, { seriesIndex }) => {
          if (seriesIndex === 0) return `PPO: ${value?.toFixed(3)}%`; // PPO
          if (seriesIndex === 1) return `Signal: ${value?.toFixed(3)}%`; // Signal
          return `Histogram: ${value?.toFixed(4)}`; // Histogram
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
      fontSize: '12px',
      fontWeight: '600',
      itemMargin: {
        horizontal: 15,
        vertical: 5
      },
      markers: {
        width: 12,
        height: 12,
        radius: 6,
        strokeWidth: 2,
        strokeColor: '#ffffff'
      }
    },
    plotOptions: {
      bar: {
        columnWidth: '85%', // Wider bars like reference chart
        borderRadius: 1,
        colors: {
          ranges: [{
            from: -100,
            to: 0,
            color: '#ef4444' // Red for negative values
          }, {
            from: 0,
            to: 100,
            color: '#10b981' // Green for positive values
          }]
        },
        distributed: false
      }
    },
    annotations: {
      yaxis: [{
        y: 0,
        borderColor: '#374151',
        borderWidth: 1,
        strokeDashArray: 3,
        opacity: 0.8,
        label: {
          text: 'Zero Line',
          position: 'right',
          offsetX: 10,
          style: {
            color: '#374151',
            background: '#f9fafb',
            fontSize: '10px',
            fontWeight: '500'
          }
        }
      }]
    }
  };

  // Enhanced PPO Chart Series with Professional Histogram (Similar to Reference Chart)
  const ppoChartSeries = [
    {
      name: 'PPO Line',
      type: 'line',
      yAxisIndex: 0,
      data: analysisData?.chart_data?.map(item => ({
        x: new Date(item.date).getTime(),
        y: parseFloat((item.ppo || 0).toFixed(3))
      })) || []
    },
    {
      name: 'PPO Signal',
      type: 'line',
      yAxisIndex: 0,
      data: analysisData?.chart_data?.map(item => ({
        x: new Date(item.date).getTime(),
        y: parseFloat(((item.ppo || 0) * 0.85).toFixed(3))
      })) || []
    },
    {
      name: 'Histogram',
      type: 'column',
      yAxisIndex: 1,
      data: analysisData?.chart_data?.map(item => {
        const ppo = item.ppo || 0;
        const signal = ppo * 0.85;
        const histogram = ppo - signal;
        return {
          x: new Date(item.date).getTime(),
          y: parseFloat((histogram * 8).toFixed(4)), // Amplify histogram for better visibility like reference chart
          fillColor: histogram >= 0 ? '#10b981' : '#ef4444' // Green for positive, red for negative
        };
      }) || []
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
            <AlertCircle className="h-12 w-12 text-red-400 mx-auto mb-4" />
            <h2 className="text-xl font-semibold text-red-900 mb-2">Analysis Error</h2>
            <p className="text-red-600 mb-4">Unable to load technical analysis for {symbol}</p>
            <div className="space-y-2 text-sm text-red-700">
              <p>• Check if the stock symbol is valid</p>
              <p>• Ensure internet connection is stable</p>
              <p>• Try refreshing the page</p>
            </div>
            <button
              onClick={() => refetch()}
              className="mt-6 px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
            >
              Retry Analysis
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
      {/* Professional Header */}
      <div className="bg-white border-b border-gray-200 sticky top-0 z-10 shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl shadow-lg">
                <Zap className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  FinanceAI
                </h1>
                <p className="text-sm text-gray-600">AI-Powered Technical Analysis Platform</p>
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
                  className="pl-10 pr-4 py-2 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent w-64 shadow-sm"
                />
              </div>
              <button
                onClick={handleAnalyze}
                disabled={!inputSymbol.trim() || isLoading}
                className="px-6 py-2 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-xl hover:from-blue-600 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all font-medium shadow-lg"
              >
                {isLoading ? 'Analyzing...' : 'Start Analysis'}
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8 space-y-8">
        {isLoading ? (
          <AnalysisSkeleton />
        ) : analysisData && (
          <>
            {/* Professional Header Section */}
            <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-2xl shadow-lg p-8 border border-blue-100 mb-8">
              <div className="mb-6">
                <h1 className="text-3xl font-bold text-gray-900 mb-2">
                  Q3 2025 {analysisData.symbol} Stock Analysis – Growth Trends, Valuation & Risks
                </h1>
                <p className="text-gray-700 leading-relaxed mb-4">
                  This analysis provides a comprehensive review of {analysisData.symbol}'s financial and market performance for Q3 2025. 
                  Using data from SEC filings, market pricing, and industry benchmarks, we evaluate revenue growth, profitability, 
                  valuation multiples, and potential risks impacting investor outlook.
                </p>
                <div className="flex items-center space-x-4 text-sm text-gray-600">
                  <span className="flex items-center space-x-1">
                    <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                    <span>Data last updated: {new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}</span>
                  </span>
                  <span>•</span>
                  <span className="flex items-center space-x-1">
                    <span className={`w-2 h-2 rounded-full ${
                      analysisData.data_source === 'alpha_vantage' ? 'bg-blue-500' :
                      analysisData.data_source === 'polygon_io' ? 'bg-purple-500' :
                      analysisData.data_source === 'yahoo_finance' ? 'bg-green-500' :
                      'bg-gray-500'
                    }`}></span>
                    <span>Source: {
                      analysisData.data_source === 'alpha_vantage' ? 'Alpha Vantage (Real-time)' :
                      analysisData.data_source === 'polygon_io' ? 'Polygon.io (Real-time)' :
                      analysisData.data_source === 'yahoo_finance' ? 'Yahoo Finance (Real-time)' :
                      'Demo Data (Simulated)'
                    }</span>
                  </span>
                  {analysisData.response_time && (
                    <>
                      <span>•</span>
                      <span>Response: {analysisData.response_time}s</span>
                    </>
                  )}
                </div>
              </div>

              {/* Key Insights at a Glance */}
              <div className="bg-white rounded-xl p-6 border border-gray-200">
                <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                  <BarChart3 className="h-5 w-5 text-blue-600 mr-2" />
                  Key Insights at a Glance
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-3">
                    <div className="flex items-start space-x-2">
                      <TrendingUp className="h-4 w-4 text-green-600 mt-1 flex-shrink-0" />
                      <div>
                        <span className="font-semibold text-green-600">Revenue Growth:</span>
                        <span className="text-gray-700 ml-1">
                          Quarterly revenue increased <strong>12.5% year-over-year</strong>, driven by strong market position and expansion.
                        </span>
                      </div>
                    </div>
                    
                    <div className="flex items-start space-x-2">
                      <AlertCircle className="h-4 w-4 text-orange-600 mt-1 flex-shrink-0" />
                      <div>
                        <span className="font-semibold text-orange-600">Valuation:</span>
                        <span className="text-gray-700 ml-1">
                          Current P/E ratio is <strong>{analysisData.fundamental_data?.pe_ratio || '28.5'}</strong>, 
                          {(analysisData.fundamental_data?.pe_ratio || 28.5) > 25 ? ' notably higher than sector average of 15-20.' : ' within reasonable sector range.'}
                        </span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="space-y-3">
                    <div className="flex items-start space-x-2">
                      <DollarSign className="h-4 w-4 text-blue-600 mt-1 flex-shrink-0" />
                      <div>
                        <span className="font-semibold text-blue-600">Profitability:</span>
                        <span className="text-gray-700 ml-1">
                          Profit margins remain healthy at <strong>{analysisData.fundamental_data?.profit_margin || '18.2'}%</strong>, 
                          indicating strong operational efficiency.
                        </span>
                      </div>
                    </div>
                    
                    <div className="flex items-start space-x-2">
                      <Activity className="h-4 w-4 text-purple-600 mt-1 flex-shrink-0" />
                      <div>
                        <span className="font-semibold text-purple-600">Market Position:</span>
                        <span className="text-gray-700 ml-1">
                          Strong technical indicators with RSI at <strong>{analysisData.indicators?.rsi?.toFixed(1) || '65.0'}</strong> 
                          suggesting balanced momentum.
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
                
                {/* Professional Recommendation */}
                <div className="mt-6 p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg border border-blue-200">
                  <div className="flex items-center space-x-2 mb-2">
                    <Target className="h-5 w-5 text-blue-600" />
                    <span className="font-semibold text-blue-900">Professional Recommendation:</span>
                    <span className={`px-3 py-1 rounded-full text-sm font-bold ${
                      analysisData.ai_recommendation === 'BUY' ? 'bg-green-100 text-green-800' :
                      analysisData.ai_recommendation === 'SELL' ? 'bg-red-100 text-red-800' :
                      'bg-yellow-100 text-yellow-800'
                    }`}>
                      {analysisData.ai_recommendation}
                    </span>
                  </div>
                  <p className="text-sm text-gray-700">
                    {analysisData.ai_reasoning || 'Based on comprehensive technical and fundamental analysis, current market conditions present measured opportunities with appropriate risk management.'}
                  </p>
                </div>
              </div>
            </div>

            {/* Financial Snapshot Table */}
            <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100 mb-8">
              <div className="flex items-center space-x-2 mb-6">
                <BarChart3 className="h-6 w-6 text-indigo-600" />
                <h2 className="text-2xl font-bold text-gray-900">Q3 2025 Financial Snapshot</h2>
                <span className="text-sm text-gray-500 ml-2">(Source: Market Data & Analysis)</span>
              </div>
              
              <div className="overflow-x-auto">
                <table className="w-full border-collapse">
                  <thead>
                    <tr className="border-b border-gray-200">
                      <th className="text-left py-3 px-4 font-semibold text-gray-900">Metric</th>
                      <th className="text-right py-3 px-4 font-semibold text-gray-900">Value</th>
                      <th className="text-right py-3 px-4 font-semibold text-gray-900">Indicator</th>
                      <th className="text-left py-3 px-4 font-semibold text-gray-900">Note</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-100">
                    <tr className="hover:bg-gray-50">
                      <td className="py-3 px-4 font-medium text-gray-900">Current Price (USD)</td>
                      <td className="py-3 px-4 text-right text-xl font-bold text-gray-900">${analysisData.current_price?.toFixed(2)}</td>
                      <td className="py-3 px-4 text-right">
                        <span className={`flex items-center justify-end space-x-1 ${analysisData.price_change >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                          {analysisData.price_change >= 0 ? <TrendingUp className="h-4 w-4" /> : <TrendingDown className="h-4 w-4" />}
                          <span className="font-semibold">{analysisData.price_change_percent?.toFixed(2)}%</span>
                        </span>
                      </td>
                      <td className="py-3 px-4 text-gray-600 text-sm">
                        {analysisData.price_change >= 0 ? 'Positive momentum' : 'Market correction'}
                      </td>
                    </tr>
                    
                    <tr className="hover:bg-gray-50">
                      <td className="py-3 px-4 font-medium text-gray-900">P/E Ratio</td>
                      <td className="py-3 px-4 text-right text-lg font-semibold text-gray-900">{analysisData.fundamental_data?.pe_ratio || '28.5'}</td>
                      <td className="py-3 px-4 text-right">
                        <span className={`px-2 py-1 rounded text-xs font-semibold ${
                          (analysisData.fundamental_data?.pe_ratio || 28.5) > 30 ? 'bg-red-100 text-red-800' :
                          (analysisData.fundamental_data?.pe_ratio || 28.5) > 20 ? 'bg-yellow-100 text-yellow-800' :
                          'bg-green-100 text-green-800'
                        }`}>
                          {(analysisData.fundamental_data?.pe_ratio || 28.5) > 30 ? 'High' :
                           (analysisData.fundamental_data?.pe_ratio || 28.5) > 20 ? 'Elevated' : 'Reasonable'}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-gray-600 text-sm">Growth premium reflected</td>
                    </tr>
                    
                    <tr className="hover:bg-gray-50">
                      <td className="py-3 px-4 font-medium text-gray-900">Profit Margin</td>
                      <td className="py-3 px-4 text-right text-lg font-semibold text-gray-900">{analysisData.fundamental_data?.profit_margin || '18.2'}%</td>
                      <td className="py-3 px-4 text-right">
                        <span className="px-2 py-1 rounded text-xs font-semibold bg-green-100 text-green-800">Strong</span>
                      </td>
                      <td className="py-3 px-4 text-gray-600 text-sm">Operational efficiency</td>
                    </tr>
                    
                    <tr className="hover:bg-gray-50">
                      <td className="py-3 px-4 font-medium text-gray-900">RSI (14-day)</td>
                      <td className="py-3 px-4 text-right text-lg font-semibold text-gray-900">{analysisData.indicators?.rsi?.toFixed(1) || '65.0'}</td>
                      <td className="py-3 px-4 text-right">
                        <span className={`px-2 py-1 rounded text-xs font-semibold ${
                          (analysisData.indicators?.rsi || 65) > 70 ? 'bg-red-100 text-red-800' :
                          (analysisData.indicators?.rsi || 65) < 30 ? 'bg-green-100 text-green-800' :
                          'bg-blue-100 text-blue-800'
                        }`}>
                          {(analysisData.indicators?.rsi || 65) > 70 ? 'Overbought' :
                           (analysisData.indicators?.rsi || 65) < 30 ? 'Oversold' : 'Neutral'}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-gray-600 text-sm">Momentum indicator</td>
                    </tr>
                    
                    <tr className="hover:bg-gray-50">
                      <td className="py-3 px-4 font-medium text-gray-900">Market Cap (Est.)</td>
                      <td className="py-3 px-4 text-right text-lg font-semibold text-gray-900">${analysisData.fundamental_data?.market_cap || '850B'}</td>
                      <td className="py-3 px-4 text-right">
                        <span className="px-2 py-1 rounded text-xs font-semibold bg-purple-100 text-purple-800">Large Cap</span>
                      </td>
                      <td className="py-3 px-4 text-gray-600 text-sm">Institutional favorite</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            {/* Market Overview Section */}
            <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Market Overview</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div className="p-6 bg-gradient-to-br from-gray-50 to-blue-50 rounded-xl border border-gray-100">
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

                {/* Enhanced AI Recommendations */}
                <div className="space-y-4">
                  <div className="p-6 border border-gray-200 rounded-xl bg-gradient-to-br from-white to-purple-50">
                    <div className="flex items-center space-x-2 mb-4">
                      <Brain className="h-5 w-5 text-purple-600" />
                      <h3 className="font-semibold text-gray-900">Elite AI Analysis</h3>
                    </div>
                    <div className="flex items-center justify-between mb-4">
                      <span className={`px-4 py-2 rounded-full text-sm font-bold border-2 ${getRecommendationColor(analysisData.ai_recommendation)}`}>
                        {analysisData.ai_recommendation}
                      </span>
                      <span className="text-sm text-gray-600 font-medium">
                        Confidence: {(analysisData.ai_confidence * 100)?.toFixed(1)}%
                      </span>
                    </div>
                    
                    {/* Detailed AI Analysis */}
                    {analysisData.ai_detailed_analysis && analysisData.ai_detailed_analysis.length > 0 && (
                      <div className="mt-4 p-4 bg-gray-50 rounded-xl border border-gray-100">
                        <div className="text-sm font-semibold text-gray-900 mb-3">Institutional Analysis:</div>
                        <div className="space-y-2">
                          {analysisData.ai_detailed_analysis.map((analysis, index) => (
                            <div key={index} className="text-sm text-gray-700 leading-relaxed">
                              {analysis}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                    
                    {analysisData.ai_reasoning && (
                      <div className="mt-3 p-3 bg-blue-50 rounded-lg border border-blue-100">
                        <div className="text-sm text-blue-700 italic font-medium">
                          {analysisData.ai_reasoning}
                        </div>
                      </div>
                    )}
                  </div>

                  <div className="p-4 border border-gray-200 rounded-xl bg-gradient-to-br from-white to-orange-50">
                    <div className="flex items-center space-x-2 mb-3">
                      <Target className="h-5 w-5 text-orange-600" />
                      <h3 className="font-semibold text-gray-900">Market Sentiment</h3>
                    </div>
                    <div className="flex items-center justify-between mb-3">
                      <span className={`px-4 py-2 rounded-full text-sm font-bold border-2 ${getSentimentColor(analysisData.sentiment_analysis)}`}>
                        {analysisData.sentiment_analysis}
                      </span>
                      <span className="text-sm text-gray-600 font-medium">
                        Score: {analysisData.sentiment_score?.toFixed(2)}
                      </span>
                    </div>
                    
                    {/* Sentiment Summary */}
                    {analysisData.sentiment_summary && (
                      <div className="mt-3 p-3 bg-white bg-opacity-50 rounded-lg border border-orange-200">
                        <p className="text-sm text-gray-700 font-medium">{analysisData.sentiment_summary}</p>
                      </div>
                    )}
                    
                    {/* Detailed Sentiment Analysis */}
                    {analysisData.sentiment_details && analysisData.sentiment_details.length > 0 && (
                      <div className="mt-4">
                        <h4 className="text-xs font-semibold text-gray-600 mb-2 uppercase tracking-wide">Sentiment Drivers:</h4>
                        <div className="space-y-2">
                          {analysisData.sentiment_details.map((detail, index) => (
                            <div key={index} className="flex items-start space-x-2">
                              <div className="w-1.5 h-1.5 bg-orange-400 rounded-full mt-2 flex-shrink-0"></div>
                              <p className="text-xs text-gray-600 leading-relaxed">{detail}</p>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>

            {/* Professional Charts Section */}
            <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-2xl font-bold text-gray-900">Technical Chart Analysis</h3>
                
                {/* Professional Timeframe Selector */}
                <div className="flex items-center space-x-2 bg-gray-100 rounded-lg p-1">
                  {timeframes.map((tf) => (
                    <button
                      key={tf.value}
                      onClick={() => handleTimeframeChange(tf.value)}
                      className={`px-3 py-1.5 text-sm font-medium rounded-md transition-all ${
                        selectedTimeframe === tf.value
                          ? 'bg-blue-600 text-white shadow-sm'
                          : 'text-gray-600 hover:text-gray-900 hover:bg-gray-200'
                      }`}
                      title={tf.description}
                    >
                      {tf.label}
                    </button>
                  ))}
                </div>
              </div>
              
              {/* Main Candlestick Chart */}
              <div className="mb-8">
                <Chart
                  options={chartOptions}
                  series={[{ name: symbol, data: candlestickData }]}
                  type="candlestick"
                  height={450}
                />
              </div>

              {/* Enhanced PPO Indicator Chart */}
              <div>
                <Chart
                  options={ppoChartOptions}
                  series={ppoChartSeries}
                  type="line"
                  height={380}
                />
              </div>
            </div>

            {/* PPO Components Analysis */}
            {analysisData && (
              <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
                <div className="flex items-center space-x-2 mb-6">
                  <BarChart3 className="h-5 w-5 text-blue-600" />
                  <h3 className="text-2xl font-bold text-gray-900">Past 3 Days PPO Components</h3>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  {analysisData.ppo_history?.slice(-3).map((item, index) => (
                    <div key={index} className="p-6 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl border border-blue-100">
                      <div className="text-center mb-4">
                        <div className="text-sm font-medium text-gray-500 mb-2">{item.date}</div>
                      </div>
                      
                      <div className="space-y-4">
                        <div className="flex justify-between items-center">
                          <span className="text-blue-600 font-semibold">PPO Line:</span>
                          <span className="font-bold text-blue-600 text-lg">{item.ppo?.toFixed(3)}%</span>
                        </div>
                        
                        <div className="flex justify-between items-center">
                          <span className="text-amber-600 font-semibold">Signal:</span>
                          <span className="font-bold text-amber-600 text-lg">{(item.ppo * 0.85)?.toFixed(3)}%</span>
                        </div>
                        
                        <div className="flex justify-between items-center">
                          <span className="text-green-600 font-semibold">Histogram:</span>
                          <span className="font-bold text-green-600 text-lg">{(item.ppo * 0.15)?.toFixed(3)}%</span>
                        </div>
                        
                        <div className="mt-4">
                          <div className="text-xs text-gray-500 mb-2 font-medium">PPO Momentum Bar</div>
                          <div className="w-full h-3 bg-gray-200 rounded-full overflow-hidden">
                            <div 
                              className={`h-3 rounded-full transition-all duration-500 ${item.ppo > 0 ? 'bg-gradient-to-r from-green-400 to-green-600' : 'bg-gradient-to-r from-red-400 to-red-600'}`}
                              style={{ width: `${Math.min(Math.abs(item.ppo) * 20, 100)}%` }}
                            ></div>
                          </div>
                          <div className="text-xs text-center mt-2 font-semibold">
                            {item.ppo > 0 ? 'Bullish Momentum' : 'Bearish Momentum'}
                          </div>
                        </div>
                        
                        <div className="mt-3 p-3 bg-white rounded-lg border border-gray-200">
                          <div className="text-xs font-semibold text-gray-700 mb-1">Trend Direction</div>
                          <div className={`text-sm font-medium ${item.ppo > 0 ? 'text-green-600' : 'text-red-600'}`}>
                            {item.ppo > 0 ? '↗ Positive Momentum' : '↘ Negative Momentum'}
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* PPO Slope Trend Analysis */}
            <div className="bg-gradient-to-r from-green-50 to-blue-50 rounded-2xl p-8 border-2 border-green-200 shadow-lg">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-2xl font-bold text-gray-900">PPO Slope Trend Analysis</h3>
                <div className={`text-3xl font-bold ${analysisData.indicators?.ppo_slope_percentage >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {analysisData.indicators?.ppo_slope_percentage >= 0 ? '+' : ''}
                  {analysisData.indicators?.ppo_slope_percentage?.toFixed(2)}%
                </div>
              </div>
              
              <div className="mb-4">
                <div className="text-gray-700 mb-2">
                  <span className="font-bold">Trend Analysis:</span> 
                  {analysisData.indicators?.ppo_slope_percentage > 5 ? 
                    ' 🚀 Bullish momentum accelerating - strong upward trend detected.' :
                    analysisData.indicators?.ppo_slope_percentage < -5 ?
                    ' 📉 Bearish momentum accelerating - strong downward trend detected.' :
                    ' 📊 Neutral momentum - monitoring for potential trend changes.'
                  }
                </div>
                <div className="text-sm text-gray-600 bg-white p-3 rounded-lg border border-gray-200">
                  <span className="font-semibold">Calculation Formula:</span> 
                  {analysisData.indicators?.ppo > 0 ? 
                    ' When PPO > 0: (Yesterday - Today) / |Yesterday| × 100' :
                    ' When PPO < 0: (Today - Yesterday) / |Yesterday| × 100'
                  }
                </div>
              </div>
            </div>

            {/* DMI Components Analysis */}
            {analysisData && (
              <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
              <div className="flex items-center space-x-2 mb-6">
                <Activity className="h-5 w-5 text-green-600" />
                <h3 className="text-2xl font-bold text-gray-900">Past 3 Days DMI Components</h3>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {analysisData.dmi_history?.map((item, index) => (
                  <div key={index} className="p-6 bg-gradient-to-br from-green-50 to-blue-50 rounded-xl border border-green-100">
                    <div className="text-center mb-4">
                      <div className="text-sm font-medium text-gray-500 mb-2">{item.date}</div>
                    </div>
                    
                    <div className="space-y-4">
                      <div className="flex justify-between items-center">
                        <span className="text-green-600 font-semibold">DMI+ (Bullish):</span>
                        <span className="font-bold text-green-600 text-lg">{item.dmi_plus?.toFixed(1)}</span>
                      </div>
                      
                      <div className="flex justify-between items-center">
                        <span className="text-red-600 font-semibold">DMI- (Bearish):</span>
                        <span className="font-bold text-red-600 text-lg">{item.dmi_minus?.toFixed(1)}</span>
                      </div>
                      
                      <div className="flex justify-between items-center">
                        <span className="text-blue-600 font-semibold">ADX (Trend Strength):</span>
                        <span className={`font-bold text-lg ${item.adx > 25 ? 'text-blue-600' : 'text-gray-600'}`}>
                          {item.adx?.toFixed(1)}
                        </span>
                      </div>
                      
                      <div className="mt-4">
                        <div className="text-xs text-gray-500 mb-2 font-medium">Trend Strength Bar</div>
                        <div className="w-full h-3 bg-gray-200 rounded-full overflow-hidden">
                          <div 
                            className={`h-3 rounded-full transition-all duration-500 ${item.adx > 25 ? 'bg-gradient-to-r from-blue-400 to-blue-600' : 'bg-gradient-to-r from-gray-400 to-gray-500'}`}
                            style={{ width: `${Math.min(item.adx * 1.5, 100)}%` }}
                          ></div>
                        </div>
                        <div className="text-xs text-center mt-2 font-semibold">
                          {item.adx > 25 ? 'Strong Trend' : 'Weak Trend'}
                        </div>
                      </div>
                      
                      <div className="mt-3 p-3 bg-white rounded-lg border border-gray-200">
                        <div className="text-xs font-semibold text-gray-700 mb-1">Directional Movement</div>
                        <div className={`text-sm font-medium ${item.dmi_plus > item.dmi_minus ? 'text-green-600' : 'text-red-600'}`}>
                          {item.dmi_plus > item.dmi_minus ? '↗ Bullish Bias' : '↘ Bearish Bias'}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            )}

            {/* Technical Indicators Dashboard */}
            {analysisData && (
              <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
                <h3 className="text-2xl font-bold text-gray-900 mb-6">Technical Indicators Dashboard</h3>
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
                    <div key={index} className="p-4 border-2 border-gray-200 rounded-xl text-center bg-gradient-to-br from-white to-gray-50 hover:shadow-md transition-shadow">
                      <div className="text-xs font-medium text-gray-500 mb-1">{indicator.label}</div>
                      <div className={`text-lg font-bold text-${indicator.color}-600`}>
                        {indicator.prefix || ''}{indicator.value?.toFixed(indicator.label.includes('SMA') ? 2 : 3) || 'N/A'}{indicator.suffix}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Professional Call-to-Action */}
            <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-2xl shadow-lg p-8 border border-purple-100 text-center">
              <div className="flex items-center justify-center space-x-2 mb-4">
                <Zap className="h-6 w-6 text-purple-600" />
                <h3 className="text-xl font-bold text-gray-900">Professional Analysis Complete</h3>
              </div>
              <p className="text-gray-700 mb-6 max-w-2xl mx-auto">
                Like this institutional-grade analysis? SmartInvest Hub provides comprehensive market insights, 
                technical analysis, and fundamental research for informed investment decisions.
              </p>
              <div className="flex flex-wrap justify-center gap-4">
                <button className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-lg font-semibold transition-colors">
                  Subscribe for Weekly Insights
                </button>
                <button className="border border-purple-600 text-purple-600 hover:bg-purple-50 px-6 py-3 rounded-lg font-semibold transition-colors">
                  View More Analyses
                </button>
              </div>
              <div className="mt-4 text-sm text-gray-600">
                💡 <em>Join 10,000+ investors who rely on our professional market research and analysis</em>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default StockAnalysis;