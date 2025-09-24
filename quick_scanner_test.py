#!/usr/bin/env python3
"""
Quick Scanner Filtering Logic Test
Tests the exact user criteria from the review request
"""

import requests
import json

# Test the exact user criteria from the review request
user_criteria = {
    "price_filter": {"type": "under", "under": 100},
    "dmi_filter": {"min": 20, "max": 60},
    "ppo_slope_filter": {"threshold": 5},
    "ppo_hook_filter": "all",
    "sector_filter": "all",
    "optionable_filter": "all",
    "earnings_filter": "all"
}

try:
    print("🎯 Testing Scanner Filtering Logic Fix")
    print("Testing exact user criteria from review request:")
    print("• Price Range: Under $100")
    print("• DMI Range: Min 20, Max 60")
    print("• PPO Slope: Min 5%")
    print()
    
    response = requests.post("https://stockwise-116.preview.emergentagent.com/api/screener/scan", 
                           json=user_criteria,
                           headers={"Content-Type": "application/json"},
                           timeout=30)
    
    if response.status_code == 200:
        data = response.json()
        stocks = data.get("stocks", [])
        total_found = data.get("results_found", 0)
        
        print(f"✅ Scanner Response: {total_found} stocks found")
        print(f"📋 Total stocks scanned: {data.get('total_scanned', 'N/A')}")
        print()
        
        # Validate filtering criteria
        violations = 0
        price_violations = 0
        dmi_violations = 0
        ppo_violations = 0
        
        for stock in stocks:
            symbol = stock.get("symbol", "UNKNOWN")
            price = stock.get("price", 0)
            adx = stock.get("adx", 0)
            ppo_slope = stock.get("ppo_slope_percentage", 0)
            
            if price > 100:
                print(f"❌ {symbol}: Price ${price:.2f} exceeds $100 filter")
                violations += 1
                price_violations += 1
            if not (20 <= adx <= 60):
                print(f"❌ {symbol}: ADX {adx:.2f} outside 20-60 range")
                violations += 1
                dmi_violations += 1
            if ppo_slope < 5:
                print(f"❌ {symbol}: PPO Slope {ppo_slope:.2f}% below 5% threshold")
                violations += 1
                ppo_violations += 1
        
        print(f"📊 FILTERING RESULTS:")
        print(f"  • Price violations: {price_violations}")
        print(f"  • DMI violations: {dmi_violations}")
        print(f"  • PPO slope violations: {ppo_violations}")
        print()
        
        if violations == 0:
            print("✅ ALL FILTERING CRITERIA PROPERLY APPLIED - NO VIOLATIONS")
            print("🎉 SCANNER FILTERING LOGIC FIX WORKING CORRECTLY")
        else:
            print(f"🚨 {violations} FILTERING VIOLATIONS DETECTED")
            print("❌ SCANNER FILTERING LOGIC NEEDS FURTHER INVESTIGATION")
            
    else:
        print(f"❌ API Error: {response.status_code}: {response.text}")
        
except Exception as e:
    print(f"❌ Test Error: {str(e)}")