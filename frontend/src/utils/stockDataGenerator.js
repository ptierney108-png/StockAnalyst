// Enhanced Stock Data Generator with Realistic Market Data
// Implements sophisticated data simulation for stock screener

import { TechnicalAnalysisEngine } from './technicalAnalysis';

export class StockDataGenerator {
  
  static stockDatabase = [
    // Technology Sector
    { symbol: 'AAPL', name: 'Apple Inc.', sector: 'Technology', industry: 'Consumer Electronics', basePrice: 175, volatility: 0.025, optionable: true },
    { symbol: 'MSFT', name: 'Microsoft Corporation', sector: 'Technology', industry: 'Software', basePrice: 380, volatility: 0.022, optionable: true },
    { symbol: 'GOOGL', name: 'Alphabet Inc.', sector: 'Technology', industry: 'Internet Services', basePrice: 138, volatility: 0.028, optionable: true },
    { symbol: 'NVDA', name: 'NVIDIA Corporation', sector: 'Technology', industry: 'Semiconductors', basePrice: 450, volatility: 0.035, optionable: true },
    { symbol: 'TSLA', name: 'Tesla, Inc.', sector: 'Technology', industry: 'Electric Vehicles', basePrice: 250, volatility: 0.045, optionable: true },
    { symbol: 'META', name: 'Meta Platforms, Inc.', sector: 'Technology', industry: 'Social Media', basePrice: 298, volatility: 0.032, optionable: true },
    { symbol: 'NFLX', name: 'Netflix, Inc.', sector: 'Technology', industry: 'Streaming Services', basePrice: 425, volatility: 0.030, optionable: true },
    { symbol: 'CRM', name: 'Salesforce, Inc.', sector: 'Technology', industry: 'Cloud Software', basePrice: 220, volatility: 0.028, optionable: true },
    { symbol: 'ADBE', name: 'Adobe Inc.', sector: 'Technology', industry: 'Software', basePrice: 485, volatility: 0.026, optionable: true },
    { symbol: 'INTC', name: 'Intel Corporation', sector: 'Technology', industry: 'Semiconductors', basePrice: 35, volatility: 0.024, optionable: true },

    // Healthcare Sector
    { symbol: 'JNJ', name: 'Johnson & Johnson', sector: 'Healthcare', industry: 'Pharmaceuticals', basePrice: 165, volatility: 0.018, optionable: true },
    { symbol: 'UNH', name: 'UnitedHealth Group Inc.', sector: 'Healthcare', industry: 'Health Insurance', basePrice: 520, volatility: 0.020, optionable: true },
    { symbol: 'PFE', name: 'Pfizer Inc.', sector: 'Healthcare', industry: 'Pharmaceuticals', basePrice: 28, volatility: 0.022, optionable: true },
    { symbol: 'ABBV', name: 'AbbVie Inc.', sector: 'Healthcare', industry: 'Biotechnology', basePrice: 155, volatility: 0.019, optionable: true },
    { symbol: 'TMO', name: 'Thermo Fisher Scientific Inc.', sector: 'Healthcare', industry: 'Life Sciences', basePrice: 580, volatility: 0.021, optionable: true },

    // Finance Sector
    { symbol: 'JPM', name: 'JPMorgan Chase & Co.', sector: 'Finance', industry: 'Banking', basePrice: 145, volatility: 0.025, optionable: true },
    { symbol: 'BAC', name: 'Bank of America Corporation', sector: 'Finance', industry: 'Banking', basePrice: 32, volatility: 0.027, optionable: true },
    { symbol: 'WFC', name: 'Wells Fargo & Company', sector: 'Finance', industry: 'Banking', basePrice: 42, volatility: 0.026, optionable: true },
    { symbol: 'GS', name: 'The Goldman Sachs Group, Inc.', sector: 'Finance', industry: 'Investment Banking', basePrice: 385, volatility: 0.029, optionable: true },
    { symbol: 'MS', name: 'Morgan Stanley', sector: 'Finance', industry: 'Investment Banking', basePrice: 88, volatility: 0.028, optionable: true },

    // Energy Sector
    { symbol: 'XOM', name: 'Exxon Mobil Corporation', sector: 'Energy', industry: 'Oil & Gas', basePrice: 115, volatility: 0.032, optionable: true },
    { symbol: 'CVX', name: 'Chevron Corporation', sector: 'Energy', industry: 'Oil & Gas', basePrice: 158, volatility: 0.030, optionable: true },
    { symbol: 'COP', name: 'ConocoPhillips', sector: 'Energy', industry: 'Oil & Gas', basePrice: 108, volatility: 0.034, optionable: true },

    // Consumer Goods
    { symbol: 'PG', name: 'The Procter & Gamble Company', sector: 'Consumer Goods', industry: 'Consumer Products', basePrice: 155, volatility: 0.016, optionable: true },
    { symbol: 'KO', name: 'The Coca-Cola Company', sector: 'Consumer Goods', industry: 'Beverages', basePrice: 58, volatility: 0.015, optionable: true },
    { symbol: 'PEP', name: 'PepsiCo, Inc.', sector: 'Consumer Goods', industry: 'Beverages', basePrice: 168, volatility: 0.017, optionable: true },
    { symbol: 'WMT', name: 'Walmart Inc.', sector: 'Consumer Goods', industry: 'Retail', basePrice: 158, volatility: 0.019, optionable: true },
    { symbol: 'HD', name: 'The Home Depot, Inc.', sector: 'Consumer Goods', industry: 'Home Improvement', basePrice: 345, volatility: 0.021, optionable: true },

    // Small/Mid Cap Stocks
    { symbol: 'ROKU', name: 'Roku, Inc.', sector: 'Technology', industry: 'Streaming Devices', basePrice: 45, volatility: 0.055, optionable: true },
    { symbol: 'ZM', name: 'Zoom Video Communications, Inc.', sector: 'Technology', industry: 'Video Conferencing', basePrice: 68, volatility: 0.042, optionable: true },
    { symbol: 'SNAP', name: 'Snap Inc.', sector: 'Technology', industry: 'Social Media', basePrice: 12, volatility: 0.048, optionable: true },
    { symbol: 'PLTR', name: 'Palantir Technologies Inc.', sector: 'Technology', industry: 'Data Analytics', basePrice: 16, volatility: 0.052, optionable: true },
    { symbol: 'RBLX', name: 'Roblox Corporation', sector: 'Technology', industry: 'Gaming', basePrice: 38, volatility: 0.047, optionable: true }
  ];

