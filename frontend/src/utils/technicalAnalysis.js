// Technical Analysis Utility Functions for Stock Screener
// Implements accurate DMI and PPO calculations

export class TechnicalAnalysisEngine {
  
  /**
   * Calculate True Range for DMI calculations
   * @param {Array} priceData - Array of {high, low, close} objects
   * @returns {Array} True Range values
   */
  static calculateTrueRange(priceData) {
    const trueRanges = [];
    
    for (let i = 1; i < priceData.length; i++) {
      const current = priceData[i];
      const previous = priceData[i - 1];
      
      const highLow = current.high - current.low;
      const highClosePrev = Math.abs(current.high - previous.close);
      const lowClosePrev = Math.abs(current.low - previous.close);
      
      trueRanges.push(Math.max(highLow, highClosePrev, lowClosePrev));
    }
    
    return trueRanges;
  }

  /**
   * Calculate Directional Movement (+DM and -DM)
   * @param {Array} priceData - Array of {high, low, close} objects
   * @returns {Object} { plusDM, minusDM }
   */
  static calculateDirectionalMovement(priceData) {
    const plusDM = [];
    const minusDM = [];
    
    for (let i = 1; i < priceData.length; i++) {
      const current = priceData[i];
      const previous = priceData[i - 1];
      
      const upMove = current.high - previous.high;
      const downMove = previous.low - current.low;
      
      let plusDMValue = 0;
      let minusDMValue = 0;
      
      if (upMove > downMove && upMove > 0) {
        plusDMValue = upMove;
      }
      
      if (downMove > upMove && downMove > 0) {
        minusDMValue = downMove;
      }
      
      plusDM.push(plusDMValue);
      minusDM.push(minusDMValue);
    }
    
    return { plusDM, minusDM };
  }

  /**
   * Calculate Smoothed Moving Average (Wilder's smoothing)
   * @param {Array} values - Array of values to smooth
   * @param {number} period - Smoothing period
   * @returns {Array} Smoothed values
   */
  static calculateSmoothedMA(values, period) {
    const smoothed = [];
    
    // First value is simple average of first 'period' values
    let sum = 0;
    for (let i = 0; i < Math.min(period, values.length); i++) {
      sum += values[i];
    }
    smoothed.push(sum / Math.min(period, values.length));
    
    // Subsequent values use Wilder's smoothing formula
    for (let i = 1; i < values.length - period + 1; i++) {
      const currentIndex = i + period - 1;
      if (currentIndex < values.length) {
        const newValue = (smoothed[i - 1] * (period - 1) + values[currentIndex]) / period;
        smoothed.push(newValue);
      }
    }
    
    return smoothed;
  }

  /**
   * Calculate 14-period DMI including DI+, DI-, and ADX
   * @param {Array} priceData - Array of {high, low, close} objects
   * @returns {Object} { diPlus, diMinus, adx, currentDMI }
   */
  static calculateDMI(priceData, period = 14) {
    if (priceData.length < period + 1) {
      throw new Error(`Insufficient data points. Need at least ${period + 1} data points.`);
    }

    // Calculate True Range and Directional Movement
    const trueRanges = this.calculateTrueRange(priceData);
    const { plusDM, minusDM } = this.calculateDirectionalMovement(priceData);

    // Calculate smoothed values using Wilder's smoothing
    const smoothedTR = this.calculateSmoothedMA(trueRanges, period);
    const smoothedPlusDM = this.calculateSmoothedMA(plusDM, period);
    const smoothedMinusDM = this.calculateSmoothedMA(minusDM, period);

    // Calculate DI+ and DI-
    const diPlus = [];
    const diMinus = [];
    
    for (let i = 0; i < Math.min(smoothedTR.length, smoothedPlusDM.length, smoothedMinusDM.length); i++) {
      if (smoothedTR[i] !== 0) {
        diPlus.push((smoothedPlusDM[i] / smoothedTR[i]) * 100);
        diMinus.push((smoothedMinusDM[i] / smoothedTR[i]) * 100);
      } else {
        diPlus.push(0);
        diMinus.push(0);
      }
    }

    // Calculate DX (Directional Index)
    const dx = [];
    for (let i = 0; i < Math.min(diPlus.length, diMinus.length); i++) {
      const diSum = diPlus[i] + diMinus[i];
      if (diSum !== 0) {
        dx.push((Math.abs(diPlus[i] - diMinus[i]) / diSum) * 100);
      } else {
        dx.push(0);
      }
    }

    // Calculate ADX (smoothed DX)
    const adx = this.calculateSmoothedMA(dx, period);

    return {
      diPlus: diPlus[diPlus.length - 1] || 0,
      diMinus: diMinus[diMinus.length - 1] || 0,
      adx: adx[adx.length - 1] || 0,
      currentDMI: adx[adx.length - 1] || 0, // ADX is commonly referred to as DMI
      history: {
        diPlus,
        diMinus,
        adx
      }
    };
  }

