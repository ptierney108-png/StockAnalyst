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

    def test_polygon_api_ppo_data_availability(self) -> bool:
        """
        CRITICAL BUG INVESTIGATION: Test Polygon API PPO data availability issue
        
        Tests the specific issue where Polygon API may not provide sufficient data
        for PPO calculations, causing missing or zero PPO values in screener results.
        """
        print(f"\n🔍 CRITICAL BUG INVESTIGATION: Polygon API PPO Data Availability")
        print("=" * 70)
        
        all_passed = True
        polygon_issues = []
        
        # Test symbols that might have limited data from Polygon
        test_symbols = ["AAPL", "GOOGL", "MSFT", "TSLA", "NVDA", "AMZN"]
        
        for symbol in test_symbols:
            print(f"\n📊 Testing PPO data availability for {symbol}")
            
            # Test /api/analyze endpoint with various timeframes
            timeframes = ["1D", "5D", "1M", "3M"]
            
            for timeframe in timeframes:
                try:
                    # Force API usage by making multiple calls to potentially trigger Polygon fallback
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
                        
                        # Check PPO data availability
                        ppo_issues = self.validate_ppo_data_availability(data, symbol, timeframe, data_source)
                        
                        if ppo_issues:
                            polygon_issues.extend(ppo_issues)
                            all_passed = False
                            self.log_test(f"PPO Data Availability ({symbol} {timeframe})", False, 
                                        f"Data source: {data_source}, Issues: {ppo_issues}", True)
                        else:
                            self.log_test(f"PPO Data Availability ({symbol} {timeframe})", True, 
                                        f"Data source: {data_source}, PPO data complete")
                        
                        # Log data source for analysis
                        print(f"  📡 Data source for {symbol} ({timeframe}): {data_source}")
                        
                    else:
                        self.log_test(f"PPO API Test ({symbol} {timeframe})", False, 
                                    f"HTTP {response.status_code}: {response.text}", True)
                        all_passed = False
                        
                except Exception as e:
                    self.log_test(f"PPO API Test ({symbol} {timeframe})", False, 
                                f"Error: {str(e)}", True)
                    all_passed = False
        
        # Test screener endpoint with focus on PPO data
        print(f"\n📊 Testing Stock Screener PPO Data Consistency")
        try:
            # Test screener with PPO-focused filters
            ppo_filters = {
                "price_filter": {"type": "under", "under": 300},
                "dmi_filter": {"min": 20, "max": 60},
                "ppo_slope_filter": {"threshold": 1},  # Low threshold to catch more stocks
                "sector_filter": "all"
            }
            
            response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                   json=ppo_filters,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                screener_ppo_issues = self.validate_screener_ppo_data(data)
                
                if screener_ppo_issues:
                    polygon_issues.extend(screener_ppo_issues)
                    all_passed = False
                    self.log_test("Screener PPO Data", False, 
                                f"PPO issues in screener: {screener_ppo_issues}", True)
                else:
                    self.log_test("Screener PPO Data", True, 
                                "All screener stocks have valid PPO data")
            else:
                self.log_test("Screener PPO Test", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                all_passed = False
                
        except Exception as e:
            self.log_test("Screener PPO Test", False, f"Error: {str(e)}", True)
            all_passed = False
        
        # Test edge case: insufficient data points for PPO calculation
        print(f"\n🔬 Testing Edge Case: Insufficient Data Points for PPO")
        try:
            # Test with very short timeframe that might not have enough data
            edge_payload = {"symbol": "AAPL", "timeframe": "1D"}
            response = requests.post(f"{BACKEND_URL}/analyze", 
                                   json=edge_payload,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                chart_data = data.get("chart_data", [])
                
                if len(chart_data) < 26:
                    # Test how system handles insufficient data for PPO calculation
                    ppo_handling = self.validate_insufficient_data_handling(data, len(chart_data))
                    if not ppo_handling:
                        all_passed = False
                        self.log_test("Insufficient Data Handling", False, 
                                    f"Poor handling of {len(chart_data)} data points for PPO", True)
                    else:
                        self.log_test("Insufficient Data Handling", True, 
                                    f"Graceful handling of {len(chart_data)} data points")
                else:
                    self.log_test("Edge Case Data Points", True, 
                                f"Sufficient data points: {len(chart_data)}")
            else:
                self.log_test("Edge Case Test", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                all_passed = False
                
        except Exception as e:
            self.log_test("Edge Case Test", False, f"Error: {str(e)}", True)
            all_passed = False
        
        # Summary of Polygon API PPO investigation
        if polygon_issues:
            print(f"\n🚨 POLYGON API PPO ISSUES FOUND ({len(polygon_issues)}):")
            for issue in polygon_issues:
                print(f"  • {issue}")
        else:
            print(f"\n✅ No Polygon API PPO issues detected")
        
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
    
    def run_comprehensive_tests(self):
        """Run all tests"""
        print("🚀 Starting Comprehensive Stock Analysis API Tests")
        print("=" * 60)
        
        # Test basic connectivity first
        if not self.test_basic_connectivity():
            print("❌ Basic connectivity failed. Stopping tests.")
            return self.results
        
        # PRIORITY: Test Polygon API PPO Data Availability (Critical Bug Investigation)
        print(f"\n🚨 CRITICAL BUG INVESTIGATION: Polygon API PPO Data Availability")
        self.test_polygon_api_ppo_data_availability()
        
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