  /**
   * Generate comprehensive stock data with technical analysis
   * @param {Object} filterCriteria - Filtering criteria from user
   * @returns {Array} Array of stock objects with technical data
   */
  static generateFilteredStocks(filterCriteria) {
    const { priceFilter, dmiFilter, ppoSlopeFilter, ppoHookFilter, sectorFilter, optionableFilter, earningsFilter } = filterCriteria;
    
    let stocks = this.stockDatabase.map(stock => {
      // Generate price data for technical analysis
      const priceData = TechnicalAnalysisEngine.generateMockPriceData(60, stock.basePrice, stock.volatility);
      const prices = priceData.map(d => d.close);
      
      try {
        // Calculate technical indicators
        const dmiResult = TechnicalAnalysisEngine.calculateDMI(priceData);
        const ppoValues = TechnicalAnalysisEngine.calculatePPO(prices);
        const ppoSlope = TechnicalAnalysisEngine.calculatePPOSlope(ppoValues);
        
        // Generate return data
        const currentPrice = prices[prices.length - 1];
        const returns = this.calculateReturns(prices);
        
        // Generate volume data with realistic patterns
        const volumeData = this.generateVolumeData(stock.symbol);
        
        // Generate options data
        const optionsData = this.generateOptionsData(currentPrice, stock.volatility);
        
        // Generate earnings data
        const earningsData = this.generateEarningsData();

        return {
          symbol: stock.symbol,
          name: stock.name,
          sector: stock.sector,
          industry: stock.industry,
          price: currentPrice,
          priceData: priceData,
          
          // Technical Indicators
          dmi: dmiResult.currentDMI,
          diPlus: dmiResult.diPlus,
          diMinus: dmiResult.diMinus,
          adx: dmiResult.adx,
          ppoValues: ppoValues.slice(-3), // Last 3 days
          ppoSlope: ppoSlope,
          
          // Returns
          return1d: returns.return1d,
          return5d: returns.return5d,
          return2w: returns.return2w,
          return1m: returns.return1m,
          return1y: returns.return1y,
          
          // Volume
          volume: volumeData.today,
          volume3m: volumeData.threeMonth,
          volumeYear: volumeData.year,
          
          // Options
          optionable: stock.optionable,
          callBid: optionsData.callBid,
          callAsk: optionsData.callAsk,
          putBid: optionsData.putBid,
          putAsk: optionsData.putAsk,
          
          // Earnings
          lastEarnings: earningsData.lastEarnings,
          nextEarnings: earningsData.nextEarnings,
          daysToEarnings: earningsData.daysToEarnings
        };
      } catch (error) {
        console.warn(`Error calculating technical indicators for ${stock.symbol}:`, error);
        return null;
      }
    }).filter(stock => stock !== null);

    // Apply filters
    stocks = this.applyPriceFilter(stocks, priceFilter);
    stocks = this.applyDMIFilter(stocks, dmiFilter);
    stocks = this.applyPPOSlopeFilter(stocks, ppoSlopeFilter);
    stocks = this.applyPPOHookFilter(stocks, ppoHookFilter); // NEW: PPO hook filtering
    stocks = this.applySectorFilter(stocks, sectorFilter);
    stocks = this.applyOptionableFilter(stocks, optionableFilter);
    stocks = this.applyEarningsFilter(stocks, earningsFilter);

    return stocks;
  }

