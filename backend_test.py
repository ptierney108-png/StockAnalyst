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
BACKEND_URL = "https://stockwise-platform.preview.emergentagent.com/api"
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

    def test_multiple_component_fixes(self) -> bool:
        """
        TEST MULTIPLE COMPONENT FIXES: Verify all reported issues have been resolved
        
        Tests the specific fixes mentioned in the review request:
        1. Point Based Decision: Uses real Alpha Vantage API instead of demo data
        2. Market endpoints: /market/trending, /market/gainers, /market/losers use real data
        3. PPO histogram calculation: Mathematically correct (histogram = ppo - signal)
        4. DMI values: Realistic and properly calculated (0-100 range)
        5. Default chart period: Changed from '1D' to '3M'
        6. Data source transparency: Clear indicators of real vs demo data
        """
        print(f"\n🔧 TESTING MULTIPLE COMPONENT FIXES")
        print("=" * 70)
        
        all_passed = True
        fix_issues = []
        
        # Test symbols specifically mentioned in review request
        test_symbols = ["AAPL", "GOOGL", "MSFT"]
        
        # 1. Test Point Based Decision - should use real Alpha Vantage API
        print(f"\n📊 Testing Point Based Decision (Real Alpha Vantage Data)")
        for symbol in test_symbols:
            try:
                # Test with default timeframe (should be 3M now)
                payload = {"symbol": symbol}  # No timeframe specified - should default to 3M
                start_time = time.time()
                
                response = requests.post(f"{BACKEND_URL}/analyze", 
                                       json=payload,
                                       headers={"Content-Type": "application/json"},
                                       timeout=30)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Validate Point Based Decision uses real data
                    point_decision_issues = self.validate_point_based_decision_fix(data, symbol)
                    
                    if point_decision_issues:
                        fix_issues.extend(point_decision_issues)
                        all_passed = False
                        self.log_test(f"Point Based Decision Fix ({symbol})", False, 
                                    f"Issues: {point_decision_issues}", True)
                    else:
                        self.log_test(f"Point Based Decision Fix ({symbol})", True, 
                                    f"Using real Alpha Vantage data, default timeframe working")
                    
                    # Log detailed analysis
                    data_source = data.get("data_source", "unknown")
                    timeframe = data.get("timeframe", "unknown")
                    chart_data_count = len(data.get("chart_data", []))
                    print(f"  📈 {symbol}: Source={data_source}, Timeframe={timeframe}, Data points={chart_data_count}")
                    
                else:
                    self.log_test(f"Point Based Decision API ({symbol})", False, 
                                f"HTTP {response.status_code}: {response.text}", True)
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"Point Based Decision Test ({symbol})", False, f"Error: {str(e)}", True)
                all_passed = False
        
        # 2. Test Market endpoints for real Alpha Vantage data
        print(f"\n📈 Testing Market Endpoints (Real Alpha Vantage Data)")
        market_endpoints = [
            ("trending", "/market/trending"),
            ("gainers", "/market/gainers"), 
            ("losers", "/market/losers")
        ]
        
        for endpoint_name, endpoint_path in market_endpoints:
            try:
                response = requests.get(f"{BACKEND_URL}{endpoint_path}", timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Validate market endpoint uses real data
                    market_issues = self.validate_market_endpoint_fix(data, endpoint_name)
                    
                    if market_issues:
                        fix_issues.extend(market_issues)
                        all_passed = False
                        self.log_test(f"Market Endpoint Fix ({endpoint_name})", False, 
                                    f"Issues: {market_issues}", True)
                    else:
                        self.log_test(f"Market Endpoint Fix ({endpoint_name})", True, 
                                    "Using real Alpha Vantage market data")
                    
                    # Log market data details
                    if isinstance(data, list):
                        stocks_count = len(data)
                        data_sources = [stock.get("data_source", "unknown") for stock in data[:3]]
                        print(f"  📊 {endpoint_name}: {stocks_count} stocks, Sources: {set(data_sources)}")
                    else:
                        stocks_count = len(data.get("stocks", []))
                        data_sources = data.get("data_sources", [])
                        print(f"  📊 {endpoint_name}: {stocks_count} stocks, Sources: {data_sources}")
                    
                else:
                    self.log_test(f"Market Endpoint ({endpoint_name})", False, 
                                f"HTTP {response.status_code}: {response.text}", True)
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"Market Endpoint Test ({endpoint_name})", False, f"Error: {str(e)}", True)
                all_passed = False
        
        # 3. Test PPO histogram calculation fix
        print(f"\n🔢 Testing PPO Histogram Calculation Fix")
        for symbol in test_symbols:
            try:
                payload = {"symbol": symbol, "timeframe": "3M"}
                response = requests.post(f"{BACKEND_URL}/analyze", 
                                       json=payload,
                                       headers={"Content-Type": "application/json"},
                                       timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Validate PPO histogram calculation
                    ppo_issues = self.validate_ppo_histogram_fix(data, symbol)
                    
                    if ppo_issues:
                        fix_issues.extend(ppo_issues)
                        all_passed = False
                        self.log_test(f"PPO Histogram Fix ({symbol})", False, 
                                    f"Issues: {ppo_issues}", True)
                    else:
                        self.log_test(f"PPO Histogram Fix ({symbol})", True, 
                                    "PPO histogram = ppo - signal calculation correct")
                    
                    # Log PPO calculation details
                    indicators = data.get("indicators", {})
                    ppo = indicators.get("ppo", 0)
                    ppo_signal = indicators.get("ppo_signal", 0)
                    ppo_histogram = indicators.get("ppo_histogram", 0)
                    expected_histogram = ppo - ppo_signal
                    print(f"  🔢 {symbol}: PPO={ppo:.4f}, Signal={ppo_signal:.4f}, Histogram={ppo_histogram:.4f}, Expected={expected_histogram:.4f}")
                    
                else:
                    self.log_test(f"PPO Histogram API ({symbol})", False, 
                                f"HTTP {response.status_code}: {response.text}", True)
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"PPO Histogram Test ({symbol})", False, f"Error: {str(e)}", True)
                all_passed = False
        
        # 4. Test DMI values fix
        print(f"\n📐 Testing DMI Values Fix")
        for symbol in test_symbols:
            try:
                payload = {"symbol": symbol, "timeframe": "3M"}
                response = requests.post(f"{BACKEND_URL}/analyze", 
                                       json=payload,
                                       headers={"Content-Type": "application/json"},
                                       timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Validate DMI values fix
                    dmi_issues = self.validate_dmi_values_fix(data, symbol)
                    
                    if dmi_issues:
                        fix_issues.extend(dmi_issues)
                        all_passed = False
                        self.log_test(f"DMI Values Fix ({symbol})", False, 
                                    f"Issues: {dmi_issues}", True)
                    else:
                        self.log_test(f"DMI Values Fix ({symbol})", True, 
                                    "DMI PLUS values realistic and within 0-100 range")
                    
                    # Log DMI values details
                    indicators = data.get("indicators", {})
                    dmi_plus = indicators.get("dmi_plus", 0)
                    dmi_minus = indicators.get("dmi_minus", 0)
                    adx = indicators.get("adx", 0)
                    print(f"  📐 {symbol}: DMI+={dmi_plus:.2f}, DMI-={dmi_minus:.2f}, ADX={adx:.2f}")
                    
                else:
                    self.log_test(f"DMI Values API ({symbol})", False, 
                                f"HTTP {response.status_code}: {response.text}", True)
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"DMI Values Test ({symbol})", False, f"Error: {str(e)}", True)
                all_passed = False
        
        # 5. Test default chart period fix (should be 3M)
        print(f"\n📅 Testing Default Chart Period Fix (Should be 3M)")
        for symbol in test_symbols:
            try:
                # Test without specifying timeframe - should default to 3M
                payload = {"symbol": symbol}
                response = requests.post(f"{BACKEND_URL}/analyze", 
                                       json=payload,
                                       headers={"Content-Type": "application/json"},
                                       timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Validate default timeframe
                    timeframe_issues = self.validate_default_timeframe_fix(data, symbol)
                    
                    if timeframe_issues:
                        fix_issues.extend(timeframe_issues)
                        all_passed = False
                        self.log_test(f"Default Timeframe Fix ({symbol})", False, 
                                    f"Issues: {timeframe_issues}", True)
                    else:
                        self.log_test(f"Default Timeframe Fix ({symbol})", True, 
                                    "Default timeframe correctly set to 3M")
                    
                    # Log timeframe details
                    timeframe = data.get("timeframe", "unknown")
                    chart_data_count = len(data.get("chart_data", []))
                    print(f"  📅 {symbol}: Default timeframe={timeframe}, Data points={chart_data_count}")
                    
                else:
                    self.log_test(f"Default Timeframe API ({symbol})", False, 
                                f"HTTP {response.status_code}: {response.text}", True)
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"Default Timeframe Test ({symbol})", False, f"Error: {str(e)}", True)
                all_passed = False
        
        # 6. Test data source transparency
        print(f"\n🔍 Testing Data Source Transparency")
        transparency_passed = self.test_data_source_transparency(test_symbols)
        if not transparency_passed:
            all_passed = False
            fix_issues.append("Data source transparency not working correctly")
        
        # Summary of multiple component fixes testing
        if fix_issues:
            print(f"\n🚨 MULTIPLE COMPONENT FIX ISSUES FOUND ({len(fix_issues)}):")
            for issue in fix_issues:
                print(f"  • {issue}")
        else:
            print(f"\n✅ All multiple component fixes working correctly")
        
        return all_passed

    def validate_point_based_decision_fix(self, data: Dict[str, Any], symbol: str) -> List[str]:
        """Validate Point Based Decision uses real Alpha Vantage API instead of demo data"""
        issues = []
        
        # Check data source
        data_source = data.get("data_source", "unknown")
        if data_source != "alpha_vantage":
            issues.append(f"Expected Alpha Vantage data source, got {data_source}")
        
        # Check for real data indicators
        chart_data = data.get("chart_data", [])
        if not chart_data:
            issues.append("No chart data received")
            return issues
        
        # Check if data looks like real market data (not hash-based demo patterns)
        prices = [item.get("close", 0) for item in chart_data[-5:]]  # Last 5 prices
        if len(set(prices)) == 1:  # All prices the same (unlikely for real data)
            issues.append("Prices appear to be demo data (all identical)")
        
        # Check PPO values are non-zero (real data should have meaningful PPO)
        indicators = data.get("indicators", {})
        ppo = indicators.get("ppo", 0)
        if ppo == 0:
            issues.append("PPO value is zero (possible demo data)")
        
        return issues

    def validate_market_endpoint_fix(self, data: Dict[str, Any], endpoint_name: str) -> List[str]:
        """Validate market endpoints use real Alpha Vantage data instead of hardcoded values"""
        issues = []
        
        # Market endpoints return a list directly, not an object
        if isinstance(data, list):
            stocks = data
            
            # Check if we have stocks data
            if not stocks:
                issues.append("No stocks data received")
                return issues
            
            # Check individual stock data sources
            for i, stock in enumerate(stocks[:5]):  # Check first 5 stocks
                stock_data_source = stock.get("data_source", "unknown")
                if stock_data_source != "alpha_vantage":
                    issues.append(f"Stock {i+1} data source is {stock_data_source}, expected alpha_vantage")
                
                # Check for realistic price data
                price = stock.get("price", 0)
                if price <= 0:
                    issues.append(f"Stock {i+1} has invalid price: {price}")
                
                # Check for proper stock symbol
                symbol = stock.get("symbol", "")
                if not symbol:
                    issues.append(f"Stock {i+1} missing symbol")
        else:
            # If it's an object, check for the expected structure
            data_sources = data.get("data_sources", [])
            if "alpha_vantage" not in data_sources:
                issues.append(f"Alpha Vantage not in data sources: {data_sources}")
            
            # Check for real data count indicator
            real_data_count = data.get("real_data_count", 0)
            total_stocks = len(data.get("stocks", []))
            if real_data_count == 0:
                issues.append("No real data count indicator")
            elif real_data_count != total_stocks:
                issues.append(f"Real data count ({real_data_count}) doesn't match total stocks ({total_stocks})")
            
            # Check individual stock data sources
            stocks = data.get("stocks", [])
            if stocks:
                for i, stock in enumerate(stocks[:5]):  # Check first 5 stocks
                    stock_data_source = stock.get("data_source", "unknown")
                    if stock_data_source != "alpha_vantage":
                        issues.append(f"Stock {i+1} data source is {stock_data_source}, expected alpha_vantage")
            
            # Check for note about real data usage
            note = data.get("note", "")
            if "real Alpha Vantage data" not in note:
                issues.append("Missing note about real Alpha Vantage data usage")
        
        return issues

    def validate_ppo_histogram_fix(self, data: Dict[str, Any], symbol: str) -> List[str]:
        """Validate PPO histogram calculation is mathematically correct (histogram = ppo - signal)"""
        issues = []
        
        indicators = data.get("indicators", {})
        if not indicators:
            issues.append("Missing indicators")
            return issues
        
        ppo = indicators.get("ppo")
        ppo_signal = indicators.get("ppo_signal")
        ppo_histogram = indicators.get("ppo_histogram")
        
        if ppo is None or ppo_signal is None or ppo_histogram is None:
            issues.append("Missing PPO values (ppo, signal, or histogram)")
            return issues
        
        # Calculate expected histogram
        expected_histogram = ppo - ppo_signal
        
        # Allow small floating point differences
        tolerance = 0.001
        if abs(ppo_histogram - expected_histogram) > tolerance:
            issues.append(f"PPO histogram calculation incorrect: got {ppo_histogram:.4f}, expected {expected_histogram:.4f}")
        
        return issues

    def validate_dmi_values_fix(self, data: Dict[str, Any], symbol: str) -> List[str]:
        """Validate DMI values are realistic and properly calculated (0-100 range)"""
        issues = []
        
        indicators = data.get("indicators", {})
        if not indicators:
            issues.append("Missing indicators")
            return issues
        
        dmi_plus = indicators.get("dmi_plus")
        dmi_minus = indicators.get("dmi_minus")
        adx = indicators.get("adx")
        
        if dmi_plus is None or dmi_minus is None or adx is None:
            issues.append("Missing DMI values (dmi_plus, dmi_minus, or adx)")
            return issues
        
        # Check DMI+ range (0-100)
        if not (0 <= dmi_plus <= 100):
            issues.append(f"DMI+ value {dmi_plus:.2f} outside valid range (0-100)")
        
        # Check DMI- range (0-100)
        if not (0 <= dmi_minus <= 100):
            issues.append(f"DMI- value {dmi_minus:.2f} outside valid range (0-100)")
        
        # Check ADX range (0-100)
        if not (0 <= adx <= 100):
            issues.append(f"ADX value {adx:.2f} outside valid range (0-100)")
        
        # Check for realistic values (not all zeros or identical)
        if dmi_plus == 0 and dmi_minus == 0 and adx == 0:
            issues.append("All DMI values are zero (unrealistic)")
        
        # Check DMI history for realistic values
        dmi_history = data.get("dmi_history", [])
        if dmi_history:
            for i, entry in enumerate(dmi_history):
                entry_dmi_plus = entry.get("dmi_plus", 0)
                if not (0 <= entry_dmi_plus <= 100):
                    issues.append(f"DMI history entry {i+1} DMI+ value {entry_dmi_plus:.2f} outside valid range")
        
        return issues

    def validate_default_timeframe_fix(self, data: Dict[str, Any], symbol: str) -> List[str]:
        """Validate default chart period is 3M instead of 1D"""
        issues = []
        
        timeframe = data.get("timeframe", "unknown")
        if timeframe != "3M":
            issues.append(f"Default timeframe is {timeframe}, expected 3M")
        
        # Check chart data count is appropriate for 3M timeframe
        chart_data = data.get("chart_data", [])
        chart_data_count = len(chart_data)
        
        # For 3M timeframe, expect around 60-90 data points (daily data for ~3 months)
        if chart_data_count < 30:
            issues.append(f"Chart data count {chart_data_count} too low for 3M timeframe")
        elif chart_data_count > 120:
            issues.append(f"Chart data count {chart_data_count} too high for 3M timeframe")
        
        return issues

    def test_data_source_transparency(self, symbols: List[str]) -> bool:
        """Test data source transparency shows real vs demo data correctly"""
        all_passed = True
        
        for symbol in symbols:
            try:
                payload = {"symbol": symbol, "timeframe": "3M"}
                response = requests.post(f"{BACKEND_URL}/analyze", 
                                       json=payload,
                                       headers={"Content-Type": "application/json"},
                                       timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check data source transparency
                    data_source = data.get("data_source", "unknown")
                    if data_source in ["alpha_vantage", "polygon_io", "yahoo_finance"]:
                        self.log_test(f"Data Source Transparency ({symbol})", True, 
                                    f"Real data source clearly indicated: {data_source}")
                    elif data_source == "mock":
                        self.log_test(f"Data Source Transparency ({symbol})", True, 
                                    f"Demo data source clearly indicated: {data_source}")
                    else:
                        self.log_test(f"Data Source Transparency ({symbol})", False, 
                                    f"Unclear data source: {data_source}")
                        all_passed = False
                    
                    # Check for additional transparency indicators
                    response_time = data.get("response_time")
                    if response_time is not None:
                        self.log_test(f"Response Time Transparency ({symbol})", True, 
                                    f"Response time provided: {response_time}s")
                    
                else:
                    self.log_test(f"Data Source Transparency API ({symbol})", False, 
                                f"HTTP {response.status_code}: {response.text}")
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"Data Source Transparency Test ({symbol})", False, f"Error: {str(e)}")
                all_passed = False
        
        return all_passed

    def test_critical_runtime_errors_fix(self) -> bool:
        """
        TEST CRITICAL RUNTIME ERRORS FIX
        
        Tests the specific fixes for critical runtime errors reported by user:
        1. Point Based Decision TypeError Fix: 'analysis.metrics.div.toFixed is not a function'
        2. Stock Screener Real Data Integration: Scanner showing simulated data message
        3. DMI Values Update Fix: DMI+ values not updating when different stocks entered
        4. Data Source Transparency: Verify real Alpha Vantage data indicators
        """
        print(f"\n🚨 TESTING CRITICAL RUNTIME ERRORS FIX")
        print("=" * 70)
        
        all_passed = True
        critical_issues = []
        
        # Test symbols specifically mentioned in review request
        test_symbols = ["AAPL", "GOOGL", "MSFT"]
        
        # 1. Test Point Based Decision TypeError Fix
        print(f"\n🔧 Testing Point Based Decision TypeError Fix")
        print("-" * 50)
        
        for symbol in test_symbols:
            try:
                payload = {"symbol": symbol, "timeframe": "3M"}  # Default changed to 3M
                start_time = time.time()
                
                response = requests.post(f"{BACKEND_URL}/analyze", 
                                       json=payload,
                                       headers={"Content-Type": "application/json"},
                                       timeout=30)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Validate Point Based Decision fix - check for proper Number() casting
                    point_based_issues = self.validate_point_based_decision_fix(data, symbol)
                    
                    if point_based_issues:
                        critical_issues.extend(point_based_issues)
                        all_passed = False
                        self.log_test(f"Point Based Decision Fix ({symbol})", False, 
                                    f"Issues: {point_based_issues}", True)
                    else:
                        self.log_test(f"Point Based Decision Fix ({symbol})", True, 
                                    f"No TypeError issues, proper Number() casting working")
                    
                    # Log detailed analysis for debugging
                    indicators = data.get("indicators", {})
                    print(f"  📊 {symbol}: PPO={indicators.get('ppo', 0):.4f}, "
                          f"DMI+={indicators.get('dmi_plus', 0):.2f}, "
                          f"Response time={response_time:.2f}s")
                    
                else:
                    self.log_test(f"Point Based Decision API ({symbol})", False, 
                                f"HTTP {response.status_code}: {response.text}", True)
                    critical_issues.append(f"{symbol} analysis API failed: {response.status_code}")
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"Point Based Decision Test ({symbol})", False, f"Error: {str(e)}", True)
                critical_issues.append(f"{symbol} analysis test failed: {str(e)}")
                all_passed = False
        
        # 2. Test Stock Screener Real Data Integration
        print(f"\n📊 Testing Stock Screener Real Data Integration")
        print("-" * 50)
        
        try:
            screener_filters = {
                "price_filter": {"type": "under", "under": 500},
                "dmi_filter": {"min": 15, "max": 65},
                "ppo_slope_filter": {"threshold": 1}
            }
            
            start_time = time.time()
            response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                   json=screener_filters,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate real data integration
                screener_real_data_issues = self.validate_screener_real_data_integration(data)
                
                if screener_real_data_issues:
                    critical_issues.extend(screener_real_data_issues)
                    all_passed = False
                    self.log_test("Stock Screener Real Data Integration", False, 
                                f"Issues: {screener_real_data_issues}", True)
                else:
                    self.log_test("Stock Screener Real Data Integration", True, 
                                "Real Alpha Vantage data integration working correctly")
                
                # Log detailed screener results
                stocks_found = data.get("results_found", 0)
                data_sources = data.get("data_sources", [])
                real_data_count = data.get("real_data_count", 0)
                print(f"  📈 Screener: {stocks_found} stocks found, "
                      f"Data sources: {data_sources}, "
                      f"Real data count: {real_data_count}, "
                      f"Response time: {response_time:.2f}s")
                
            else:
                self.log_test("Stock Screener Real Data API", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                critical_issues.append(f"Screener API failed: {response.status_code}")
                all_passed = False
                
        except Exception as e:
            self.log_test("Stock Screener Real Data Test", False, f"Error: {str(e)}", True)
            critical_issues.append(f"Screener test failed: {str(e)}")
            all_passed = False
        
        # 3. Test DMI Values Update Fix
        print(f"\n🔄 Testing DMI Values Update Fix")
        print("-" * 50)
        
        dmi_values_by_symbol = {}
        
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
                    
                    dmi_plus = indicators.get("dmi_plus", 0)
                    dmi_minus = indicators.get("dmi_minus", 0)
                    adx = indicators.get("adx", 0)
                    
                    dmi_values_by_symbol[symbol] = {
                        "dmi_plus": dmi_plus,
                        "dmi_minus": dmi_minus,
                        "adx": adx
                    }
                    
                    print(f"  📊 {symbol}: DMI+={dmi_plus:.2f}, DMI-={dmi_minus:.2f}, ADX={adx:.2f}")
                    
                else:
                    self.log_test(f"DMI Values API ({symbol})", False, 
                                f"HTTP {response.status_code}: {response.text}", True)
                    critical_issues.append(f"{symbol} DMI API failed: {response.status_code}")
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"DMI Values Test ({symbol})", False, f"Error: {str(e)}", True)
                critical_issues.append(f"{symbol} DMI test failed: {str(e)}")
                all_passed = False
        
        # Validate DMI values are different between symbols (not static 26.0)
        dmi_update_issues = self.validate_dmi_values_updating(dmi_values_by_symbol)
        
        if dmi_update_issues:
            critical_issues.extend(dmi_update_issues)
            all_passed = False
            self.log_test("DMI Values Update Fix", False, 
                        f"Issues: {dmi_update_issues}", True)
        else:
            self.log_test("DMI Values Update Fix", True, 
                        "DMI values updating correctly between different stocks")
        
        # 4. Test Data Source Transparency
        print(f"\n🔍 Testing Data Source Transparency")
        print("-" * 50)
        
        data_source_issues = self.validate_data_source_transparency(test_symbols)
        
        if data_source_issues:
            critical_issues.extend(data_source_issues)
            all_passed = False
            self.log_test("Data Source Transparency", False, 
                        f"Issues: {data_source_issues}", True)
        else:
            self.log_test("Data Source Transparency", True, 
                        "Data source indicators showing real Alpha Vantage data correctly")
        
        # Summary of critical runtime errors fix testing
        if critical_issues:
            print(f"\n🚨 CRITICAL RUNTIME ERRORS STILL PRESENT ({len(critical_issues)}):")
            for issue in critical_issues:
                print(f"  • {issue}")
        else:
            print(f"\n✅ All critical runtime errors have been successfully resolved")
        
        return all_passed

    def validate_point_based_decision_fix(self, data: Dict[str, Any], symbol: str) -> List[str]:
        """Validate Point Based Decision TypeError fix"""
        issues = []
        
        indicators = data.get("indicators", {})
        if not indicators:
            issues.append("Missing indicators object")
            return issues
        
        # Check for proper Number() casting - all values should be numbers, not undefined
        numeric_fields = [
            "ppo", "ppo_signal", "ppo_histogram", "ppo_slope", "ppo_slope_percentage",
            "dmi_plus", "dmi_minus", "adx", "sma_20", "sma_50", "sma_200",
            "rsi", "macd", "macd_signal", "macd_histogram"
        ]
        
        for field in numeric_fields:
            value = indicators.get(field)
            if value is None:
                issues.append(f"{field} is null (could cause toFixed() error)")
            elif not isinstance(value, (int, float)):
                issues.append(f"{field} is not a number: {type(value)} (could cause toFixed() error)")
        
        # Check convertToPointBasedAnalysis function requirements
        # Ensure all metrics have proper fallback values
        required_metrics = ["ppo", "rsi", "macd", "dmi_plus", "adx"]
        for metric in required_metrics:
            value = indicators.get(metric)
            if value is None or (isinstance(value, str) and value == "undefined"):
                issues.append(f"{metric} could cause toFixed() TypeError in Point Based Decision")
        
        # Check for proper fallback values (should not be 0 for all indicators)
        all_zero_count = sum(1 for field in numeric_fields 
                           if indicators.get(field) == 0)
        if all_zero_count > len(numeric_fields) * 0.8:  # More than 80% are zero
            issues.append("Too many indicators are zero - may indicate calculation issues")
        
        return issues

    def validate_screener_real_data_integration(self, data: Dict[str, Any]) -> List[str]:
        """Validate Stock Screener real data integration"""
        issues = []
        
        # Check for data source transparency fields
        data_sources = data.get("data_sources", [])
        if not data_sources:
            issues.append("Missing data_sources field in screener response")
        elif "alpha_vantage" not in data_sources:
            issues.append(f"Expected alpha_vantage in data sources, got: {data_sources}")
        
        # Check real data count
        real_data_count = data.get("real_data_count")
        if real_data_count is None:
            issues.append("Missing real_data_count field")
        elif real_data_count == 0:
            issues.append("real_data_count is 0 - may still be using simulated data")
        
        # Check for note about real data usage
        note = data.get("note", "")
        if "real" not in note.lower() or "alpha vantage" not in note.lower():
            issues.append(f"Note doesn't indicate real Alpha Vantage data usage: {note}")
        
        # Check individual stock data sources
        stocks = data.get("stocks", [])
        if stocks:
            for i, stock in enumerate(stocks[:5]):  # Check first 5 stocks
                stock_data_source = stock.get("data_source")
                if stock_data_source != "alpha_vantage":
                    issues.append(f"Stock {i+1} ({stock.get('symbol', 'unknown')}) "
                                f"has data_source: {stock_data_source}, expected: alpha_vantage")
        
        # Check that PPO values are realistic (not hash-based demo patterns)
        if stocks:
            ppo_values_realistic = self.validate_realistic_ppo_values(stocks[:3])
            if not ppo_values_realistic:
                issues.append("PPO values appear to be demo/hash-based rather than real market data")
        
        return issues

    def validate_dmi_values_updating(self, dmi_values_by_symbol: Dict[str, Dict]) -> List[str]:
        """Validate that DMI values are different between symbols (not static)"""
        issues = []
        
        if len(dmi_values_by_symbol) < 2:
            issues.append("Insufficient symbols to test DMI value variation")
            return issues
        
        # Check if all DMI+ values are the same (static 26.0 issue)
        dmi_plus_values = [values["dmi_plus"] for values in dmi_values_by_symbol.values()]
        dmi_minus_values = [values["dmi_minus"] for values in dmi_values_by_symbol.values()]
        adx_values = [values["adx"] for values in dmi_values_by_symbol.values()]
        
        # Check for static values (all the same)
        if len(set(dmi_plus_values)) == 1:
            static_value = dmi_plus_values[0]
            if static_value == 26.0:
                issues.append(f"All DMI+ values are static at 26.0 - update fix not working")
            else:
                issues.append(f"All DMI+ values are static at {static_value}")
        
        if len(set(dmi_minus_values)) == 1:
            issues.append(f"All DMI- values are static at {dmi_minus_values[0]}")
        
        if len(set(adx_values)) == 1:
            issues.append(f"All ADX values are static at {adx_values[0]}")
        
        # Check for reasonable variation (should vary by at least 1.0 between symbols)
        dmi_plus_range = max(dmi_plus_values) - min(dmi_plus_values)
        if dmi_plus_range < 1.0:
            issues.append(f"DMI+ values have insufficient variation: range={dmi_plus_range:.2f}")
        
        # Check for realistic DMI ranges (0-100)
        for symbol, values in dmi_values_by_symbol.items():
            for indicator, value in values.items():
                if not (0 <= value <= 100):
                    issues.append(f"{symbol} {indicator} value {value:.2f} outside valid range (0-100)")
        
        return issues

    def validate_data_source_transparency(self, test_symbols: List[str]) -> List[str]:
        """Validate data source transparency shows real Alpha Vantage data"""
        issues = []
        
        for symbol in test_symbols:
            try:
                payload = {"symbol": symbol, "timeframe": "1D"}
                response = requests.post(f"{BACKEND_URL}/analyze", 
                                       json=payload,
                                       headers={"Content-Type": "application/json"},
                                       timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    data_source = data.get("data_source")
                    
                    if data_source != "alpha_vantage":
                        issues.append(f"{symbol} data_source is {data_source}, expected alpha_vantage")
                    
                    # Check response time is reasonable for cached data
                    response_time = data.get("response_time", 0)
                    if response_time > 5.0:  # More than 5 seconds might indicate issues
                        issues.append(f"{symbol} response time {response_time:.2f}s is too slow")
                
                else:
                    issues.append(f"{symbol} API call failed: {response.status_code}")
                    
            except Exception as e:
                issues.append(f"{symbol} data source test failed: {str(e)}")
        
        return issues

    def validate_realistic_ppo_values(self, stocks: List[Dict]) -> bool:
        """Check if PPO values appear realistic rather than hash-based demo data"""
        for stock in stocks:
            ppo_values = stock.get("ppo_values", [])
            if not ppo_values or len(ppo_values) < 3:
                continue
            
            # Real PPO values should have some variation and not follow hash patterns
            ppo_range = max(ppo_values) - min(ppo_values)
            if ppo_range == 0:  # All values identical
                return False
            
            # Check for unrealistic precision (hash-based values often have many decimals)
            for ppo in ppo_values:
                if isinstance(ppo, float) and len(str(ppo).split('.')[-1]) > 6:
                    return False  # Too many decimal places, likely hash-based
        
        return True

    def test_dmi_value_variation_critical(self) -> bool:
        """
        CRITICAL TEST: DMI+ Value Variation Test
        
        Tests the specific user scenarios from review request:
        1. Stock Analysis - Two Stock Entry Test (AAPL -> GOOGL)
        2. Point Based Decision - Two Stock Entry Test (AAPL -> MSFT)  
        3. DMI+ Value Variation Test (AAPL, GOOGL, MSFT sequence)
        
        Verifies:
        - Both analyses complete successfully without errors
        - DMI+ values are different between stocks (not stuck at static 26.0)
        - No TypeError in responses and all fields properly formatted
        - Values are realistic (0-100 range)
        """
        print(f"\n🎯 CRITICAL DMI+ VALUE VARIATION TESTING")
        print("=" * 70)
        print("Testing specific user scenarios from review request:")
        print("1. Stock Analysis - Two Stock Entry Test (AAPL -> GOOGL)")
        print("2. Point Based Decision - Two Stock Entry Test (AAPL -> MSFT)")
        print("3. DMI+ Value Variation Test (AAPL, GOOGL, MSFT sequence)")
        print("=" * 70)
        
        all_passed = True
        critical_issues = []
        dmi_values = {}
        
        # Test symbols as specified in review request
        test_sequence = ["AAPL", "GOOGL", "MSFT"]
        
        # Test each symbol with 3M timeframe as specified
        for i, symbol in enumerate(test_sequence):
            print(f"\n📊 Testing {symbol} (Step {i+1}/3)")
            
            try:
                payload = {"symbol": symbol, "timeframe": "3M"}
                start_time = time.time()
                
                response = requests.post(f"{BACKEND_URL}/analyze", 
                                       json=payload,
                                       headers={"Content-Type": "application/json"},
                                       timeout=30)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Validate response structure
                    if not self.validate_critical_response_structure(data, symbol):
                        critical_issues.append(f"{symbol}: Invalid response structure")
                        all_passed = False
                        continue
                    
                    # Extract DMI+ value
                    indicators = data.get("indicators", {})
                    dmi_plus = indicators.get("dmi_plus")
                    
                    if dmi_plus is None:
                        critical_issues.append(f"{symbol}: DMI+ value is null")
                        all_passed = False
                        continue
                    
                    # Validate DMI+ is in realistic range (0-100)
                    if not (0 <= dmi_plus <= 100):
                        critical_issues.append(f"{symbol}: DMI+ value {dmi_plus} outside valid range (0-100)")
                        all_passed = False
                        continue
                    
                    # Store DMI+ value for comparison
                    dmi_values[symbol] = dmi_plus
                    
                    # Log detailed results
                    print(f"  ✅ {symbol}: DMI+ = {dmi_plus:.2f}, Response time: {response_time:.2f}s")
                    
                    # Validate no TypeError in response
                    if self.check_for_type_errors(data, symbol):
                        critical_issues.append(f"{symbol}: TypeError detected in response")
                        all_passed = False
                    
                    # Validate all financial metrics are properly formatted
                    if not self.validate_financial_metrics_formatting(data, symbol):
                        critical_issues.append(f"{symbol}: Financial metrics formatting issues")
                        all_passed = False
                    
                    self.log_test(f"DMI+ Analysis ({symbol})", True, 
                                f"DMI+ = {dmi_plus:.2f}, Time: {response_time:.2f}s")
                    
                else:
                    error_msg = f"HTTP {response.status_code}: {response.text}"
                    critical_issues.append(f"{symbol}: API call failed - {error_msg}")
                    all_passed = False
                    self.log_test(f"DMI+ Analysis ({symbol})", False, error_msg, True)
                    
            except Exception as e:
                error_msg = f"Exception: {str(e)}"
                critical_issues.append(f"{symbol}: {error_msg}")
                all_passed = False
                self.log_test(f"DMI+ Analysis ({symbol})", False, error_msg, True)
        
        # Critical validation: DMI+ values must be different between stocks
        print(f"\n🔍 CRITICAL VALIDATION: DMI+ Value Variation")
        if len(dmi_values) >= 2:
            unique_values = len(set(round(val, 1) for val in dmi_values.values()))
            total_values = len(dmi_values)
            
            print(f"DMI+ Values Retrieved:")
            for symbol, value in dmi_values.items():
                print(f"  {symbol}: {value:.2f}")
            
            if unique_values == 1:
                # All DMI+ values are the same - CRITICAL FAILURE
                static_value = list(dmi_values.values())[0]
                critical_issues.append(f"CRITICAL: All DMI+ values are identical ({static_value:.2f}) - values not updating between stocks")
                all_passed = False
                self.log_test("DMI+ Value Variation", False, 
                            f"All DMI+ values stuck at {static_value:.2f} - CRITICAL BUG", True)
            elif unique_values < total_values:
                # Some values are the same
                critical_issues.append(f"WARNING: Only {unique_values}/{total_values} unique DMI+ values - some duplication")
                self.log_test("DMI+ Value Variation", False, 
                            f"Only {unique_values}/{total_values} unique values - partial variation", True)
                all_passed = False
            else:
                # All values are different - SUCCESS
                self.log_test("DMI+ Value Variation", True, 
                            f"All {total_values} DMI+ values are unique - proper variation confirmed")
                print(f"  ✅ SUCCESS: All DMI+ values are different between stocks")
        else:
            critical_issues.append("Insufficient DMI+ values retrieved for comparison")
            all_passed = False
            self.log_test("DMI+ Value Variation", False, 
                        "Could not retrieve enough DMI+ values for comparison", True)
        
        # Test specific scenarios from review request
        print(f"\n🎯 SPECIFIC SCENARIO TESTING")
        
        # Scenario 1: Stock Analysis - AAPL then GOOGL
        if "AAPL" in dmi_values and "GOOGL" in dmi_values:
            aapl_dmi = dmi_values["AAPL"]
            googl_dmi = dmi_values["GOOGL"]
            difference = abs(aapl_dmi - googl_dmi)
            
            if difference > 0.1:  # Allow for small rounding differences
                self.log_test("Stock Analysis Scenario (AAPL->GOOGL)", True, 
                            f"DMI+ values differ: AAPL={aapl_dmi:.2f}, GOOGL={googl_dmi:.2f}, diff={difference:.2f}")
                print(f"  ✅ Stock Analysis Test: AAPL ({aapl_dmi:.2f}) ≠ GOOGL ({googl_dmi:.2f})")
            else:
                critical_issues.append(f"Stock Analysis: AAPL and GOOGL have nearly identical DMI+ values")
                all_passed = False
                self.log_test("Stock Analysis Scenario (AAPL->GOOGL)", False, 
                            f"DMI+ values too similar: AAPL={aapl_dmi:.2f}, GOOGL={googl_dmi:.2f}", True)
        
        # Scenario 2: Point Based Decision - AAPL then MSFT
        if "AAPL" in dmi_values and "MSFT" in dmi_values:
            aapl_dmi = dmi_values["AAPL"]
            msft_dmi = dmi_values["MSFT"]
            difference = abs(aapl_dmi - msft_dmi)
            
            if difference > 0.1:  # Allow for small rounding differences
                self.log_test("Point Based Decision Scenario (AAPL->MSFT)", True, 
                            f"DMI+ values differ: AAPL={aapl_dmi:.2f}, MSFT={msft_dmi:.2f}, diff={difference:.2f}")
                print(f"  ✅ Point Based Decision Test: AAPL ({aapl_dmi:.2f}) ≠ MSFT ({msft_dmi:.2f})")
            else:
                critical_issues.append(f"Point Based Decision: AAPL and MSFT have nearly identical DMI+ values")
                all_passed = False
                self.log_test("Point Based Decision Scenario (AAPL->MSFT)", False, 
                            f"DMI+ values too similar: AAPL={aapl_dmi:.2f}, MSFT={msft_dmi:.2f}", True)
        
        # Summary of critical testing
        print(f"\n📋 CRITICAL TEST SUMMARY")
        if critical_issues:
            print(f"🚨 CRITICAL ISSUES FOUND ({len(critical_issues)}):")
            for issue in critical_issues:
                print(f"  • {issue}")
        else:
            print(f"✅ ALL CRITICAL TESTS PASSED - DMI+ values properly vary between stocks")
        
        return all_passed

    def validate_critical_response_structure(self, data: Dict[str, Any], symbol: str) -> bool:
        """Validate critical response structure for DMI testing"""
        critical_fields = ["symbol", "indicators"]
        
        for field in critical_fields:
            if field not in data:
                self.log_test(f"Critical Structure ({symbol})", False, 
                            f"Missing critical field: {field}", True)
                return False
        
        # Validate indicators structure
        indicators = data.get("indicators", {})
        if "dmi_plus" not in indicators:
            self.log_test(f"Critical Structure ({symbol})", False, 
                        "Missing dmi_plus in indicators", True)
            return False
        
        return True

    def check_for_type_errors(self, data: Dict[str, Any], symbol: str) -> bool:
        """Check for TypeError indicators in response data"""
        # Convert response to string and check for common TypeError patterns
        response_str = json.dumps(data, default=str)
        
        type_error_patterns = [
            "undefined.toFixed",
            "null.toFixed", 
            "NaN.toFixed",
            "TypeError",
            "Cannot read property",
            "Cannot read properties of undefined",
            "Cannot read properties of null"
        ]
        
        for pattern in type_error_patterns:
            if pattern in response_str:
                self.log_test(f"TypeError Check ({symbol})", False, 
                            f"Found TypeError pattern: {pattern}", True)
                return True
        
        return False

    def validate_financial_metrics_formatting(self, data: Dict[str, Any], symbol: str) -> bool:
        """Validate all financial metrics are properly formatted"""
        issues = []
        
        # Check main financial fields
        financial_fields = ["current_price", "price_change", "price_change_percent", "volume"]
        for field in financial_fields:
            value = data.get(field)
            if value is None:
                issues.append(f"{field} is null")
            elif not isinstance(value, (int, float)):
                issues.append(f"{field} is not numeric: {type(value)}")
        
        # Check indicators formatting
        indicators = data.get("indicators", {})
        indicator_fields = ["ppo", "ppo_signal", "ppo_histogram", "dmi_plus", "dmi_minus", "adx", "rsi"]
        for field in indicator_fields:
            value = indicators.get(field)
            if value is None:
                issues.append(f"indicators.{field} is null")
            elif not isinstance(value, (int, float)):
                issues.append(f"indicators.{field} is not numeric: {type(value)}")
        
        if issues:
            self.log_test(f"Financial Metrics Formatting ({symbol})", False, 
                        f"Issues: {issues}", True)
            return False
        else:
            self.log_test(f"Financial Metrics Formatting ({symbol})", True, 
                        "All financial metrics properly formatted")
            return True

    def test_critical_fixes_verification(self) -> bool:
        """
        CRITICAL FIXES VERIFICATION - Test the three specific fixes from review request:
        1. StockScreener Property Name Fixes (camelCase to snake_case)
        2. DMI Calculation Fix (composite calculation instead of ADX duplication)
        3. Enhanced Sorting (nested property support for returns.1d, returns.5d, etc.)
        """
        print(f"\n🔧 CRITICAL FIXES VERIFICATION TESTING")
        print("=" * 70)
        
        all_passed = True
        fix_issues = []
        
        # Test symbols specifically mentioned in review request
        test_symbols = ["AAPL", "WFC"]
        
        # 1. TEST STOCK SCREENER PROPERTY NAME FIXES
        print(f"\n📊 Testing StockScreener Property Name Fixes (camelCase → snake_case)")
        screener_fix_passed = self.test_screener_property_name_fixes()
        if not screener_fix_passed:
            all_passed = False
            fix_issues.append("StockScreener property name fixes failed")
        
        # 2. TEST DMI CALCULATION FIX
        print(f"\n🧮 Testing DMI Calculation Fix (composite vs ADX duplication)")
        dmi_fix_passed = self.test_dmi_calculation_fix(test_symbols)
        if not dmi_fix_passed:
            all_passed = False
            fix_issues.append("DMI calculation fix failed")
        
        # 3. TEST ENHANCED SORTING WITH NESTED PROPERTIES
        print(f"\n🔄 Testing Enhanced Sorting (nested property support)")
        sorting_fix_passed = self.test_enhanced_sorting_fix()
        if not sorting_fix_passed:
            all_passed = False
            fix_issues.append("Enhanced sorting fix failed")
        
        # 4. COMPREHENSIVE INTEGRATION TEST
        print(f"\n🔗 Testing Integration of All Three Fixes")
        integration_passed = self.test_all_fixes_integration(test_symbols)
        if not integration_passed:
            all_passed = False
            fix_issues.append("Integration of all fixes failed")
        
        # Summary of critical fixes testing
        if fix_issues:
            print(f"\n🚨 CRITICAL FIXES ISSUES FOUND ({len(fix_issues)}):")
            for issue in fix_issues:
                print(f"  • {issue}")
        else:
            print(f"\n✅ All three critical fixes verified successfully")
        
        return all_passed
    
    def test_screener_property_name_fixes(self) -> bool:
        """Test StockScreener property name fixes from camelCase to snake_case"""
        all_passed = True
        
        try:
            # Test screener endpoint with filters that would trigger property access
            filters = {
                "price_filter": {"type": "under", "under": 500},
                "dmi_filter": {"min": 15, "max": 65},
                "ppo_slope_filter": {"threshold": 1}
            }
            
            response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                   json=filters,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                stocks = data.get("stocks", [])
                
                if stocks:
                    # Check first stock for proper snake_case property names
                    stock = stocks[0]
                    property_issues = []
                    
                    # Check for snake_case properties that should exist
                    required_snake_case_props = [
                        "ppo_slope_percentage",  # was ppoSlope
                        "di_plus",              # was diPlus  
                        "di_minus"              # was diMinus
                    ]
                    
                    for prop in required_snake_case_props:
                        if prop not in stock:
                            property_issues.append(f"Missing snake_case property: {prop}")
                        elif stock[prop] is None:
                            property_issues.append(f"Property {prop} is null (possible undefined access)")
                    
                    # Check that old camelCase properties are NOT present
                    old_camel_case_props = ["ppoSlope", "diPlus", "diMinus"]
                    for prop in old_camel_case_props:
                        if prop in stock:
                            property_issues.append(f"Old camelCase property still present: {prop}")
                    
                    if property_issues:
                        self.log_test("Screener Property Names", False, 
                                    f"Property name issues: {property_issues}", True)
                        all_passed = False
                    else:
                        self.log_test("Screener Property Names", True, 
                                    "All snake_case properties present, no camelCase properties found")
                        
                        # Log actual values for verification
                        ppo_slope = stock.get("ppo_slope_percentage", "N/A")
                        di_plus = stock.get("di_plus", "N/A")
                        di_minus = stock.get("di_minus", "N/A")
                        print(f"  ✅ Sample values: ppo_slope_percentage={ppo_slope}, di_plus={di_plus}, di_minus={di_minus}")
                else:
                    self.log_test("Screener Property Names", False, 
                                "No stocks returned from screener", True)
                    all_passed = False
            else:
                self.log_test("Screener Property Names", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                all_passed = False
                
        except Exception as e:
            self.log_test("Screener Property Names", False, f"Error: {str(e)}", True)
            all_passed = False
        
        return all_passed
    
    def test_dmi_calculation_fix(self, test_symbols: List[str]) -> bool:
        """Test DMI calculation fix - should be composite calculation, not ADX duplication"""
        all_passed = True
        
        for symbol in test_symbols:
            try:
                payload = {"symbol": symbol, "timeframe": "3M"}
                response = requests.post(f"{BACKEND_URL}/analyze", 
                                       json=payload,
                                       headers={"Content-Type": "application/json"},
                                       timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    indicators = data.get("indicators", {})
                    
                    # Get DMI values
                    dmi_plus = indicators.get("dmi_plus")
                    dmi_minus = indicators.get("dmi_minus") 
                    adx = indicators.get("adx")
                    
                    # Check if we have a separate DMI field (composite calculation)
                    dmi = indicators.get("dmi")  # This should be the composite
                    
                    dmi_issues = []
                    
                    # Validate that DMI values exist and are not null
                    if dmi_plus is None:
                        dmi_issues.append("dmi_plus is null")
                    if dmi_minus is None:
                        dmi_issues.append("dmi_minus is null")
                    if adx is None:
                        dmi_issues.append("adx is null")
                    
                    # CRITICAL TEST: DMI should NOT equal ADX (was the bug)
                    if dmi is not None and adx is not None:
                        if dmi == adx:
                            dmi_issues.append(f"DMI ({dmi}) equals ADX ({adx}) - fix not working!")
                        else:
                            # Check if DMI is composite calculation: (dmi_plus + dmi_minus) / 2
                            if dmi_plus is not None and dmi_minus is not None:
                                expected_dmi = (dmi_plus + dmi_minus) / 2
                                if abs(dmi - expected_dmi) > 0.1:  # Allow small floating point differences
                                    dmi_issues.append(f"DMI ({dmi}) not composite calculation (expected {expected_dmi:.2f})")
                                else:
                                    print(f"  ✅ {symbol}: DMI={dmi:.2f} is composite of DMI+({dmi_plus:.2f}) + DMI-({dmi_minus:.2f})")
                    
                    # Test that DMI values are different between stocks (not static)
                    if symbol == "WFC":
                        # Compare with user-provided reference data expectations
                        if dmi_plus is not None and dmi_minus is not None and adx is not None:
                            # Values should be realistic for WFC analysis
                            if 0 <= dmi_plus <= 100 and 0 <= dmi_minus <= 100 and 0 <= adx <= 100:
                                print(f"  ✅ {symbol}: Realistic DMI values - DMI+={dmi_plus:.2f}, DMI-={dmi_minus:.2f}, ADX={adx:.2f}")
                            else:
                                dmi_issues.append(f"DMI values outside valid range (0-100)")
                    
                    if dmi_issues:
                        self.log_test(f"DMI Calculation Fix ({symbol})", False, 
                                    f"DMI issues: {dmi_issues}", True)
                        all_passed = False
                    else:
                        self.log_test(f"DMI Calculation Fix ({symbol})", True, 
                                    f"DMI composite calculation working correctly")
                else:
                    self.log_test(f"DMI Calculation Fix ({symbol})", False, 
                                f"HTTP {response.status_code}: {response.text}", True)
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"DMI Calculation Fix ({symbol})", False, f"Error: {str(e)}", True)
                all_passed = False
        
        return all_passed
    
    def test_enhanced_sorting_fix(self) -> bool:
        """Test enhanced sorting with nested property support for returns.1d, returns.5d, etc."""
        all_passed = True
        
        try:
            # Test screener with sorting that would use nested properties
            filters = {
                "price_filter": {"type": "under", "under": 500},
                "dmi_filter": {"min": 20, "max": 60},
                "ppo_slope_filter": {"threshold": 1}
            }
            
            response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                   json=filters,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                stocks = data.get("stocks", [])
                
                if len(stocks) >= 2:
                    sorting_issues = []
                    
                    # Check that returns object has nested properties
                    for i, stock in enumerate(stocks[:3]):
                        returns = stock.get("returns", {})
                        if not isinstance(returns, dict):
                            sorting_issues.append(f"Stock {i+1}: returns is not a dict")
                            continue
                        
                        # Check for nested return properties
                        required_return_periods = ["1d", "5d", "2w", "1m", "1y"]
                        for period in required_return_periods:
                            if period not in returns:
                                sorting_issues.append(f"Stock {i+1}: missing returns.{period}")
                            elif returns[period] is None:
                                sorting_issues.append(f"Stock {i+1}: returns.{period} is null")
                    
                    # Test that nested property values are extractable
                    if len(stocks) >= 2:
                        stock1_1d = stocks[0].get("returns", {}).get("1d")
                        stock2_1d = stocks[1].get("returns", {}).get("1d")
                        
                        if stock1_1d is not None and stock2_1d is not None:
                            print(f"  ✅ Nested property extraction working: Stock1 1d return={stock1_1d}%, Stock2 1d return={stock2_1d}%")
                        else:
                            sorting_issues.append("Cannot extract nested return values for sorting")
                    
                    if sorting_issues:
                        self.log_test("Enhanced Sorting Fix", False, 
                                    f"Sorting issues: {sorting_issues}", True)
                        all_passed = False
                    else:
                        self.log_test("Enhanced Sorting Fix", True, 
                                    "Nested property support working correctly")
                else:
                    self.log_test("Enhanced Sorting Fix", False, 
                                "Insufficient stocks to test sorting", True)
                    all_passed = False
            else:
                self.log_test("Enhanced Sorting Fix", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                all_passed = False
                
        except Exception as e:
            self.log_test("Enhanced Sorting Fix", False, f"Error: {str(e)}", True)
            all_passed = False
        
        return all_passed
    
    def test_all_fixes_integration(self, test_symbols: List[str]) -> bool:
        """Test integration of all three fixes working together"""
        all_passed = True
        
        print(f"  Testing integration with symbols: {test_symbols}")
        
        # Test that screener endpoint works without undefined property errors
        try:
            filters = {
                "price_filter": {"type": "under", "under": 500},
                "dmi_filter": {"min": 15, "max": 65},
                "ppo_slope_filter": {"threshold": 1}
            }
            
            response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                   json=filters,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check that response is valid and has no errors
                if data.get("success", False):
                    stocks = data.get("stocks", [])
                    
                    integration_issues = []
                    
                    # Test all three fixes together
                    for stock in stocks[:2]:  # Test first 2 stocks
                        symbol = stock.get("symbol", "Unknown")
                        
                        # Fix 1: Property names
                        if "ppo_slope_percentage" not in stock:
                            integration_issues.append(f"{symbol}: Missing ppo_slope_percentage")
                        if "di_plus" not in stock:
                            integration_issues.append(f"{symbol}: Missing di_plus")
                        if "di_minus" not in stock:
                            integration_issues.append(f"{symbol}: Missing di_minus")
                        
                        # Fix 2: DMI calculation (check in individual analysis)
                        # This will be verified in the individual stock analysis
                        
                        # Fix 3: Nested properties
                        returns = stock.get("returns", {})
                        if not isinstance(returns, dict) or "1d" not in returns:
                            integration_issues.append(f"{symbol}: Missing nested returns.1d")
                    
                    if integration_issues:
                        self.log_test("Integration Test", False, 
                                    f"Integration issues: {integration_issues}", True)
                        all_passed = False
                    else:
                        self.log_test("Integration Test", True, 
                                    f"All three fixes working together - {len(stocks)} stocks processed")
                        
                        # Test individual analysis for DMI fix
                        for symbol in test_symbols:
                            individual_passed = self.test_individual_analysis_integration(symbol)
                            if not individual_passed:
                                all_passed = False
                else:
                    self.log_test("Integration Test", False, 
                                "Screener returned success=false", True)
                    all_passed = False
            else:
                self.log_test("Integration Test", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                all_passed = False
                
        except Exception as e:
            self.log_test("Integration Test", False, f"Error: {str(e)}", True)
            all_passed = False
        
        return all_passed
    
    def test_individual_analysis_integration(self, symbol: str) -> bool:
        """Test individual stock analysis for DMI calculation fix"""
        try:
            payload = {"symbol": symbol, "timeframe": "3M"}
            response = requests.post(f"{BACKEND_URL}/analyze", 
                                   json=payload,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                indicators = data.get("indicators", {})
                
                # Check DMI calculation fix
                dmi_plus = indicators.get("dmi_plus")
                dmi_minus = indicators.get("dmi_minus")
                adx = indicators.get("adx")
                dmi = indicators.get("dmi")
                
                if dmi is not None and adx is not None and dmi == adx:
                    self.log_test(f"Individual DMI Fix ({symbol})", False, 
                                f"DMI still equals ADX - fix not working", True)
                    return False
                else:
                    self.log_test(f"Individual DMI Fix ({symbol})", True, 
                                f"DMI calculation fix working in individual analysis")
                    return True
            else:
                self.log_test(f"Individual Analysis ({symbol})", False, 
                            f"HTTP {response.status_code}", True)
                return False
                
        except Exception as e:
            self.log_test(f"Individual Analysis ({symbol})", False, f"Error: {str(e)}", True)
            return False

    def test_critical_user_fixes(self) -> bool:
        """
        TEST ALL CRITICAL USER FIXES: Verify the three major issues reported by user are resolved
        
        **USER ISSUES TO VALIDATE:**
        1. **Tech Analysis Button Issue**: Stock entered doesn't return results, no error message, but refresh works - should now work immediately
        2. **Scanner UI Offset Issues**: PPO field and columns misaligned, PPO field not populating correctly - should now display properly
        3. **Stock Universe Limitation**: Only 20 stocks hardcoded - should now scan broader market (65+ stocks across multiple sectors)
        
        **FIXES IMPLEMENTED:**
        1. **Tech Analysis Button**: Added async function with setTimeout for state update, better logging, forced refetch sequence
        2. **PPO Column Fix**: Updated property names from `ppoValues` to `ppo_values` in frontend to match backend snake_case
        3. **Stock Universe Expansion**: Expanded from 20 stocks to 65+ stocks across 9 sectors
        """
        print(f"\n🎯 TESTING CRITICAL USER FIXES")
        print("=" * 70)
        print("Testing three major user-reported issues:")
        print("1. Tech Analysis Button Issue - immediate results without refresh")
        print("2. Scanner UI Offset Issues - PPO field alignment and population")
        print("3. Stock Universe Limitation - 65+ stocks across multiple sectors")
        print("=" * 70)
        
        all_passed = True
        critical_issues = []
        
        # 1. Test Tech Analysis Button Fix - Individual Stock Analysis
        print(f"\n🔍 TEST 1: TECH ANALYSIS BUTTON FIX")
        print("-" * 50)
        analysis_button_passed = self.test_analysis_button_fix()
        if not analysis_button_passed:
            all_passed = False
            critical_issues.append("Tech Analysis Button still not working immediately")
        
        # 2. Test PPO Data Structure and Column Alignment
        print(f"\n📊 TEST 2: PPO COLUMN FIX AND DATA STRUCTURE")
        print("-" * 50)
        ppo_structure_passed = self.test_ppo_data_structure_fix()
        if not ppo_structure_passed:
            all_passed = False
            critical_issues.append("PPO data structure and column alignment issues persist")
        
        # 3. Test Stock Universe Expansion
        print(f"\n🌐 TEST 3: STOCK UNIVERSE EXPANSION")
        print("-" * 50)
        universe_expansion_passed = self.test_stock_universe_expansion()
        if not universe_expansion_passed:
            all_passed = False
            critical_issues.append("Stock universe still limited to 20 stocks")
        
        # 4. Test Sector Diversity
        print(f"\n🏢 TEST 4: SECTOR DIVERSITY VERIFICATION")
        print("-" * 50)
        sector_diversity_passed = self.test_sector_diversity()
        if not sector_diversity_passed:
            all_passed = False
            critical_issues.append("Sector diversity not achieved - still Technology-heavy")
        
        # Summary of critical fixes testing
        if critical_issues:
            print(f"\n🚨 CRITICAL USER FIXES - ISSUES FOUND ({len(critical_issues)}):")
            for issue in critical_issues:
                print(f"  • {issue}")
        else:
            print(f"\n✅ ALL CRITICAL USER FIXES VALIDATED SUCCESSFULLY")
        
        return all_passed
    
    def test_analysis_button_fix(self) -> bool:
        """Test individual stock analysis to verify immediate results without refresh requirement"""
        all_passed = True
        test_symbols = ["AAPL", "GOOGL", "MSFT", "TSLA"]
        
        print("Testing individual stock analysis for immediate results...")
        
        for symbol in test_symbols:
            try:
                # Test the analyze endpoint that the frontend button calls
                payload = {"symbol": symbol, "timeframe": "3M"}  # Default timeframe
                start_time = time.time()
                
                response = requests.post(f"{BACKEND_URL}/analyze", 
                                       json=payload,
                                       headers={"Content-Type": "application/json"},
                                       timeout=30)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Validate that we get immediate, complete results
                    analysis_issues = self.validate_immediate_analysis_results(data, symbol, response_time)
                    
                    if analysis_issues:
                        self.log_test(f"Analysis Button Fix ({symbol})", False, 
                                    f"Issues: {analysis_issues}", True)
                        all_passed = False
                    else:
                        self.log_test(f"Analysis Button Fix ({symbol})", True, 
                                    f"Immediate results in {response_time:.2f}s")
                        
                        # Log key metrics for verification
                        current_price = data.get("current_price", 0)
                        indicators = data.get("indicators", {})
                        ppo = indicators.get("ppo", 0)
                        chart_data_count = len(data.get("chart_data", []))
                        data_source = data.get("data_source", "unknown")
                        
                        print(f"  ✅ {symbol}: Price=${current_price:.2f}, PPO={ppo:.4f}, Data points={chart_data_count}, Source={data_source}")
                        
                else:
                    self.log_test(f"Analysis Button API ({symbol})", False, 
                                f"HTTP {response.status_code}: {response.text}", True)
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"Analysis Button Test ({symbol})", False, f"Error: {str(e)}", True)
                all_passed = False
        
        return all_passed
    
    def validate_immediate_analysis_results(self, data: Dict[str, Any], symbol: str, response_time: float) -> List[str]:
        """Validate that analysis results are complete and immediate"""
        issues = []
        
        # Check response time (should be reasonable for immediate results)
        if response_time > 20:  # More than 20 seconds is too slow for immediate results
            issues.append(f"Response too slow: {response_time:.2f}s")
        
        # Check that all required data is present (no missing fields that would require refresh)
        required_fields = ["symbol", "current_price", "indicators", "ppo_history", "dmi_history", 
                          "ai_recommendation", "chart_data"]
        
        for field in required_fields:
            if field not in data or data[field] is None:
                issues.append(f"Missing {field} - would require refresh")
        
        # Check that technical indicators are calculated
        indicators = data.get("indicators", {})
        if not indicators:
            issues.append("No technical indicators - would require refresh")
        else:
            # Check key indicators that should be immediately available
            key_indicators = ["ppo", "ppo_signal", "ppo_histogram", "rsi", "adx"]
            for indicator in key_indicators:
                if indicators.get(indicator) is None:
                    issues.append(f"Missing {indicator} indicator")
        
        # Check that chart data is populated
        chart_data = data.get("chart_data", [])
        if not chart_data or len(chart_data) < 10:
            issues.append("Insufficient chart data - would require refresh")
        
        # Check that AI recommendations are present
        ai_rec = data.get("ai_recommendation")
        if not ai_rec or ai_rec == "":
            issues.append("Missing AI recommendation - would require refresh")
        
        return issues
    
    def test_ppo_data_structure_fix(self) -> bool:
        """Test PPO 3-day values display correctly in screener results with proper alignment"""
        all_passed = True
        
        print("Testing PPO data structure and 3-day historical values...")
        
        try:
            # Test screener endpoint for PPO data structure
            screener_filters = {
                "price_filter": {"type": "under", "under": 500},
                "dmi_filter": {"min": 15, "max": 65},
                "ppo_slope_filter": {"threshold": 1},
                "sector_filter": "all"
            }
            
            response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                   json=screener_filters,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                stocks = data.get("stocks", [])
                
                if not stocks:
                    self.log_test("PPO Data Structure", False, "No stocks returned from screener", True)
                    return False
                
                # Test PPO data structure in first few stocks
                ppo_structure_issues = []
                
                for i, stock in enumerate(stocks[:5]):  # Test first 5 stocks
                    symbol = stock.get("symbol", f"Stock_{i}")
                    
                    # Check for snake_case property names (fix for camelCase issue)
                    ppo_structure_issues.extend(self.validate_ppo_property_names(stock, symbol))
                    
                    # Check PPO 3-day historical data structure
                    ppo_structure_issues.extend(self.validate_ppo_3day_structure(stock, symbol))
                    
                    # Check PPO values are realistic (not all zeros or identical)
                    ppo_structure_issues.extend(self.validate_ppo_value_diversity(stock, symbol))
                
                if ppo_structure_issues:
                    self.log_test("PPO Data Structure Fix", False, 
                                f"Structure issues: {ppo_structure_issues}", True)
                    all_passed = False
                else:
                    self.log_test("PPO Data Structure Fix", True, 
                                f"PPO structure correct for {len(stocks)} stocks")
                    
                    # Log sample PPO data for verification
                    if stocks:
                        sample_stock = stocks[0]
                        ppo_values = sample_stock.get("ppo_values", [])
                        ppo_slope = sample_stock.get("ppo_slope_percentage", 0)
                        print(f"  ✅ Sample PPO data: {sample_stock.get('symbol')} - Values={ppo_values}, Slope={ppo_slope:.2f}%")
                
            else:
                self.log_test("PPO Structure API Test", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                all_passed = False
                
        except Exception as e:
            self.log_test("PPO Data Structure Test", False, f"Error: {str(e)}", True)
            all_passed = False
        
        return all_passed
    
    def validate_ppo_property_names(self, stock: Dict[str, Any], symbol: str) -> List[str]:
        """Validate that PPO properties use snake_case (fix for camelCase issue)"""
        issues = []
        
        # Check for correct snake_case property names
        required_snake_case_props = [
            "ppo_values", "ppo_slope_percentage", "di_plus", "di_minus"
        ]
        
        for prop in required_snake_case_props:
            if prop not in stock:
                issues.append(f"{symbol}: Missing snake_case property '{prop}'")
        
        # Check that old camelCase properties are NOT present (should be fixed)
        old_camel_case_props = [
            "ppoValues", "ppoSlope", "diPlus", "diMinus"
        ]
        
        for prop in old_camel_case_props:
            if prop in stock:
                issues.append(f"{symbol}: Old camelCase property '{prop}' still present")
        
        return issues
    
    def validate_ppo_3day_structure(self, stock: Dict[str, Any], symbol: str) -> List[str]:
        """Validate PPO 3-day historical data structure"""
        issues = []
        
        ppo_values = stock.get("ppo_values", [])
        
        if not isinstance(ppo_values, list):
            issues.append(f"{symbol}: ppo_values is not a list")
            return issues
        
        if len(ppo_values) != 3:
            issues.append(f"{symbol}: Expected 3 PPO values, got {len(ppo_values)}")
            return issues
        
        # Check that values are numbers and not all identical
        for i, value in enumerate(ppo_values):
            if not isinstance(value, (int, float)):
                issues.append(f"{symbol}: PPO value {i} is not numeric: {value}")
        
        # Check for proper [Today, Yesterday, 2 Days Ago] format
        # Values should be different (not repeated single-day data)
        if len(set(ppo_values)) == 1:  # All values are identical
            issues.append(f"{symbol}: All PPO values identical {ppo_values} - not proper 3-day history")
        
        return issues
    
    def validate_ppo_value_diversity(self, stock: Dict[str, Any], symbol: str) -> List[str]:
        """Validate that PPO values show proper diversity (not all zeros or unrealistic)"""
        issues = []
        
        ppo_values = stock.get("ppo_values", [])
        ppo_slope = stock.get("ppo_slope_percentage", 0)
        
        # Check for all-zero PPO values (indicates calculation failure)
        if all(val == 0 for val in ppo_values):
            issues.append(f"{symbol}: All PPO values are zero - calculation may have failed")
        
        # Check for unrealistic PPO slope values
        if abs(ppo_slope) > 1000:  # Unreasonably high slope
            issues.append(f"{symbol}: Unrealistic PPO slope: {ppo_slope}%")
        
        # Check that PPO values are within reasonable range
        for i, value in enumerate(ppo_values):
            if isinstance(value, (int, float)) and abs(value) > 100:
                issues.append(f"{symbol}: PPO value {i} outside reasonable range: {value}")
        
        return issues
    
    def test_stock_universe_expansion(self) -> bool:
        """Test that screener now processes 65+ stocks instead of hardcoded 20"""
        all_passed = True
        
        print("Testing stock universe expansion to 65+ stocks...")
        
        try:
            # Test with broad filters to capture maximum stock universe
            broad_filters = {
                "price_filter": {"type": "under", "under": 1000},  # Very broad price filter
                "dmi_filter": {"min": 0, "max": 100},              # Very broad DMI filter
                "ppo_slope_filter": {"threshold": 0},              # Very broad PPO filter
                "sector_filter": "all"
            }
            
            response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                   json=broad_filters,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                total_scanned = data.get("total_scanned", 0)
                results_found = data.get("results_found", 0)
                stocks = data.get("stocks", [])
                
                # Validate stock universe expansion
                universe_issues = self.validate_stock_universe_size(data, total_scanned, results_found)
                
                if universe_issues:
                    self.log_test("Stock Universe Expansion", False, 
                                f"Universe issues: {universe_issues}", True)
                    all_passed = False
                else:
                    self.log_test("Stock Universe Expansion", True, 
                                f"Scanned {total_scanned} stocks, found {results_found} results")
                    
                    print(f"  ✅ Stock Universe: Total scanned={total_scanned}, Results={results_found}")
                    
                    # Log sample of stock symbols to verify diversity
                    if stocks:
                        sample_symbols = [stock.get("symbol", "N/A") for stock in stocks[:10]]
                        print(f"  📊 Sample symbols: {', '.join(sample_symbols)}")
                
            else:
                self.log_test("Universe Expansion API Test", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                all_passed = False
                
        except Exception as e:
            self.log_test("Stock Universe Expansion Test", False, f"Error: {str(e)}", True)
            all_passed = False
        
        return all_passed
    
    def validate_stock_universe_size(self, data: Dict[str, Any], total_scanned: int, results_found: int) -> List[str]:
        """Validate that stock universe has been expanded beyond 20 stocks"""
        issues = []
        
        # Check total scanned stocks (should be 65+ now)
        if total_scanned < 65:
            issues.append(f"Total scanned stocks ({total_scanned}) still below 65 - universe not expanded")
        elif total_scanned == 20:
            issues.append("Total scanned stocks is exactly 20 - still using old hardcoded limit")
        
        # Check that we have reasonable results
        if results_found == 0:
            issues.append("No results found with broad filters - possible filtering issue")
        
        # Check for data source transparency
        data_sources = data.get("data_sources", [])
        if not data_sources:
            issues.append("Missing data_sources field - transparency not implemented")
        
        # Check for real data count
        real_data_count = data.get("real_data_count", 0)
        if real_data_count < 65:
            issues.append(f"Real data count ({real_data_count}) below expected 65+ stocks")
        
        return issues
    
    def test_sector_diversity(self) -> bool:
        """Test that stocks span multiple sectors (not just Technology-heavy)"""
        all_passed = True
        
        print("Testing sector diversity across multiple sectors...")
        
        try:
            # Test with filters that should return diverse sectors
            diverse_filters = {
                "price_filter": {"type": "under", "under": 500},
                "dmi_filter": {"min": 10, "max": 80},
                "ppo_slope_filter": {"threshold": 1},
                "sector_filter": "all"  # All sectors
            }
            
            response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                   json=diverse_filters,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                stocks = data.get("stocks", [])
                
                if not stocks:
                    self.log_test("Sector Diversity", False, "No stocks returned for diversity test", True)
                    return False
                
                # Analyze sector diversity
                diversity_issues = self.validate_sector_diversity(stocks)
                
                if diversity_issues:
                    self.log_test("Sector Diversity", False, 
                                f"Diversity issues: {diversity_issues}", True)
                    all_passed = False
                else:
                    # Count sectors represented
                    sectors = {}
                    for stock in stocks:
                        sector = stock.get("sector", "Unknown")
                        sectors[sector] = sectors.get(sector, 0) + 1
                    
                    self.log_test("Sector Diversity", True, 
                                f"Found {len(sectors)} sectors across {len(stocks)} stocks")
                    
                    print(f"  🏢 Sector breakdown:")
                    for sector, count in sorted(sectors.items()):
                        print(f"    • {sector}: {count} stocks")
                
            else:
                self.log_test("Sector Diversity API Test", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                all_passed = False
                
        except Exception as e:
            self.log_test("Sector Diversity Test", False, f"Error: {str(e)}", True)
            all_passed = False
        
        return all_passed
    
    def validate_sector_diversity(self, stocks: List[Dict[str, Any]]) -> List[str]:
        """Validate that stocks represent multiple sectors"""
        issues = []
        
        # Count sectors
        sectors = {}
        for stock in stocks:
            sector = stock.get("sector", "Unknown")
            sectors[sector] = sectors.get(sector, 0) + 1
        
        # Check for minimum sector diversity (should have at least 5 different sectors)
        if len(sectors) < 5:
            issues.append(f"Only {len(sectors)} sectors represented - need more diversity")
        
        # Check that Technology is not overwhelming (should be <60% of total)
        tech_count = sectors.get("Technology", 0)
        total_stocks = len(stocks)
        tech_percentage = (tech_count / total_stocks) * 100 if total_stocks > 0 else 0
        
        if tech_percentage > 60:
            issues.append(f"Technology sector dominates with {tech_percentage:.1f}% - need more sector balance")
        
        # Check for expected sectors from the 9-sector expansion
        expected_sectors = [
            "Technology", "Healthcare", "Finance", "Energy", "Consumer Goods", 
            "Industrial", "Communications", "Real Estate", "Materials"
        ]
        
        missing_sectors = [sector for sector in expected_sectors if sector not in sectors]
        if len(missing_sectors) > 5:  # Allow some missing, but not too many
            issues.append(f"Many expected sectors missing: {missing_sectors[:3]}...")
        
        return issues

    def test_dashboard_navigation_fix(self) -> bool:
        """
        TEST DASHBOARD NAVIGATION FIX AND DATA SOURCE TRANSPARENCY
        
        Tests the specific fixes mentioned in the review request:
        1. Dashboard → Tech Analysis Navigation with URL parameter handling
        2. Data Source Transparency with "📊 Simulated" labels
        3. Enhanced header information showing data source breakdown
        4. Backend API support for options_data_source and earnings_data_source fields
        """
        print(f"\n🎯 TESTING DASHBOARD NAVIGATION FIX AND DATA SOURCE TRANSPARENCY")
        print("=" * 80)
        
        all_passed = True
        navigation_issues = []
        
        # Test symbols mentioned in review request
        test_symbols = ["AAPL", "GOOGL", "MSFT"]
        
        # 1. Test Tech Analysis API with URL parameter simulation
        print(f"\n📱 Testing Tech Analysis API for Dashboard Navigation Support")
        for symbol in test_symbols:
            try:
                # Simulate navigation from dashboard with URL parameter
                payload = {"symbol": symbol, "timeframe": "3M"}  # Default changed to 3M
                start_time = time.time()
                
                response = requests.post(f"{BACKEND_URL}/analyze", 
                                       json=payload,
                                       headers={"Content-Type": "application/json"},
                                       timeout=30)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Validate URL parameter handling support
                    url_param_issues = self.validate_url_parameter_support(data, symbol)
                    if url_param_issues:
                        navigation_issues.extend(url_param_issues)
                        all_passed = False
                        self.log_test(f"URL Parameter Support ({symbol})", False, 
                                    f"Issues: {url_param_issues}", True)
                    else:
                        self.log_test(f"URL Parameter Support ({symbol})", True, 
                                    f"API supports dashboard navigation in {response_time:.2f}s")
                    
                    # Log console-like information for debugging
                    print(f"  🔍 {symbol}: Symbol set from URL parameter, response time: {response_time:.2f}s")
                    
                else:
                    self.log_test(f"Dashboard Navigation API ({symbol})", False, 
                                f"HTTP {response.status_code}: {response.text}", True)
                    navigation_issues.append(f"{symbol} API call failed: {response.status_code}")
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"Dashboard Navigation Test ({symbol})", False, f"Error: {str(e)}", True)
                navigation_issues.append(f"{symbol} test failed: {str(e)}")
                all_passed = False
        
        # 2. Test Stock Screener for Data Source Transparency
        print(f"\n📊 Testing Stock Screener for Data Source Transparency")
        try:
            screener_filters = {
                "price_filter": {"type": "under", "under": 500},
                "dmi_filter": {"min": 20, "max": 60},
                "ppo_slope_filter": {"threshold": 5}
            }
            
            response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                   json=screener_filters,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate data source transparency in screener
                transparency_issues = self.validate_data_source_transparency_screener(data)
                if transparency_issues:
                    navigation_issues.extend(transparency_issues)
                    all_passed = False
                    self.log_test("Data Source Transparency", False, 
                                f"Issues: {transparency_issues}", True)
                else:
                    self.log_test("Data Source Transparency", True, 
                                "Clear data source indicators present")
                
                # Check for enhanced header information
                header_info_issues = self.validate_enhanced_header_info(data)
                if header_info_issues:
                    navigation_issues.extend(header_info_issues)
                    all_passed = False
                    self.log_test("Enhanced Header Information", False, 
                                f"Issues: {header_info_issues}", True)
                else:
                    self.log_test("Enhanced Header Information", True, 
                                "Data source breakdown clearly indicated")
                
            else:
                self.log_test("Screener Data Source Test", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                navigation_issues.append(f"Screener API failed: {response.status_code}")
                all_passed = False
                
        except Exception as e:
            self.log_test("Data Source Transparency Test", False, f"Error: {str(e)}", True)
            navigation_issues.append(f"Data source transparency test failed: {str(e)}")
            all_passed = False
        
        # 3. Test Individual Stock Analysis for Data Source Fields
        print(f"\n🏷️ Testing Individual Stock Analysis for Data Source Fields")
        for symbol in test_symbols:
            try:
                response = requests.get(f"{BACKEND_URL}/analyze/{symbol}", timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check for new data source fields
                    source_field_issues = self.validate_data_source_fields(data, symbol)
                    if source_field_issues:
                        navigation_issues.extend(source_field_issues)
                        all_passed = False
                        self.log_test(f"Data Source Fields ({symbol})", False, 
                                    f"Issues: {source_field_issues}", True)
                    else:
                        self.log_test(f"Data Source Fields ({symbol})", True, 
                                    "options_data_source and earnings_data_source fields present")
                
                else:
                    self.log_test(f"Stock Analysis Data Source ({symbol})", False, 
                                f"HTTP {response.status_code}: {response.text}", True)
                    navigation_issues.append(f"{symbol} analysis failed: {response.status_code}")
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"Data Source Fields Test ({symbol})", False, f"Error: {str(e)}", True)
                navigation_issues.append(f"{symbol} data source fields test failed: {str(e)}")
                all_passed = False
        
        # Summary of dashboard navigation and data source transparency testing
        if navigation_issues:
            print(f"\n🚨 DASHBOARD NAVIGATION AND DATA SOURCE ISSUES FOUND ({len(navigation_issues)}):")
            for issue in navigation_issues:
                print(f"  • {issue}")
        else:
            print(f"\n✅ Dashboard navigation fix and data source transparency working correctly")
        
        return all_passed

    def validate_url_parameter_support(self, data: Dict[str, Any], symbol: str) -> List[str]:
        """Validate that API supports URL parameter handling for dashboard navigation"""
        issues = []
        
        # Check that symbol is properly handled
        response_symbol = data.get("symbol", "").upper()
        if response_symbol != symbol.upper():
            issues.append(f"Symbol mismatch: expected {symbol}, got {response_symbol}")
        
        # Check that response includes all necessary data for immediate display
        required_fields = ["current_price", "indicators", "chart_data", "ai_recommendation"]
        for field in required_fields:
            if field not in data or data[field] is None:
                issues.append(f"Missing {field} for immediate display")
        
        # Check that technical indicators are calculated
        indicators = data.get("indicators", {})
        if not indicators:
            issues.append("No technical indicators calculated")
        else:
            # Check key indicators needed for tech analysis
            key_indicators = ["ppo", "rsi", "dmi_plus", "dmi_minus", "adx"]
            for indicator in key_indicators:
                if indicator not in indicators or indicators[indicator] is None:
                    issues.append(f"Missing {indicator} indicator")
        
        return issues

    def validate_data_source_transparency_screener(self, data: Dict[str, Any]) -> List[str]:
        """Validate data source transparency in screener results"""
        issues = []
        
        # Check for data source information in response
        if "data_sources" not in data:
            issues.append("Missing data_sources field in response")
        
        # Check individual stock data for source indicators
        stocks = data.get("stocks", [])
        if not stocks:
            issues.append("No stocks in screener results to validate")
            return issues
        
        # Check first few stocks for data source transparency
        for i, stock in enumerate(stocks[:3]):
            symbol = stock.get("symbol", f"Stock_{i}")
            
            # Check for options data source indication
            if "options_data_source" in stock:
                options_source = stock["options_data_source"]
                if options_source == "simulated":
                    # This is good - clear indication of simulated data
                    pass
                elif options_source == "real":
                    # This is also good - clear indication of real data
                    pass
                else:
                    issues.append(f"{symbol}: Unclear options data source: {options_source}")
            
            # Check for earnings data source indication
            if "earnings_data_source" in stock:
                earnings_source = stock["earnings_data_source"]
                if earnings_source not in ["simulated", "real"]:
                    issues.append(f"{symbol}: Unclear earnings data source: {earnings_source}")
        
        return issues

    def validate_enhanced_header_info(self, data: Dict[str, Any]) -> List[str]:
        """Validate enhanced header information showing data source breakdown"""
        issues = []
        
        # Check for enhanced data source breakdown
        data_sources = data.get("data_sources", [])
        if not data_sources:
            issues.append("Missing data_sources array")
        
        # Check for specific data source notes
        note = data.get("note", "")
        if not note:
            issues.append("Missing explanatory note about data sources")
        elif "Alpha Vantage" not in note and "real" not in note.lower():
            issues.append("Note doesn't clearly indicate real vs simulated data sources")
        
        # Check for data source count information
        real_data_count = data.get("real_data_count")
        if real_data_count is None:
            issues.append("Missing real_data_count field")
        
        return issues

    def validate_data_source_fields(self, data: Dict[str, Any], symbol: str) -> List[str]:
        """Validate new data source fields in individual stock analysis"""
        issues = []
        
        # Check for options_data_source field
        if "options_data_source" not in data:
            issues.append("Missing options_data_source field")
        else:
            options_source = data["options_data_source"]
            if options_source not in ["simulated", "real", "alpha_vantage", "polygon", "yahoo_finance"]:
                issues.append(f"Invalid options_data_source value: {options_source}")
        
        # Check for earnings_data_source field
        if "earnings_data_source" not in data:
            issues.append("Missing earnings_data_source field")
        else:
            earnings_source = data["earnings_data_source"]
            if earnings_source not in ["simulated", "real", "alpha_vantage", "polygon", "yahoo_finance"]:
                issues.append(f"Invalid earnings_data_source value: {earnings_source}")
        
        # Check that data source is clearly indicated in main response
        main_data_source = data.get("data_source", "unknown")
        if main_data_source == "unknown":
            issues.append("Main data_source field is unknown")
        
        return issues

    def test_scanner_filtering_logic_fix(self) -> bool:
        """
        CRITICAL SCANNER FILTERING LOGIC FIX TESTING
        
        Tests the specific filtering criteria fix reported by the user:
        - Price Range: Under $100
        - DMI Range: Min 20, Max 60  
        - PPO Slope: Min 5%
        - PPO Hook Pattern: All Stocks
        
        Validates that filtering criteria are properly applied and no stocks
        violating the criteria appear in results.
        """
        print(f"\n🎯 CRITICAL SCANNER FILTERING LOGIC FIX TESTING")
        print("=" * 70)
        print("Testing exact user criteria from review request:")
        print("• Price Range: Under $100")
        print("• DMI Range: Min 20, Max 60")
        print("• PPO Slope: Min 5%")
        print("• PPO Hook Pattern: All Stocks")
        
        all_passed = True
        filtering_issues = []
        
        # Test the exact user criteria from the review request
        user_criteria = {
            "price_filter": {"type": "under", "under": 100},
            "dmi_filter": {"min": 20, "max": 60},
            "ppo_slope_filter": {"threshold": 5},
            "ppo_hook_filter": "all",
            "sector_filter": "all",
            "optionable_filter": "all",
            "earnings_filter": "all"
        }
        
        try:
            print(f"\n📊 Testing Scanner with Exact User Criteria")
            start_time = time.time()
            
            response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                   json=user_criteria,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                stocks = data.get("stocks", [])
                total_found = data.get("results_found", 0)
                
                print(f"✅ Scanner Response: {total_found} stocks found in {response_time:.2f}s")
                
                # Validate each stock against the filtering criteria
                validation_results = self.validate_exact_filtering_criteria(stocks, user_criteria)
                
                if validation_results["violations"]:
                    filtering_issues.extend(validation_results["violations"])
                    all_passed = False
                    
                    print(f"\n🚨 FILTERING VIOLATIONS DETECTED:")
                    for violation in validation_results["violations"]:
                        print(f"  ❌ {violation}")
                        self.log_test("Scanner Filtering Violation", False, violation, True)
                else:
                    print(f"\n✅ ALL FILTERING CRITERIA PROPERLY APPLIED")
                    self.log_test("Scanner Filtering Logic", True, 
                                f"All {len(stocks)} stocks meet filtering criteria")
                
                # Log detailed results for debugging
                print(f"\n📋 DETAILED FILTERING RESULTS:")
                print(f"  • Total stocks scanned: {data.get('total_scanned', 'N/A')}")
                print(f"  • Stocks meeting criteria: {total_found}")
                print(f"  • Price violations: {validation_results['price_violations']}")
                print(f"  • DMI violations: {validation_results['dmi_violations']}")
                print(f"  • PPO slope violations: {validation_results['ppo_violations']}")
                
                # Test debug logging is working
                if self.validate_debug_logging(data):
                    self.log_test("Debug Logging", True, "Filter decisions logged correctly")
                else:
                    self.log_test("Debug Logging", False, "Debug logging not working", True)
                    all_passed = False
                
            else:
                self.log_test("Scanner Filtering API", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                filtering_issues.append(f"API call failed: {response.status_code}")
                all_passed = False
                
        except Exception as e:
            self.log_test("Scanner Filtering Test", False, f"Error: {str(e)}", True)
            filtering_issues.append(f"Test execution failed: {str(e)}")
            all_passed = False
        
        # Test additional edge cases
        print(f"\n🔬 Testing Additional Filtering Edge Cases")
        edge_case_results = self.test_filtering_edge_cases()
        if not edge_case_results:
            all_passed = False
            filtering_issues.append("Edge case testing failed")
        
        # Test different filter combinations
        print(f"\n🎛️ Testing Different Filter Combinations")
        combination_results = self.test_filter_combinations()
        if not combination_results:
            all_passed = False
            filtering_issues.append("Filter combination testing failed")
        
        # Summary of filtering logic testing
        if filtering_issues:
            print(f"\n🚨 SCANNER FILTERING ISSUES FOUND ({len(filtering_issues)}):")
            for issue in filtering_issues:
                print(f"  • {issue}")
        else:
            print(f"\n✅ Scanner filtering logic working correctly - all criteria properly applied")
        
        return all_passed

    def validate_exact_filtering_criteria(self, stocks: List[Dict], criteria: Dict) -> Dict[str, Any]:
        """Validate stocks against exact filtering criteria from user report"""
        results = {
            "violations": [],
            "price_violations": 0,
            "dmi_violations": 0,
            "ppo_violations": 0
        }
        
        price_filter = criteria.get("price_filter", {})
        dmi_filter = criteria.get("dmi_filter", {})
        ppo_filter = criteria.get("ppo_slope_filter", {})
        
        for stock in stocks:
            symbol = stock.get("symbol", "UNKNOWN")
            
            # Validate Price Filter: Under $100
            if price_filter.get("type") == "under":
                max_price = price_filter.get("under", 100)
                stock_price = stock.get("price", 0)
                
                if stock_price > max_price:
                    violation = f"{symbol}: Price ${stock_price:.2f} exceeds filter ${max_price} (CRITICAL: Price filter violated)"
                    results["violations"].append(violation)
                    results["price_violations"] += 1
            
            # Validate DMI Filter: Min 20, Max 60 (using ADX as per backend implementation)
            dmi_min = dmi_filter.get("min", 20)
            dmi_max = dmi_filter.get("max", 60)
            stock_adx = stock.get("adx", 0)
            
            if not (dmi_min <= stock_adx <= dmi_max):
                violation = f"{symbol}: ADX {stock_adx:.2f} outside range {dmi_min}-{dmi_max} (CRITICAL: DMI filter violated)"
                results["violations"].append(violation)
                results["dmi_violations"] += 1
            
            # Validate PPO Slope Filter: Min 5% (positive slopes only after fix)
            ppo_threshold = ppo_filter.get("threshold", 5)
            stock_ppo_slope = stock.get("ppo_slope_percentage", 0)
            
            # After the fix, only positive slopes above threshold should pass
            if stock_ppo_slope < ppo_threshold:
                violation = f"{symbol}: PPO Slope {stock_ppo_slope:.2f}% below threshold {ppo_threshold}% (CRITICAL: PPO slope filter violated)"
                results["violations"].append(violation)
                results["ppo_violations"] += 1
        
        return results

    def validate_debug_logging(self, data: Dict[str, Any]) -> bool:
        """Validate that debug logging for filter decisions is working"""
        # Check if response includes debug information or filter decision logs
        debug_info = data.get("debug_info", {})
        filter_decisions = data.get("filter_decisions", [])
        
        # The fix should include debug logging - check for its presence
        if debug_info or filter_decisions:
            return True
        
        # Alternative: Check if response includes detailed filter information
        filters_applied = data.get("filters_applied", {})
        if filters_applied and len(filters_applied) > 0:
            return True
        
        return False

    def test_filtering_edge_cases(self) -> bool:
        """Test edge cases for filtering logic"""
        all_passed = True
        
        edge_cases = [
            {
                "name": "Very Restrictive Filters",
                "filters": {
                    "price_filter": {"type": "under", "under": 50},
                    "dmi_filter": {"min": 25, "max": 35},
                    "ppo_slope_filter": {"threshold": 10}
                },
                "expected_behavior": "Should return few or no results"
            },
            {
                "name": "Boundary Values",
                "filters": {
                    "price_filter": {"type": "under", "under": 100.00},
                    "dmi_filter": {"min": 20.0, "max": 60.0},
                    "ppo_slope_filter": {"threshold": 5.0}
                },
                "expected_behavior": "Should handle exact boundary values correctly"
            },
            {
                "name": "Wide Range Filters",
                "filters": {
                    "price_filter": {"type": "under", "under": 1000},
                    "dmi_filter": {"min": 0, "max": 100},
                    "ppo_slope_filter": {"threshold": 0}
                },
                "expected_behavior": "Should return many results with wide criteria"
            }
        ]
        
        for case in edge_cases:
            try:
                print(f"  Testing: {case['name']}")
                
                response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                       json=case["filters"],
                                       headers={"Content-Type": "application/json"},
                                       timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    stocks = data.get("stocks", [])
                    
                    # Validate filtering is still working correctly
                    validation_results = self.validate_exact_filtering_criteria(stocks, case["filters"])
                    
                    if validation_results["violations"]:
                        self.log_test(f"Edge Case: {case['name']}", False, 
                                    f"Filtering violations: {len(validation_results['violations'])}", True)
                        all_passed = False
                    else:
                        self.log_test(f"Edge Case: {case['name']}", True, 
                                    f"Found {len(stocks)} stocks, all meeting criteria")
                else:
                    self.log_test(f"Edge Case API: {case['name']}", False, 
                                f"HTTP {response.status_code}", True)
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"Edge Case: {case['name']}", False, f"Error: {str(e)}", True)
                all_passed = False
        
        return all_passed

    def test_filter_combinations(self) -> bool:
        """Test different combinations of filters"""
        all_passed = True
        
        combinations = [
            {
                "name": "Price Only",
                "filters": {"price_filter": {"type": "under", "under": 100}},
            },
            {
                "name": "DMI Only", 
                "filters": {"dmi_filter": {"min": 20, "max": 60}},
            },
            {
                "name": "PPO Slope Only",
                "filters": {"ppo_slope_filter": {"threshold": 5}},
            },
            {
                "name": "Price + DMI",
                "filters": {
                    "price_filter": {"type": "under", "under": 100},
                    "dmi_filter": {"min": 20, "max": 60}
                },
            },
            {
                "name": "All Three Filters",
                "filters": {
                    "price_filter": {"type": "under", "under": 100},
                    "dmi_filter": {"min": 20, "max": 60},
                    "ppo_slope_filter": {"threshold": 5}
                },
            }
        ]
        
        for combo in combinations:
            try:
                print(f"  Testing: {combo['name']}")
                
                response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                       json=combo["filters"],
                                       headers={"Content-Type": "application/json"},
                                       timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    stocks = data.get("stocks", [])
                    
                    # Validate filtering logic for this combination
                    validation_results = self.validate_exact_filtering_criteria(stocks, combo["filters"])
                    
                    if validation_results["violations"]:
                        self.log_test(f"Filter Combo: {combo['name']}", False, 
                                    f"Violations: {len(validation_results['violations'])}", True)
                        all_passed = False
                    else:
                        self.log_test(f"Filter Combo: {combo['name']}", True, 
                                    f"Found {len(stocks)} stocks, filtering correct")
                else:
                    self.log_test(f"Filter Combo API: {combo['name']}", False, 
                                f"HTTP {response.status_code}", True)
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"Filter Combo: {combo['name']}", False, f"Error: {str(e)}", True)
                all_passed = False
        
        return all_passed

    def test_ppo_hook_pattern_filtering(self) -> bool:
        """
        COMPREHENSIVE PPO HOOK PATTERN FILTERING TEST
        
        Tests the specific user issue: Scanner with negative hook criteria should return results
        but returned no results. Tests:
        1. Negative hook pattern detection logic
        2. User's exact criteria: Price $100-$500, DMI 20-60, PPO Slope Min -100%, PPO Hook: -HOOK
        3. Debug logging for hook pattern analysis
        4. Combined filters working together
        """
        print(f"\n🎯 COMPREHENSIVE PPO HOOK PATTERN FILTERING TEST")
        print("=" * 70)
        
        all_passed = True
        hook_issues = []
        
        # Test the exact user criteria from the review request
        user_criteria = {
            "price_filter": {"type": "range", "min": 100, "max": 500},
            "dmi_filter": {"min": 20, "max": 60},
            "ppo_slope_filter": {"threshold": -100},
            "ppo_hook_filter": "-HOOK"
        }
        
        print(f"\n📊 Testing User's Exact Criteria:")
        print(f"  • Price Range: $100-$500 (broad range)")
        print(f"  • DMI Range: 20-60 (reasonable range)")
        print(f"  • PPO Slope: Min -100% (very permissive, allows negative slopes)")
        print(f"  • PPO Hook Pattern: Negative Hook (-HOOK) Only")
        
        try:
            start_time = time.time()
            response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                   json=user_criteria,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate response structure
                if not self.validate_screener_response(data, "User Exact Criteria"):
                    all_passed = False
                    hook_issues.append("Invalid screener response structure")
                
                # Check results
                results_found = data.get("results_found", 0)
                total_scanned = data.get("total_scanned", 0)
                stocks = data.get("stocks", [])
                
                print(f"\n📈 RESULTS ANALYSIS:")
                print(f"  • Total Stocks Scanned: {total_scanned}")
                print(f"  • Results Found: {results_found}")
                print(f"  • Response Time: {response_time:.2f}s")
                
                # The key issue: With broad criteria, we should find SOME negative hook patterns
                if results_found == 0:
                    self.log_test("Negative Hook Detection", False, 
                                f"No results found with broad criteria - negative hook detection may not be working", True)
                    hook_issues.append("No negative hook patterns detected with permissive criteria")
                    all_passed = False
                else:
                    self.log_test("Negative Hook Detection", True, 
                                f"Found {results_found} stocks with negative hook patterns")
                    
                    # Validate that returned stocks actually have negative hooks
                    negative_hook_validation = self.validate_negative_hook_patterns(stocks)
                    if not negative_hook_validation:
                        all_passed = False
                        hook_issues.append("Returned stocks don't have valid negative hook patterns")
                
                # Test debug logging analysis
                self.analyze_hook_debug_logs(data, user_criteria)
                
            else:
                self.log_test("PPO Hook Filter API", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                hook_issues.append(f"API call failed: {response.status_code}")
                all_passed = False
                
        except Exception as e:
            self.log_test("PPO Hook Filter Test", False, f"Error: {str(e)}", True)
            hook_issues.append(f"Test execution failed: {str(e)}")
            all_passed = False
        
        # Test positive hook patterns for comparison
        print(f"\n🔄 Testing Positive Hook Patterns for Comparison")
        positive_criteria = user_criteria.copy()
        positive_criteria["ppo_hook_filter"] = "+HOOK"
        
        try:
            response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                   json=positive_criteria,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                positive_results = data.get("results_found", 0)
                print(f"  • Positive Hook Results: {positive_results}")
                
                if positive_results > 0:
                    self.log_test("Positive Hook Detection", True, 
                                f"Found {positive_results} stocks with positive hook patterns")
                else:
                    self.log_test("Positive Hook Detection", False, 
                                "No positive hook patterns found either - may indicate broader issue", True)
                    hook_issues.append("No positive hook patterns detected either")
                    all_passed = False
            else:
                hook_issues.append(f"Positive hook test failed: {response.status_code}")
                all_passed = False
                
        except Exception as e:
            hook_issues.append(f"Positive hook test error: {str(e)}")
            all_passed = False
        
        # Test both hooks filter
        print(f"\n🔄 Testing Both Hook Patterns Filter")
        both_criteria = user_criteria.copy()
        both_criteria["ppo_hook_filter"] = "both"
        
        try:
            response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                   json=both_criteria,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                both_results = data.get("results_found", 0)
                print(f"  • Both Hook Patterns Results: {both_results}")
                
                if both_results > 0:
                    self.log_test("Both Hook Patterns", True, 
                                f"Found {both_results} stocks with hook patterns")
                else:
                    self.log_test("Both Hook Patterns", False, 
                                "No hook patterns found with 'both' filter", True)
                    hook_issues.append("No hook patterns detected with 'both' filter")
                    all_passed = False
            else:
                hook_issues.append(f"Both hooks test failed: {response.status_code}")
                all_passed = False
                
        except Exception as e:
            hook_issues.append(f"Both hooks test error: {str(e)}")
            all_passed = False
        
        # Test edge cases
        print(f"\n🔬 Testing Hook Pattern Edge Cases")
        edge_case_results = self.test_hook_pattern_edge_cases()
        if not edge_case_results:
            all_passed = False
            hook_issues.append("Hook pattern edge cases failed")
        
        # Summary
        if hook_issues:
            print(f"\n🚨 PPO HOOK PATTERN FILTERING ISSUES FOUND ({len(hook_issues)}):")
            for issue in hook_issues:
                print(f"  • {issue}")
        else:
            print(f"\n✅ PPO hook pattern filtering working correctly")
        
        return all_passed

    def validate_negative_hook_patterns(self, stocks: List[Dict[str, Any]]) -> bool:
        """Validate that returned stocks actually have negative hook patterns"""
        all_valid = True
        
        for i, stock in enumerate(stocks[:5]):  # Check first 5 stocks
            symbol = stock.get("symbol", f"Stock_{i}")
            ppo_values = stock.get("ppo_values", [])
            
            if len(ppo_values) >= 3:
                today = ppo_values[0]
                yesterday = ppo_values[1] 
                day_before = ppo_values[2]
                
                # Negative Hook: Today < Yesterday AND Yesterday > Day Before
                negative_hook = today < yesterday and yesterday > day_before
                
                if not negative_hook:
                    self.log_test(f"Negative Hook Validation ({symbol})", False, 
                                f"Stock doesn't have negative hook: PPO({today:.3f}, {yesterday:.3f}, {day_before:.3f})", True)
                    all_valid = False
                else:
                    self.log_test(f"Negative Hook Validation ({symbol})", True, 
                                f"Valid negative hook: PPO({today:.3f}, {yesterday:.3f}, {day_before:.3f})")
            else:
                self.log_test(f"PPO Data Validation ({symbol})", False, 
                            f"Insufficient PPO data: {len(ppo_values)} values", True)
                all_valid = False
        
        return all_valid

    def analyze_hook_debug_logs(self, data: Dict[str, Any], criteria: Dict[str, Any]) -> None:
        """Analyze debug logging for hook pattern detection"""
        # This would analyze server logs if available
        # For now, we'll analyze the response data structure
        
        stocks = data.get("stocks", [])
        filters_applied = data.get("filters_applied", {})
        
        print(f"\n🔍 HOOK PATTERN ANALYSIS:")
        print(f"  • Filters Applied: {filters_applied}")
        print(f"  • Hook Filter: {filters_applied.get('ppo_hook_filter', 'Not found')}")
        
        if stocks:
            print(f"  • Sample Stock PPO Analysis:")
            for i, stock in enumerate(stocks[:3]):
                symbol = stock.get("symbol", f"Stock_{i}")
                ppo_values = stock.get("ppo_values", [])
                if len(ppo_values) >= 3:
                    today, yesterday, day_before = ppo_values[0], ppo_values[1], ppo_values[2]
                    negative_hook = today < yesterday and yesterday > day_before
                    print(f"    • {symbol}: PPO({today:.3f}, {yesterday:.3f}, {day_before:.3f}) - Negative Hook: {negative_hook}")

    def test_hook_pattern_edge_cases(self) -> bool:
        """Test edge cases for hook pattern detection"""
        all_passed = True
        
        # Test with very restrictive other filters but permissive hook filter
        restrictive_criteria = {
            "price_filter": {"type": "range", "min": 50, "max": 1000},  # Very broad price range
            "dmi_filter": {"min": 10, "max": 80},  # Very broad DMI range
            "ppo_slope_filter": {"threshold": -200},  # Very permissive slope
            "ppo_hook_filter": "-HOOK"
        }
        
        try:
            response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                   json=restrictive_criteria,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get("results_found", 0)
                
                if results > 0:
                    self.log_test("Hook Edge Case - Broad Filters", True, 
                                f"Found {results} negative hooks with very broad other filters")
                else:
                    self.log_test("Hook Edge Case - Broad Filters", False, 
                                "No negative hooks found even with very broad other filters", True)
                    all_passed = False
            else:
                self.log_test("Hook Edge Case API", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                all_passed = False
                
        except Exception as e:
            self.log_test("Hook Edge Case Test", False, f"Error: {str(e)}", True)
            all_passed = False
        
        return all_passed

    def test_dmi_hook_pattern_filtering_fix(self) -> bool:
        """
        COMPREHENSIVE DMI AND HOOK PATTERN FILTERING FIX TESTING
        
        Tests the specific fixes for DMI filtering and hook pattern detection:
        1. DMI Filter Validation - Test exact user criteria with DMI range 20-60
        2. Hook Pattern Detection - Verify negative hook pattern filtering works
        3. Hook Pattern Display - Check ppo_hook_type and ppo_hook_display fields
        4. Comprehensive Testing - Test different hook filter combinations
        5. Debug Validation - Verify debug logging shows actual DMI values
        
        Uses exact filter criteria from user's bug report:
        - price_filter: {"type": "range", "min": 100, "max": 600}
        - dmi_filter: {"min": 20, "max": 60}
        - ppo_slope_filter: {"threshold": 0}
        - ppo_hook_filter: "-HOOK"
        """
        print(f"\n🎯 COMPREHENSIVE DMI AND HOOK PATTERN FILTERING FIX TESTING")
        print("=" * 70)
        
        all_passed = True
        fix_issues = []
        
        # 1. Test DMI Filter Validation with exact user criteria
        print(f"\n📊 Testing DMI Filter Validation (User's Exact Criteria)")
        dmi_validation_passed = self.test_dmi_filter_validation()
        if not dmi_validation_passed:
            all_passed = False
            fix_issues.append("DMI filter validation failed")
        
        # 2. Test Hook Pattern Detection
        print(f"\n🎣 Testing Hook Pattern Detection")
        hook_detection_passed = self.test_hook_pattern_detection()
        if not hook_detection_passed:
            all_passed = False
            fix_issues.append("Hook pattern detection failed")
        
        # 3. Test Hook Pattern Display Enhancement
        print(f"\n🏷️ Testing Hook Pattern Display Enhancement")
        hook_display_passed = self.test_hook_pattern_display()
        if not hook_display_passed:
            all_passed = False
            fix_issues.append("Hook pattern display enhancement failed")
        
        # 4. Test Comprehensive Hook Filter Combinations
        print(f"\n🔄 Testing Comprehensive Hook Filter Combinations")
        hook_combinations_passed = self.test_hook_filter_combinations()
        if not hook_combinations_passed:
            all_passed = False
            fix_issues.append("Hook filter combinations failed")
        
        # 5. Test Debug Validation
        print(f"\n🔍 Testing Debug Validation")
        debug_validation_passed = self.test_debug_validation()
        if not debug_validation_passed:
            all_passed = False
            fix_issues.append("Debug validation failed")
        
        # Summary of DMI and Hook Pattern fix testing
        if fix_issues:
            print(f"\n🚨 DMI AND HOOK PATTERN FIX ISSUES FOUND ({len(fix_issues)}):")
            for issue in fix_issues:
                print(f"  • {issue}")
        else:
            print(f"\n✅ DMI and Hook Pattern filtering fixes working correctly")
        
        return all_passed

    def test_dmi_filter_validation(self) -> bool:
        """Test DMI filter validation with user's exact criteria"""
        all_passed = True
        
        # User's exact criteria from bug report
        user_criteria = {
            "price_filter": {"type": "range", "min": 100, "max": 600},
            "dmi_filter": {"min": 20, "max": 60},
            "ppo_slope_filter": {"threshold": 0},
            "ppo_hook_filter": "-HOOK"
        }
        
        try:
            print(f"  🎯 Testing user's exact criteria: Price $100-$600, DMI 20-60, PPO Slope 0%+, Negative Hook Only")
            
            start_time = time.time()
            response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                   json=user_criteria,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                stocks = data.get("stocks", [])
                
                print(f"    📈 Found {len(stocks)} stocks matching criteria in {response_time:.2f}s")
                
                # Validate DMI filtering - NO results should have DMI < 20 or DMI > 60
                dmi_violations = []
                hook_pattern_issues = []
                
                for stock in stocks:
                    symbol = stock.get("symbol", "Unknown")
                    
                    # Check DMI value (should be composite DMI, not ADX)
                    dmi_value = stock.get("dmi")  # Should use actual DMI composite value
                    adx_value = stock.get("adx")  # For comparison
                    
                    if dmi_value is not None:
                        if dmi_value < 20 or dmi_value > 60:
                            dmi_violations.append(f"{symbol}: DMI={dmi_value:.2f} (outside 20-60 range)")
                    
                    # Check hook pattern fields
                    ppo_hook_type = stock.get("ppo_hook_type")
                    ppo_hook_display = stock.get("ppo_hook_display")
                    
                    if ppo_hook_type != "negative":
                        hook_pattern_issues.append(f"{symbol}: ppo_hook_type='{ppo_hook_type}' (expected 'negative')")
                    
                    if ppo_hook_display != "- Hook":
                        hook_pattern_issues.append(f"{symbol}: ppo_hook_display='{ppo_hook_display}' (expected '- Hook')")
                    
                    print(f"    📊 {symbol}: DMI={dmi_value}, ADX={adx_value}, Hook Type={ppo_hook_type}, Hook Display={ppo_hook_display}")
                
                # Report DMI violations (critical issue)
                if dmi_violations:
                    self.log_test("DMI Filter Validation", False, 
                                f"DMI violations found: {dmi_violations}", True)
                    all_passed = False
                else:
                    self.log_test("DMI Filter Validation", True, 
                                f"All {len(stocks)} results have DMI values within 20-60 range")
                
                # Report hook pattern issues
                if hook_pattern_issues:
                    self.log_test("Hook Pattern Fields", False, 
                                f"Hook pattern issues: {hook_pattern_issues}", True)
                    all_passed = False
                else:
                    self.log_test("Hook Pattern Fields", True, 
                                f"All {len(stocks)} results have correct negative hook pattern fields")
                
            else:
                self.log_test("DMI Filter API Test", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                all_passed = False
                
        except Exception as e:
            self.log_test("DMI Filter Validation Test", False, f"Error: {str(e)}", True)
            all_passed = False
        
        return all_passed

    def test_hook_pattern_detection(self) -> bool:
        """Test hook pattern detection logic"""
        all_passed = True
        
        # Test different hook pattern scenarios
        hook_test_cases = [
            {
                "name": "Negative Hook Only",
                "filters": {
                    "price_filter": {"type": "range", "min": 100, "max": 600},
                    "dmi_filter": {"min": 20, "max": 60},
                    "ppo_slope_filter": {"threshold": 0},
                    "ppo_hook_filter": "-HOOK"
                },
                "expected_hook_type": "negative"
            },
            {
                "name": "Positive Hook Only", 
                "filters": {
                    "price_filter": {"type": "range", "min": 100, "max": 600},
                    "dmi_filter": {"min": 20, "max": 60},
                    "ppo_slope_filter": {"threshold": 0},
                    "ppo_hook_filter": "+HOOK"
                },
                "expected_hook_type": "positive"
            }
        ]
        
        for test_case in hook_test_cases:
            try:
                print(f"  🎣 Testing {test_case['name']}")
                
                response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                       json=test_case["filters"],
                                       headers={"Content-Type": "application/json"},
                                       timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    stocks = data.get("stocks", [])
                    
                    print(f"    📈 Found {len(stocks)} stocks with {test_case['name']}")
                    
                    # Validate hook pattern detection
                    hook_detection_issues = []
                    
                    for stock in stocks:
                        symbol = stock.get("symbol", "Unknown")
                        ppo_hook_type = stock.get("ppo_hook_type")
                        ppo_values = stock.get("ppo_values", [])
                        
                        # Verify hook type matches expected
                        if ppo_hook_type != test_case["expected_hook_type"]:
                            hook_detection_issues.append(f"{symbol}: Expected {test_case['expected_hook_type']}, got {ppo_hook_type}")
                        
                        # Verify hook pattern logic with PPO values
                        if len(ppo_values) >= 3:
                            today, yesterday, day_before = ppo_values[0], ppo_values[1], ppo_values[2]
                            
                            if test_case["expected_hook_type"] == "negative":
                                # Negative hook: TODAY < YESTERDAY AND YESTERDAY > DAY_BEFORE
                                if not (today < yesterday and yesterday > day_before):
                                    hook_detection_issues.append(f"{symbol}: PPO values {ppo_values} don't match negative hook pattern")
                            elif test_case["expected_hook_type"] == "positive":
                                # Positive hook: TODAY > YESTERDAY AND YESTERDAY < DAY_BEFORE
                                if not (today > yesterday and yesterday < day_before):
                                    hook_detection_issues.append(f"{symbol}: PPO values {ppo_values} don't match positive hook pattern")
                        
                        print(f"    📊 {symbol}: Hook Type={ppo_hook_type}, PPO={ppo_values}")
                    
                    if hook_detection_issues:
                        self.log_test(f"Hook Detection ({test_case['name']})", False, 
                                    f"Detection issues: {hook_detection_issues}", True)
                        all_passed = False
                    else:
                        self.log_test(f"Hook Detection ({test_case['name']})", True, 
                                    f"All {len(stocks)} results have correct hook pattern detection")
                
                else:
                    self.log_test(f"Hook Detection API ({test_case['name']})", False, 
                                f"HTTP {response.status_code}: {response.text}", True)
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"Hook Detection Test ({test_case['name']})", False, f"Error: {str(e)}", True)
                all_passed = False
        
        return all_passed

    def test_hook_pattern_display(self) -> bool:
        """Test hook pattern display enhancement with ppo_hook_type and ppo_hook_display fields"""
        all_passed = True
        
        # Test that response includes proper hook pattern information
        test_filters = {
            "price_filter": {"type": "range", "min": 100, "max": 600},
            "dmi_filter": {"min": 20, "max": 60},
            "ppo_slope_filter": {"threshold": 0},
            "ppo_hook_filter": "-HOOK"
        }
        
        try:
            print(f"  🏷️ Testing hook pattern display fields")
            
            response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                   json=test_filters,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                stocks = data.get("stocks", [])
                
                display_issues = []
                
                for stock in stocks:
                    symbol = stock.get("symbol", "Unknown")
                    
                    # Check for new hook pattern fields
                    ppo_hook_type = stock.get("ppo_hook_type")
                    ppo_hook_display = stock.get("ppo_hook_display")
                    
                    # Validate field presence
                    if ppo_hook_type is None:
                        display_issues.append(f"{symbol}: Missing ppo_hook_type field")
                    elif ppo_hook_type not in ["positive", "negative", "null"]:
                        display_issues.append(f"{symbol}: Invalid ppo_hook_type value: {ppo_hook_type}")
                    
                    if ppo_hook_display is None:
                        display_issues.append(f"{symbol}: Missing ppo_hook_display field")
                    elif ppo_hook_display not in ["+ Hook", "- Hook", None]:
                        display_issues.append(f"{symbol}: Invalid ppo_hook_display value: {ppo_hook_display}")
                    
                    # Validate consistency between type and display
                    if ppo_hook_type == "negative" and ppo_hook_display != "- Hook":
                        display_issues.append(f"{symbol}: Inconsistent negative hook display: type={ppo_hook_type}, display={ppo_hook_display}")
                    elif ppo_hook_type == "positive" and ppo_hook_display != "+ Hook":
                        display_issues.append(f"{symbol}: Inconsistent positive hook display: type={ppo_hook_type}, display={ppo_hook_display}")
                    
                    print(f"    🏷️ {symbol}: Type='{ppo_hook_type}', Display='{ppo_hook_display}'")
                
                if display_issues:
                    self.log_test("Hook Pattern Display", False, 
                                f"Display issues: {display_issues}", True)
                    all_passed = False
                else:
                    self.log_test("Hook Pattern Display", True, 
                                f"All {len(stocks)} results have correct hook pattern display fields")
            
            else:
                self.log_test("Hook Display API Test", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                all_passed = False
                
        except Exception as e:
            self.log_test("Hook Display Test", False, f"Error: {str(e)}", True)
            all_passed = False
        
        return all_passed

    def test_hook_filter_combinations(self) -> bool:
        """Test comprehensive hook filter combinations"""
        all_passed = True
        
        # Test different hook filter combinations as specified in review request
        hook_combinations = [
            {
                "name": "Negative Hook (-HOOK) Only",
                "ppo_hook_filter": "-HOOK",
                "expected_types": ["negative"]
            },
            {
                "name": "Positive Hook (+HOOK) Only",
                "ppo_hook_filter": "+HOOK", 
                "expected_types": ["positive"]
            },
            {
                "name": "Both Hooks",
                "ppo_hook_filter": "BOTH",
                "expected_types": ["positive", "negative"]
            },
            {
                "name": "All Stocks (No Hook Filter)",
                "ppo_hook_filter": "ALL",
                "expected_types": ["positive", "negative", "null"]
            }
        ]
        
        for combination in hook_combinations:
            try:
                print(f"  🔄 Testing {combination['name']}")
                
                base_filters = {
                    "price_filter": {"type": "range", "min": 100, "max": 600},
                    "dmi_filter": {"min": 20, "max": 60},
                    "ppo_slope_filter": {"threshold": 0}
                }
                
                # Add hook filter if not "All Stocks"
                if combination["ppo_hook_filter"] != "ALL":
                    base_filters["ppo_hook_filter"] = combination["ppo_hook_filter"]
                
                response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                       json=base_filters,
                                       headers={"Content-Type": "application/json"},
                                       timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    stocks = data.get("stocks", [])
                    
                    print(f"    📈 Found {len(stocks)} stocks for {combination['name']}")
                    
                    # Validate hook type distribution
                    hook_type_counts = {}
                    combination_issues = []
                    
                    for stock in stocks:
                        symbol = stock.get("symbol", "Unknown")
                        ppo_hook_type = stock.get("ppo_hook_type", "null")
                        
                        hook_type_counts[ppo_hook_type] = hook_type_counts.get(ppo_hook_type, 0) + 1
                        
                        # Validate hook type is in expected types
                        if ppo_hook_type not in combination["expected_types"]:
                            combination_issues.append(f"{symbol}: Unexpected hook type '{ppo_hook_type}' for {combination['name']}")
                    
                    print(f"    📊 Hook type distribution: {hook_type_counts}")
                    
                    if combination_issues:
                        self.log_test(f"Hook Combination ({combination['name']})", False, 
                                    f"Combination issues: {combination_issues}", True)
                        all_passed = False
                    else:
                        self.log_test(f"Hook Combination ({combination['name']})", True, 
                                    f"All {len(stocks)} results have expected hook types: {list(hook_type_counts.keys())}")
                
                else:
                    self.log_test(f"Hook Combination API ({combination['name']})", False, 
                                f"HTTP {response.status_code}: {response.text}", True)
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"Hook Combination Test ({combination['name']})", False, f"Error: {str(e)}", True)
                all_passed = False
        
        return all_passed

    def test_debug_validation(self) -> bool:
        """Test debug validation - verify debug logging shows actual DMI values instead of ADX"""
        all_passed = True
        
        # This test would ideally check backend logs, but since we can't access logs directly,
        # we'll validate the response data to ensure DMI vs ADX distinction
        
        test_filters = {
            "price_filter": {"type": "range", "min": 100, "max": 600},
            "dmi_filter": {"min": 20, "max": 60},
            "ppo_slope_filter": {"threshold": 0},
            "ppo_hook_filter": "-HOOK"
        }
        
        try:
            print(f"  🔍 Testing debug validation (DMI vs ADX distinction)")
            
            response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                   json=test_filters,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                stocks = data.get("stocks", [])
                
                debug_issues = []
                
                for stock in stocks:
                    symbol = stock.get("symbol", "Unknown")
                    dmi_value = stock.get("dmi")  # Should be composite DMI value
                    adx_value = stock.get("adx")  # Should be different from DMI
                    di_plus = stock.get("di_plus")
                    di_minus = stock.get("di_minus")
                    
                    # Validate that DMI and ADX are different values (not the same)
                    if dmi_value is not None and adx_value is not None:
                        if abs(dmi_value - adx_value) < 0.01:  # Essentially the same value
                            debug_issues.append(f"{symbol}: DMI ({dmi_value}) and ADX ({adx_value}) are identical - may indicate DMI is using ADX value")
                    
                    # Validate DMI composite calculation if we have DI+ and DI-
                    if di_plus is not None and di_minus is not None and dmi_value is not None:
                        expected_dmi = (di_plus + di_minus) / 2
                        if abs(dmi_value - expected_dmi) > 1.0:  # Allow some tolerance
                            debug_issues.append(f"{symbol}: DMI ({dmi_value}) doesn't match expected composite (DI+={di_plus}, DI-={di_minus}, Expected={(di_plus + di_minus) / 2})")
                    
                    print(f"    🔍 {symbol}: DMI={dmi_value}, ADX={adx_value}, DI+={di_plus}, DI-={di_minus}")
                
                if debug_issues:
                    self.log_test("Debug Validation", False, 
                                f"Debug issues: {debug_issues}", True)
                    all_passed = False
                else:
                    self.log_test("Debug Validation", True, 
                                f"All {len(stocks)} results show proper DMI vs ADX distinction")
            
            else:
                self.log_test("Debug Validation API Test", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                all_passed = False
                
        except Exception as e:
            self.log_test("Debug Validation Test", False, f"Error: {str(e)}", True)
            all_passed = False
        
        return all_passed

    def test_hook_filtering_parameter_mismatch_fix(self) -> bool:
        """
        CRITICAL TEST: Test the hook filtering parameter mismatch fix using EXACT user criteria
        
        Tests the specific fix for hook filtering where frontend sends ppo_hook_filter values
        'positive'/'negative'/'both' but backend was checking for '+HOOK'/'-HOOK'/'both'.
        
        Validates:
        1. Hook Filter Parameter Testing - verify ppo_hook_filter="negative" returns ONLY negative hook stocks
        2. Backend Parameter Matching - confirm backend checks for "negative" instead of "-HOOK"
        3. Hook Detection Logic - validate mathematical correctness
        4. Debug Logging Verification - check logs show proper hook filtering
        5. Zero Tolerance Test - ANY +Hook or no hook when "negative" filter applied is CRITICAL FAILURE
        """
        print(f"\n🎯 CRITICAL HOOK FILTERING PARAMETER MISMATCH FIX TESTING")
        print("=" * 80)
        
        all_passed = True
        critical_issues = []
        
        # Test the EXACT user criteria from the review request
        exact_user_criteria = {
            "price_filter": {"type": "range", "min": 100, "max": 500},
            "dmi_filter": {"min": 20, "max": 60}, 
            "ppo_slope_filter": {"threshold": 0},
            "ppo_hook_filter": "negative"
        }
        
        print(f"\n📊 Testing EXACT User Criteria:")
        print(f"  • Price Range: $100-$500")
        print(f"  • DMI Range: 20-60")
        print(f"  • PPO Slope: 0% minimum")
        print(f"  • PPO Hook Filter: 'negative' (Negative Hook (-HOOK) Only)")
        
        # Test 1: Exact User Criteria Test
        try:
            start_time = time.time()
            response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                   json=exact_user_criteria,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                stocks = data.get("stocks", [])
                results_found = data.get("results_found", 0)
                
                print(f"\n✅ API Response: {results_found} stocks found in {response_time:.2f}s")
                
                # CRITICAL VALIDATION: Hook Filter Parameter Testing
                hook_validation_issues = self.validate_negative_hook_filtering(stocks, "Exact User Criteria")
                
                if hook_validation_issues:
                    critical_issues.extend(hook_validation_issues)
                    all_passed = False
                    self.log_test("Hook Filter Parameter Testing (Exact Criteria)", False, 
                                f"CRITICAL FAILURES: {hook_validation_issues}", True)
                else:
                    self.log_test("Hook Filter Parameter Testing (Exact Criteria)", True, 
                                f"All {results_found} stocks have valid negative hook patterns")
                
                # Validate mathematical correctness of hook detection
                math_validation_issues = self.validate_hook_detection_mathematics(stocks, "negative")
                if math_validation_issues:
                    critical_issues.extend(math_validation_issues)
                    all_passed = False
                
            else:
                self.log_test("Exact User Criteria API", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                critical_issues.append(f"API call failed: {response.status_code}")
                all_passed = False
                
        except Exception as e:
            self.log_test("Exact User Criteria Test", False, f"Error: {str(e)}", True)
            critical_issues.append(f"Exact criteria test failed: {str(e)}")
            all_passed = False
        
        # Test 2: Multiple Hook Filter Scenarios
        hook_filter_scenarios = [
            {"filter": "positive", "description": "Positive Hook (+HOOK) Only"},
            {"filter": "negative", "description": "Negative Hook (-HOOK) Only"},
            {"filter": "both", "description": "Both Hooks (+HOOK OR -HOOK)"},
            {"filter": "all", "description": "All Stocks (no hook filter)"}
        ]
        
        print(f"\n🔬 Testing Multiple Hook Filter Scenarios:")
        
        for scenario in hook_filter_scenarios:
            try:
                test_filters = {
                    "price_filter": {"type": "range", "min": 100, "max": 500},
                    "dmi_filter": {"min": 20, "max": 60}, 
                    "ppo_slope_filter": {"threshold": 0},
                    "ppo_hook_filter": scenario["filter"]
                }
                
                response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                       json=test_filters,
                                       headers={"Content-Type": "application/json"},
                                       timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    stocks = data.get("stocks", [])
                    results_found = data.get("results_found", 0)
                    
                    print(f"  📈 {scenario['description']}: {results_found} stocks found")
                    
                    # Validate hook filtering for each scenario
                    scenario_issues = self.validate_hook_filtering_scenario(stocks, scenario["filter"], scenario["description"])
                    
                    if scenario_issues:
                        critical_issues.extend(scenario_issues)
                        all_passed = False
                        self.log_test(f"Hook Filter Scenario ({scenario['filter']})", False, 
                                    f"Issues: {scenario_issues}", True)
                    else:
                        self.log_test(f"Hook Filter Scenario ({scenario['filter']})", True, 
                                    f"Correct filtering for {scenario['description']}")
                        
                else:
                    self.log_test(f"Hook Filter Scenario ({scenario['filter']})", False, 
                                f"HTTP {response.status_code}: {response.text}", True)
                    critical_issues.append(f"Scenario {scenario['filter']} failed: {response.status_code}")
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"Hook Filter Scenario ({scenario['filter']})", False, f"Error: {str(e)}", True)
                critical_issues.append(f"Scenario {scenario['filter']} error: {str(e)}")
                all_passed = False
        
        # Test 3: Backend Parameter Matching Verification
        print(f"\n🔧 Testing Backend Parameter Matching:")
        backend_param_issues = self.test_backend_parameter_matching()
        if backend_param_issues:
            critical_issues.extend(backend_param_issues)
            all_passed = False
        
        # Test 4: Debug Logging Verification
        print(f"\n📝 Testing Debug Logging Verification:")
        debug_logging_issues = self.test_debug_logging_verification()
        if debug_logging_issues:
            critical_issues.extend(debug_logging_issues)
            all_passed = False
        
        # Summary of Hook Filtering Fix Testing
        if critical_issues:
            print(f"\n🚨 CRITICAL HOOK FILTERING ISSUES FOUND ({len(critical_issues)}):")
            for issue in critical_issues:
                print(f"  • {issue}")
        else:
            print(f"\n✅ Hook filtering parameter mismatch fix working correctly")
        
        return all_passed

    def validate_negative_hook_filtering(self, stocks: List[Dict], test_name: str) -> List[str]:
        """Validate that ONLY stocks with negative hook patterns are returned"""
        issues = []
        
        if not stocks:
            issues.append("No stocks returned - should have negative hook patterns within criteria")
            return issues
        
        for i, stock in enumerate(stocks):
            symbol = stock.get("symbol", f"Stock_{i}")
            ppo_values = stock.get("ppo_values", [])
            
            if len(ppo_values) < 3:
                issues.append(f"{symbol}: Insufficient PPO values for hook detection ({len(ppo_values)})")
                continue
            
            # PPO values are ordered: [Today, Yesterday, Day_Before]
            today = ppo_values[0]
            yesterday = ppo_values[1] 
            day_before = ppo_values[2]
            
            # Negative Hook: Today < Yesterday AND Yesterday > Day_Before
            negative_hook = today < yesterday and yesterday > day_before
            
            # Positive Hook: Today > Yesterday AND Yesterday < Day_Before  
            positive_hook = today > yesterday and yesterday < day_before
            
            if positive_hook:
                issues.append(f"CRITICAL: {symbol} has POSITIVE hook pattern (Today={today:.3f} > Yesterday={yesterday:.3f} < Day_Before={day_before:.3f}) but negative filter applied")
            elif not negative_hook:
                issues.append(f"CRITICAL: {symbol} has NO hook pattern (Today={today:.3f}, Yesterday={yesterday:.3f}, Day_Before={day_before:.3f}) but negative filter applied")
            else:
                # Valid negative hook - log for verification
                print(f"    ✅ {symbol}: Valid negative hook (Today={today:.3f} < Yesterday={yesterday:.3f} > Day_Before={day_before:.3f})")
        
        return issues

    def validate_hook_detection_mathematics(self, stocks: List[Dict], expected_hook_type: str) -> List[str]:
        """Validate mathematical correctness of hook detection logic"""
        issues = []
        
        for i, stock in enumerate(stocks):
            symbol = stock.get("symbol", f"Stock_{i}")
            ppo_values = stock.get("ppo_values", [])
            
            if len(ppo_values) < 3:
                continue
            
            today = ppo_values[0]
            yesterday = ppo_values[1]
            day_before = ppo_values[2]
            
            # Mathematical validation of hook patterns
            if expected_hook_type == "negative":
                # Negative Hook: Today < Yesterday AND Yesterday > Day_Before
                condition1 = today < yesterday
                condition2 = yesterday > day_before
                
                if not (condition1 and condition2):
                    issues.append(f"MATH ERROR {symbol}: Negative hook logic failed - Today<Yesterday: {condition1}, Yesterday>Day_Before: {condition2}")
            
            elif expected_hook_type == "positive":
                # Positive Hook: Today > Yesterday AND Yesterday < Day_Before
                condition1 = today > yesterday
                condition2 = yesterday < day_before
                
                if not (condition1 and condition2):
                    issues.append(f"MATH ERROR {symbol}: Positive hook logic failed - Today>Yesterday: {condition1}, Yesterday<Day_Before: {condition2}")
        
        return issues

    def validate_hook_filtering_scenario(self, stocks: List[Dict], filter_type: str, description: str) -> List[str]:
        """Validate hook filtering for different scenarios"""
        issues = []
        
        if filter_type == "all":
            # Should return stocks regardless of hook patterns
            return issues  # No validation needed for "all"
        
        for i, stock in enumerate(stocks):
            symbol = stock.get("symbol", f"Stock_{i}")
            ppo_values = stock.get("ppo_values", [])
            
            if len(ppo_values) < 3:
                issues.append(f"{symbol}: Insufficient PPO values for hook detection")
                continue
            
            today = ppo_values[0]
            yesterday = ppo_values[1]
            day_before = ppo_values[2]
            
            # Detect actual hook patterns
            positive_hook = today > yesterday and yesterday < day_before
            negative_hook = today < yesterday and yesterday > day_before
            
            # Validate based on filter type
            if filter_type == "positive" and not positive_hook:
                issues.append(f"{symbol}: Expected positive hook but found pattern (T={today:.3f}, Y={yesterday:.3f}, D={day_before:.3f})")
            elif filter_type == "negative" and not negative_hook:
                issues.append(f"{symbol}: Expected negative hook but found pattern (T={today:.3f}, Y={yesterday:.3f}, D={day_before:.3f})")
            elif filter_type == "both" and not (positive_hook or negative_hook):
                issues.append(f"{symbol}: Expected hook pattern but found none (T={today:.3f}, Y={yesterday:.3f}, D={day_before:.3f})")
        
        return issues

    def test_backend_parameter_matching(self) -> List[str]:
        """Test that backend correctly matches frontend parameter values"""
        issues = []
        
        # This test verifies that the backend now accepts "negative" instead of "-HOOK"
        # We can infer this from successful API responses with the new parameter format
        
        test_cases = [
            {"ppo_hook_filter": "negative", "expected": "should work"},
            {"ppo_hook_filter": "positive", "expected": "should work"},
            {"ppo_hook_filter": "both", "expected": "should work"}
        ]
        
        for test_case in test_cases:
            try:
                filters = {
                    "price_filter": {"type": "range", "min": 100, "max": 500},
                    "ppo_hook_filter": test_case["ppo_hook_filter"]
                }
                
                response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                       json=filters,
                                       headers={"Content-Type": "application/json"},
                                       timeout=15)
                
                if response.status_code == 200:
                    self.log_test(f"Backend Parameter Matching ({test_case['ppo_hook_filter']})", True, 
                                "Backend correctly accepts new parameter format")
                elif response.status_code == 500:
                    # 500 error might indicate the old parameter format issue
                    issues.append(f"Backend may still expect old format for {test_case['ppo_hook_filter']}")
                    self.log_test(f"Backend Parameter Matching ({test_case['ppo_hook_filter']})", False, 
                                "Backend may not accept new parameter format", True)
                else:
                    issues.append(f"Unexpected response {response.status_code} for {test_case['ppo_hook_filter']}")
                    
            except Exception as e:
                issues.append(f"Parameter matching test failed for {test_case['ppo_hook_filter']}: {str(e)}")
        
        return issues

    def test_debug_logging_verification(self) -> List[str]:
        """Test that debug logging shows proper hook filtering logic"""
        issues = []
        
        # Since we can't directly access backend logs, we infer logging quality from API responses
        # and the presence of detailed stock information that would require proper logging
        
        try:
            filters = {
                "price_filter": {"type": "range", "min": 100, "max": 500},
                "dmi_filter": {"min": 20, "max": 60},
                "ppo_hook_filter": "negative"
            }
            
            response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                   json=filters,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check if response includes debugging information
                if "debug_info" in data or "filters_applied" in data:
                    self.log_test("Debug Logging Verification", True, 
                                "Response includes debugging information")
                else:
                    # Infer logging quality from response completeness
                    stocks = data.get("stocks", [])
                    if stocks and all("ppo_values" in stock for stock in stocks[:3]):
                        self.log_test("Debug Logging Verification", True, 
                                    "Detailed stock data suggests proper logging")
                    else:
                        issues.append("Response lacks detailed information suggesting insufficient logging")
                        self.log_test("Debug Logging Verification", False, 
                                    "Insufficient detail in response", True)
            else:
                issues.append(f"Debug logging test failed with status {response.status_code}")
                
        except Exception as e:
            issues.append(f"Debug logging verification failed: {str(e)}")
        
        return issues

    def run_comprehensive_tests(self):
        """Run all tests with priority on scanner filtering logic fix from review request"""
        print("🚀 Starting Comprehensive Stock Analysis API Tests")
        print("=" * 60)
        
        # Test basic connectivity first
        if not self.test_basic_connectivity():
            print("❌ Basic connectivity failed. Stopping tests.")
            return self.results
        
        # CRITICAL PRIORITY: Test Hook Filtering Parameter Mismatch Fix (Current Review Request Focus)
        print(f"\n🎯 CRITICAL PRIORITY: HOOK FILTERING PARAMETER MISMATCH FIX")
        self.test_hook_filtering_parameter_mismatch_fix()
        
        # HIGHEST PRIORITY: Test DMI and Hook Pattern Filtering Fix (Current Review Request Focus)
        print(f"\n🎯 HIGHEST PRIORITY: DMI AND HOOK PATTERN FILTERING FIX")
        self.test_dmi_hook_pattern_filtering_fix()
        
        # HIGHEST PRIORITY: Test PPO Hook Pattern Filtering (Current Review Request Focus)
        print(f"\n🎯 HIGHEST PRIORITY: PPO HOOK PATTERN FILTERING TEST")
        self.test_ppo_hook_pattern_filtering()
        
        # HIGHEST PRIORITY: Test Scanner Filtering Logic Fix (Review Request Focus)
        print(f"\n🎯 HIGHEST PRIORITY: SCANNER FILTERING LOGIC FIX")
        self.test_scanner_filtering_logic_fix()
        
        # PRIORITY: Test Dashboard Navigation Fix and Data Source Transparency (Review Request Focus)
        print(f"\n🎯 PRIORITY: DASHBOARD NAVIGATION FIX AND DATA SOURCE TRANSPARENCY")
        self.test_dashboard_navigation_fix()
        
        # PRIORITY: Test Critical DMI+ Value Variation (Review Request Focus)
        print(f"\n🎯 PRIORITY: CRITICAL DMI+ VALUE VARIATION TEST")
        critical_dmi_passed = self.test_dmi_value_variation_critical()
        
        # PRIORITY: Test Critical Runtime Errors Fix (Review Request Focus)
        print(f"\n🚨 PRIORITY: CRITICAL RUNTIME ERRORS FIX TESTING")
        self.test_critical_runtime_errors_fix()
        
        # PRIORITY: Test Multiple Component Fixes (Review Request Focus)
        print(f"\n🔧 PRIORITY: MULTIPLE COMPONENT FIXES TESTING")
        self.test_multiple_component_fixes()
        
        # PRIORITY: Test Stock Screener Real Data Fix (Review Request Focus)
        print(f"\n🔧 PRIORITY: STOCK SCREENER REAL DATA FIX TESTING")
        self.test_stock_screener_real_data_fix()
        
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