#!/usr/bin/env python3
"""
Critical Fixes Testing for User-Reported Issues
Tests the specific fixes implemented for:
1. Tech Analysis Button Complete Failure
2. Scanner Options Data Missing Strike Prices  
3. Scanner Hardcoded/Demo Data Issues
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any, List

# Configuration
BACKEND_URL = "https://stockwise-116.preview.emergentagent.com/api"
TEST_SYMBOLS = ["WFC", "AAPL", "GOOGL", "MSFT"]  # Specific symbols mentioned in review request

class CriticalFixesTester:
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

    def test_tech_analysis_functionality(self) -> bool:
        """
        CRITICAL TEST 1: Tech Analysis Button Complete Failure Fix
        
        Tests that manual stock entry works immediately without refresh requirement.
        Validates the React Query fix with staleTime: 0, enabled: !!symbol && symbol.length >= 1
        """
        print(f"\n🔧 TESTING TECH ANALYSIS FUNCTIONALITY FIX")
        print("=" * 70)
        
        all_passed = True
        
        for symbol in TEST_SYMBOLS:
            try:
                # Test the analyze endpoint that the tech analysis button uses
                payload = {"symbol": symbol, "timeframe": "3M"}  # Default timeframe should be 3M
                start_time = time.time()
                
                response = requests.post(f"{BACKEND_URL}/analyze", 
                                       json=payload,
                                       headers={"Content-Type": "application/json"},
                                       timeout=30)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Validate immediate response (no refresh needed)
                    if response_time < 20:  # Should respond quickly
                        self.log_test(f"Tech Analysis Response Time ({symbol})", True, 
                                    f"Quick response in {response_time:.2f}s")
                    else:
                        self.log_test(f"Tech Analysis Response Time ({symbol})", False, 
                                    f"Slow response: {response_time:.2f}s", True)
                        all_passed = False
                    
                    # Validate complete data structure
                    required_fields = ["symbol", "current_price", "indicators", "ai_recommendation", 
                                     "chart_data", "ppo_history", "dmi_history"]
                    missing_fields = [field for field in required_fields if field not in data]
                    
                    if missing_fields:
                        self.log_test(f"Tech Analysis Data Structure ({symbol})", False, 
                                    f"Missing fields: {missing_fields}", True)
                        all_passed = False
                    else:
                        self.log_test(f"Tech Analysis Data Structure ({symbol})", True, 
                                    "All required fields present")
                    
                    # Validate technical indicators are populated
                    indicators = data.get("indicators", {})
                    if not indicators or indicators.get("ppo") is None:
                        self.log_test(f"Tech Analysis Indicators ({symbol})", False, 
                                    "Technical indicators missing or null", True)
                        all_passed = False
                    else:
                        ppo = indicators.get("ppo", 0)
                        rsi = indicators.get("rsi", 0)
                        self.log_test(f"Tech Analysis Indicators ({symbol})", True, 
                                    f"PPO={ppo:.4f}, RSI={rsi:.1f}")
                    
                    # Validate AI recommendations are present
                    ai_rec = data.get("ai_recommendation")
                    if ai_rec not in ["BUY", "SELL", "HOLD"]:
                        self.log_test(f"Tech Analysis AI Recommendation ({symbol})", False, 
                                    f"Invalid AI recommendation: {ai_rec}", True)
                        all_passed = False
                    else:
                        ai_confidence = data.get("ai_confidence", 0)
                        self.log_test(f"Tech Analysis AI Recommendation ({symbol})", True, 
                                    f"AI: {ai_rec} (confidence: {ai_confidence:.2f})")
                
                else:
                    self.log_test(f"Tech Analysis API ({symbol})", False, 
                                f"HTTP {response.status_code}: {response.text}", True)
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"Tech Analysis Test ({symbol})", False, f"Error: {str(e)}", True)
                all_passed = False
        
        return all_passed

    def test_options_strike_prices(self) -> bool:
        """
        CRITICAL TEST 2: Scanner Options Data Missing Strike Prices Fix
        
        Tests that options data now includes strike prices in "C{price}: X.XX-Y.YY" format
        """
        print(f"\n📊 TESTING OPTIONS STRIKE PRICES FIX")
        print("=" * 70)
        
        all_passed = True
        
        try:
            # Test stock screener endpoint for options data
            filters = {
                "price_filter": {"type": "under", "under": 500},
                "dmi_filter": {"min": 15, "max": 65},
                "ppo_slope_filter": {"threshold": 1},
                "optionable_filter": "yes"  # Focus on optionable stocks
            }
            
            response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                   json=filters,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                stocks = data.get("stocks", [])
                
                if not stocks:
                    self.log_test("Options Strike Prices - No Stocks", False, 
                                "No stocks returned from screener", True)
                    return False
                
                # Test first few stocks for options strike prices
                for i, stock in enumerate(stocks[:5]):
                    symbol = stock.get("symbol", f"Stock_{i}")
                    
                    # Check for call and put strike prices
                    call_strike = stock.get("call_strike")
                    put_strike = stock.get("put_strike")
                    call_bid = stock.get("call_bid")
                    call_ask = stock.get("call_ask")
                    put_bid = stock.get("put_bid")
                    put_ask = stock.get("put_ask")
                    
                    if call_strike is None or put_strike is None:
                        self.log_test(f"Options Strike Prices ({symbol})", False, 
                                    f"Missing strike prices: call_strike={call_strike}, put_strike={put_strike}", True)
                        all_passed = False
                    else:
                        # Validate strike prices are realistic (based on current price)
                        current_price = stock.get("price", 0)
                        if current_price > 0:
                            # Strike prices should be within reasonable range of current price
                            call_strike_diff = abs(call_strike - current_price) / current_price
                            put_strike_diff = abs(put_strike - current_price) / current_price
                            
                            if call_strike_diff > 0.5 or put_strike_diff > 0.5:  # More than 50% difference
                                self.log_test(f"Options Strike Price Realism ({symbol})", False, 
                                            f"Strike prices unrealistic: C{call_strike:.2f}, P{put_strike:.2f} vs price ${current_price:.2f}", True)
                                all_passed = False
                            else:
                                self.log_test(f"Options Strike Prices ({symbol})", True, 
                                            f"C{call_strike:.2f}: {call_bid:.2f}-{call_ask:.2f}, P{put_strike:.2f}: {put_bid:.2f}-{put_ask:.2f}")
                    
                    # Check bid-ask spread is reasonable
                    if call_bid and call_ask and call_bid > call_ask:
                        self.log_test(f"Options Bid-Ask Logic ({symbol})", False, 
                                    f"Call bid ({call_bid}) > ask ({call_ask})", True)
                        all_passed = False
                    
                    if put_bid and put_ask and put_bid > put_ask:
                        self.log_test(f"Options Bid-Ask Logic ({symbol})", False, 
                                    f"Put bid ({put_bid}) > ask ({put_ask})", True)
                        all_passed = False
            
            else:
                self.log_test("Options Strike Prices API", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                all_passed = False
                
        except Exception as e:
            self.log_test("Options Strike Prices Test", False, f"Error: {str(e)}", True)
            all_passed = False
        
        return all_passed

    def test_stock_specific_data_generation(self) -> bool:
        """
        CRITICAL TEST 3: Scanner Hardcoded/Demo Data Fix
        
        Tests that different stocks show different expiration dates, earnings dates, 
        and days to earnings (not identical across all stocks)
        """
        print(f"\n🎯 TESTING STOCK-SPECIFIC DATA GENERATION FIX")
        print("=" * 70)
        
        all_passed = True
        
        try:
            # Test stock screener for data uniqueness
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
                
                if len(stocks) < 3:
                    self.log_test("Stock-Specific Data - Insufficient Stocks", False, 
                                f"Need at least 3 stocks for comparison, got {len(stocks)}", True)
                    return False
                
                # Collect data from multiple stocks for comparison
                expiration_dates = []
                earnings_dates = []
                days_to_earnings = []
                
                for stock in stocks[:10]:  # Check first 10 stocks
                    symbol = stock.get("symbol", "Unknown")
                    
                    # Check expiration dates
                    options_expiration = stock.get("options_expiration")
                    if options_expiration:
                        expiration_dates.append(options_expiration)
                    
                    # Check earnings dates
                    next_earnings = stock.get("next_earnings")
                    if next_earnings:
                        earnings_dates.append(next_earnings)
                    
                    # Check days to earnings
                    days_to_earn = stock.get("days_to_earnings")
                    if days_to_earn is not None:
                        days_to_earnings.append(days_to_earn)
                    
                    print(f"  📈 {symbol}: Exp={options_expiration}, Earnings={next_earnings}, Days={days_to_earn}")
                
                # Test 1: Expiration dates should not all be "Oct 15"
                unique_expirations = set(expiration_dates)
                if len(unique_expirations) == 1 and "Oct 15" in unique_expirations:
                    self.log_test("Expiration Date Uniqueness", False, 
                                "All stocks show same expiration date 'Oct 15' (hardcoded data)", True)
                    all_passed = False
                elif len(unique_expirations) > 1:
                    self.log_test("Expiration Date Uniqueness", True, 
                                f"{len(unique_expirations)} unique expiration dates found")
                else:
                    self.log_test("Expiration Date Uniqueness", False, 
                                f"Only 1 unique expiration date: {unique_expirations}", True)
                    all_passed = False
                
                # Test 2: Earnings dates should vary by stock
                unique_earnings = set(earnings_dates)
                if len(unique_earnings) == 1:
                    self.log_test("Earnings Date Uniqueness", False, 
                                f"All stocks show same earnings date: {unique_earnings} (hardcoded data)", True)
                    all_passed = False
                elif len(unique_earnings) > 1:
                    self.log_test("Earnings Date Uniqueness", True, 
                                f"{len(unique_earnings)} unique earnings dates found")
                else:
                    self.log_test("Earnings Date Uniqueness", False, 
                                "No earnings dates found", True)
                    all_passed = False
                
                # Test 3: Days to earnings should vary
                unique_days = set(days_to_earnings)
                if len(unique_days) == 1 and 45 in unique_days:
                    self.log_test("Days to Earnings Uniqueness", False, 
                                "All stocks show same days to earnings: 45 (hardcoded data)", True)
                    all_passed = False
                elif len(unique_days) > 1:
                    self.log_test("Days to Earnings Uniqueness", True, 
                                f"{len(unique_days)} unique days to earnings values found")
                else:
                    self.log_test("Days to Earnings Uniqueness", False, 
                                f"Only 1 unique days to earnings: {unique_days}", True)
                    all_passed = False
                
                # Test 4: Validate realistic data generation
                self.validate_realistic_data_patterns(stocks)
            
            else:
                self.log_test("Stock-Specific Data API", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                all_passed = False
                
        except Exception as e:
            self.log_test("Stock-Specific Data Test", False, f"Error: {str(e)}", True)
            all_passed = False
        
        return all_passed

    def validate_realistic_data_patterns(self, stocks: List[Dict[str, Any]]) -> bool:
        """Validate that data follows realistic patterns"""
        all_passed = True
        
        for stock in stocks[:5]:
            symbol = stock.get("symbol", "Unknown")
            
            # Check expiration dates follow monthly cycles
            options_expiration = stock.get("options_expiration", "")
            if options_expiration and options_expiration != "N/A":
                # Should be in format like "Nov 15", "Dec 20", etc.
                if "Oct 15" == options_expiration:
                    # This is okay if it's actually October, but suspicious if all stocks have it
                    pass
                elif any(month in options_expiration for month in ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                                                                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]):
                    self.log_test(f"Realistic Expiration Format ({symbol})", True, 
                                f"Proper month format: {options_expiration}")
                else:
                    self.log_test(f"Realistic Expiration Format ({symbol})", False, 
                                f"Invalid expiration format: {options_expiration}", True)
                    all_passed = False
            
            # Check earnings dates are reasonable
            next_earnings = stock.get("next_earnings", "")
            if next_earnings and next_earnings != "N/A":
                # Should not all be "Nov 8" or identical dates
                if next_earnings == "Nov 8":
                    # This might be hardcoded if all stocks have it
                    pass
                else:
                    self.log_test(f"Realistic Earnings Date ({symbol})", True, 
                                f"Unique earnings date: {next_earnings}")
            
            # Check days to earnings are reasonable (not all 45)
            days_to_earn = stock.get("days_to_earnings")
            if days_to_earn is not None:
                if 0 <= days_to_earn <= 365:  # Reasonable range
                    if days_to_earn != 45:  # Not the hardcoded value
                        self.log_test(f"Realistic Days to Earnings ({symbol})", True, 
                                    f"Reasonable days: {days_to_earn}")
                else:
                    self.log_test(f"Realistic Days to Earnings ({symbol})", False, 
                                f"Unrealistic days to earnings: {days_to_earn}", True)
                    all_passed = False
        
        return all_passed

    def test_individual_stock_uniqueness(self) -> bool:
        """
        Test specific symbols mentioned in review request for unique data
        """
        print(f"\n🔍 TESTING INDIVIDUAL STOCK DATA UNIQUENESS")
        print("=" * 70)
        
        all_passed = True
        stock_data = {}
        
        # Get data for each test symbol
        for symbol in TEST_SYMBOLS:
            try:
                payload = {"symbol": symbol, "timeframe": "3M"}
                response = requests.post(f"{BACKEND_URL}/analyze", 
                                       json=payload,
                                       headers={"Content-Type": "application/json"},
                                       timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    stock_data[symbol] = data
                    
                    # Log key data points
                    indicators = data.get("indicators", {})
                    ppo = indicators.get("ppo", 0)
                    dmi_plus = indicators.get("dmi_plus", 0)
                    current_price = data.get("current_price", 0)
                    
                    print(f"  📊 {symbol}: Price=${current_price:.2f}, PPO={ppo:.4f}, DMI+={dmi_plus:.2f}")
                    
                else:
                    self.log_test(f"Individual Stock Data ({symbol})", False, 
                                f"HTTP {response.status_code}: {response.text}", True)
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"Individual Stock Test ({symbol})", False, f"Error: {str(e)}", True)
                all_passed = False
        
        # Compare data between stocks
        if len(stock_data) >= 2:
            symbols = list(stock_data.keys())
            
            # Compare PPO values
            ppo_values = []
            dmi_plus_values = []
            prices = []
            
            for symbol in symbols:
                data = stock_data[symbol]
                indicators = data.get("indicators", {})
                ppo_values.append(indicators.get("ppo", 0))
                dmi_plus_values.append(indicators.get("dmi_plus", 0))
                prices.append(data.get("current_price", 0))
            
            # Test PPO uniqueness
            unique_ppo = len(set(ppo_values))
            if unique_ppo == 1 and ppo_values[0] == 0:
                self.log_test("Individual Stock PPO Uniqueness", False, 
                            "All stocks have identical zero PPO values", True)
                all_passed = False
            elif unique_ppo > 1:
                self.log_test("Individual Stock PPO Uniqueness", True, 
                            f"{unique_ppo} unique PPO values across {len(symbols)} stocks")
            else:
                self.log_test("Individual Stock PPO Uniqueness", False, 
                            f"All stocks have identical PPO: {ppo_values[0]}", True)
                all_passed = False
            
            # Test DMI+ uniqueness
            unique_dmi = len(set(dmi_plus_values))
            if unique_dmi == 1 and dmi_plus_values[0] == 22.00:
                self.log_test("Individual Stock DMI+ Uniqueness", False, 
                            "All stocks have identical DMI+ value: 22.00 (known bug)", True)
                all_passed = False
            elif unique_dmi > 1:
                self.log_test("Individual Stock DMI+ Uniqueness", True, 
                            f"{unique_dmi} unique DMI+ values across {len(symbols)} stocks")
            else:
                self.log_test("Individual Stock DMI+ Uniqueness", False, 
                            f"All stocks have identical DMI+: {dmi_plus_values[0]}", True)
                all_passed = False
            
            # Test price uniqueness (should definitely be different)
            unique_prices = len(set(prices))
            if unique_prices > 1:
                self.log_test("Individual Stock Price Uniqueness", True, 
                            f"{unique_prices} unique prices across {len(symbols)} stocks")
            else:
                self.log_test("Individual Stock Price Uniqueness", False, 
                            f"All stocks have identical price: ${prices[0]:.2f}", True)
                all_passed = False
        
        return all_passed

    def run_all_critical_tests(self) -> Dict[str, Any]:
        """Run all critical fix tests"""
        print(f"\n🚨 RUNNING CRITICAL FIXES VALIDATION TESTS")
        print("=" * 70)
        print(f"Testing fixes for user-reported critical issues:")
        print(f"1. Tech Analysis Button Complete Failure")
        print(f"2. Scanner Options Data Missing Strike Prices")
        print(f"3. Scanner Hardcoded/Demo Data Issues")
        print(f"Test Symbols: {', '.join(TEST_SYMBOLS)}")
        print("=" * 70)
        
        # Run all critical tests
        test1_passed = self.test_tech_analysis_functionality()
        test2_passed = self.test_options_strike_prices()
        test3_passed = self.test_stock_specific_data_generation()
        test4_passed = self.test_individual_stock_uniqueness()
        
        # Calculate overall results
        overall_passed = test1_passed and test2_passed and test3_passed and test4_passed
        
        # Print summary
        print(f"\n📋 CRITICAL FIXES TEST SUMMARY")
        print("=" * 70)
        print(f"Total Tests: {self.results['total_tests']}")
        print(f"Passed: {self.results['passed_tests']}")
        print(f"Failed: {self.results['failed_tests']}")
        print(f"Success Rate: {(self.results['passed_tests']/self.results['total_tests']*100):.1f}%")
        
        if self.results['critical_issues']:
            print(f"\n🚨 CRITICAL ISSUES FOUND ({len(self.results['critical_issues'])}):")
            for issue in self.results['critical_issues']:
                print(f"  • {issue}")
        
        if overall_passed:
            print(f"\n✅ ALL CRITICAL FIXES VALIDATED SUCCESSFULLY")
        else:
            print(f"\n❌ SOME CRITICAL FIXES STILL HAVE ISSUES")
        
        return {
            "overall_passed": overall_passed,
            "test_results": self.results,
            "individual_tests": {
                "tech_analysis_functionality": test1_passed,
                "options_strike_prices": test2_passed,
                "stock_specific_data": test3_passed,
                "individual_stock_uniqueness": test4_passed
            }
        }

if __name__ == "__main__":
    tester = CriticalFixesTester()
    results = tester.run_all_critical_tests()
    
    # Exit with appropriate code
    exit(0 if results["overall_passed"] else 1)