  /**
   * Calculate returns for different timeframes
   * @param {Array} prices - Array of closing prices
   * @returns {Object} Returns object
   */
  static calculateReturns(prices) {
    const currentPrice = prices[prices.length - 1];
    
    return {
      return1d: prices.length >= 2 ? ((currentPrice - prices[prices.length - 2]) / prices[prices.length - 2]) * 100 : 0,
      return5d: prices.length >= 6 ? ((currentPrice - prices[prices.length - 6]) / prices[prices.length - 6]) * 100 : 0,
      return2w: prices.length >= 15 ? ((currentPrice - prices[prices.length - 15]) / prices[prices.length - 15]) * 100 : 0,
      return1m: prices.length >= 31 ? ((currentPrice - prices[prices.length - 31]) / prices[prices.length - 31]) * 100 : 0,
      return1y: prices.length >= 252 ? ((currentPrice - prices[0]) / prices[0]) * 100 : 
                ((currentPrice - prices[0]) / prices[0]) * 100 // Use available data
    };
  }

  /**
   * Generate realistic volume data
   * @param {string} symbol - Stock symbol
   * @returns {Object} Volume data
   */
  static generateVolumeData(symbol) {
    const baseVolume = 1000000 + (symbol.length * 500000); // Base volume varies by symbol
    const randomFactor = 0.5 + Math.random();
    
    return {
      today: Math.floor(baseVolume * randomFactor * (0.8 + Math.random() * 0.4)),
      threeMonth: Math.floor(baseVolume * randomFactor * 0.85),
      year: Math.floor(baseVolume * randomFactor * 0.9)
    };
  }

  /**
   * Generate realistic options data
   * @param {number} currentPrice - Current stock price
   * @param {number} volatility - Stock volatility
   * @returns {Object} Options data
   */
  static generateOptionsData(currentPrice, volatility) {
    // Calculate at-the-money strike (rounded to nearest $5 for most stocks)
    const atmStrike = Math.round(currentPrice / 5) * 5;
    
    // Base option price based on volatility and time to expiration (assume 30 days)
    const baseOptionValue = currentPrice * volatility * Math.sqrt(30 / 365) * 1.5;
    
    // Add realistic bid-ask spreads
    const spreadFactor = 0.05 + (volatility * 0.1);
    
    return {
      callBid: Math.max(0.05, baseOptionValue * (0.95 - spreadFactor/2)),
      callAsk: baseOptionValue * (1.05 + spreadFactor/2),
      putBid: Math.max(0.05, baseOptionValue * (0.9 - spreadFactor/2)),
      putAsk: baseOptionValue * (1.0 + spreadFactor/2)
    };
  }