  /**
   * Calculate PPO (Percentage Price Oscillator)
   * @param {Array} prices - Array of closing prices
   * @param {number} fastPeriod - Fast EMA period (default 12)
   * @param {number} slowPeriod - Slow EMA period (default 26)
   * @returns {Array} PPO values
   */
  static calculatePPO(prices, fastPeriod = 12, slowPeriod = 26) {
    if (prices.length < slowPeriod) {
      throw new Error(`Insufficient data points. Need at least ${slowPeriod} prices.`);
    }

    // Calculate EMAs
    const fastEMA = this.calculateEMA(prices, fastPeriod);
    const slowEMA = this.calculateEMA(prices, slowPeriod);

    const ppo = [];
    const startIndex = slowPeriod - 1;

    for (let i = startIndex; i < prices.length; i++) {
      const fastIndex = i - (slowPeriod - fastPeriod);
      if (fastIndex >= 0 && slowEMA[i - startIndex] !== 0) {
        const ppoValue = ((fastEMA[fastIndex] - slowEMA[i - startIndex]) / slowEMA[i - startIndex]) * 100;
        ppo.push(ppoValue);
      }
    }

    return ppo;
  }

  /**
   * Calculate Exponential Moving Average
   * @param {Array} prices - Array of prices
   * @param {number} period - EMA period
   * @returns {Array} EMA values
   */
  static calculateEMA(prices, period) {
    const multiplier = 2 / (period + 1);
    const ema = [];
    
    // First EMA is simple average of first 'period' values
    let sum = 0;
    for (let i = 0; i < Math.min(period, prices.length); i++) {
      sum += prices[i];
    }
    ema.push(sum / Math.min(period, prices.length));
    
    // Calculate subsequent EMA values
    for (let i = 1; i < prices.length; i++) {
      const newEMA = (prices[i] * multiplier) + (ema[i - 1] * (1 - multiplier));
      ema.push(newEMA);
    }
    
    return ema;
  }

  /**
   * Calculate PPO Slope using conditional logic as specified
   * @param {Array} ppoValues - Array of PPO values (must have at least 3 values)
   * @returns {number} PPO slope percentage
   */
  static calculatePPOSlope(ppoValues) {
    if (ppoValues.length < 3) {
      throw new Error('Need at least 3 PPO values for slope calculation');
    }

    // Get last 3 values: [day before yesterday, yesterday, today]
    const dayBeforeYesterday = ppoValues[ppoValues.length - 3];
    const yesterday = ppoValues[ppoValues.length - 2];
    const today = ppoValues[ppoValues.length - 1];

    let slope = 0;

    // Conditional logic as specified:
    // When PPO < 0 use (today - yesterday)/yesterday
    // When PPO > 0 use (yesterday - today)/yesterday
    if (today < 0) {
      if (yesterday !== 0) {
        slope = ((today - yesterday) / Math.abs(yesterday)) * 100;
      }
    } else if (today > 0) {
      if (yesterday !== 0) {
        slope = ((yesterday - today) / Math.abs(yesterday)) * 100;
      }
    } else {
      // PPO is exactly 0, calculate simple slope
      if (yesterday !== 0) {
        slope = ((today - yesterday) / Math.abs(yesterday)) * 100;
      }
    }

    return slope;
  }

  /**
   * Validate price range inputs
   * @param {Object} priceFilter - Price filter configuration
   * @returns {Object} { isValid, errors }
   */
  static validatePriceRange(priceFilter) {
    const errors = [];
    const { type, under, min, max } = priceFilter;

    if (type === 'under') {
      if (!under || under < 1) {
        errors.push('Maximum price must be at least $1');
      }
      if (under > 1000) {
        errors.push('Maximum price cannot exceed $1000');
      }
    } else if (type === 'range') {
      if (!min || min < 1) {
        errors.push('Minimum price must be at least $1');
      }
      if (!max || max > 1000) {
        errors.push('Maximum price cannot exceed $1000');
      }
      if (min && max && min >= max) {
        errors.push('Minimum price must be less than maximum price');
      }
      if (max - min < 1) {
        errors.push('Price range must be at least $1');
      }
    }

    return {
      isValid: errors.length === 0,
      errors
    };
  }

  /**
   * Generate realistic stock price data for testing
   * @param {number} days - Number of days of data
   * @param {number} startPrice - Starting price
   * @param {number} volatility - Price volatility factor
   * @returns {Array} Array of {high, low, close} objects
   */
  static generateMockPriceData(days = 50, startPrice = 100, volatility = 0.02) {
    const data = [];
    let currentPrice = startPrice;

    for (let i = 0; i < days; i++) {
      // Generate daily price movement
      const change = (Math.random() - 0.5) * 2 * volatility * currentPrice;
      currentPrice = Math.max(1, currentPrice + change);

      // Generate OHLC data
      const dayVolatility = volatility * currentPrice * 0.5;
      const high = currentPrice + (Math.random() * dayVolatility);
      const low = currentPrice - (Math.random() * dayVolatility);
      const close = low + (Math.random() * (high - low));

      data.push({
        date: new Date(Date.now() - (days - i) * 24 * 60 * 60 * 1000),
        high: Math.max(high, low, close),
        low: Math.min(high, low, close),
        close: close,
        open: i === 0 ? startPrice : data[i - 1].close
      });
    }

    return data;
  }
}

// Export individual functions for easier testing
export const {
  calculateTrueRange,
  calculateDirectionalMovement,
  calculateSmoothedMA,
  calculateDMI,
  calculatePPO,
  calculateEMA,
  calculatePPOSlope,
  validatePriceRange,
  generateMockPriceData
} = TechnicalAnalysisEngine;