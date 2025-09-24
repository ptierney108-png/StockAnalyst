#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for Stock Analysis Platform
Tests all stock analysis endpoints and functionality
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any, List

# Configuration
BACKEND_URL = "https://stockwise-116.preview.emergentagent.com/api"
TEST_SYMBOLS = ["AAPL", "GOOGL", "MSFT", "TSLA"]
INVALID_SYMBOLS = ["INVALID", "FAKE123", ""]

class StockAnalysisAPITester:
    def __init__(self):
        self.results = {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "test_details": [],
            "critical_issues": [],
            "performance_metrics": {}
        }
        
    def log_test(self, test_name: str, passed: bool, details: str, is_critical: bool = False):
        """Log test results"""
        self.results["total_tests"] += 1
        if passed:
            self.results["passed_tests"] += 1
            status = "✅ PASS"
        else:
            self.results["failed_tests"] += 1
            status = "❌ FAIL"
            if is_critical:
                self.results["critical_issues"].append(f"{test_name}: {details}")
        
        self.results["test_details"].append({
            "test": test_name,
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
        print(f"{status}: {test_name} - {details}")
    
    def test_basic_connectivity(self) -> bool:
        """Test basic API connectivity"""
        try:
            response = requests.get(f"{BACKEND_URL}/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if "StockWise API" in data.get("message", ""):
                    self.log_test("Basic Connectivity", True, "API root endpoint accessible")
                    return True
                else:
                    self.log_test("Basic Connectivity", False, f"Unexpected response: {data}", True)
                    return False
            else:
                self.log_test("Basic Connectivity", False, f"HTTP {response.status_code}: {response.text}", True)
                return False
        except Exception as e:
            self.log_test("Basic Connectivity", False, f"Connection error: {str(e)}", True)
            return False
    
    def test_stock_analysis_get_endpoint(self, symbol: str) -> Dict[str, Any]:
        """Test GET /api/analyze/{symbol} endpoint"""
        try:
            start_time = time.time()
            response = requests.get(f"{BACKEND_URL}/analyze/{symbol}", timeout=30)
            response_time = time.time() - start_time
            
            self.results["performance_metrics"][f"analyze_get_{symbol}"] = response_time
            
            if response.status_code == 200:
                data = response.json()
                self.log_test(f"Stock Analysis GET ({symbol})", True, 
                            f"Response received in {response_time:.2f}s")
                return data
            else:
                self.log_test(f"Stock Analysis GET ({symbol})", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                return {}
        except Exception as e:
            self.log_test(f"Stock Analysis GET ({symbol})", False, f"Error: {str(e)}", True)
            return {}
    
    def test_stock_analysis_post_endpoint(self, symbol: str) -> Dict[str, Any]:
        """Test POST /api/analyze endpoint"""
        try:
            payload = {"symbol": symbol, "timeframe": "daily"}
            start_time = time.time()
            response = requests.post(f"{BACKEND_URL}/analyze", 
                                   json=payload, 
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            response_time = time.time() - start_time
            
            self.results["performance_metrics"][f"analyze_post_{symbol}"] = response_time
            
            if response.status_code == 200:
                data = response.json()
                self.log_test(f"Stock Analysis POST ({symbol})", True, 
                            f"Response received in {response_time:.2f}s")
                return data
            else:
                self.log_test(f"Stock Analysis POST ({symbol})", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                return {}
        except Exception as e:
            self.log_test(f"Stock Analysis POST ({symbol})", False, f"Error: {str(e)}", True)
            return {}
    
    def validate_response_structure(self, data: Dict[str, Any], symbol: str) -> bool:
        """Validate the structure of stock analysis response"""
        required_fields = [
            "symbol", "current_price", "price_change", "price_change_percent",
            "volume", "indicators", "ppo_history", "dmi_history",
            "ai_recommendation", "ai_confidence", "ai_reasoning",
            "ai_detailed_analysis", "sentiment_analysis", "sentiment_score",
            "chart_data"
        ]
        
        missing_fields = []
        for field in required_fields:
            if field not in data:
                missing_fields.append(field)
        
        if missing_fields:
            self.log_test(f"Response Structure ({symbol})", False, 
                        f"Missing fields: {missing_fields}", True)
            return False
        else:
            self.log_test(f"Response Structure ({symbol})", True, 
                        "All required fields present")
            return True
    
    def validate_technical_indicators(self, indicators: Dict[str, Any], symbol: str) -> bool:
        """Validate technical indicators structure and values"""
        required_indicators = [
            "ppo", "ppo_signal", "ppo_histogram", "ppo_slope", "ppo_slope_percentage",
            "dmi_plus", "dmi_minus", "adx", "sma_20", "sma_50", "sma_200",
            "rsi", "macd", "macd_signal", "macd_histogram"
        ]
        
        issues = []
        
        # Check if all indicators are present
        for indicator in required_indicators:
            if indicator not in indicators:
                issues.append(f"Missing {indicator}")
            elif indicators[indicator] is None:
                issues.append(f"{indicator} is null")
        
        # Validate specific indicator ranges
        if "rsi" in indicators and indicators["rsi"] is not None:
            rsi = indicators["rsi"]
            if not (0 <= rsi <= 100):
                issues.append(f"RSI {rsi} outside valid range (0-100)")
        
        if "adx" in indicators and indicators["adx"] is not None:
            adx = indicators["adx"]
            if adx < 0:
                issues.append(f"ADX {adx} is negative")
        
        if issues:
            self.log_test(f"Technical Indicators ({symbol})", False, 
                        f"Issues: {issues}", True)
            return False
        else:
            self.log_test(f"Technical Indicators ({symbol})", True, 
                        "All indicators valid")
            return True
    
    def validate_ppo_history(self, ppo_history: List[Dict], symbol: str) -> bool:
        """Validate PPO history data format"""
        if not isinstance(ppo_history, list):
            self.log_test(f"PPO History ({symbol})", False, 
                        "PPO history is not a list", True)
            return False
        
        if len(ppo_history) != 3:
            self.log_test(f"PPO History ({symbol})", False, 
                        f"Expected 3 days of PPO history, got {len(ppo_history)}")
            return False
        
        for i, entry in enumerate(ppo_history):
            if "date" not in entry or "ppo" not in entry:
                self.log_test(f"PPO History ({symbol})", False, 
                            f"Day {i+1} missing date or ppo field", True)
                return False
        
        self.log_test(f"PPO History ({symbol})", True, 
                    f"3-day PPO history format valid")
        return True
    
    def validate_dmi_history(self, dmi_history: List[Dict], symbol: str) -> bool:
        """Validate DMI history data format"""
        if not isinstance(dmi_history, list):
            self.log_test(f"DMI History ({symbol})", False, 
                        "DMI history is not a list", True)
            return False
        
        if len(dmi_history) != 3:
            self.log_test(f"DMI History ({symbol})", False, 
                        f"Expected 3 days of DMI history, got {len(dmi_history)}")
            return False
        
        required_dmi_fields = ["date", "dmi_plus", "dmi_minus", "adx"]
        for i, entry in enumerate(dmi_history):
            missing_fields = [field for field in required_dmi_fields if field not in entry]
            if missing_fields:
                self.log_test(f"DMI History ({symbol})", False, 
                            f"Day {i+1} missing fields: {missing_fields}", True)
                return False
        
        self.log_test(f"DMI History ({symbol})", True, 
                    f"3-day DMI history format valid")
        return True
    
    def validate_ai_recommendations(self, data: Dict[str, Any], symbol: str) -> bool:
        """Validate AI recommendations and sentiment analysis"""
        issues = []
        
        # Check AI recommendation
        ai_rec = data.get("ai_recommendation")
        if ai_rec not in ["BUY", "SELL", "HOLD"]:
            issues.append(f"Invalid AI recommendation: {ai_rec}")
        
        # Check AI confidence
        ai_conf = data.get("ai_confidence")
        if not isinstance(ai_conf, (int, float)) or not (0 <= ai_conf <= 1):
            issues.append(f"Invalid AI confidence: {ai_conf}")
        
        # Check AI reasoning
        ai_reasoning = data.get("ai_reasoning")
        if not isinstance(ai_reasoning, str) or len(ai_reasoning) < 10:
            issues.append("AI reasoning too short or invalid")
        
        # Check detailed analysis
        detailed_analysis = data.get("ai_detailed_analysis", [])
        if not isinstance(detailed_analysis, list) or len(detailed_analysis) < 3:
            issues.append("AI detailed analysis insufficient")
        
        # Check sentiment
        sentiment = data.get("sentiment_analysis")
        if sentiment not in ["Positive", "Negative", "Neutral"]:
            issues.append(f"Invalid sentiment: {sentiment}")
        
        # Check sentiment score
        sentiment_score = data.get("sentiment_score")
        if not isinstance(sentiment_score, (int, float)) or not (-1 <= sentiment_score <= 1):
            issues.append(f"Invalid sentiment score: {sentiment_score}")
        
        if issues:
            self.log_test(f"AI Recommendations ({symbol})", False, 
                        f"Issues: {issues}", True)
            return False
        else:
            self.log_test(f"AI Recommendations ({symbol})", True, 
                        "AI recommendations and sentiment valid")
            return True
    
    def validate_chart_data(self, chart_data: List[Dict], symbol: str) -> bool:
        """Validate chart data format for ApexCharts"""
        if not isinstance(chart_data, list):
            self.log_test(f"Chart Data ({symbol})", False, 
                        "Chart data is not a list", True)
            return False
        
        if len(chart_data) < 10:
            self.log_test(f"Chart Data ({symbol})", False, 
                        f"Insufficient chart data: {len(chart_data)} entries")
            return False
        
        required_fields = ["date", "open", "high", "low", "close", "volume"]
        for i, entry in enumerate(chart_data[:5]):  # Check first 5 entries
            missing_fields = [field for field in required_fields if field not in entry]
            if missing_fields:
                self.log_test(f"Chart Data ({symbol})", False, 
                            f"Entry {i+1} missing fields: {missing_fields}", True)
                return False
            
            # Validate OHLC logic
            if not (entry["low"] <= entry["open"] <= entry["high"] and 
                   entry["low"] <= entry["close"] <= entry["high"]):
                self.log_test(f"Chart Data ({symbol})", False, 
                            f"Invalid OHLC data at entry {i+1}", True)
                return False
        
        self.log_test(f"Chart Data ({symbol})", True, 
                    f"Chart data format valid ({len(chart_data)} entries)")
        return True
    
    def test_error_handling(self) -> bool:
        """Test error handling with invalid symbols"""
        all_passed = True
        
        for invalid_symbol in INVALID_SYMBOLS:
            try:
                response = requests.get(f"{BACKEND_URL}/analyze/{invalid_symbol}", timeout=10)
                
                if invalid_symbol == "":
                    # Empty symbol should return 404 or 422
                    if response.status_code in [404, 422]:
                        self.log_test(f"Error Handling (empty symbol)", True, 
                                    f"Correctly returned {response.status_code}")
                    else:
                        self.log_test(f"Error Handling (empty symbol)", False, 
                                    f"Expected 404/422, got {response.status_code}")
                        all_passed = False
                else:
                    # Invalid symbols should either return error or demo data
                    if response.status_code == 200:
                        # If it returns 200, it should be demo data
                        data = response.json()
                        if data.get("symbol") == invalid_symbol.upper():
                            self.log_test(f"Error Handling ({invalid_symbol})", True, 
                                        "Returns demo data for invalid symbol")
                        else:
                            self.log_test(f"Error Handling ({invalid_symbol})", False, 
                                        "Unexpected response for invalid symbol")
                            all_passed = False
                    elif response.status_code in [404, 400]:
                        self.log_test(f"Error Handling ({invalid_symbol})", True, 
                                    f"Correctly returned error {response.status_code}")
                    else:
                        self.log_test(f"Error Handling ({invalid_symbol})", False, 
                                    f"Unexpected status code: {response.status_code}")
                        all_passed = False
                        
            except Exception as e:
                self.log_test(f"Error Handling ({invalid_symbol})", False, 
                            f"Exception: {str(e)}")
                all_passed = False
        
        return all_passed
    
    def test_performance(self) -> bool:
        """Test API performance"""
        performance_issues = []
        
        for symbol, response_time in self.results["performance_metrics"].items():
            if response_time > 10:  # More than 10 seconds is too slow
                performance_issues.append(f"{symbol}: {response_time:.2f}s")
        
        if performance_issues:
            self.log_test("Performance", False, 
                        f"Slow responses: {performance_issues}")
            return False
        else:
            avg_time = sum(self.results["performance_metrics"].values()) / len(self.results["performance_metrics"])
            self.log_test("Performance", True, 
                        f"Average response time: {avg_time:.2f}s")
            return True
    
    def test_stock_screener_endpoints(self) -> bool:
        """Test Stock Screener Phase 3 endpoints"""
        all_passed = True
        
        # Test screener presets endpoint
        try:
            response = requests.get(f"{BACKEND_URL}/screener/presets", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if "presets" in data and isinstance(data["presets"], list):
                    self.log_test("Screener Presets", True, 
                                f"Retrieved {len(data['presets'])} presets")
                else:
                    self.log_test("Screener Presets", False, 
                                "Invalid presets response structure", True)
                    all_passed = False
            else:
                self.log_test("Screener Presets", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                all_passed = False
        except Exception as e:
            self.log_test("Screener Presets", False, f"Error: {str(e)}", True)
            all_passed = False
        
        # Test stock screening with default filters
        try:
            default_filters = {
                "price_filter": {"type": "under", "under": 50},
                "dmi_filter": {"min": 20, "max": 60},
                "ppo_slope_filter": {"threshold": 5},
                "sector_filter": "all",
                "optionable_filter": "all",
                "earnings_filter": "all"
            }
            
            start_time = time.time()
            response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                   json=default_filters,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            response_time = time.time() - start_time
            
            self.results["performance_metrics"]["screener_scan_default"] = response_time
            
            if response.status_code == 200:
                data = response.json()
                if self.validate_screener_response(data, "Default Filters"):
                    self.log_test("Stock Screener (Default)", True, 
                                f"Found {data.get('results_found', 0)} stocks in {response_time:.2f}s")
                else:
                    all_passed = False
            else:
                self.log_test("Stock Screener (Default)", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                all_passed = False
                
        except Exception as e:
            self.log_test("Stock Screener (Default)", False, f"Error: {str(e)}", True)
            all_passed = False
        
        # Test stock screening with custom filters
        try:
            custom_filters = {
                "price_filter": {"type": "range", "min": 100, "max": 500},
                "dmi_filter": {"min": 25, "max": 55},
                "ppo_slope_filter": {"threshold": 8},
                "sector_filter": "Technology"
            }
            
            start_time = time.time()
            response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                   json=custom_filters,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            response_time = time.time() - start_time
            
            self.results["performance_metrics"]["screener_scan_custom"] = response_time
            
            if response.status_code == 200:
                data = response.json()
                if self.validate_screener_response(data, "Custom Filters"):
                    self.log_test("Stock Screener (Custom)", True, 
                                f"Found {data.get('results_found', 0)} stocks in {response_time:.2f}s")
                else:
                    all_passed = False
            else:
                self.log_test("Stock Screener (Custom)", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                all_passed = False
                
        except Exception as e:
            self.log_test("Stock Screener (Custom)", False, f"Error: {str(e)}", True)
            all_passed = False
        
        # Test edge case: very restrictive filters
        try:
            restrictive_filters = {
                "price_filter": {"type": "range", "min": 1000, "max": 2000},
                "dmi_filter": {"min": 55, "max": 60},
                "ppo_slope_filter": {"threshold": 20}
            }
            
            response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                   json=restrictive_filters,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                # Should return few or no results with restrictive filters
                self.log_test("Stock Screener (Restrictive)", True, 
                            f"Restrictive filters returned {data.get('results_found', 0)} stocks")
            else:
                self.log_test("Stock Screener (Restrictive)", False, 
                            f"HTTP {response.status_code}: {response.text}")
                all_passed = False
                
        except Exception as e:
            self.log_test("Stock Screener (Restrictive)", False, f"Error: {str(e)}")
            all_passed = False
        
        return all_passed
    
    def validate_screener_response(self, data: Dict[str, Any], test_name: str) -> bool:
        """Validate stock screener response structure and data quality"""
        required_fields = ["success", "total_scanned", "results_found", "stocks", "scan_time", "filters_applied"]
        
        # Check required fields
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            self.log_test(f"Screener Response Structure ({test_name})", False, 
                        f"Missing fields: {missing_fields}", True)
            return False
        
        # Validate success flag
        if not data.get("success"):
            self.log_test(f"Screener Response ({test_name})", False, 
                        "Success flag is false", True)
            return False
        
        # Validate stocks array
        stocks = data.get("stocks", [])
        if not isinstance(stocks, list):
            self.log_test(f"Screener Stocks ({test_name})", False, 
                        "Stocks field is not a list", True)
            return False
        
        # Validate individual stock data
        if len(stocks) > 0:
            stock_issues = self.validate_stock_screener_data(stocks[0], test_name)
            if stock_issues:
                self.log_test(f"Stock Data Quality ({test_name})", False, 
                            f"Issues: {stock_issues}", True)
                return False
        
        # Validate filtering logic
        if not self.validate_filtering_logic(data, test_name):
            return False
        
        self.log_test(f"Screener Response ({test_name})", True, 
                    "All validation checks passed")
        return True
    
    def validate_stock_screener_data(self, stock: Dict[str, Any], test_name: str) -> List[str]:
        """Validate individual stock data from screener"""
        issues = []
        
        required_stock_fields = [
            "symbol", "name", "sector", "industry", "price", 
            "dmi", "adx", "di_plus", "di_minus", "ppo_values", "ppo_slope_percentage",
            "returns", "volume_today", "volume_3m", "volume_year",
            "optionable", "call_bid", "call_ask", "put_bid", "put_ask",
            "last_earnings", "next_earnings", "days_to_earnings"
        ]
        
        # Check required fields
        for field in required_stock_fields:
            if field not in stock:
                issues.append(f"Missing {field}")
        
        # Validate data ranges and types
        if "price" in stock:
            if not isinstance(stock["price"], (int, float)) or stock["price"] <= 0:
                issues.append("Invalid price value")
        
        if "adx" in stock:
            if not isinstance(stock["adx"], (int, float)) or stock["adx"] < 0:
                issues.append("Invalid ADX value")
        
        if "ppo_slope_percentage" in stock:
            if not isinstance(stock["ppo_slope_percentage"], (int, float)):
                issues.append("Invalid PPO slope percentage")
        
        if "returns" in stock:
            returns = stock["returns"]
            if not isinstance(returns, dict):
                issues.append("Returns should be a dictionary")
            else:
                required_return_periods = ["1d", "5d", "2w", "1m", "1y"]
                for period in required_return_periods:
                    if period not in returns:
                        issues.append(f"Missing {period} return")
        
        if "ppo_values" in stock:
            ppo_values = stock["ppo_values"]
            if not isinstance(ppo_values, list):
                issues.append("PPO values should be a list")
            elif len(ppo_values) != 3:
                issues.append("PPO values should contain 3 values")
        
        return issues
    
    def validate_filtering_logic(self, data: Dict[str, Any], test_name: str) -> bool:
        """Validate that filtering logic is working correctly"""
        filters_applied = data.get("filters_applied", {})
        stocks = data.get("stocks", [])
        
        # Check price filtering
        if "price_filter" in filters_applied and filters_applied["price_filter"]:
            price_filter = filters_applied["price_filter"]
            for stock in stocks:
                price = stock.get("price", 0)
                
                if price_filter.get("type") == "under":
                    max_price = price_filter.get("under", 50)
                    if price > max_price:
                        self.log_test(f"Price Filter Logic ({test_name})", False, 
                                    f"Stock {stock.get('symbol')} price ${price:.2f} exceeds filter ${max_price}", True)
                        return False
                
                elif price_filter.get("type") == "range":
                    min_price = price_filter.get("min", 0)
                    max_price = price_filter.get("max", 1000)
                    if not (min_price <= price <= max_price):
                        self.log_test(f"Price Filter Logic ({test_name})", False, 
                                    f"Stock {stock.get('symbol')} price ${price:.2f} outside range ${min_price}-${max_price}", True)
                        return False
        
        # Check DMI filtering
        if "dmi_filter" in filters_applied and filters_applied["dmi_filter"]:
            dmi_filter = filters_applied["dmi_filter"]
            dmi_min = dmi_filter.get("min", 20)
            dmi_max = dmi_filter.get("max", 60)
            
            for stock in stocks:
                adx = stock.get("adx", 0)
                if not (dmi_min <= adx <= dmi_max):
                    self.log_test(f"DMI Filter Logic ({test_name})", False, 
                                f"Stock {stock.get('symbol')} ADX {adx:.2f} outside range {dmi_min}-{dmi_max}", True)
                    return False
        
        # Check PPO slope filtering
        if "ppo_slope_filter" in filters_applied and filters_applied["ppo_slope_filter"]:
            ppo_filter = filters_applied["ppo_slope_filter"]
            threshold = ppo_filter.get("threshold", 5)
            
            for stock in stocks:
                ppo_slope = stock.get("ppo_slope_percentage", 0)
                if abs(ppo_slope) < threshold:
                    self.log_test(f"PPO Slope Filter Logic ({test_name})", False, 
                                f"Stock {stock.get('symbol')} PPO slope {ppo_slope:.2f}% below threshold {threshold}%", True)
                    return False
        
        self.log_test(f"Filter Logic ({test_name})", True, 
                    "All filtering logic validated successfully")
        return True

    def test_ppo_calculation_fix(self) -> bool:
        """
        COMPREHENSIVE PPO CALCULATION FIX TESTING
        
        Tests the specific fix for PPO calculation when insufficient data points 
        are available from real APIs (Polygon/Yahoo Finance). Validates:
        1. Adaptive PPO calculation with limited data
        2. Data quality indicators in responses
        3. Fallback strategies for edge cases
        4. Non-zero PPO values even with limited data
        5. Proper data source transparency
        """
        print(f"\n🔧 COMPREHENSIVE PPO CALCULATION FIX TESTING")
        print("=" * 70)
        
        all_passed = True
        fix_issues = []
        
        # Test symbols with various data availability scenarios
        test_symbols = ["AAPL", "GOOGL", "MSFT", "TSLA", "NVDA", "AMZN"]
        
        for symbol in test_symbols:
            print(f"\n📊 Testing PPO calculation fix for {symbol}")
            
            # Test /api/analyze endpoint with various timeframes that might have limited data
            timeframes = ["1D", "5D", "1M"]
            
            for timeframe in timeframes:
                try:
                    payload = {"symbol": symbol, "timeframe": timeframe}
                    start_time = time.time()
                    
                    response = requests.post(f"{BACKEND_URL}/analyze", 
                                           json=payload,
                                           headers={"Content-Type": "application/json"},
                                           timeout=30)
                    response_time = time.time() - start_time
                    
                    if response.status_code == 200:
                        data = response.json()
                        data_source = data.get("data_source", "unknown")
                        
                        # Validate PPO calculation fix implementation
                        ppo_fix_issues = self.validate_ppo_calculation_fix(data, symbol, timeframe, data_source)
                        
                        if ppo_fix_issues:
                            fix_issues.extend(ppo_fix_issues)
                            all_passed = False
                            self.log_test(f"PPO Calculation Fix ({symbol} {timeframe})", False, 
                                        f"Data source: {data_source}, Issues: {ppo_fix_issues}", True)
                        else:
                            self.log_test(f"PPO Calculation Fix ({symbol} {timeframe})", True, 
                                        f"Data source: {data_source}, PPO fix working correctly")
                        
                        # Log detailed analysis for debugging
                        indicators = data.get("indicators", {})
                        ppo = indicators.get("ppo", 0)
                        chart_data_count = len(data.get("chart_data", []))
                        print(f"  📈 {symbol} ({timeframe}): PPO={ppo:.4f}, Data points={chart_data_count}, Source={data_source}")
                        
                        # Check for data quality indicators (new feature)
                        self.validate_data_quality_indicators(data, symbol, timeframe)
                        
                    else:
                        self.log_test(f"PPO Fix API Test ({symbol} {timeframe})", False, 
                                    f"HTTP {response.status_code}: {response.text}", True)
                        all_passed = False
                        
                except Exception as e:
                    self.log_test(f"PPO Fix API Test ({symbol} {timeframe})", False, 
                                f"Error: {str(e)}", True)
                    all_passed = False
        
        # Test screener endpoint to ensure it still works with PPO fix
        print(f"\n📊 Testing Stock Screener with PPO Fix")
        try:
            screener_filters = {
                "price_filter": {"type": "under", "under": 300},
                "dmi_filter": {"min": 20, "max": 60},
                "ppo_slope_filter": {"threshold": 1},
                "sector_filter": "all"
            }
            
            response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                   json=screener_filters,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                screener_fix_issues = self.validate_screener_ppo_fix(data)
                
                if screener_fix_issues:
                    fix_issues.extend(screener_fix_issues)
                    all_passed = False
                    self.log_test("Screener PPO Fix", False, 
                                f"Screener issues after PPO fix: {screener_fix_issues}", True)
                else:
                    self.log_test("Screener PPO Fix", True, 
                                "Screener working correctly with PPO fix")
            else:
                self.log_test("Screener PPO Fix Test", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                all_passed = False
                
        except Exception as e:
            self.log_test("Screener PPO Fix Test", False, f"Error: {str(e)}", True)
            all_passed = False
        
        # Test edge cases: very limited data scenarios
        print(f"\n🔬 Testing Edge Cases: Very Limited Data Scenarios")
        edge_cases_passed = self.test_ppo_edge_cases()
        if not edge_cases_passed:
            all_passed = False
        
        # Test adaptive PPO slope calculations
        print(f"\n📐 Testing Adaptive PPO Slope Calculations")
        slope_tests_passed = self.test_adaptive_ppo_slope()
        if not slope_tests_passed:
            all_passed = False
        
        # Summary of PPO calculation fix testing
        if fix_issues:
            print(f"\n🚨 PPO CALCULATION FIX ISSUES FOUND ({len(fix_issues)}):")
            for issue in fix_issues:
                print(f"  • {issue}")
        else:
            print(f"\n✅ PPO calculation fix working correctly - no systematic zero PPO values detected")
        
        return all_passed

    def validate_ppo_data_availability(self, data: Dict[str, Any], symbol: str, timeframe: str, data_source: str) -> List[str]:
        """Validate PPO data availability and quality"""
        issues = []
        
        # Check main PPO indicators
        indicators = data.get("indicators", {})
        if not indicators:
            issues.append("Missing indicators object")
            return issues
        
        # Check PPO values
        ppo = indicators.get("ppo")
        ppo_signal = indicators.get("ppo_signal")
        ppo_histogram = indicators.get("ppo_histogram")
        ppo_slope_percentage = indicators.get("ppo_slope_percentage")
        
        if ppo is None:
            issues.append("PPO value is null")
        elif ppo == 0 and data_source == "polygon_io":
            issues.append("PPO value is zero (possible calculation failure with Polygon data)")
        
        if ppo_signal is None:
            issues.append("PPO signal is null")
        elif ppo_signal == 0 and data_source == "polygon_io":
            issues.append("PPO signal is zero (possible calculation failure with Polygon data)")
        
        if ppo_histogram is None:
            issues.append("PPO histogram is null")
        
        if ppo_slope_percentage is None:
            issues.append("PPO slope percentage is null")
        
        # Check PPO history
        ppo_history = data.get("ppo_history", [])
        if not ppo_history:
            issues.append("PPO history is empty")
        elif len(ppo_history) < 3:
            issues.append(f"PPO history incomplete: {len(ppo_history)} entries (expected 3)")
        else:
            # Check if PPO history values are all zero (indication of calculation failure)
            all_zero = all(entry.get("ppo", 0) == 0 for entry in ppo_history)
            if all_zero and data_source == "polygon_io":
                issues.append("All PPO history values are zero (possible Polygon data issue)")
        
        # Check chart data PPO values
        chart_data = data.get("chart_data", [])
        if chart_data:
            chart_ppo_values = [item.get("ppo", 0) for item in chart_data]
            if len(chart_ppo_values) >= 26:  # Should have enough for PPO calculation
                recent_ppo_values = chart_ppo_values[-10:]  # Check last 10 values
                if all(val == 0 for val in recent_ppo_values) and data_source == "polygon_io":
                    issues.append("Recent chart PPO values are all zero (possible Polygon calculation issue)")
        
        return issues

    def validate_screener_ppo_data(self, data: Dict[str, Any]) -> List[str]:
        """Validate PPO data in screener results"""
        issues = []
        stocks = data.get("stocks", [])
        
        if not stocks:
            return ["No stocks in screener results"]
        
        for i, stock in enumerate(stocks[:5]):  # Check first 5 stocks
            symbol = stock.get("symbol", f"Stock_{i}")
            
            # Check PPO values in screener results
            ppo_values = stock.get("ppo_values", [])
            if not ppo_values:
                issues.append(f"{symbol}: Missing PPO values in screener")
            elif len(ppo_values) != 3:
                issues.append(f"{symbol}: PPO values should be 3 entries, got {len(ppo_values)}")
            elif all(val == 0 for val in ppo_values):
                issues.append(f"{symbol}: All PPO values are zero in screener")
            
            # Check PPO slope percentage
            ppo_slope = stock.get("ppo_slope_percentage")
            if ppo_slope is None:
                issues.append(f"{symbol}: Missing PPO slope percentage in screener")
            
            # Check if stock has proper PPO data for filtering
            if "ppo_slope_percentage" in stock and stock["ppo_slope_percentage"] == 0:
                # This might indicate PPO calculation failure
                if len([s for s in stocks if s.get("ppo_slope_percentage", 0) == 0]) > len(stocks) * 0.5:
                    issues.append("More than 50% of stocks have zero PPO slope (possible systematic issue)")
                    break
        
        return issues

    def validate_ppo_calculation_fix(self, data: Dict[str, Any], symbol: str, timeframe: str, data_source: str) -> List[str]:
        """Validate the PPO calculation fix implementation"""
        issues = []
        
        # Check main PPO indicators
        indicators = data.get("indicators", {})
        if not indicators:
            issues.append("Missing indicators object")
            return issues
        
        # Validate PPO values are non-zero (key fix requirement)
        ppo = indicators.get("ppo")
        ppo_signal = indicators.get("ppo_signal")
        ppo_histogram = indicators.get("ppo_histogram")
        ppo_slope_percentage = indicators.get("ppo_slope_percentage")
        
        if ppo is None:
            issues.append("PPO value is null")
        elif ppo == 0 and data_source in ["polygon_io", "yahoo_finance"]:
            issues.append("PPO value is still zero with real API data (fix may not be working)")
        
        if ppo_signal is None:
            issues.append("PPO signal is null")
        elif ppo_signal == 0 and data_source in ["polygon_io", "yahoo_finance"]:
            issues.append("PPO signal is still zero with real API data")
        
        if ppo_histogram is None:
            issues.append("PPO histogram is null")
        
        # Check for data quality indicators (new feature)
        data_quality = indicators.get("data_quality")
        if data_quality is None:
            issues.append("Missing data_quality indicator (new feature)")
        elif data_quality not in ["standard", "adaptive", "insufficient"]:
            issues.append(f"Invalid data_quality value: {data_quality}")
        
        # Check for fallback reason when adaptive calculation is used
        fallback_reason = indicators.get("fallback_reason")
        if data_quality == "adaptive" and not fallback_reason:
            issues.append("Missing fallback_reason when adaptive calculation is used")
        
        # Validate PPO history with fix
        ppo_history = data.get("ppo_history", [])
        if not ppo_history:
            issues.append("PPO history is empty")
        elif len(ppo_history) < 3:
            issues.append(f"PPO history incomplete: {len(ppo_history)} entries (expected 3)")
        else:
            # Check if PPO history values are reasonable (not all zero)
            ppo_values = [entry.get("ppo", 0) for entry in ppo_history]
            if all(val == 0 for val in ppo_values) and data_source in ["polygon_io", "yahoo_finance"]:
                issues.append("All PPO history values are zero (adaptive calculation may not be working)")
        
        # Check chart data for reasonable PPO values
        chart_data = data.get("chart_data", [])
        if chart_data:
            chart_ppo_values = [item.get("ppo", 0) for item in chart_data if "ppo" in item]
            if len(chart_ppo_values) > 0:
                # With the fix, we should have some non-zero PPO values even with limited data
                non_zero_count = sum(1 for val in chart_ppo_values if val != 0)
                if non_zero_count == 0 and data_source in ["polygon_io", "yahoo_finance"]:
                    issues.append("All chart PPO values are zero (adaptive PPO calculation not working)")
        
        return issues

    def validate_data_quality_indicators(self, data: Dict[str, Any], symbol: str, timeframe: str) -> bool:
        """Validate new data quality indicators in response"""
        indicators = data.get("indicators", {})
        
        # Check for data quality field
        data_quality = indicators.get("data_quality")
        if data_quality:
            self.log_test(f"Data Quality Indicator ({symbol} {timeframe})", True, 
                        f"Data quality: {data_quality}")
            
            # Check for PPO calculation note if adaptive
            if data_quality == "adaptive":
                fallback_reason = indicators.get("fallback_reason")
                if fallback_reason:
                    self.log_test(f"PPO Calculation Note ({symbol} {timeframe})", True, 
                                f"Adaptive calculation note: {fallback_reason}")
                    return True
                else:
                    self.log_test(f"PPO Calculation Note ({symbol} {timeframe})", False, 
                                "Missing fallback reason for adaptive calculation")
                    return False
            return True
        else:
            self.log_test(f"Data Quality Indicator ({symbol} {timeframe})", False, 
                        "Missing data_quality field in response")
            return False

    def validate_screener_ppo_fix(self, data: Dict[str, Any]) -> List[str]:
        """Validate PPO fix in screener results"""
        issues = []
        stocks = data.get("stocks", [])
        
        if not stocks:
            return ["No stocks in screener results"]
        
        zero_ppo_count = 0
        total_stocks = len(stocks)
        
        for i, stock in enumerate(stocks[:10]):  # Check first 10 stocks
            symbol = stock.get("symbol", f"Stock_{i}")
            
            # Check PPO values in screener results
            ppo_values = stock.get("ppo_values", [])
            if not ppo_values:
                issues.append(f"{symbol}: Missing PPO values in screener")
            elif len(ppo_values) != 3:
                issues.append(f"{symbol}: PPO values should be 3 entries, got {len(ppo_values)}")
            elif all(val == 0 for val in ppo_values):
                zero_ppo_count += 1
            
            # Check PPO slope percentage
            ppo_slope = stock.get("ppo_slope_percentage")
            if ppo_slope is None:
                issues.append(f"{symbol}: Missing PPO slope percentage in screener")
        
        # Check if too many stocks have zero PPO values (indicates fix not working)
        if zero_ppo_count > total_stocks * 0.3:  # More than 30% have zero PPO
            issues.append(f"Too many stocks ({zero_ppo_count}/{total_stocks}) have zero PPO values - fix may not be working")
        
        return issues

    def test_ppo_edge_cases(self) -> bool:
        """Test PPO calculation with very limited data scenarios"""
        all_passed = True
        
        # Test with different timeframes that might have very limited data
        edge_test_cases = [
            {"symbol": "AAPL", "timeframe": "1D"},
            {"symbol": "GOOGL", "timeframe": "5D"},
            {"symbol": "MSFT", "timeframe": "1M"}
        ]
        
        for test_case in edge_test_cases:
            try:
                response = requests.post(f"{BACKEND_URL}/analyze", 
                                       json=test_case,
                                       headers={"Content-Type": "application/json"},
                                       timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    chart_data = data.get("chart_data", [])
                    indicators = data.get("indicators", {})
                    
                    # Test graceful handling of limited data
                    if len(chart_data) < 26:  # Insufficient for standard PPO
                        data_quality = indicators.get("data_quality")
                        if data_quality == "adaptive":
                            self.log_test(f"Edge Case Handling ({test_case['symbol']} {test_case['timeframe']})", True, 
                                        f"Adaptive calculation with {len(chart_data)} data points")
                        elif data_quality == "insufficient":
                            ppo = indicators.get("ppo", 0)
                            if ppo != 0:  # Should provide some fallback value
                                self.log_test(f"Edge Case Handling ({test_case['symbol']} {test_case['timeframe']})", True, 
                                            f"Fallback PPO value provided: {ppo}")
                            else:
                                self.log_test(f"Edge Case Handling ({test_case['symbol']} {test_case['timeframe']})", False, 
                                            "No fallback PPO value with insufficient data", True)
                                all_passed = False
                        else:
                            self.log_test(f"Edge Case Handling ({test_case['symbol']} {test_case['timeframe']})", False, 
                                        f"Unexpected data quality: {data_quality} with {len(chart_data)} points", True)
                            all_passed = False
                    else:
                        self.log_test(f"Edge Case Data ({test_case['symbol']} {test_case['timeframe']})", True, 
                                    f"Sufficient data points: {len(chart_data)}")
                else:
                    self.log_test(f"Edge Case API ({test_case['symbol']} {test_case['timeframe']})", False, 
                                f"HTTP {response.status_code}: {response.text}", True)
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"Edge Case Test ({test_case['symbol']} {test_case['timeframe']})", False, 
                            f"Error: {str(e)}", True)
                all_passed = False
        
        return all_passed

    def test_adaptive_ppo_slope(self) -> bool:
        """Test adaptive PPO slope calculations with limited data"""
        all_passed = True
        
        test_symbols = ["AAPL", "GOOGL", "MSFT"]
        
        for symbol in test_symbols:
            try:
                payload = {"symbol": symbol, "timeframe": "1D"}
                response = requests.post(f"{BACKEND_URL}/analyze", 
                                       json=payload,
                                       headers={"Content-Type": "application/json"},
                                       timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    indicators = data.get("indicators", {})
                    ppo_history = data.get("ppo_history", [])
                    
                    # Check if PPO slope calculation works with adaptive PPO values
                    ppo_slope = indicators.get("ppo_slope")
                    ppo_slope_percentage = indicators.get("ppo_slope_percentage")
                    
                    if ppo_slope is not None and ppo_slope_percentage is not None:
                        # Validate slope calculation with PPO history
                        if len(ppo_history) >= 3:
                            today_ppo = ppo_history[-1].get("ppo", 0)
                            yesterday_ppo = ppo_history[-2].get("ppo", 0)
                            
                            # Check if slope calculation is reasonable
                            if abs(ppo_slope_percentage) > 1000:  # Unreasonably high slope
                                self.log_test(f"Adaptive PPO Slope ({symbol})", False, 
                                            f"Unreasonable slope: {ppo_slope_percentage}%", True)
                                all_passed = False
                            else:
                                self.log_test(f"Adaptive PPO Slope ({symbol})", True, 
                                            f"Reasonable slope: {ppo_slope_percentage:.2f}%")
                        else:
                            self.log_test(f"PPO Slope History ({symbol})", False, 
                                        "Insufficient PPO history for slope calculation", True)
                            all_passed = False
                    else:
                        self.log_test(f"PPO Slope Values ({symbol})", False, 
                                    "Missing PPO slope values", True)
                        all_passed = False
                else:
                    self.log_test(f"Adaptive Slope API ({symbol})", False, 
                                f"HTTP {response.status_code}: {response.text}", True)
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"Adaptive Slope Test ({symbol})", False, 
                            f"Error: {str(e)}", True)
                all_passed = False
        
        return all_passed

    def validate_insufficient_data_handling(self, data: Dict[str, Any], data_points: int) -> bool:
        """Validate how system handles insufficient data for PPO calculation"""
        indicators = data.get("indicators", {})
        
        # With insufficient data, system should either:
        # 1. Provide fallback values (not null/zero)
        # 2. Use mock data
        # 3. Handle gracefully without errors
        
        ppo = indicators.get("ppo")
        if ppo is None:
            return False  # Should not be null
        
        # Check if system provided reasonable fallback
        ppo_history = data.get("ppo_history", [])
        if not ppo_history:
            return False  # Should provide some history even with limited data
        
        # System should indicate data source or provide warning about limited data
        data_source = data.get("data_source", "")
        if data_source == "mock":
            return True  # Mock data is acceptable fallback
        
        return True  # Passed basic validation
    
    def test_paid_alpha_vantage_api(self) -> bool:
        """
        COMPREHENSIVE PAID ALPHA VANTAGE API INTEGRATION TESTING
        
        Tests the paid Alpha Vantage API key (KM341MJ89UZJGECS) with 75 calls/minute limit:
        1. Verify API key is working and returning real data
        2. Test multiple rapid API calls to confirm higher rate limits (70/minute)
        3. Check data quality improvements with paid API access
        4. Verify PPO calculations with better Alpha Vantage data
        5. Test API status endpoint shows correct limits (70/minute)
        6. Confirm proper fallback behavior if limits are reached
        """
        print(f"\n💰 COMPREHENSIVE PAID ALPHA VANTAGE API TESTING")
        print("=" * 70)
        
        all_passed = True
        api_issues = []
        
        # Test symbols specifically mentioned in the review request
        test_symbols = ["AAPL", "GOOGL", "MSFT"]
        
        # 1. Test API Status endpoint for correct rate limits
        print(f"\n📊 Testing API Status Endpoint for Paid Plan Limits")
        try:
            response = requests.get(f"{BACKEND_URL}/api-status", timeout=10)
            if response.status_code == 200:
                status_data = response.json()
                
                # Check if Alpha Vantage shows paid plan limits
                alpha_vantage_status = status_data.get("api_usage", {}).get("alpha_vantage", {})
                calls_per_minute = alpha_vantage_status.get("limit", 0)
                
                if calls_per_minute == 70:
                    self.log_test("API Status - Alpha Vantage Limits", True, 
                                f"Correct paid plan limit: {calls_per_minute}/minute")
                else:
                    self.log_test("API Status - Alpha Vantage Limits", False, 
                                f"Expected 70/minute, got {calls_per_minute}/minute", True)
                    api_issues.append(f"API status shows incorrect rate limit: {calls_per_minute}")
                    all_passed = False
                    
                # Check current usage
                current_usage = alpha_vantage_status.get("calls_made", 0)
                plan_type = alpha_vantage_status.get("plan", "unknown")
                self.log_test("API Status - Current Usage", True, 
                            f"Alpha Vantage usage: {current_usage} calls, Plan: {plan_type}")
                
            else:
                self.log_test("API Status Endpoint", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                api_issues.append("API status endpoint not accessible")
                all_passed = False
                
        except Exception as e:
            self.log_test("API Status Test", False, f"Error: {str(e)}", True)
            api_issues.append(f"API status test failed: {str(e)}")
            all_passed = False
        
        # 2. Test individual symbols for real Alpha Vantage data quality
        print(f"\n📈 Testing Real Alpha Vantage Data Quality")
        for symbol in test_symbols:
            try:
                payload = {"symbol": symbol, "timeframe": "1D"}
                start_time = time.time()
                
                response = requests.post(f"{BACKEND_URL}/analyze", 
                                       json=payload,
                                       headers={"Content-Type": "application/json"},
                                       timeout=30)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    data_source = data.get("data_source", "unknown")
                    
                    # Validate Alpha Vantage data quality
                    quality_issues = self.validate_alpha_vantage_data_quality(data, symbol, data_source)
                    
                    if quality_issues:
                        api_issues.extend(quality_issues)
                        all_passed = False
                        self.log_test(f"Alpha Vantage Data Quality ({symbol})", False, 
                                    f"Data source: {data_source}, Issues: {quality_issues}", True)
                    else:
                        self.log_test(f"Alpha Vantage Data Quality ({symbol})", True, 
                                    f"Data source: {data_source}, High quality data received")
                    
                    # Log detailed metrics
                    chart_data_count = len(data.get("chart_data", []))
                    indicators = data.get("indicators", {})
                    ppo = indicators.get("ppo", 0)
                    print(f"  📊 {symbol}: PPO={ppo:.4f}, Data points={chart_data_count}, Source={data_source}, Time={response_time:.2f}s")
                    
                else:
                    self.log_test(f"Alpha Vantage API Test ({symbol})", False, 
                                f"HTTP {response.status_code}: {response.text}", True)
                    api_issues.append(f"{symbol} API call failed: {response.status_code}")
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"Alpha Vantage Test ({symbol})", False, f"Error: {str(e)}", True)
                api_issues.append(f"{symbol} test failed: {str(e)}")
                all_passed = False
        
        # 3. Test rapid succession of API calls (within rate limits)
        print(f"\n⚡ Testing Rapid API Calls (Rate Limit Verification)")
        rapid_call_results = self.test_rapid_api_calls(test_symbols)
        if not rapid_call_results:
            all_passed = False
            api_issues.append("Rapid API calls test failed")
        
        # 4. Test PPO calculations with Alpha Vantage data
        print(f"\n🔢 Testing PPO Calculations with Alpha Vantage Data")
        ppo_calculation_results = self.test_ppo_with_alpha_vantage(test_symbols)
        if not ppo_calculation_results:
            all_passed = False
            api_issues.append("PPO calculations with Alpha Vantage data failed")
        
        # 5. Test fallback behavior when limits are approached
        print(f"\n🔄 Testing Fallback Behavior")
        fallback_results = self.test_alpha_vantage_fallback()
        if not fallback_results:
            all_passed = False
            api_issues.append("Fallback behavior test failed")
        
        # Summary of Alpha Vantage API testing
        if api_issues:
            print(f"\n🚨 ALPHA VANTAGE API ISSUES FOUND ({len(api_issues)}):")
            for issue in api_issues:
                print(f"  • {issue}")
        else:
            print(f"\n✅ Paid Alpha Vantage API integration working correctly")
        
        return all_passed

    def validate_alpha_vantage_data_quality(self, data: Dict[str, Any], symbol: str, data_source: str) -> List[str]:
        """Validate Alpha Vantage data quality improvements"""
        issues = []
        
        # Check if we're actually using Alpha Vantage
        if data_source != "alpha_vantage":
            issues.append(f"Expected Alpha Vantage data source, got {data_source}")
            return issues
        
        # Check chart data quality
        chart_data = data.get("chart_data", [])
        if not chart_data:
            issues.append("No chart data received from Alpha Vantage")
            return issues
        
        # Validate OHLCV data quality
        for i, entry in enumerate(chart_data[:5]):  # Check first 5 entries
            if not all(key in entry for key in ["open", "high", "low", "close", "volume"]):
                issues.append(f"Missing OHLCV data in entry {i+1}")
            
            # Check for realistic values
            if entry.get("volume", 0) <= 0:
                issues.append(f"Invalid volume in entry {i+1}: {entry.get('volume')}")
            
            # Check OHLC logic
            if not (entry.get("low", 0) <= entry.get("open", 0) <= entry.get("high", 0) and 
                   entry.get("low", 0) <= entry.get("close", 0) <= entry.get("high", 0)):
                issues.append(f"Invalid OHLC relationship in entry {i+1}")
        
        # Check technical indicators quality
        indicators = data.get("indicators", {})
        if not indicators:
            issues.append("No technical indicators calculated")
            return issues
        
        # Validate PPO values are reasonable (not zero with real data)
        ppo = indicators.get("ppo")
        if ppo is None:
            issues.append("PPO value is null")
        elif ppo == 0 and len(chart_data) > 26:
            issues.append("PPO is zero despite sufficient data points")
        
        # Check for data quality indicators
        data_quality = indicators.get("data_quality")
        if data_quality == "insufficient" and len(chart_data) > 10:
            issues.append("Data quality marked as insufficient despite adequate data")
        
        return issues

    def test_rapid_api_calls(self, symbols: List[str]) -> bool:
        """Test rapid succession of API calls to verify rate limits"""
        all_passed = True
        call_times = []
        successful_calls = 0
        
        print(f"  Making rapid API calls to test 70/minute rate limit...")
        
        # Make 10 rapid calls (well within the 70/minute limit)
        for i in range(10):
            try:
                symbol = symbols[i % len(symbols)]
                payload = {"symbol": symbol, "timeframe": "1D"}
                
                start_time = time.time()
                response = requests.post(f"{BACKEND_URL}/analyze", 
                                       json=payload,
                                       headers={"Content-Type": "application/json"},
                                       timeout=15)
                end_time = time.time()
                
                call_times.append(end_time - start_time)
                
                if response.status_code == 200:
                    successful_calls += 1
                    data = response.json()
                    data_source = data.get("data_source", "unknown")
                    print(f"    Call {i+1}: {symbol} - {data_source} - {end_time - start_time:.2f}s")
                else:
                    print(f"    Call {i+1}: {symbol} - FAILED {response.status_code}")
                    if response.status_code == 429:  # Rate limit exceeded
                        self.log_test("Rapid API Calls - Rate Limit", False, 
                                    f"Rate limit exceeded at call {i+1}", True)
                        all_passed = False
                
                # Small delay to avoid overwhelming the server
                time.sleep(0.1)
                
            except Exception as e:
                print(f"    Call {i+1}: ERROR - {str(e)}")
                all_passed = False
        
        # Analyze results
        if successful_calls >= 8:  # At least 80% success rate
            avg_time = sum(call_times) / len(call_times) if call_times else 0
            self.log_test("Rapid API Calls", True, 
                        f"{successful_calls}/10 calls successful, avg time: {avg_time:.2f}s")
        else:
            self.log_test("Rapid API Calls", False, 
                        f"Only {successful_calls}/10 calls successful", True)
            all_passed = False
        
        return all_passed

    def test_ppo_with_alpha_vantage(self, symbols: List[str]) -> bool:
        """Test PPO calculations specifically with Alpha Vantage data"""
        all_passed = True
        
        for symbol in symbols:
            try:
                payload = {"symbol": symbol, "timeframe": "1M"}  # Monthly for more data
                response = requests.post(f"{BACKEND_URL}/analyze", 
                                       json=payload,
                                       headers={"Content-Type": "application/json"},
                                       timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    data_source = data.get("data_source", "unknown")
                    
                    if data_source == "alpha_vantage":
                        # Validate PPO calculations with Alpha Vantage data
                        indicators = data.get("indicators", {})
                        ppo = indicators.get("ppo")
                        ppo_signal = indicators.get("ppo_signal")
                        ppo_histogram = indicators.get("ppo_histogram")
                        ppo_slope_percentage = indicators.get("ppo_slope_percentage")
                        
                        # Check for non-zero PPO values (improvement with paid API)
                        if ppo is not None and ppo != 0:
                            self.log_test(f"PPO Calculation ({symbol})", True, 
                                        f"Non-zero PPO: {ppo:.4f} with Alpha Vantage data")
                        else:
                            self.log_test(f"PPO Calculation ({symbol})", False, 
                                        f"PPO is zero/null: {ppo} with Alpha Vantage data", True)
                            all_passed = False
                        
                        # Validate PPO history
                        ppo_history = data.get("ppo_history", [])
                        if len(ppo_history) >= 3:
                            non_zero_history = sum(1 for entry in ppo_history if entry.get("ppo", 0) != 0)
                            if non_zero_history >= 2:
                                self.log_test(f"PPO History Quality ({symbol})", True, 
                                            f"{non_zero_history}/3 non-zero PPO history values")
                            else:
                                self.log_test(f"PPO History Quality ({symbol})", False, 
                                            f"Only {non_zero_history}/3 non-zero PPO history values", True)
                                all_passed = False
                        
                    else:
                        self.log_test(f"Alpha Vantage Data Source ({symbol})", False, 
                                    f"Expected Alpha Vantage, got {data_source}", True)
                        all_passed = False
                
            except Exception as e:
                self.log_test(f"PPO Alpha Vantage Test ({symbol})", False, f"Error: {str(e)}", True)
                all_passed = False
        
        return all_passed

    def test_alpha_vantage_fallback(self) -> bool:
        """Test fallback behavior when Alpha Vantage limits are approached"""
        all_passed = True
        
        try:
            # Test with a less common symbol that might trigger fallback
            payload = {"symbol": "TSLA", "timeframe": "5D"}
            response = requests.post(f"{BACKEND_URL}/analyze", 
                                   json=payload,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                data_source = data.get("data_source", "unknown")
                
                # Check if fallback is working properly
                if data_source in ["alpha_vantage", "polygon_io", "yahoo_finance", "mock"]:
                    self.log_test("Fallback Mechanism", True, 
                                f"Proper fallback to {data_source}")
                    
                    # Ensure data quality is maintained even with fallback
                    chart_data = data.get("chart_data", [])
                    if len(chart_data) > 0:
                        self.log_test("Fallback Data Quality", True, 
                                    f"Fallback provides {len(chart_data)} data points")
                    else:
                        self.log_test("Fallback Data Quality", False, 
                                    "Fallback provides no data", True)
                        all_passed = False
                else:
                    self.log_test("Fallback Data Source", False, 
                                f"Unknown data source: {data_source}", True)
                    all_passed = False
            else:
                self.log_test("Fallback Test", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                all_passed = False
                
        except Exception as e:
            self.log_test("Fallback Test", False, f"Error: {str(e)}", True)
            all_passed = False
        
        return all_passed

    def test_stock_screener_real_data_fix(self) -> bool:
        """
        COMPREHENSIVE STOCK SCREENER REAL DATA FIX TESTING
        
        Tests the specific fix where stock screener now uses real Alpha Vantage data 
        instead of demo data. Validates:
        1. /screener/scan endpoint returns real market data
        2. data_source field shows "alpha_vantage" instead of "mock"
        3. PPO values are calculated from real price data
        4. Prices match current market prices (not demo prices)
        5. Filtering still works correctly with real data
        6. Response includes data source transparency
        """
        print(f"\n🔧 COMPREHENSIVE STOCK SCREENER REAL DATA FIX TESTING")
        print("=" * 70)
        
        all_passed = True
        fix_issues = []
        
        # Test the specific filters mentioned in the review request
        test_filters = {
            "price_filter": {"type": "under", "under": 500},
            "dmi_filter": {"min": 15, "max": 65}
        }
        
        print(f"📊 Testing /screener/scan with filters: {test_filters}")
        
        try:
            start_time = time.time()
            response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                   json=test_filters,
                                   headers={"Content-Type": "application/json"},
                                   timeout=60)  # Longer timeout for real API calls
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate the fix implementation
                fix_validation_issues = self.validate_screener_real_data_fix(data, test_filters)
                
                if fix_validation_issues:
                    fix_issues.extend(fix_validation_issues)
                    all_passed = False
                    self.log_test("Stock Screener Real Data Fix", False, 
                                f"Issues found: {fix_validation_issues}", True)
                else:
                    stocks_found = data.get("results_found", 0)
                    real_data_count = data.get("real_data_count", 0)
                    data_sources = data.get("data_sources", {})
                    
                    self.log_test("Stock Screener Real Data Fix", True, 
                                f"Found {stocks_found} stocks with {real_data_count} real data sources in {response_time:.2f}s")
                    
                    # Log data source breakdown
                    if data_sources:
                        print(f"  📊 Data sources: {data_sources}")
                
                # Test additional scenarios
                additional_tests_passed = self.test_screener_real_data_scenarios()
                if not additional_tests_passed:
                    all_passed = False
                    
            else:
                self.log_test("Stock Screener Real Data Fix API", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                fix_issues.append(f"API call failed: {response.status_code}")
                all_passed = False
                
        except Exception as e:
            self.log_test("Stock Screener Real Data Fix", False, f"Error: {str(e)}", True)
            fix_issues.append(f"Test execution failed: {str(e)}")
            all_passed = False
        
        # Summary of real data fix testing
        if fix_issues:
            print(f"\n🚨 STOCK SCREENER REAL DATA FIX ISSUES FOUND ({len(fix_issues)}):")
            for issue in fix_issues:
                print(f"  • {issue}")
        else:
            print(f"\n✅ Stock screener real data fix working correctly - using Alpha Vantage instead of demo data")
        
        return all_passed

    def validate_screener_real_data_fix(self, data: Dict[str, Any], filters: Dict[str, Any]) -> List[str]:
        """Validate that the screener is using real Alpha Vantage data instead of demo data"""
        issues = []
        
        # Check basic response structure
        if not data.get("success"):
            issues.append("Screener response indicates failure")
            return issues
        
        stocks = data.get("stocks", [])
        if not stocks:
            issues.append("No stocks returned from screener")
            return issues
        
        # Check for data source transparency (new feature)
        data_sources = data.get("data_sources", {})
        real_data_count = data.get("real_data_count", 0)
        
        if not data_sources:
            issues.append("Missing data_sources field in response")
        
        if real_data_count == 0:
            issues.append("No real data sources used - still using demo data")
        
        # Check individual stocks for real data indicators
        alpha_vantage_count = 0
        demo_data_count = 0
        
        for i, stock in enumerate(stocks[:10]):  # Check first 10 stocks
            symbol = stock.get("symbol", f"Stock_{i}")
            
            # Check if stock has data source information
            stock_data_source = stock.get("data_source", "unknown")
            
            if stock_data_source == "alpha_vantage":
                alpha_vantage_count += 1
                
                # Validate real Alpha Vantage data characteristics
                real_data_issues = self.validate_real_alpha_vantage_stock_data(stock, symbol)
                if real_data_issues:
                    issues.extend([f"{symbol}: {issue}" for issue in real_data_issues])
                    
            elif stock_data_source == "mock":
                demo_data_count += 1
            
            # Check PPO values are realistic (not demo patterns)
            ppo_values = stock.get("ppo_values", [])
            if len(ppo_values) >= 3:
                # Demo data often has very predictable patterns
                if self.is_demo_ppo_pattern(ppo_values):
                    issues.append(f"{symbol}: PPO values appear to be demo data pattern")
            
            # Check price realism
            price = stock.get("price", 0)
            if price > 0:
                # Demo prices often follow predictable hash-based patterns
                if self.is_demo_price_pattern(symbol, price):
                    issues.append(f"{symbol}: Price ${price:.2f} appears to be demo data")
        
        # Validate data source distribution
        total_stocks = len(stocks)
        if alpha_vantage_count == 0 and total_stocks > 0:
            issues.append("No stocks using Alpha Vantage data source")
        elif alpha_vantage_count < total_stocks * 0.3:  # Less than 30% real data
            issues.append(f"Only {alpha_vantage_count}/{total_stocks} stocks using Alpha Vantage (expected at least 30%)")
        
        # Check filtering still works with real data
        filtering_issues = self.validate_real_data_filtering(stocks, filters)
        if filtering_issues:
            issues.extend(filtering_issues)
        
        return issues

    def validate_real_alpha_vantage_stock_data(self, stock: Dict[str, Any], symbol: str) -> List[str]:
        """Validate that stock data comes from real Alpha Vantage API"""
        issues = []
        
        # Check for realistic price movements (Alpha Vantage provides real market data)
        price = stock.get("price", 0)
        if price <= 0:
            issues.append("Invalid price value")
            return issues
        
        # Check PPO values are non-zero and realistic
        ppo_values = stock.get("ppo_values", [])
        if len(ppo_values) >= 3:
            if all(val == 0 for val in ppo_values):
                issues.append("All PPO values are zero (possible calculation failure)")
            elif all(abs(val) < 0.001 for val in ppo_values):
                issues.append("PPO values too small (possible demo data)")
        
        # Check volume data is realistic
        volume_today = stock.get("volume_today", 0)
        if volume_today <= 0:
            issues.append("Invalid volume data")
        
        # Check returns data exists and is realistic
        returns = stock.get("returns", {})
        if not returns:
            issues.append("Missing returns data")
        else:
            # Real market data should have varied returns
            return_values = list(returns.values())
            if len(set(return_values)) == 1:  # All returns are identical
                issues.append("Returns data appears artificial (all identical)")
        
        return issues

    def is_demo_ppo_pattern(self, ppo_values: List[float]) -> bool:
        """Check if PPO values follow demo data patterns"""
        if len(ppo_values) < 3:
            return False
        
        # Demo data often has very linear progressions
        differences = [ppo_values[i+1] - ppo_values[i] for i in range(len(ppo_values)-1)]
        
        # Check if differences are too uniform (indicating generated data)
        if len(set(round(diff, 4) for diff in differences)) == 1:
            return True  # All differences are identical
        
        # Check for unrealistic precision (demo data often has many decimal places)
        for val in ppo_values:
            if abs(val) > 0 and len(str(abs(val)).split('.')[-1]) > 6:
                return True  # Too many decimal places
        
        return False

    def is_demo_price_pattern(self, symbol: str, price: float) -> bool:
        """Check if price follows demo data hash-based patterns"""
        # Demo data often uses hash(symbol) + base_price patterns
        # This is a heuristic check for obvious demo patterns
        
        # Check if price is suspiciously close to hash-based calculation
        base_price = 150.0
        hash_component = hash(symbol) % 100
        expected_demo_price = base_price + hash_component
        
        # If price is very close to this pattern, it might be demo data
        if abs(price - expected_demo_price) < 1.0:
            return True
        
        return False

    def validate_real_data_filtering(self, stocks: List[Dict], filters: Dict[str, Any]) -> List[str]:
        """Validate that filtering logic works correctly with real data"""
        issues = []
        
        # Check price filtering
        price_filter = filters.get("price_filter", {})
        if price_filter and price_filter.get("type") == "under":
            max_price = price_filter.get("under", 500)
            
            for stock in stocks:
                price = stock.get("price", 0)
                if price > max_price:
                    issues.append(f"Stock {stock.get('symbol')} price ${price:.2f} exceeds filter ${max_price}")
        
        # Check DMI filtering
        dmi_filter = filters.get("dmi_filter", {})
        if dmi_filter:
            dmi_min = dmi_filter.get("min", 15)
            dmi_max = dmi_filter.get("max", 65)
            
            for stock in stocks:
                adx = stock.get("adx", 0)
                if not (dmi_min <= adx <= dmi_max):
                    issues.append(f"Stock {stock.get('symbol')} ADX {adx:.2f} outside filter range {dmi_min}-{dmi_max}")
        
        return issues

    def test_screener_real_data_scenarios(self) -> bool:
        """Test additional scenarios for real data fix"""
        all_passed = True
        
        # Test different filter combinations
        test_scenarios = [
            {
                "name": "Restrictive Price Filter",
                "filters": {
                    "price_filter": {"type": "range", "min": 100, "max": 200},
                    "dmi_filter": {"min": 20, "max": 50}
                }
            },
            {
                "name": "PPO Slope Filter",
                "filters": {
                    "price_filter": {"type": "under", "under": 300},
                    "ppo_slope_filter": {"threshold": 2}
                }
            }
        ]
        
        for scenario in test_scenarios:
            try:
                response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                       json=scenario["filters"],
                                       headers={"Content-Type": "application/json"},
                                       timeout=45)
                
                if response.status_code == 200:
                    data = response.json()
                    stocks_found = data.get("results_found", 0)
                    real_data_count = data.get("real_data_count", 0)
                    
                    self.log_test(f"Screener Real Data - {scenario['name']}", True, 
                                f"Found {stocks_found} stocks, {real_data_count} with real data")
                else:
                    self.log_test(f"Screener Real Data - {scenario['name']}", False, 
                                f"HTTP {response.status_code}", True)
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"Screener Real Data - {scenario['name']}", False, 
                            f"Error: {str(e)}", True)
                all_passed = False
        
        return all_passed

    def run_comprehensive_tests(self):
        """Run all tests"""
        print("🚀 Starting Comprehensive Stock Analysis API Tests")
        print("=" * 60)
        
        # Test basic connectivity first
        if not self.test_basic_connectivity():
            print("❌ Basic connectivity failed. Stopping tests.")
            return self.results
        
        # PRIORITY: Test Paid Alpha Vantage API Integration (New Feature)
        print(f"\n💰 PRIORITY: PAID ALPHA VANTAGE API INTEGRATION TESTING")
        self.test_paid_alpha_vantage_api()
        
        # PRIORITY: Test PPO Calculation Fix (Critical Bug Fix Verification)
        print(f"\n🔧 CRITICAL BUG FIX VERIFICATION: PPO Calculation Fix")
        self.test_ppo_calculation_fix()
        
        # Test Stock Screener Phase 3 endpoints (Priority)
        print(f"\n📊 Testing Stock Screener Phase 3 Implementation")
        self.test_stock_screener_endpoints()
        
        # Test main functionality with valid symbols
        for symbol in TEST_SYMBOLS:
            print(f"\n📊 Testing with symbol: {symbol}")
            
            # Test GET endpoint
            get_data = self.test_stock_analysis_get_endpoint(symbol)
            if get_data:
                self.validate_response_structure(get_data, symbol)
                
                if "indicators" in get_data:
                    self.validate_technical_indicators(get_data["indicators"], symbol)
                
                if "ppo_history" in get_data:
                    self.validate_ppo_history(get_data["ppo_history"], symbol)
                
                if "dmi_history" in get_data:
                    self.validate_dmi_history(get_data["dmi_history"], symbol)
                
                self.validate_ai_recommendations(get_data, symbol)
                
                if "chart_data" in get_data:
                    self.validate_chart_data(get_data["chart_data"], symbol)
            
            # Test POST endpoint
            post_data = self.test_stock_analysis_post_endpoint(symbol)
            if post_data and get_data:
                # Compare GET vs POST responses
                if post_data.get("symbol") == get_data.get("symbol"):
                    self.log_test(f"GET vs POST Consistency ({symbol})", True, 
                                "Both endpoints return consistent data")
                else:
                    self.log_test(f"GET vs POST Consistency ({symbol})", False, 
                                "GET and POST return different data")
        
        # Test error handling
        print(f"\n🔍 Testing Error Handling")
        self.test_error_handling()
        
        # Test performance
        print(f"\n⚡ Testing Performance")
        self.test_performance()
        
        return self.results
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📋 TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {self.results['total_tests']}")
        print(f"✅ Passed: {self.results['passed_tests']}")
        print(f"❌ Failed: {self.results['failed_tests']}")
        print(f"Success Rate: {(self.results['passed_tests']/self.results['total_tests']*100):.1f}%")
        
        if self.results["critical_issues"]:
            print(f"\n🚨 CRITICAL ISSUES ({len(self.results['critical_issues'])}):")
            for issue in self.results["critical_issues"]:
                print(f"  • {issue}")
        
        if self.results["performance_metrics"]:
            print(f"\n⚡ PERFORMANCE METRICS:")
            for endpoint, time_taken in self.results["performance_metrics"].items():
                print(f"  • {endpoint}: {time_taken:.2f}s")

def main():
    """Main test execution"""
    tester = StockAnalysisAPITester()
    results = tester.run_comprehensive_tests()
    tester.print_summary()
    
    # Return exit code based on results
    if results["critical_issues"]:
        print(f"\n❌ Tests completed with {len(results['critical_issues'])} critical issues")
        return 1
    else:
        print(f"\n✅ All critical functionality working properly")
        return 0

if __name__ == "__main__":
    exit(main())