#!/usr/bin/env python3
"""
Focused test for Multiple Component Fixes
Tests only the specific fixes mentioned in the review request
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BACKEND_URL = "https://market-analyzer-95.preview.emergentagent.com/api"
TEST_SYMBOLS = ["AAPL", "GOOGL", "MSFT"]

def test_multiple_component_fixes():
    """Test all the multiple component fixes"""
    print(f"\n🔧 FOCUSED TESTING: MULTIPLE COMPONENT FIXES")
    print("=" * 70)
    
    results = {
        "point_based_decision": [],
        "market_endpoints": [],
        "ppo_histogram": [],
        "dmi_values": [],
        "default_timeframe": [],
        "data_source_transparency": []
    }
    
    # 1. Test Point Based Decision - should use real Alpha Vantage API
    print(f"\n📊 Testing Point Based Decision (Real Alpha Vantage Data)")
    for symbol in TEST_SYMBOLS:
        try:
            # Test with default timeframe (should be 3M now)
            payload = {"symbol": symbol}  # No timeframe specified - should default to 3M
            
            response = requests.post(f"{BACKEND_URL}/analyze", 
                                   json=payload,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                data_source = data.get("data_source", "unknown")
                timeframe = data.get("timeframe", "unknown")
                chart_data_count = len(data.get("chart_data", []))
                
                result = {
                    "symbol": symbol,
                    "status": "PASS" if data_source == "alpha_vantage" else "FAIL",
                    "data_source": data_source,
                    "timeframe": timeframe,
                    "data_points": chart_data_count,
                    "details": f"Source={data_source}, Timeframe={timeframe}, Data points={chart_data_count}"
                }
                results["point_based_decision"].append(result)
                
                status = "✅ PASS" if result["status"] == "PASS" else "❌ FAIL"
                print(f"  {status}: {symbol} - {result['details']}")
                
            else:
                result = {
                    "symbol": symbol,
                    "status": "FAIL",
                    "error": f"HTTP {response.status_code}: {response.text[:100]}"
                }
                results["point_based_decision"].append(result)
                print(f"  ❌ FAIL: {symbol} - {result['error']}")
                
        except Exception as e:
            result = {
                "symbol": symbol,
                "status": "FAIL",
                "error": f"Exception: {str(e)}"
            }
            results["point_based_decision"].append(result)
            print(f"  ❌ FAIL: {symbol} - {result['error']}")
    
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
                
                # Market endpoints return a list directly
                if isinstance(data, list) and data:
                    stocks_count = len(data)
                    alpha_vantage_count = sum(1 for stock in data if stock.get("data_source") == "alpha_vantage")
                    
                    result = {
                        "endpoint": endpoint_name,
                        "status": "PASS" if alpha_vantage_count > 0 else "FAIL",
                        "stocks_count": stocks_count,
                        "alpha_vantage_count": alpha_vantage_count,
                        "details": f"{stocks_count} stocks, {alpha_vantage_count} using Alpha Vantage"
                    }
                    results["market_endpoints"].append(result)
                    
                    status = "✅ PASS" if result["status"] == "PASS" else "❌ FAIL"
                    print(f"  {status}: {endpoint_name} - {result['details']}")
                else:
                    result = {
                        "endpoint": endpoint_name,
                        "status": "FAIL",
                        "error": "No data or invalid format"
                    }
                    results["market_endpoints"].append(result)
                    print(f"  ❌ FAIL: {endpoint_name} - {result['error']}")
                    
            else:
                result = {
                    "endpoint": endpoint_name,
                    "status": "FAIL",
                    "error": f"HTTP {response.status_code}: {response.text[:100]}"
                }
                results["market_endpoints"].append(result)
                print(f"  ❌ FAIL: {endpoint_name} - {result['error']}")
                
        except Exception as e:
            result = {
                "endpoint": endpoint_name,
                "status": "FAIL",
                "error": f"Exception: {str(e)}"
            }
            results["market_endpoints"].append(result)
            print(f"  ❌ FAIL: {endpoint_name} - {result['error']}")
    
    # 3. Test PPO histogram calculation fix
    print(f"\n🔢 Testing PPO Histogram Calculation Fix")
    for symbol in TEST_SYMBOLS:
        try:
            payload = {"symbol": symbol, "timeframe": "3M"}
            response = requests.post(f"{BACKEND_URL}/analyze", 
                                   json=payload,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                indicators = data.get("indicators", {})
                
                ppo = indicators.get("ppo", 0)
                ppo_signal = indicators.get("ppo_signal", 0)
                ppo_histogram = indicators.get("ppo_histogram", 0)
                expected_histogram = ppo - ppo_signal
                
                # Allow small floating point differences
                tolerance = 0.001
                is_correct = abs(ppo_histogram - expected_histogram) <= tolerance
                
                result = {
                    "symbol": symbol,
                    "status": "PASS" if is_correct else "FAIL",
                    "ppo": ppo,
                    "ppo_signal": ppo_signal,
                    "ppo_histogram": ppo_histogram,
                    "expected_histogram": expected_histogram,
                    "difference": abs(ppo_histogram - expected_histogram),
                    "details": f"PPO={ppo:.4f}, Signal={ppo_signal:.4f}, Histogram={ppo_histogram:.4f}, Expected={expected_histogram:.4f}"
                }
                results["ppo_histogram"].append(result)
                
                status = "✅ PASS" if result["status"] == "PASS" else "❌ FAIL"
                print(f"  {status}: {symbol} - {result['details']}")
                
            else:
                result = {
                    "symbol": symbol,
                    "status": "FAIL",
                    "error": f"HTTP {response.status_code}: {response.text[:100]}"
                }
                results["ppo_histogram"].append(result)
                print(f"  ❌ FAIL: {symbol} - {result['error']}")
                
        except Exception as e:
            result = {
                "symbol": symbol,
                "status": "FAIL",
                "error": f"Exception: {str(e)}"
            }
            results["ppo_histogram"].append(result)
            print(f"  ❌ FAIL: {symbol} - {result['error']}")
    
    # 4. Test DMI values fix
    print(f"\n📐 Testing DMI Values Fix")
    for symbol in TEST_SYMBOLS:
        try:
            payload = {"symbol": symbol, "timeframe": "3M"}
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
                
                # Check if values are within 0-100 range
                dmi_plus_valid = 0 <= dmi_plus <= 100
                dmi_minus_valid = 0 <= dmi_minus <= 100
                adx_valid = 0 <= adx <= 100
                all_valid = dmi_plus_valid and dmi_minus_valid and adx_valid
                
                result = {
                    "symbol": symbol,
                    "status": "PASS" if all_valid else "FAIL",
                    "dmi_plus": dmi_plus,
                    "dmi_minus": dmi_minus,
                    "adx": adx,
                    "dmi_plus_valid": dmi_plus_valid,
                    "dmi_minus_valid": dmi_minus_valid,
                    "adx_valid": adx_valid,
                    "details": f"DMI+={dmi_plus:.2f}, DMI-={dmi_minus:.2f}, ADX={adx:.2f}"
                }
                results["dmi_values"].append(result)
                
                status = "✅ PASS" if result["status"] == "PASS" else "❌ FAIL"
                print(f"  {status}: {symbol} - {result['details']}")
                
            else:
                result = {
                    "symbol": symbol,
                    "status": "FAIL",
                    "error": f"HTTP {response.status_code}: {response.text[:100]}"
                }
                results["dmi_values"].append(result)
                print(f"  ❌ FAIL: {symbol} - {result['error']}")
                
        except Exception as e:
            result = {
                "symbol": symbol,
                "status": "FAIL",
                "error": f"Exception: {str(e)}"
            }
            results["dmi_values"].append(result)
            print(f"  ❌ FAIL: {symbol} - {result['error']}")
    
    # 5. Test default chart period fix (should be 3M)
    print(f"\n📅 Testing Default Chart Period Fix (Should be 3M)")
    for symbol in TEST_SYMBOLS:
        try:
            # Test without specifying timeframe - should default to 3M
            payload = {"symbol": symbol}
            response = requests.post(f"{BACKEND_URL}/analyze", 
                                   json=payload,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                timeframe = data.get("timeframe", "unknown")
                chart_data_count = len(data.get("chart_data", []))
                
                # Check if default timeframe is 3M
                is_3m = timeframe == "3M"
                
                result = {
                    "symbol": symbol,
                    "status": "PASS" if is_3m else "FAIL",
                    "timeframe": timeframe,
                    "data_points": chart_data_count,
                    "details": f"Default timeframe={timeframe}, Data points={chart_data_count}"
                }
                results["default_timeframe"].append(result)
                
                status = "✅ PASS" if result["status"] == "PASS" else "❌ FAIL"
                print(f"  {status}: {symbol} - {result['details']}")
                
            else:
                result = {
                    "symbol": symbol,
                    "status": "FAIL",
                    "error": f"HTTP {response.status_code}: {response.text[:100]}"
                }
                results["default_timeframe"].append(result)
                print(f"  ❌ FAIL: {symbol} - {result['error']}")
                
        except Exception as e:
            result = {
                "symbol": symbol,
                "status": "FAIL",
                "error": f"Exception: {str(e)}"
            }
            results["default_timeframe"].append(result)
            print(f"  ❌ FAIL: {symbol} - {result['error']}")
    
    # 6. Test data source transparency
    print(f"\n🔍 Testing Data Source Transparency")
    for symbol in TEST_SYMBOLS:
        try:
            payload = {"symbol": symbol, "timeframe": "3M"}
            response = requests.post(f"{BACKEND_URL}/analyze", 
                                   json=payload,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                data_source = data.get("data_source", "unknown")
                response_time = data.get("response_time")
                
                # Check if data source is clearly indicated
                is_clear = data_source in ["alpha_vantage", "polygon_io", "yahoo_finance", "mock"]
                
                result = {
                    "symbol": symbol,
                    "status": "PASS" if is_clear else "FAIL",
                    "data_source": data_source,
                    "response_time": response_time,
                    "details": f"Data source={data_source}, Response time={response_time}s"
                }
                results["data_source_transparency"].append(result)
                
                status = "✅ PASS" if result["status"] == "PASS" else "❌ FAIL"
                print(f"  {status}: {symbol} - {result['details']}")
                
            else:
                result = {
                    "symbol": symbol,
                    "status": "FAIL",
                    "error": f"HTTP {response.status_code}: {response.text[:100]}"
                }
                results["data_source_transparency"].append(result)
                print(f"  ❌ FAIL: {symbol} - {result['error']}")
                
        except Exception as e:
            result = {
                "symbol": symbol,
                "status": "FAIL",
                "error": f"Exception: {str(e)}"
            }
            results["data_source_transparency"].append(result)
            print(f"  ❌ FAIL: {symbol} - {result['error']}")
    
    # Summary
    print(f"\n" + "=" * 70)
    print(f"🎯 MULTIPLE COMPONENT FIXES TEST SUMMARY")
    print("=" * 70)
    
    total_tests = 0
    passed_tests = 0
    
    for category, tests in results.items():
        category_passed = sum(1 for test in tests if test["status"] == "PASS")
        category_total = len(tests)
        total_tests += category_total
        passed_tests += category_passed
        
        print(f"{category.replace('_', ' ').title()}: {category_passed}/{category_total} passed")
    
    success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    print(f"\nOverall: {passed_tests}/{total_tests} tests passed ({success_rate:.1f}%)")
    
    # Detailed failures
    print(f"\n🚨 DETAILED FAILURES:")
    for category, tests in results.items():
        failed_tests = [test for test in tests if test["status"] == "FAIL"]
        if failed_tests:
            print(f"\n{category.replace('_', ' ').title()}:")
            for test in failed_tests:
                if "error" in test:
                    print(f"  • {test.get('symbol', test.get('endpoint', 'Unknown'))}: {test['error']}")
                else:
                    print(f"  • {test.get('symbol', test.get('endpoint', 'Unknown'))}: {test.get('details', 'Failed validation')}")
    
    return results

if __name__ == "__main__":
    test_multiple_component_fixes()