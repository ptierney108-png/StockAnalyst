#!/usr/bin/env python3
"""
PPO Calculation Fix Validation Script
Tests the specific requirements from the review request
"""

import requests
import json
import time

BACKEND_URL = "https://stockwise-platform.preview.emergentagent.com/api"

def test_ppo_fix_requirements():
    """Test all requirements from the review request"""
    print("🔧 PPO CALCULATION FIX VALIDATION")
    print("=" * 50)
    
    results = {
        "total_tests": 0,
        "passed_tests": 0,
        "failed_tests": 0,
        "issues": []
    }
    
    def log_test(name, passed, details):
        results["total_tests"] += 1
        if passed:
            results["passed_tests"] += 1
            print(f"✅ {name}: {details}")
        else:
            results["failed_tests"] += 1
            results["issues"].append(f"{name}: {details}")
            print(f"❌ {name}: {details}")
    
    # Test 1: PPO values are no longer zero with various symbols and timeframes
    print("\n📊 Test 1: Non-zero PPO values with limited data")
    test_cases = [
        {"symbol": "AAPL", "timeframe": "1D"},
        {"symbol": "GOOGL", "timeframe": "5D"},
        {"symbol": "MSFT", "timeframe": "1M"}
    ]
    
    for case in test_cases:
        try:
            response = requests.post(f"{BACKEND_URL}/analyze", json=case, timeout=30)
            if response.status_code == 200:
                data = response.json()
                indicators = data.get("indicators", {})
                ppo = indicators.get("ppo", 0)
                
                if ppo != 0:
                    log_test(f"Non-zero PPO ({case['symbol']} {case['timeframe']})", True, 
                           f"PPO = {ppo:.6f}")
                else:
                    log_test(f"Non-zero PPO ({case['symbol']} {case['timeframe']})", False, 
                           "PPO is still zero")
            else:
                log_test(f"API Response ({case['symbol']} {case['timeframe']})", False, 
                       f"HTTP {response.status_code}")
        except Exception as e:
            log_test(f"API Test ({case['symbol']} {case['timeframe']})", False, str(e))
    
    # Test 2: Data quality indicators are included
    print("\n📋 Test 2: Data quality indicators in responses")
    try:
        response = requests.post(f"{BACKEND_URL}/analyze", 
                               json={"symbol": "AAPL", "timeframe": "1D"}, timeout=30)
        if response.status_code == 200:
            data = response.json()
            
            # Check for data_quality field
            data_quality_obj = data.get("data_quality", {})
            if data_quality_obj and "data_quality" in data_quality_obj:
                log_test("Data Quality Field", True, 
                       f"Quality: {data_quality_obj['data_quality']}")
            else:
                log_test("Data Quality Field", False, "Missing data_quality field")
            
            # Check for ppo_calculation_note
            ppo_note = data.get("ppo_calculation_note")
            if ppo_note:
                log_test("PPO Calculation Note", True, f"Note: {ppo_note}")
            else:
                log_test("PPO Calculation Note", False, "Missing ppo_calculation_note")
                
    except Exception as e:
        log_test("Data Quality Test", False, str(e))
    
    # Test 3: PPO slope calculations work with adaptive values
    print("\n📐 Test 3: PPO slope calculations with adaptive values")
    try:
        response = requests.post(f"{BACKEND_URL}/analyze", 
                               json={"symbol": "MSFT", "timeframe": "1D"}, timeout=30)
        if response.status_code == 200:
            data = response.json()
            indicators = data.get("indicators", {})
            
            ppo_slope = indicators.get("ppo_slope")
            ppo_slope_percentage = indicators.get("ppo_slope_percentage")
            
            if ppo_slope is not None and ppo_slope_percentage is not None:
                log_test("PPO Slope Calculation", True, 
                       f"Slope: {ppo_slope:.4f}, Percentage: {ppo_slope_percentage:.2f}%")
            else:
                log_test("PPO Slope Calculation", False, "Missing PPO slope values")
                
    except Exception as e:
        log_test("PPO Slope Test", False, str(e))
    
    # Test 4: Fallback handling for very limited data
    print("\n🔬 Test 4: Fallback handling for edge cases")
    try:
        response = requests.post(f"{BACKEND_URL}/analyze", 
                               json={"symbol": "AAPL", "timeframe": "1D"}, timeout=30)
        if response.status_code == 200:
            data = response.json()
            data_quality_obj = data.get("data_quality", {})
            chart_data = data.get("chart_data", [])
            
            if len(chart_data) < 26:  # Limited data scenario
                if data_quality_obj.get("data_quality") == "adaptive":
                    fallback_reason = data_quality_obj.get("fallback_reason", "")
                    if "adapted" in fallback_reason.lower():
                        log_test("Fallback Handling", True, 
                               f"Adaptive calculation with {len(chart_data)} points")
                    else:
                        log_test("Fallback Handling", False, "Missing fallback reason")
                else:
                    log_test("Fallback Handling", False, "Not using adaptive calculation")
            else:
                log_test("Fallback Handling", True, f"Sufficient data: {len(chart_data)} points")
                
    except Exception as e:
        log_test("Fallback Test", False, str(e))
    
    # Test 5: Screener endpoint continues to work
    print("\n🔍 Test 5: Stock screener functionality")
    try:
        filters = {
            "price_filter": {"type": "under", "under": 300},
            "dmi_filter": {"min": 20, "max": 60},
            "ppo_slope_filter": {"threshold": 1}
        }
        
        response = requests.post(f"{BACKEND_URL}/screener/scan", json=filters, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and data.get("results_found", 0) > 0:
                stocks = data.get("stocks", [])
                if stocks:
                    first_stock = stocks[0]
                    ppo_values = first_stock.get("ppo_values", [])
                    if ppo_values and any(val != 0 for val in ppo_values):
                        log_test("Screener Functionality", True, 
                               f"Found {data['results_found']} stocks with valid PPO data")
                    else:
                        log_test("Screener Functionality", False, "Screener stocks have zero PPO values")
                else:
                    log_test("Screener Functionality", False, "No stocks in screener results")
            else:
                log_test("Screener Functionality", False, "Screener returned no results")
        else:
            log_test("Screener Functionality", False, f"HTTP {response.status_code}")
            
    except Exception as e:
        log_test("Screener Test", False, str(e))
    
    # Test 6: Data source transparency
    print("\n🔍 Test 6: Data source transparency")
    try:
        response = requests.post(f"{BACKEND_URL}/analyze", 
                               json={"symbol": "GOOGL", "timeframe": "1D"}, timeout=30)
        if response.status_code == 200:
            data = response.json()
            data_quality_obj = data.get("data_quality", {})
            data_source = data_quality_obj.get("data_source")
            
            if data_source:
                log_test("Data Source Transparency", True, f"Source: {data_source}")
            else:
                log_test("Data Source Transparency", False, "Missing data source information")
                
    except Exception as e:
        log_test("Data Source Test", False, str(e))
    
    # Print summary
    print("\n" + "=" * 50)
    print("📋 PPO FIX VALIDATION SUMMARY")
    print("=" * 50)
    print(f"Total Tests: {results['total_tests']}")
    print(f"✅ Passed: {results['passed_tests']}")
    print(f"❌ Failed: {results['failed_tests']}")
    print(f"Success Rate: {(results['passed_tests']/results['total_tests']*100):.1f}%")
    
    if results["issues"]:
        print(f"\n🚨 ISSUES FOUND ({len(results['issues'])}):")
        for issue in results["issues"]:
            print(f"  • {issue}")
    else:
        print(f"\n✅ ALL PPO CALCULATION FIX REQUIREMENTS VALIDATED SUCCESSFULLY!")
    
    return results

if __name__ == "__main__":
    test_ppo_fix_requirements()