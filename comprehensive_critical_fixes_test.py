#!/usr/bin/env python3
"""
COMPREHENSIVE TESTING OF ALL CRITICAL FIXES
Tests all user-reported issues from the review request to ensure they are resolved
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any, List

# Configuration
BACKEND_URL = "https://stockwise-platform.preview.emergentagent.com/api"
TEST_SYMBOLS = ["AAPL", "GOOGL", "MSFT", "TSLA"]

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

    def test_stock_scanner_filter_logic(self) -> bool:
        """
        CRITICAL TEST 1: Stock Scanner Filter Logic
        Verify filters are properly applied and don't return same 20 stocks regardless of criteria
        """
        print(f"\n🔍 TESTING STOCK SCANNER FILTER LOGIC")
        print("=" * 60)
        
        all_passed = True
        
        # Test Scenario 1: Filter stocks under $100 - should return limited results
        print(f"\n📊 Scenario 1: Filter stocks under $100")
        try:
            filters_under_100 = {
                "price_filter": {"type": "under", "under": 100},
                "dmi_filter": {"min": 15, "max": 65},
                "ppo_slope_filter": {"threshold": 1}
            }
            
            response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                   json=filters_under_100,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            
            if response.status_code == 200:
                data_100 = response.json()
                stocks_under_100 = data_100.get("stocks", [])
                count_under_100 = len(stocks_under_100)
                
                # Validate all stocks are actually under $100
                price_violations = []
                for stock in stocks_under_100:
                    price = stock.get("price", 0)
                    if price > 100:
                        price_violations.append(f"{stock.get('symbol', 'Unknown')}: ${price:.2f}")
                
                if price_violations:
                    self.log_test("Filter Under $100 - Price Validation", False, 
                                f"Stocks over $100 found: {price_violations}", True)
                    all_passed = False
                else:
                    self.log_test("Filter Under $100 - Price Validation", True, 
                                f"All {count_under_100} stocks correctly under $100")
                
                print(f"  📈 Results: {count_under_100} stocks found under $100")
                
            else:
                self.log_test("Filter Under $100 - API Call", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                all_passed = False
                return all_passed
                
        except Exception as e:
            self.log_test("Filter Under $100 - Exception", False, f"Error: {str(e)}", True)
            all_passed = False
            return all_passed
        
        # Test Scenario 2: Filter stocks under $500 - should return more results than Scenario 1
        print(f"\n📊 Scenario 2: Filter stocks under $500")
        try:
            filters_under_500 = {
                "price_filter": {"type": "under", "under": 500},
                "dmi_filter": {"min": 15, "max": 65},
                "ppo_slope_filter": {"threshold": 1}
            }
            
            response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                   json=filters_under_500,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            
            if response.status_code == 200:
                data_500 = response.json()
                stocks_under_500 = data_500.get("stocks", [])
                count_under_500 = len(stocks_under_500)
                
                # Validate all stocks are actually under $500
                price_violations = []
                for stock in stocks_under_500:
                    price = stock.get("price", 0)
                    if price > 500:
                        price_violations.append(f"{stock.get('symbol', 'Unknown')}: ${price:.2f}")
                
                if price_violations:
                    self.log_test("Filter Under $500 - Price Validation", False, 
                                f"Stocks over $500 found: {price_violations}", True)
                    all_passed = False
                else:
                    self.log_test("Filter Under $500 - Price Validation", True, 
                                f"All {count_under_500} stocks correctly under $500")
                
                print(f"  📈 Results: {count_under_500} stocks found under $500")
                
                # CRITICAL COMPARISON: Under $500 should return MORE stocks than under $100
                if count_under_500 > count_under_100:
                    self.log_test("Filter Logic Comparison", True, 
                                f"Correct: $500 filter ({count_under_500}) > $100 filter ({count_under_100})")
                elif count_under_500 == count_under_100:
                    self.log_test("Filter Logic Comparison", False, 
                                f"CRITICAL BUG: Same count for both filters ({count_under_500})", True)
                    all_passed = False
                else:
                    self.log_test("Filter Logic Comparison", False, 
                                f"CRITICAL BUG: $500 filter ({count_under_500}) < $100 filter ({count_under_100})", True)
                    all_passed = False
                
            else:
                self.log_test("Filter Under $500 - API Call", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                all_passed = False
                
        except Exception as e:
            self.log_test("Filter Under $500 - Exception", False, f"Error: {str(e)}", True)
            all_passed = False
        
        # Test Scenario 3: Verify filters don't always return same 20 stocks
        print(f"\n📊 Scenario 3: Different filter combinations should return different results")
        try:
            # Test with different DMI ranges
            filters_dmi_narrow = {
                "price_filter": {"type": "under", "under": 300},
                "dmi_filter": {"min": 40, "max": 60},
                "ppo_slope_filter": {"threshold": 2}
            }
            
            filters_dmi_wide = {
                "price_filter": {"type": "under", "under": 300},
                "dmi_filter": {"min": 10, "max": 80},
                "ppo_slope_filter": {"threshold": 2}
            }
            
            # Get results for narrow DMI range
            response1 = requests.post(f"{BACKEND_URL}/screener/scan", 
                                    json=filters_dmi_narrow,
                                    headers={"Content-Type": "application/json"},
                                    timeout=30)
            
            # Get results for wide DMI range
            response2 = requests.post(f"{BACKEND_URL}/screener/scan", 
                                    json=filters_dmi_wide,
                                    headers={"Content-Type": "application/json"},
                                    timeout=30)
            
            if response1.status_code == 200 and response2.status_code == 200:
                data1 = response1.json()
                data2 = response2.json()
                
                stocks1 = data1.get("stocks", [])
                stocks2 = data2.get("stocks", [])
                
                symbols1 = set(stock.get("symbol", "") for stock in stocks1)
                symbols2 = set(stock.get("symbol", "") for stock in stocks2)
                
                # Check if results are different
                if symbols1 == symbols2 and len(symbols1) == 20 and len(symbols2) == 20:
                    self.log_test("Filter Variation Test", False, 
                                "CRITICAL BUG: Different filters return identical 20 stocks", True)
                    all_passed = False
                else:
                    overlap = len(symbols1.intersection(symbols2))
                    total_unique = len(symbols1.union(symbols2))
                    self.log_test("Filter Variation Test", True, 
                                f"Filters return different results: {overlap} overlap, {total_unique} total unique")
                
                print(f"  📊 Narrow DMI (40-60): {len(stocks1)} stocks")
                print(f"  📊 Wide DMI (10-80): {len(stocks2)} stocks")
                
            else:
                self.log_test("Filter Variation Test - API", False, 
                            f"API calls failed: {response1.status_code}, {response2.status_code}", True)
                all_passed = False
                
        except Exception as e:
            self.log_test("Filter Variation Test - Exception", False, f"Error: {str(e)}", True)
            all_passed = False
        
        return all_passed

    def test_ppo_3day_historical_data(self) -> bool:
        """
        CRITICAL TEST 2: PPO 3-Day Historical Data
        Verify PPO values show actual 3 different days of data, not 3 identical values for single day
        """
        print(f"\n📈 TESTING PPO 3-DAY HISTORICAL DATA")
        print("=" * 60)
        
        all_passed = True
        
        # Test Scenario 3: Check AAPL PPO values for 3 distinct historical days
        print(f"\n📊 Scenario 3: Check AAPL PPO values for 3 distinct historical days")
        try:
            payload = {"symbol": "AAPL", "timeframe": "3M"}  # Use 3M for better historical data
            response = requests.post(f"{BACKEND_URL}/analyze", 
                                   json=payload,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                ppo_history = data.get("ppo_history", [])
                
                if len(ppo_history) != 3:
                    self.log_test("PPO History Length", False, 
                                f"Expected 3 days, got {len(ppo_history)}", True)
                    all_passed = False
                else:
                    # Extract PPO values and dates
                    ppo_values = [entry.get("ppo", 0) for entry in ppo_history]
                    dates = [entry.get("date", "") for entry in ppo_history]
                    
                    print(f"  📅 PPO History:")
                    for i, (date, ppo) in enumerate(zip(dates, ppo_values)):
                        print(f"    Day {i+1}: {date} - PPO: {ppo:.6f}")
                    
                    # CRITICAL CHECK: Values should be different (not identical)
                    unique_values = len(set(ppo_values))
                    if unique_values == 1:
                        self.log_test("PPO Historical Variation", False, 
                                    f"CRITICAL BUG: All 3 PPO values are identical: {ppo_values[0]:.6f}", True)
                        all_passed = False
                    elif unique_values == 2:
                        self.log_test("PPO Historical Variation", True, 
                                    f"Good: 2 unique PPO values out of 3: {ppo_values}")
                    else:  # unique_values == 3
                        self.log_test("PPO Historical Variation", True, 
                                    f"Excellent: All 3 PPO values are unique: {ppo_values}")
                    
                    # Check dates are different
                    unique_dates = len(set(dates))
                    if unique_dates != 3:
                        self.log_test("PPO Date Variation", False, 
                                    f"Expected 3 unique dates, got {unique_dates}: {dates}", True)
                        all_passed = False
                    else:
                        self.log_test("PPO Date Variation", True, 
                                    f"All 3 dates are unique: {dates}")
                    
                    # Validate PPO values are realistic (not zero or extreme)
                    realistic_values = all(-10 <= ppo <= 10 for ppo in ppo_values)
                    if not realistic_values:
                        self.log_test("PPO Value Realism", False, 
                                    f"PPO values seem unrealistic: {ppo_values}", True)
                        all_passed = False
                    else:
                        self.log_test("PPO Value Realism", True, 
                                    f"PPO values are within realistic range: {ppo_values}")
                
            else:
                self.log_test("PPO History API Call", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                all_passed = False
                
        except Exception as e:
            self.log_test("PPO History Test - Exception", False, f"Error: {str(e)}", True)
            all_passed = False
        
        # Test additional symbols for consistency
        print(f"\n📊 Testing PPO historical data for multiple symbols")
        for symbol in ["GOOGL", "MSFT"]:
            try:
                payload = {"symbol": symbol, "timeframe": "3M"}
                response = requests.post(f"{BACKEND_URL}/analyze", 
                                       json=payload,
                                       headers={"Content-Type": "application/json"},
                                       timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    ppo_history = data.get("ppo_history", [])
                    
                    if len(ppo_history) == 3:
                        ppo_values = [entry.get("ppo", 0) for entry in ppo_history]
                        unique_values = len(set(ppo_values))
                        
                        if unique_values >= 2:
                            self.log_test(f"PPO History Variation ({symbol})", True, 
                                        f"{unique_values} unique values: {ppo_values}")
                        else:
                            self.log_test(f"PPO History Variation ({symbol})", False, 
                                        f"All identical values: {ppo_values[0]:.6f}", True)
                            all_passed = False
                    else:
                        self.log_test(f"PPO History Length ({symbol})", False, 
                                    f"Expected 3 days, got {len(ppo_history)}", True)
                        all_passed = False
                else:
                    self.log_test(f"PPO History API ({symbol})", False, 
                                f"HTTP {response.status_code}", True)
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"PPO History Test ({symbol})", False, f"Error: {str(e)}", True)
                all_passed = False
        
        return all_passed

    def test_option_data_population(self) -> bool:
        """
        CRITICAL TEST 3: Option Data Population
        Verify all option fields are properly populated with realistic values
        """
        print(f"\n📊 TESTING OPTION DATA POPULATION")
        print("=" * 60)
        
        all_passed = True
        
        # Test Scenario 4: Verify option data completeness and mathematical relationships
        print(f"\n📊 Scenario 4: Verify option data completeness")
        try:
            # Test screener endpoint for option data
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
                    self.log_test("Option Data - No Stocks", False, 
                                "No stocks returned from screener", True)
                    all_passed = False
                    return all_passed
                
                # Check option data for first 5 stocks
                option_issues = []
                for i, stock in enumerate(stocks[:5]):
                    symbol = stock.get("symbol", f"Stock_{i}")
                    
                    # Required option fields
                    required_option_fields = ["call_bid", "call_ask", "put_bid", "put_ask", "options_expiration"]
                    
                    missing_fields = []
                    for field in required_option_fields:
                        if field not in stock:
                            missing_fields.append(field)
                        elif stock[field] is None:
                            missing_fields.append(f"{field} (null)")
                    
                    if missing_fields:
                        option_issues.append(f"{symbol}: Missing {missing_fields}")
                    else:
                        # Validate option values are realistic
                        call_bid = stock.get("call_bid", 0)
                        call_ask = stock.get("call_ask", 0)
                        put_bid = stock.get("put_bid", 0)
                        put_ask = stock.get("put_ask", 0)
                        
                        # Check bid-ask relationships (ask should be >= bid)
                        if call_ask < call_bid:
                            option_issues.append(f"{symbol}: Call ask ({call_ask}) < call bid ({call_bid})")
                        if put_ask < put_bid:
                            option_issues.append(f"{symbol}: Put ask ({put_ask}) < put bid ({put_bid})")
                        
                        # Check values are positive
                        if any(val < 0 for val in [call_bid, call_ask, put_bid, put_ask]):
                            option_issues.append(f"{symbol}: Negative option prices")
                        
                        # Check values are not all zero
                        if all(val == 0 for val in [call_bid, call_ask, put_bid, put_ask]):
                            option_issues.append(f"{symbol}: All option prices are zero")
                        
                        print(f"  📊 {symbol}: Call ${call_bid:.2f}/${call_ask:.2f}, Put ${put_bid:.2f}/${put_ask:.2f}, Exp: {stock.get('options_expiration', 'N/A')}")
                
                if option_issues:
                    self.log_test("Option Data Validation", False, 
                                f"Issues found: {option_issues}", True)
                    all_passed = False
                else:
                    self.log_test("Option Data Validation", True, 
                                f"All option fields properly populated for {len(stocks[:5])} stocks")
                
                # Check options_expiration format
                expiration_formats = set()
                for stock in stocks[:5]:
                    exp = stock.get("options_expiration", "")
                    expiration_formats.add(exp)
                
                print(f"  📅 Options expiration formats found: {expiration_formats}")
                
                # Validate expiration format consistency
                if len(expiration_formats) == 1 and "N/A" in expiration_formats:
                    self.log_test("Options Expiration Format", True, 
                                "Consistent 'N/A' format for options expiration")
                elif all("Exp:" in exp for exp in expiration_formats if exp):
                    self.log_test("Options Expiration Format", True, 
                                "Proper 'Exp:' format for options expiration")
                else:
                    self.log_test("Options Expiration Format", False, 
                                f"Inconsistent expiration formats: {expiration_formats}")
                    all_passed = False
                
            else:
                self.log_test("Option Data API Call", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                all_passed = False
                
        except Exception as e:
            self.log_test("Option Data Test - Exception", False, f"Error: {str(e)}", True)
            all_passed = False
        
        return all_passed

    def test_data_quality_and_reliability(self) -> bool:
        """
        CRITICAL TEST 4: Data Quality and Reliability
        Ensure results are reliable and accurate, not suspect
        """
        print(f"\n🔍 TESTING DATA QUALITY AND RELIABILITY")
        print("=" * 60)
        
        all_passed = True
        
        # Test realistic price ranges
        print(f"\n📊 Testing realistic price ranges and technical indicators")
        try:
            # Test individual stock analysis for data quality
            for symbol in ["AAPL", "GOOGL", "MSFT"]:
                payload = {"symbol": symbol, "timeframe": "3M"}
                response = requests.post(f"{BACKEND_URL}/analyze", 
                                       json=payload,
                                       headers={"Content-Type": "application/json"},
                                       timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check data source transparency
                    data_source = data.get("data_source", "unknown")
                    if data_source == "unknown":
                        self.log_test(f"Data Source Transparency ({symbol})", False, 
                                    "Data source not specified", True)
                        all_passed = False
                    else:
                        self.log_test(f"Data Source Transparency ({symbol})", True, 
                                    f"Data source: {data_source}")
                    
                    # Check price realism
                    current_price = data.get("current_price", 0)
                    if current_price <= 0 or current_price > 10000:
                        self.log_test(f"Price Realism ({symbol})", False, 
                                    f"Unrealistic price: ${current_price:.2f}", True)
                        all_passed = False
                    else:
                        self.log_test(f"Price Realism ({symbol})", True, 
                                    f"Realistic price: ${current_price:.2f}")
                    
                    # Check technical indicators
                    indicators = data.get("indicators", {})
                    
                    # DMI values should be 0-100 range
                    dmi_plus = indicators.get("dmi_plus", 0)
                    dmi_minus = indicators.get("dmi_minus", 0)
                    adx = indicators.get("adx", 0)
                    
                    if not (0 <= dmi_plus <= 100) or not (0 <= dmi_minus <= 100) or not (0 <= adx <= 100):
                        self.log_test(f"DMI Range Check ({symbol})", False, 
                                    f"DMI values out of range: DMI+={dmi_plus:.2f}, DMI-={dmi_minus:.2f}, ADX={adx:.2f}", True)
                        all_passed = False
                    else:
                        self.log_test(f"DMI Range Check ({symbol})", True, 
                                    f"DMI values in valid range: DMI+={dmi_plus:.2f}, DMI-={dmi_minus:.2f}, ADX={adx:.2f}")
                    
                    # Check DMI composite calculation (should be different from ADX)
                    dmi_composite = (dmi_plus + dmi_minus) / 2
                    if abs(dmi_composite - adx) < 0.01:  # Too similar suggests ADX duplication bug
                        self.log_test(f"DMI Composite Calculation ({symbol})", False, 
                                    f"DMI composite ({dmi_composite:.2f}) too similar to ADX ({adx:.2f}) - possible duplication bug", True)
                        all_passed = False
                    else:
                        self.log_test(f"DMI Composite Calculation ({symbol})", True, 
                                    f"DMI composite ({dmi_composite:.2f}) properly differs from ADX ({adx:.2f})")
                    
                    # RSI should be 0-100 range
                    rsi = indicators.get("rsi", 50)
                    if not (0 <= rsi <= 100):
                        self.log_test(f"RSI Range Check ({symbol})", False, 
                                    f"RSI out of range: {rsi:.2f}", True)
                        all_passed = False
                    else:
                        self.log_test(f"RSI Range Check ({symbol})", True, 
                                    f"RSI in valid range: {rsi:.2f}")
                    
                    print(f"  📊 {symbol}: Price=${current_price:.2f}, DMI+={dmi_plus:.2f}, DMI-={dmi_minus:.2f}, ADX={adx:.2f}, RSI={rsi:.2f}")
                    
                else:
                    self.log_test(f"Data Quality API ({symbol})", False, 
                                f"HTTP {response.status_code}: {response.text}", True)
                    all_passed = False
                    
        except Exception as e:
            self.log_test("Data Quality Test - Exception", False, f"Error: {str(e)}", True)
            all_passed = False
        
        # Test screener data quality
        print(f"\n📊 Testing screener data quality and consistency")
        try:
            filters = {
                "price_filter": {"type": "under", "under": 300},
                "dmi_filter": {"min": 20, "max": 60},
                "ppo_slope_filter": {"threshold": 2}
            }
            
            response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                   json=filters,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                stocks = data.get("stocks", [])
                
                # Check data source consistency
                data_sources = set()
                for stock in stocks:
                    data_source = stock.get("data_source", "unknown")
                    data_sources.add(data_source)
                
                if "unknown" in data_sources:
                    self.log_test("Screener Data Source", False, 
                                "Some stocks have unknown data source", True)
                    all_passed = False
                else:
                    self.log_test("Screener Data Source", True, 
                                f"Data sources: {data_sources}")
                
                # Check for realistic stock data distribution
                if len(stocks) > 0:
                    prices = [stock.get("price", 0) for stock in stocks]
                    avg_price = sum(prices) / len(prices)
                    
                    if avg_price < 1 or avg_price > 1000:
                        self.log_test("Screener Price Distribution", False, 
                                    f"Unrealistic average price: ${avg_price:.2f}", True)
                        all_passed = False
                    else:
                        self.log_test("Screener Price Distribution", True, 
                                    f"Realistic average price: ${avg_price:.2f}")
                
                print(f"  📊 Screener returned {len(stocks)} stocks with data sources: {data_sources}")
                
            else:
                self.log_test("Screener Data Quality API", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                all_passed = False
                
        except Exception as e:
            self.log_test("Screener Data Quality - Exception", False, f"Error: {str(e)}", True)
            all_passed = False
        
        return all_passed

    def test_frontend_backend_integration(self) -> bool:
        """
        CRITICAL TEST 5: Frontend-Backend Integration
        Test the snake_case vs camelCase fix and ensure proper communication
        """
        print(f"\n🔗 TESTING FRONTEND-BACKEND INTEGRATION")
        print("=" * 60)
        
        all_passed = True
        
        # Test that backend uses snake_case property names
        print(f"\n📊 Testing snake_case property names in backend responses")
        try:
            filters = {
                "price_filter": {"type": "under", "under": 200},
                "dmi_filter": {"min": 20, "max": 60},
                "ppo_slope_filter": {"threshold": 3}
            }
            
            response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                   json=filters,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                stocks = data.get("stocks", [])
                
                if stocks:
                    stock = stocks[0]
                    
                    # Check for snake_case properties (not camelCase)
                    required_snake_case = [
                        "ppo_slope_percentage",  # Not ppoSlope
                        "di_plus",              # Not diPlus  
                        "di_minus",             # Not diMinus
                        "options_expiration",   # Not optionsExpiration
                        "volume_3m",           # Not volume3M
                        "last_earnings",       # Not lastEarnings
                        "next_earnings"        # Not nextEarnings
                    ]
                    
                    missing_snake_case = []
                    for prop in required_snake_case:
                        if prop not in stock:
                            missing_snake_case.append(prop)
                    
                    if missing_snake_case:
                        self.log_test("Snake Case Properties", False, 
                                    f"Missing snake_case properties: {missing_snake_case}", True)
                        all_passed = False
                    else:
                        self.log_test("Snake Case Properties", True, 
                                    "All required snake_case properties present")
                    
                    # Check that camelCase properties are NOT present (would indicate old bug)
                    old_camel_case = ["ppoSlope", "diPlus", "diMinus", "optionsExpiration"]
                    found_camel_case = []
                    for prop in old_camel_case:
                        if prop in stock:
                            found_camel_case.append(prop)
                    
                    if found_camel_case:
                        self.log_test("CamelCase Cleanup", False, 
                                    f"Old camelCase properties still present: {found_camel_case}", True)
                        all_passed = False
                    else:
                        self.log_test("CamelCase Cleanup", True, 
                                    "No old camelCase properties found")
                    
                    print(f"  📊 Sample stock properties: {list(stock.keys())[:10]}...")
                    
                else:
                    self.log_test("Integration Test - No Stocks", False, 
                                "No stocks returned for integration test", True)
                    all_passed = False
                    
            else:
                self.log_test("Integration Test API", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                all_passed = False
                
        except Exception as e:
            self.log_test("Integration Test - Exception", False, f"Error: {str(e)}", True)
            all_passed = False
        
        return all_passed

    def run_all_critical_tests(self) -> Dict[str, Any]:
        """Run all critical fix tests"""
        print(f"\n🚀 STARTING COMPREHENSIVE CRITICAL FIXES TESTING")
        print("=" * 80)
        print(f"Testing Backend URL: {BACKEND_URL}")
        print(f"Test Symbols: {TEST_SYMBOLS}")
        print(f"Timestamp: {datetime.now().isoformat()}")
        print("=" * 80)
        
        # Run all critical tests
        test_results = {
            "stock_scanner_filter_logic": self.test_stock_scanner_filter_logic(),
            "ppo_3day_historical_data": self.test_ppo_3day_historical_data(),
            "option_data_population": self.test_option_data_population(),
            "data_quality_reliability": self.test_data_quality_and_reliability(),
            "frontend_backend_integration": self.test_frontend_backend_integration()
        }
        
        # Calculate overall results
        total_test_categories = len(test_results)
        passed_categories = sum(1 for result in test_results.values() if result)
        
        print(f"\n📊 COMPREHENSIVE CRITICAL FIXES TEST SUMMARY")
        print("=" * 80)
        print(f"Total Test Categories: {total_test_categories}")
        print(f"Passed Categories: {passed_categories}")
        print(f"Failed Categories: {total_test_categories - passed_categories}")
        print(f"Success Rate: {(passed_categories / total_test_categories) * 100:.1f}%")
        print()
        
        # Detailed results
        for test_name, result in test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status}: {test_name.replace('_', ' ').title()}")
        
        print(f"\nDetailed Test Results:")
        print(f"Total Individual Tests: {self.results['total_tests']}")
        print(f"Passed Tests: {self.results['passed_tests']}")
        print(f"Failed Tests: {self.results['failed_tests']}")
        
        if self.results['critical_issues']:
            print(f"\n🚨 CRITICAL ISSUES FOUND ({len(self.results['critical_issues'])}):")
            for issue in self.results['critical_issues']:
                print(f"  • {issue}")
        else:
            print(f"\n✅ NO CRITICAL ISSUES FOUND - All user-reported problems appear to be resolved!")
        
        return {
            "overall_success": passed_categories == total_test_categories,
            "category_results": test_results,
            "detailed_results": self.results,
            "summary": {
                "total_categories": total_test_categories,
                "passed_categories": passed_categories,
                "success_rate": (passed_categories / total_test_categories) * 100,
                "critical_issues_count": len(self.results['critical_issues'])
            }
        }

if __name__ == "__main__":
    tester = CriticalFixesTester()
    results = tester.run_all_critical_tests()
    
    # Exit with appropriate code
    exit_code = 0 if results["overall_success"] else 1
    print(f"\nExiting with code: {exit_code}")
    exit(exit_code)