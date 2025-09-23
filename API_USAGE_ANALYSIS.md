# StockWise API Usage Analysis & Optimization Plan

## 🚨 CRITICAL ISSUE: Excessive API Calls Burning Through Limits

### Current API Call Triggers:

#### 1. **Technical Analysis Page** - HIGHEST API USAGE
- **Symbol Changes**: New API call for each symbol entered
- **Timeframe Changes**: New API call for each timeframe (1D, 5D, 1M, 3M, 6M, YTD, 1Y, 5Y, All) 
- **Auto-refresh**: React Query refetches every 30 seconds (DISABLED in recent optimization)
- **Page Refreshes**: Cache is in-memory only, lost on refresh

**Estimated Calls**: ~50-100 calls per user session

#### 2. **Dashboard Market Data** - MODERATE API USAGE  
- Trending Stocks: 1 call
- Top Gainers: 1 call  
- Top Losers: 1 call
- Auto-refresh: Every page visit

**Estimated Calls**: ~3-10 calls per session

#### 3. **Stock Screener** - POTENTIALLY HIGH API USAGE
- Currently using mock data, but could make many calls if switched to real data
- Each screening could potentially call multiple symbols

**Estimated Calls**: 0 (mock data) or 100+ (if real data)

#### 4. **Point Based Decision System** - MODERATE API USAGE
- Makes API calls for analysis data per symbol

**Estimated Calls**: ~10-20 calls per session

### API Rate Limits (Typical):
- **Alpha Vantage Free**: 25 calls/day, 5 calls/minute  
- **Polygon.io Free**: 5 calls/minute
- **Yahoo Finance**: Unofficial, can be blocked

## 🛠️ OPTIMIZATION STRATEGY

### Phase 1: Aggressive Caching (Immediate - 90% reduction)
1. **Persistent Cache**: Replace in-memory with localStorage/sessionStorage
2. **Longer Cache Duration**: Extend from 5 minutes to 4-6 hours for intraday, 24 hours for daily data
3. **Smart Cache Keys**: Include date to auto-expire overnight
4. **Preemptive Fallback**: Use mock data when approaching limits

### Phase 2: Smart Request Batching (Medium term - 50% reduction)  
1. **Symbol Grouping**: Batch similar timeframe requests
2. **Request Deduplication**: Prevent multiple calls for same symbol+timeframe
3. **Stale-While-Revalidate**: Serve cached data while fetching fresh in background

### Phase 3: API Call Budgeting (Long term - 80% reduction)
1. **Call Counter**: Track daily usage per API
2. **Intelligent Fallback**: Switch to mock data when near limits
3. **Premium Mode**: Allow users to add their own API keys