  /**
   * Generate realistic earnings data
   * @returns {Object} Earnings data
   */
  static generateEarningsData() {
    // Generate random last earnings date (1-120 days ago)
    const lastEarningsAgo = Math.floor(Math.random() * 120) + 1;
    const lastEarnings = new Date(Date.now() - lastEarningsAgo * 24 * 60 * 60 * 1000);
    
    // Generate next earnings date (typically quarterly, so ~90 days from last)
    const daysUntilNext = Math.floor(Math.random() * 60) + 30; // 30-90 days
    const nextEarnings = new Date(lastEarnings.getTime() + (90 + daysUntilNext) * 24 * 60 * 60 * 1000);
    
    return {
      lastEarnings,
      nextEarnings,
      daysToEarnings: Math.floor((nextEarnings.getTime() - Date.now()) / (24 * 60 * 60 * 1000))
    };
  }

  // Filter application methods
  static applyPriceFilter(stocks, priceFilter) {
    if (!priceFilter) return stocks;
    
    return stocks.filter(stock => {
      if (priceFilter.type === 'under') {
        return stock.price <= priceFilter.under;
      } else if (priceFilter.type === 'range') {
        return stock.price >= priceFilter.min && stock.price <= priceFilter.max;
      }
      return true;
    });
  }

  static applyDMIFilter(stocks, dmiFilter) {
    if (!dmiFilter || (dmiFilter.min === undefined && dmiFilter.max === undefined)) return stocks;
    
    return stocks.filter(stock => {
      const dmi = stock.dmi;
      if (dmiFilter.min !== undefined && dmi < dmiFilter.min) return false;
      if (dmiFilter.max !== undefined && dmi > dmiFilter.max) return false;
      return true;
    });
  }

  static applyPPOSlopeFilter(stocks, ppoSlopeFilter) {
    if (!ppoSlopeFilter || ppoSlopeFilter.threshold === undefined) return stocks;
    
    return stocks.filter(stock => {
      return Math.abs(stock.ppoSlope) >= ppoSlopeFilter.threshold;
    });
  }

  static applyPPOHookFilter(stocks, ppoHookFilter) {
    if (!ppoHookFilter || ppoHookFilter === 'all') return stocks;
    
    return stocks.filter(stock => {
      // Detect PPO hook pattern using the same logic as the UI
      const ppoValues = stock.ppoValues;
      if (!ppoValues || ppoValues.length < 3) return false;
      
      const today = ppoValues[0];      // Today (index 0)
      const yesterday = ppoValues[1];   // Yesterday (index 1) 
      const dayBefore = ppoValues[2];   // Day before yesterday (index 2)
      
      // Positive hook: TODAY > YESTERDAY AND YESTERDAY < PRIOR DAY
      const hasPositiveHook = today > yesterday && yesterday < dayBefore;
      
      // Negative hook: TODAY < YESTERDAY AND YESTERDAY > PRIOR DAY  
      const hasNegativeHook = today < yesterday && yesterday > dayBefore;
      
      switch(ppoHookFilter) {
        case 'positive':
          return hasPositiveHook;
        case 'negative':
          return hasNegativeHook;
        case 'both':
          return hasPositiveHook || hasNegativeHook;
        default:
          return true;
      }
    });
  }

  static applySectorFilter(stocks, sectorFilter) {
    if (!sectorFilter || sectorFilter === 'all') return stocks;
    
    return stocks.filter(stock => 
      stock.sector.toLowerCase() === sectorFilter.toLowerCase()
    );
  }

  static applyOptionableFilter(stocks, optionableFilter) {
    if (!optionableFilter || optionableFilter === 'all') return stocks;
    
    return stocks.filter(stock => {
      if (optionableFilter === 'yes') return stock.optionable;
      if (optionableFilter === 'no') return !stock.optionable;
      return true;
    });
  }

  static applyEarningsFilter(stocks, earningsFilter) {
    if (!earningsFilter || earningsFilter === 'all') return stocks;
    
    return stocks.filter(stock => {
      if (earningsFilter === 'within7') return stock.daysToEarnings <= 7;
      if (earningsFilter === 'after7') return stock.daysToEarnings > 7;
      return true;
    });
  }
}

export default StockDataGenerator;