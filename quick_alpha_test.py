#!/usr/bin/env python3
"""
Quick Alpha Vantage API Test
"""

import requests
import json

BACKEND_URL = "https://stockwise-120.preview.emergentagent.com/api"

def main():
    print("💰 QUICK ALPHA VANTAGE API TEST")
    print("=" * 40)
    
    # Test 1: API Status
    print("\n1. Testing API Status...")
    response = requests.get(f"{BACKEND_URL}/api-status", timeout=10)
    if response.status_code == 200:
        data = response.json()
        alpha_vantage = data.get("api_usage", {}).get("alpha_vantage", {})
        limit = alpha_vantage.get("limit", 0)
        plan = alpha_vantage.get("plan", "unknown")
        calls_made = alpha_vantage.get("calls_made", 0)
        
        print(f"   ✅ API Status: {response.status_code}")
        print(f"   ✅ Rate Limit: {limit}/minute")
        print(f"   ✅ Plan Type: {plan}")
        print(f"   ✅ Calls Made: {calls_made}")
        
        if limit == 70 and plan == "paid":
            print("   ✅ PAID PLAN CORRECTLY CONFIGURED")
        else:
            print("   ❌ PAID PLAN NOT PROPERLY CONFIGURED")
    else:
        print(f"   ❌ API Status failed: {response.status_code}")
    
    # Test 2: Single API Call
    print("\n2. Testing Single API Call...")
    payload = {"symbol": "AAPL", "timeframe": "1D"}
    response = requests.post(f"{BACKEND_URL}/analyze", 
                           json=payload,
                           headers={"Content-Type": "application/json"},
                           timeout=30)
    
    if response.status_code == 200:
        data = response.json()
        data_source = data.get("data_source", "unknown")
        chart_data_count = len(data.get("chart_data", []))
        ppo = data.get("indicators", {}).get("ppo", 0)
        response_time = data.get("response_time", 0)
        
        print(f"   ✅ API Call: {response.status_code}")
        print(f"   ✅ Data Source: {data_source}")
        print(f"   ✅ Chart Data Points: {chart_data_count}")
        print(f"   ✅ PPO Value: {ppo:.6f}")
        print(f"   ✅ Response Time: {response_time}s")
        
        if data_source == "alpha_vantage":
            print("   ✅ ALPHA VANTAGE API WORKING")
        else:
            print(f"   ⚠️  Using fallback: {data_source}")
    else:
        print(f"   ❌ API Call failed: {response.status_code}")
    
    # Test 3: Check API Usage After Call
    print("\n3. Checking API Usage After Call...")
    response = requests.get(f"{BACKEND_URL}/api-status", timeout=10)
    if response.status_code == 200:
        data = response.json()
        alpha_vantage = data.get("api_usage", {}).get("alpha_vantage", {})
        calls_made = alpha_vantage.get("calls_made", 0)
        remaining = alpha_vantage.get("remaining", 0)
        
        print(f"   ✅ Calls Made: {calls_made}")
        print(f"   ✅ Remaining: {remaining}")
        
        if calls_made > 0:
            print("   ✅ API CALL TRACKING WORKING")
        else:
            print("   ⚠️  API call tracking may not be working")
    
    print("\n" + "=" * 40)
    print("✅ ALPHA VANTAGE API INTEGRATION TEST COMPLETE")

if __name__ == "__main__":
    main()