#!/usr/bin/env python3
"""
Test PPO Hook Pattern Filtering specifically
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BACKEND_URL = "https://stockwise-116.preview.emergentagent.com/api"

def test_ppo_hook_pattern_filtering():
    """Test the specific user issue: Scanner with negative hook criteria should return results"""
    print(f"🎯 TESTING PPO HOOK PATTERN FILTERING")
    print("=" * 70)
    
    # Test the exact user criteria from the review request
    user_criteria = {
        "price_filter": {"type": "range", "min": 100, "max": 500},
        "dmi_filter": {"min": 20, "max": 60},
        "ppo_slope_filter": {"threshold": -100},
        "ppo_hook_filter": "-HOOK"
    }
    
    print(f"\n📊 Testing User's Exact Criteria:")
    print(f"  • Price Range: $100-$500 (broad range)")
    print(f"  • DMI Range: 20-60 (reasonable range)")
    print(f"  • PPO Slope: Min -100% (very permissive, allows negative slopes)")
    print(f"  • PPO Hook Pattern: Negative Hook (-HOOK) Only")
    
    try:
        start_time = time.time()
        response = requests.post(f"{BACKEND_URL}/screener/scan", 
                               json=user_criteria,
                               headers={"Content-Type": "application/json"},
                               timeout=30)
        response_time = time.time() - start_time
        
        print(f"\n📈 RESPONSE ANALYSIS:")
        print(f"  • Status Code: {response.status_code}")
        print(f"  • Response Time: {response_time:.2f}s")
        
        if response.status_code == 200:
            data = response.json()
            
            # Check results
            results_found = data.get("results_found", 0)
            total_scanned = data.get("total_scanned", 0)
            stocks = data.get("stocks", [])
            filters_applied = data.get("filters_applied", {})
            
            print(f"  • Total Stocks Scanned: {total_scanned}")
            print(f"  • Results Found: {results_found}")
            print(f"  • Filters Applied: {filters_applied}")
            
            # The key issue: With broad criteria, we should find SOME negative hook patterns
            if results_found == 0:
                print(f"\n❌ ISSUE CONFIRMED: No results found with broad criteria")
                print(f"   This indicates negative hook detection may not be working")
                
                # Check if the ppo_hook_filter is even being processed
                hook_filter_applied = filters_applied.get("ppo_hook_filter")
                if hook_filter_applied is None:
                    print(f"   🚨 CRITICAL: ppo_hook_filter not found in filters_applied")
                    print(f"   This suggests the filter is not being processed by the backend")
                else:
                    print(f"   Hook filter applied: {hook_filter_applied}")
                    
            else:
                print(f"\n✅ SUCCESS: Found {results_found} stocks with negative hook patterns")
                
                # Validate that returned stocks actually have negative hooks
                print(f"\n🔍 VALIDATING NEGATIVE HOOK PATTERNS:")
                for i, stock in enumerate(stocks[:3]):
                    symbol = stock.get("symbol", f"Stock_{i}")
                    ppo_values = stock.get("ppo_values", [])
                    
                    if len(ppo_values) >= 3:
                        today = ppo_values[0]
                        yesterday = ppo_values[1] 
                        day_before = ppo_values[2]
                        
                        # Negative Hook: Today < Yesterday AND Yesterday > Day Before
                        negative_hook = today < yesterday and yesterday > day_before
                        
                        print(f"  • {symbol}: PPO({today:.3f}, {yesterday:.3f}, {day_before:.3f}) - Negative Hook: {negative_hook}")
                    else:
                        print(f"  • {symbol}: Insufficient PPO data: {len(ppo_values)} values")
            
        else:
            print(f"\n❌ API ERROR: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"\n❌ EXCEPTION: {str(e)}")

    # Test positive hook patterns for comparison
    print(f"\n🔄 Testing Positive Hook Patterns for Comparison")
    positive_criteria = user_criteria.copy()
    positive_criteria["ppo_hook_filter"] = "+HOOK"
    
    try:
        response = requests.post(f"{BACKEND_URL}/screener/scan", 
                               json=positive_criteria,
                               headers={"Content-Type": "application/json"},
                               timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            positive_results = data.get("results_found", 0)
            print(f"  • Positive Hook Results: {positive_results}")
        else:
            print(f"  • Positive Hook Test Failed: {response.status_code}")
            
    except Exception as e:
        print(f"  • Positive Hook Test Error: {str(e)}")

    # Test without hook filter to see baseline
    print(f"\n🔄 Testing Without Hook Filter (Baseline)")
    baseline_criteria = {
        "price_filter": {"type": "range", "min": 100, "max": 500},
        "dmi_filter": {"min": 20, "max": 60},
        "ppo_slope_filter": {"threshold": -100}
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/screener/scan", 
                               json=baseline_criteria,
                               headers={"Content-Type": "application/json"},
                               timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            baseline_results = data.get("results_found", 0)
            print(f"  • Baseline Results (no hook filter): {baseline_results}")
        else:
            print(f"  • Baseline Test Failed: {response.status_code}")
            
    except Exception as e:
        print(f"  • Baseline Test Error: {str(e)}")

if __name__ == "__main__":
    test_ppo_hook_pattern_filtering()