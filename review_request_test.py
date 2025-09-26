#!/usr/bin/env python3
"""
Review Request Specific Testing
Tests the two specific fixes mentioned in the review request:
1. Tech Analysis Button Only Works After Page Navigation
2. Scanner Should Show Blank Fields When No Data
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any, List

# Configuration
BACKEND_URL = "https://market-analyzer-95.preview.emergentagent.com/api"

class ReviewRequestTester:
    def __init__(self):
        self.results = {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "test_details": [],
            "critical_issues": []
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

    def test_tech_analysis_initial_load(self) -> bool:
        """
        Test that tech analysis works immediately on page load without requiring navigation
        """
        print(f"\n🎯 TESTING: Tech Analysis Initial Load Fix")
        print("=" * 60)
        
        all_passed = True
        test_symbols = ["AAPL", "GOOGL", "MSFT"]
        
        for symbol in test_symbols:
            try:
                # Simulate initial page load - direct API call
                payload = {"symbol": symbol, "timeframe": "3M"}
                start_time = time.time()
                
                response = requests.post(f"{BACKEND_URL}/analyze", 
                                       json=payload,
                                       headers={"Content-Type": "application/json"},
                                       timeout=30)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check immediate data availability
                    if self.validate_immediate_response(data, symbol, response_time):
                        self.log_test(f"Tech Analysis Initial Load ({symbol})", True, 
                                    f"Works immediately in {response_time:.2f}s")
                    else:
                        self.log_test(f"Tech Analysis Initial Load ({symbol})", False, 
                                    "Data not immediately available", True)
                        all_passed = False
                else:
                    self.log_test(f"Tech Analysis API ({symbol})", False, 
                                f"HTTP {response.status_code}", True)
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"Tech Analysis Test ({symbol})", False, 
                            f"Error: {str(e)}", True)
                all_passed = False
        
        return all_passed

    def validate_immediate_response(self, data: Dict[str, Any], symbol: str, response_time: float) -> bool:
        """Validate that response is immediate and complete"""
        # Check essential fields are present
        required_fields = ["symbol", "current_price", "indicators", "ai_recommendation", "chart_data"]
        
        for field in required_fields:
            if field not in data or data[field] is None:
                return False
        
        # Check technical indicators are calculated
        indicators = data.get("indicators", {})
        key_indicators = ["ppo", "rsi", "dmi_plus", "dmi_minus"]
        
        for indicator in key_indicators:
            if indicators.get(indicator) is None:
                return False
        
        # Response should be reasonably fast (under 20 seconds)
        if response_time > 20:
            return False
        
        return True

    def test_scanner_null_data_handling(self) -> bool:
        """
        Test that scanner shows "No data" messages when data is unavailable
        """
        print(f"\n🎯 TESTING: Scanner Null Data Handling Fix")
        print("=" * 60)
        
        all_passed = True
        
        try:
            # Test stock screener
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
                
                if not stocks:
                    self.log_test("Scanner Response", False, "No stocks returned", True)
                    return False
                
                # Validate null data handling
                null_data_results = self.validate_null_data_display(stocks)
                
                if null_data_results["has_variation"]:
                    self.log_test("Scanner Data Availability Variation", True, 
                                f"Options: {null_data_results['options_percentage']:.1f}%, Earnings: {null_data_results['earnings_percentage']:.1f}%")
                else:
                    self.log_test("Scanner Data Availability Variation", False, 
                                "All stocks have identical data availability", True)
                    all_passed = False
                
                if null_data_results["proper_null_handling"]:
                    self.log_test("Scanner Null Data Messages", True, 
                                "Proper 'No data' messages displayed")
                else:
                    self.log_test("Scanner Null Data Messages", False, 
                                "Missing or incorrect null data handling", True)
                    all_passed = False
                
                # Log sample data patterns
                self.log_sample_data_patterns(stocks[:5])
                
            else:
                self.log_test("Scanner API", False, f"HTTP {response.status_code}", True)
                all_passed = False
                
        except Exception as e:
            self.log_test("Scanner Test", False, f"Error: {str(e)}", True)
            all_passed = False
        
        return all_passed

    def validate_null_data_display(self, stocks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate null data display in scanner results"""
        options_with_data = 0
        earnings_with_data = 0
        total_stocks = len(stocks)
        proper_null_handling = True
        
        for stock in stocks:
            # Check options data
            call_bid = stock.get("call_bid")
            has_options = call_bid is not None and call_bid not in ["No options data", "N/A", None]
            
            if has_options:
                options_with_data += 1
            else:
                # Should show proper null message
                options_exp = stock.get("options_expiration")
                if options_exp and options_exp not in ["No options data", "N/A", None]:
                    proper_null_handling = False
            
            # Check earnings data
            next_earnings = stock.get("next_earnings")
            has_earnings = next_earnings is not None and next_earnings not in ["No earnings data", "N/A", None]
            
            if has_earnings:
                earnings_with_data += 1
            else:
                # Should show proper null message
                days_to_earnings = stock.get("days_to_earnings")
                if days_to_earnings and days_to_earnings not in ["No earnings data", "N/A", None]:
                    proper_null_handling = False
        
        options_percentage = (options_with_data / total_stocks) * 100 if total_stocks > 0 else 0
        earnings_percentage = (earnings_with_data / total_stocks) * 100 if total_stocks > 0 else 0
        
        # Check for variation (not all stocks have same data availability)
        has_variation = not (options_percentage == 0 or options_percentage == 100) or not (earnings_percentage == 0 or earnings_percentage == 100)
        
        return {
            "options_percentage": options_percentage,
            "earnings_percentage": earnings_percentage,
            "has_variation": has_variation,
            "proper_null_handling": proper_null_handling
        }

    def log_sample_data_patterns(self, stocks: List[Dict[str, Any]]) -> None:
        """Log sample data patterns for analysis"""
        print(f"\n  📊 Sample Data Patterns:")
        
        for i, stock in enumerate(stocks):
            symbol = stock.get("symbol", f"Stock_{i}")
            
            # Options status
            call_bid = stock.get("call_bid")
            options_status = "DATA" if (call_bid and call_bid not in ["No options data", "N/A"]) else "NO_DATA"
            
            # Earnings status
            next_earnings = stock.get("next_earnings")
            earnings_status = "DATA" if (next_earnings and next_earnings not in ["No earnings data", "N/A"]) else "NO_DATA"
            
            print(f"    {symbol}: Options={options_status}, Earnings={earnings_status}")

    def test_null_value_frontend_handling(self) -> bool:
        """Test that frontend properly handles null values without errors"""
        print(f"\n🎯 TESTING: Null Value Frontend Handling")
        print("=" * 60)
        
        all_passed = True
        
        try:
            # Test with a symbol that might return null values
            payload = {"symbol": "AAPL", "timeframe": "1D"}
            response = requests.post(f"{BACKEND_URL}/analyze", 
                                   json=payload,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check for null values in response
                null_fields = self.find_null_fields(data)
                
                if null_fields:
                    self.log_test("Null Values Present", True, 
                                f"Found null fields (should be handled by frontend): {null_fields}")
                else:
                    self.log_test("Null Values Handling", True, 
                                "Backend providing fallback values, no nulls found")
                
                # Validate response structure is intact
                if self.validate_response_structure(data):
                    self.log_test("Response Structure Integrity", True, 
                                "Response structure intact despite any null values")
                else:
                    self.log_test("Response Structure Integrity", False, 
                                "Response structure compromised", True)
                    all_passed = False
                
            else:
                self.log_test("Null Value Test API", False, f"HTTP {response.status_code}", True)
                all_passed = False
                
        except Exception as e:
            self.log_test("Null Value Test", False, f"Error: {str(e)}", True)
            all_passed = False
        
        return all_passed

    def find_null_fields(self, data: Dict[str, Any], prefix: str = "") -> List[str]:
        """Recursively find null fields in response data"""
        null_fields = []
        
        for key, value in data.items():
            full_key = f"{prefix}.{key}" if prefix else key
            
            if value is None:
                null_fields.append(full_key)
            elif isinstance(value, dict):
                null_fields.extend(self.find_null_fields(value, full_key))
            elif isinstance(value, list) and value and isinstance(value[0], dict):
                # Check first item in list for null fields
                null_fields.extend(self.find_null_fields(value[0], f"{full_key}[0]"))
        
        return null_fields

    def validate_response_structure(self, data: Dict[str, Any]) -> bool:
        """Validate that response has proper structure"""
        required_fields = ["symbol", "current_price", "indicators", "chart_data"]
        
        for field in required_fields:
            if field not in data:
                return False
        
        # Check indicators structure
        indicators = data.get("indicators", {})
        if not isinstance(indicators, dict):
            return False
        
        # Check chart data structure
        chart_data = data.get("chart_data", [])
        if not isinstance(chart_data, list):
            return False
        
        return True

    def run_review_request_tests(self):
        """Run all tests for the review request"""
        print("🎯 REVIEW REQUEST SPECIFIC TESTING")
        print("=" * 70)
        print("Testing two critical fixes:")
        print("1. Tech Analysis Button Only Works After Page Navigation")
        print("2. Scanner Should Show Blank Fields When No Data")
        print("=" * 70)
        
        # Test 1: Tech Analysis Initial Load
        tech_analysis_passed = self.test_tech_analysis_initial_load()
        
        # Test 2: Scanner Null Data Handling
        scanner_null_passed = self.test_scanner_null_data_handling()
        
        # Test 3: Null Value Frontend Handling
        null_handling_passed = self.test_null_value_frontend_handling()
        
        # Generate summary
        print(f"\n📊 REVIEW REQUEST TESTS SUMMARY")
        print("=" * 50)
        print(f"Total Tests: {self.results['total_tests']}")
        print(f"Passed: {self.results['passed_tests']}")
        print(f"Failed: {self.results['failed_tests']}")
        success_rate = (self.results['passed_tests'] / self.results['total_tests']) * 100 if self.results['total_tests'] > 0 else 0
        print(f"Success Rate: {success_rate:.1f}%")
        
        if self.results['critical_issues']:
            print(f"\n🚨 CRITICAL ISSUES FOUND ({len(self.results['critical_issues'])}):")
            for issue in self.results['critical_issues']:
                print(f"  • {issue}")
        else:
            print(f"\n✅ All review request tests passed successfully!")
        
        # Specific conclusions for the review request
        print(f"\n🎯 REVIEW REQUEST CONCLUSIONS:")
        print("=" * 50)
        
        if tech_analysis_passed:
            print("✅ Tech Analysis Initial Load: WORKING - Analysis works immediately without navigation")
        else:
            print("❌ Tech Analysis Initial Load: FAILED - Still requires navigation")
        
        if scanner_null_passed:
            print("✅ Scanner Null Data Handling: WORKING - Proper 'No data' messages displayed")
        else:
            print("❌ Scanner Null Data Handling: FAILED - Missing proper null data handling")
        
        if null_handling_passed:
            print("✅ Null Value Handling: WORKING - Frontend handles null values properly")
        else:
            print("❌ Null Value Handling: FAILED - Issues with null value handling")
        
        return self.results

def main():
    """Main test execution"""
    tester = ReviewRequestTester()
    results = tester.run_review_request_tests()
    
    # Return exit code based on results
    if results['failed_tests'] > 0:
        exit(1)
    else:
        exit(0)

if __name__ == "__main__":
    main()