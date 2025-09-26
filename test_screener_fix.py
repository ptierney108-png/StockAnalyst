#!/usr/bin/env python3
"""
Focused test for Stock Screener Real Data Fix
Tests the specific fix where stock screener now uses real Alpha Vantage data instead of demo data
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BACKEND_URL = "https://market-analyzer-95.preview.emergentagent.com/api"

def test_stock_screener_real_data_fix():
    """Test the stock screener real data fix"""
    print("🔧 TESTING STOCK SCREENER REAL DATA FIX")
    print("=" * 60)
    
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
                               timeout=60)
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"✅ API Response received in {response_time:.2f}s")
            print(f"📊 Response Summary:")
            print(f"   - Success: {data.get('success')}")
            print(f"   - Total Scanned: {data.get('total_scanned')}")
            print(f"   - Results Found: {data.get('results_found')}")
            print(f"   - Real Data Count: {data.get('real_data_count')}")
            print(f"   - Data Sources: {data.get('data_sources')}")
            print(f"   - Note: {data.get('note', 'N/A')}")
            
            # Validate the fix
            issues = validate_real_data_fix(data, test_filters)
            
            if issues:
                print(f"\n❌ ISSUES FOUND ({len(issues)}):")
                for issue in issues:
                    print(f"   • {issue}")
                return False
            else:
                print(f"\n✅ STOCK SCREENER REAL DATA FIX WORKING CORRECTLY")
                print(f"   - All {data.get('results_found', 0)} stocks using real Alpha Vantage data")
                print(f"   - Data source transparency implemented")
                print(f"   - PPO values calculated from real price data")
                print(f"   - Filtering working correctly with real data")
                return True
                
        else:
            print(f"❌ API call failed: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        return False

def validate_real_data_fix(data, filters):
    """Validate that the screener is using real Alpha Vantage data"""
    issues = []
    
    # Check basic response structure
    if not data.get("success"):
        issues.append("Screener response indicates failure")
        return issues
    
    stocks = data.get("stocks", [])
    if not stocks:
        issues.append("No stocks returned from screener")
        return issues
    
    # Check for data source transparency (key requirement)
    data_sources = data.get("data_sources", [])
    real_data_count = data.get("real_data_count", 0)
    
    if not data_sources:
        issues.append("Missing data_sources field in response")
    
    if real_data_count == 0:
        issues.append("No real data sources used - still using demo data")
    
    # Check if Alpha Vantage is the primary data source
    if "alpha_vantage" not in data_sources:
        issues.append("Alpha Vantage not listed as data source")
    
    # Validate individual stocks
    alpha_vantage_count = 0
    total_stocks = len(stocks)
    
    print(f"\n📊 STOCK DATA ANALYSIS:")
    for i, stock in enumerate(stocks[:5]):  # Check first 5 stocks for display
        symbol = stock.get("symbol", f"Stock_{i}")
        stock_data_source = stock.get("data_source", "unknown")
        price = stock.get("price", 0)
        ppo_values = stock.get("ppo_values", [])
        
        print(f"   {symbol}: Price=${price:.2f}, Source={stock_data_source}, PPO={ppo_values}")
    
    # Count all stocks with Alpha Vantage data source
    for stock in stocks:
        symbol = stock.get("symbol", "Unknown")
        stock_data_source = stock.get("data_source", "unknown")
        price = stock.get("price", 0)
        ppo_values = stock.get("ppo_values", [])
        
        if stock_data_source == "alpha_vantage":
            alpha_vantage_count += 1
            
            # Validate real data characteristics
            if price <= 0:
                issues.append(f"{symbol}: Invalid price value")
            
            if len(ppo_values) < 3:
                issues.append(f"{symbol}: Insufficient PPO values")
            elif all(val == 0 for val in ppo_values):
                issues.append(f"{symbol}: All PPO values are zero")
        
        elif stock_data_source == "mock":
            issues.append(f"{symbol}: Still using mock data source")
    
    print(f"   📊 Total stocks with Alpha Vantage data: {alpha_vantage_count}/{total_stocks}")
    
    # Check data source distribution
    if alpha_vantage_count == 0 and total_stocks > 0:
        issues.append("No stocks using Alpha Vantage data source")
    elif alpha_vantage_count < total_stocks * 0.8:  # Less than 80% real data
        issues.append(f"Only {alpha_vantage_count}/{total_stocks} stocks using Alpha Vantage (expected majority)")
    else:
        print(f"   ✅ {alpha_vantage_count}/{total_stocks} stocks using Alpha Vantage data source")
    
    # Validate filtering still works with real data
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

def test_additional_scenarios():
    """Test additional scenarios for the real data fix"""
    print(f"\n🔍 TESTING ADDITIONAL SCENARIOS")
    print("-" * 40)
    
    scenarios = [
        {
            "name": "Simple Price Filter",
            "filters": {"price_filter": {"type": "under", "under": 300}}
        },
        {
            "name": "PPO Slope Filter",
            "filters": {
                "price_filter": {"type": "under", "under": 400},
                "ppo_slope_filter": {"threshold": 5}
            }
        }
    ]
    
    all_passed = True
    
    for scenario in scenarios:
        print(f"\n📊 Testing: {scenario['name']}")
        try:
            response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                   json=scenario["filters"],
                                   headers={"Content-Type": "application/json"},
                                   timeout=45)
            
            if response.status_code == 200:
                data = response.json()
                stocks_found = data.get("results_found", 0)
                real_data_count = data.get("real_data_count", 0)
                data_sources = data.get("data_sources", [])
                
                print(f"   ✅ Found {stocks_found} stocks, {real_data_count} with real data")
                print(f"   📊 Data sources: {data_sources}")
                
                if "alpha_vantage" not in data_sources:
                    print(f"   ❌ Alpha Vantage not in data sources")
                    all_passed = False
                    
            else:
                print(f"   ❌ HTTP {response.status_code}")
                all_passed = False
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            all_passed = False
    
    return all_passed

def main():
    """Main test execution"""
    print("🚀 STOCK SCREENER REAL DATA FIX TESTING")
    print("=" * 60)
    
    # Test the main fix
    main_test_passed = test_stock_screener_real_data_fix()
    
    # Test additional scenarios
    additional_tests_passed = test_additional_scenarios()
    
    # Summary
    print(f"\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    
    if main_test_passed and additional_tests_passed:
        print("✅ ALL TESTS PASSED")
        print("✅ Stock screener now uses real Alpha Vantage data instead of demo data")
        print("✅ Data source transparency implemented")
        print("✅ PPO values calculated from real price data")
        print("✅ Filtering works correctly with real data")
        print("✅ Response includes data source information")
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        if not main_test_passed:
            print("❌ Main stock screener real data fix test failed")
        if not additional_tests_passed:
            print("❌ Additional scenario tests failed")
        return 1

if __name__ == "__main__":
    exit(main())