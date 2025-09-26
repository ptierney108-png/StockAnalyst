#!/usr/bin/env python3
"""
Focused Alpha Vantage API Testing
Tests the paid Alpha Vantage API key integration specifically
"""

import requests
import json
import time
from datetime import datetime

BACKEND_URL = "https://stockwise-120.preview.emergentagent.com/api"
TEST_SYMBOLS = ["AAPL", "GOOGL", "MSFT"]

def test_api_status():
    """Test API status endpoint"""
    print("🔍 Testing API Status Endpoint...")
    response = requests.get(f"{BACKEND_URL}/api-status", timeout=10)
    if response.status_code == 200:
        data = response.json()
        alpha_vantage = data.get("api_usage", {}).get("alpha_vantage", {})
        print(f"✅ Alpha Vantage Status:")
        print(f"   - Limit: {alpha_vantage.get('limit', 'N/A')}/minute")
        print(f"   - Calls made: {alpha_vantage.get('calls_made', 'N/A')}")
        print(f"   - Remaining: {alpha_vantage.get('remaining', 'N/A')}")
        print(f"   - Plan: {alpha_vantage.get('plan', 'N/A')}")
        return alpha_vantage.get('limit') == 70
    else:
        print(f"❌ API Status failed: {response.status_code}")
        return False

def test_alpha_vantage_data_quality(symbol):
    """Test Alpha Vantage data quality for a symbol"""
    print(f"\n📊 Testing Alpha Vantage data quality for {symbol}...")
    
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
        chart_data_count = len(data.get("chart_data", []))
        indicators = data.get("indicators", {})
        ppo = indicators.get("ppo", 0)
        
        print(f"✅ {symbol} Analysis Results:")
        print(f"   - Data source: {data_source}")
        print(f"   - Response time: {response_time:.2f}s")
        print(f"   - Chart data points: {chart_data_count}")
        print(f"   - PPO value: {ppo:.6f}")
        print(f"   - Current price: ${data.get('current_price', 'N/A')}")
        
        # Validate data quality
        issues = []
        if data_source != "alpha_vantage":
            issues.append(f"Expected Alpha Vantage, got {data_source}")
        if chart_data_count < 10:
            issues.append(f"Insufficient chart data: {chart_data_count}")
        if ppo == 0 and chart_data_count > 20:
            issues.append("PPO is zero despite sufficient data")
        
        if issues:
            print(f"⚠️  Issues found: {issues}")
            return False
        else:
            print(f"✅ Data quality validation passed")
            return True
    else:
        print(f"❌ API call failed: {response.status_code}")
        return False

def test_rapid_calls():
    """Test rapid API calls within rate limits"""
    print(f"\n⚡ Testing rapid API calls (rate limit verification)...")
    
    successful_calls = 0
    total_calls = 5
    
    for i in range(total_calls):
        symbol = TEST_SYMBOLS[i % len(TEST_SYMBOLS)]
        payload = {"symbol": symbol, "timeframe": "1D"}
        
        start_time = time.time()
        response = requests.post(f"{BACKEND_URL}/analyze", 
                               json=payload,
                               headers={"Content-Type": "application/json"},
                               timeout=15)
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            data_source = data.get("data_source", "unknown")
            successful_calls += 1
            print(f"   Call {i+1}: {symbol} - {data_source} - {response_time:.2f}s ✅")
        else:
            print(f"   Call {i+1}: {symbol} - FAILED {response.status_code} ❌")
        
        time.sleep(0.2)  # Small delay
    
    success_rate = (successful_calls / total_calls) * 100
    print(f"✅ Rapid calls test: {successful_calls}/{total_calls} successful ({success_rate:.1f}%)")
    return success_rate >= 80

def test_ppo_calculations():
    """Test PPO calculations with Alpha Vantage data"""
    print(f"\n🔢 Testing PPO calculations with Alpha Vantage data...")
    
    all_passed = True
    for symbol in TEST_SYMBOLS:
        payload = {"symbol": symbol, "timeframe": "1M"}
        response = requests.post(f"{BACKEND_URL}/analyze", 
                               json=payload,
                               headers={"Content-Type": "application/json"},
                               timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            data_source = data.get("data_source", "unknown")
            indicators = data.get("indicators", {})
            
            ppo = indicators.get("ppo")
            ppo_signal = indicators.get("ppo_signal")
            ppo_histogram = indicators.get("ppo_histogram")
            ppo_slope_percentage = indicators.get("ppo_slope_percentage")
            
            print(f"   {symbol} PPO Analysis:")
            print(f"     - Data source: {data_source}")
            print(f"     - PPO: {ppo:.6f}")
            print(f"     - PPO Signal: {ppo_signal:.6f}")
            print(f"     - PPO Histogram: {ppo_histogram:.6f}")
            print(f"     - PPO Slope %: {ppo_slope_percentage:.2f}%")
            
            # Validate PPO calculations
            if data_source == "alpha_vantage":
                if ppo is not None and ppo != 0:
                    print(f"     ✅ Non-zero PPO with Alpha Vantage data")
                else:
                    print(f"     ❌ PPO is zero/null with Alpha Vantage data")
                    all_passed = False
            else:
                print(f"     ⚠️  Not using Alpha Vantage data source")
        else:
            print(f"   ❌ {symbol} API call failed: {response.status_code}")
            all_passed = False
    
    return all_passed

def main():
    """Run focused Alpha Vantage API tests"""
    print("💰 FOCUSED ALPHA VANTAGE API TESTING")
    print("=" * 50)
    
    results = {
        "api_status": False,
        "data_quality": 0,
        "rapid_calls": False,
        "ppo_calculations": False
    }
    
    # Test 1: API Status
    results["api_status"] = test_api_status()
    
    # Test 2: Data Quality for each symbol
    passed_symbols = 0
    for symbol in TEST_SYMBOLS:
        if test_alpha_vantage_data_quality(symbol):
            passed_symbols += 1
    results["data_quality"] = passed_symbols
    
    # Test 3: Rapid calls
    results["rapid_calls"] = test_rapid_calls()
    
    # Test 4: PPO calculations
    results["ppo_calculations"] = test_ppo_calculations()
    
    # Summary
    print(f"\n📋 ALPHA VANTAGE API TEST SUMMARY")
    print("=" * 50)
    print(f"✅ API Status (70/min limit): {'PASS' if results['api_status'] else 'FAIL'}")
    print(f"✅ Data Quality ({results['data_quality']}/{len(TEST_SYMBOLS)} symbols): {'PASS' if results['data_quality'] == len(TEST_SYMBOLS) else 'PARTIAL' if results['data_quality'] > 0 else 'FAIL'}")
    print(f"✅ Rapid API Calls: {'PASS' if results['rapid_calls'] else 'FAIL'}")
    print(f"✅ PPO Calculations: {'PASS' if results['ppo_calculations'] else 'FAIL'}")
    
    # Overall assessment
    total_tests = 4
    passed_tests = sum([
        results["api_status"],
        results["data_quality"] == len(TEST_SYMBOLS),
        results["rapid_calls"],
        results["ppo_calculations"]
    ])
    
    success_rate = (passed_tests / total_tests) * 100
    print(f"\n🎯 Overall Success Rate: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
    
    if success_rate >= 75:
        print("✅ PAID ALPHA VANTAGE API INTEGRATION: WORKING CORRECTLY")
        return 0
    else:
        print("❌ PAID ALPHA VANTAGE API INTEGRATION: ISSUES DETECTED")
        return 1

if __name__ == "__main__":
    exit(main())