#!/usr/bin/env python3
"""
Test debug logging for PPO hook pattern detection
"""

import requests
import json

# Configuration
BACKEND_URL = "https://stockwise-116.preview.emergentagent.com/api"

def test_debug_logging():
    """Test debug logging for hook pattern detection"""
    print(f"🔍 TESTING DEBUG LOGGING FOR HOOK PATTERN DETECTION")
    print("=" * 70)
    
    # Test with a small set to see debug output clearly
    criteria = {
        "price_filter": {"type": "range", "min": 100, "max": 500},
        "dmi_filter": {"min": 20, "max": 60},
        "ppo_slope_filter": {"threshold": -100},
        "ppo_hook_filter": "-HOOK"
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/screener/scan", 
                               json=criteria,
                               headers={"Content-Type": "application/json"},
                               timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            results_found = data.get("results_found", 0)
            stocks = data.get("stocks", [])
            
            print(f"✅ Found {results_found} stocks with negative hook patterns")
            
            # Show detailed analysis of first few stocks
            print(f"\n📊 DETAILED HOOK PATTERN ANALYSIS:")
            for i, stock in enumerate(stocks[:5]):
                symbol = stock.get("symbol", f"Stock_{i}")
                ppo_values = stock.get("ppo_values", [])
                
                if len(ppo_values) >= 3:
                    today = ppo_values[0]
                    yesterday = ppo_values[1]
                    day_before = ppo_values[2]
                    
                    # Check hook patterns
                    positive_hook = today > yesterday and yesterday < day_before
                    negative_hook = today < yesterday and yesterday > day_before
                    
                    hook_type = "Positive" if positive_hook else "Negative" if negative_hook else "None"
                    
                    print(f"  • {symbol}:")
                    print(f"    PPO Values: Today={today:.3f}, Yesterday={yesterday:.3f}, Day Before={day_before:.3f}")
                    print(f"    Hook Pattern: {hook_type}")
                    print(f"    Negative Hook Logic: {today:.3f} < {yesterday:.3f} AND {yesterday:.3f} > {day_before:.3f} = {negative_hook}")
                    
                    # Additional stock info
                    price = stock.get("price", 0)
                    adx = stock.get("adx", 0)
                    ppo_slope = stock.get("ppo_slope_percentage", 0)
                    print(f"    Price: ${price:.2f}, ADX: {adx:.1f}, PPO Slope: {ppo_slope:.2f}%")
                    print()
            
            print(f"🎯 VALIDATION SUMMARY:")
            print(f"  • All returned stocks should have negative hook patterns")
            print(f"  • Negative Hook Definition: Today < Yesterday AND Yesterday > Day Before")
            print(f"  • This represents a downward reversal in PPO momentum")
            
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

if __name__ == "__main__":
    test_debug_logging()