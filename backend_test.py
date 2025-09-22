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
BACKEND_URL = "https://smartinvest-hub-2.preview.emergentagent.com/api"
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
    
    def run_comprehensive_tests(self):
        """Run all tests"""
        print("🚀 Starting Comprehensive Stock Analysis API Tests")
        print("=" * 60)
        
        # Test basic connectivity first
        if not self.test_basic_connectivity():
            print("❌ Basic connectivity failed. Stopping tests.")
            return self.results
        
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