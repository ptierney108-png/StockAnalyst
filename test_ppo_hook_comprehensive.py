#!/usr/bin/env python3
"""
Comprehensive PPO Hook Pattern Filtering Test
"""

import requests
import json
import time

# Configuration
BACKEND_URL = "https://stockwise-116.preview.emergentagent.com/api"

def test_comprehensive_ppo_hook_filtering():
    """Comprehensive test of PPO hook pattern filtering"""
    print(f"🎯 COMPREHENSIVE PPO HOOK PATTERN FILTERING TEST")
    print("=" * 70)
    
    test_results = []
    
    # Test 1: User's exact criteria (the original issue)
    print(f"\n📊 Test 1: User's Exact Criteria (Original Issue)")
    user_criteria = {
        "price_filter": {"type": "range", "min": 100, "max": 500},
        "dmi_filter": {"min": 20, "max": 60},
        "ppo_slope_filter": {"threshold": -100},
        "ppo_hook_filter": "-HOOK"
    }
    
    result1 = run_screener_test("Negative Hook (User Criteria)", user_criteria)
    test_results.append(result1)
    
    # Test 2: Positive hook patterns
    print(f"\n📊 Test 2: Positive Hook Patterns")
    positive_criteria = user_criteria.copy()
    positive_criteria["ppo_hook_filter"] = "+HOOK"
    
    result2 = run_screener_test("Positive Hook", positive_criteria)
    test_results.append(result2)
    
    # Test 3: Both hook patterns
    print(f"\n📊 Test 3: Both Hook Patterns")
    both_criteria = user_criteria.copy()
    both_criteria["ppo_hook_filter"] = "both"
    
    result3 = run_screener_test("Both Hooks", both_criteria)
    test_results.append(result3)
    
    # Test 4: No hook filter (baseline)
    print(f"\n📊 Test 4: No Hook Filter (Baseline)")
    baseline_criteria = {
        "price_filter": {"type": "range", "min": 100, "max": 500},
        "dmi_filter": {"min": 20, "max": 60},
        "ppo_slope_filter": {"threshold": -100}
    }
    
    result4 = run_screener_test("No Hook Filter", baseline_criteria)
    test_results.append(result4)
    
    # Test 5: Very permissive criteria with negative hooks
    print(f"\n📊 Test 5: Very Permissive Criteria with Negative Hooks")
    permissive_criteria = {
        "price_filter": {"type": "range", "min": 50, "max": 1000},
        "dmi_filter": {"min": 10, "max": 80},
        "ppo_slope_filter": {"threshold": -200},
        "ppo_hook_filter": "-HOOK"
    }
    
    result5 = run_screener_test("Permissive Negative Hook", permissive_criteria)
    test_results.append(result5)
    
    # Test 6: All stocks filter (should return all stocks regardless of hook pattern)
    print(f"\n📊 Test 6: All Stocks Filter")
    all_criteria = user_criteria.copy()
    all_criteria["ppo_hook_filter"] = "all"
    
    result6 = run_screener_test("All Stocks", all_criteria)
    test_results.append(result6)
    
    # Summary
    print(f"\n📈 COMPREHENSIVE TEST SUMMARY")
    print("=" * 70)
    
    for result in test_results:
        status = "✅ PASS" if result["success"] else "❌ FAIL"
        print(f"{status}: {result['name']} - {result['results']} results in {result['time']:.2f}s")
        if result["error"]:
            print(f"    Error: {result['error']}")
    
    # Analysis
    negative_hook_results = result1["results"]
    positive_hook_results = result2["results"]
    both_hook_results = result3["results"]
    baseline_results = result4["results"]
    
    print(f"\n🔍 ANALYSIS:")
    print(f"  • Negative Hooks: {negative_hook_results}")
    print(f"  • Positive Hooks: {positive_hook_results}")
    print(f"  • Both Hooks: {both_hook_results}")
    print(f"  • Baseline (no filter): {baseline_results}")
    
    # Validation checks
    validation_passed = True
    
    if negative_hook_results == 0:
        print(f"  ❌ Issue: No negative hook patterns found with broad criteria")
        validation_passed = False
    else:
        print(f"  ✅ Negative hook detection working")
    
    if both_hook_results < max(negative_hook_results, positive_hook_results):
        print(f"  ✅ Both hooks filter working correctly (should be >= max of individual filters)")
    
    if baseline_results < both_hook_results:
        print(f"  ❌ Issue: Baseline should have more results than filtered results")
        validation_passed = False
    else:
        print(f"  ✅ Filtering logic working correctly")
    
    overall_status = "✅ ALL TESTS PASSED" if validation_passed else "❌ SOME TESTS FAILED"
    print(f"\n{overall_status}")
    
    return validation_passed

def run_screener_test(name, criteria):
    """Run a single screener test"""
    result = {
        "name": name,
        "success": False,
        "results": 0,
        "time": 0,
        "error": None
    }
    
    try:
        start_time = time.time()
        response = requests.post(f"{BACKEND_URL}/screener/scan", 
                               json=criteria,
                               headers={"Content-Type": "application/json"},
                               timeout=30)
        result["time"] = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            result["results"] = data.get("results_found", 0)
            result["success"] = True
            
            # Validate hook patterns if applicable
            if "ppo_hook_filter" in criteria and criteria["ppo_hook_filter"] != "all":
                stocks = data.get("stocks", [])
                hook_validation = validate_hook_patterns(stocks, criteria["ppo_hook_filter"])
                if not hook_validation:
                    result["error"] = "Hook pattern validation failed"
                    result["success"] = False
            
        else:
            result["error"] = f"HTTP {response.status_code}: {response.text}"
            
    except Exception as e:
        result["error"] = str(e)
    
    return result

def validate_hook_patterns(stocks, hook_filter):
    """Validate that returned stocks have the correct hook patterns"""
    if not stocks:
        return True  # No stocks to validate
    
    for stock in stocks[:5]:  # Check first 5 stocks
        ppo_values = stock.get("ppo_values", [])
        if len(ppo_values) >= 3:
            today = ppo_values[0]
            yesterday = ppo_values[1]
            day_before = ppo_values[2]
            
            positive_hook = today > yesterday and yesterday < day_before
            negative_hook = today < yesterday and yesterday > day_before
            
            if hook_filter == "+HOOK" and not positive_hook:
                return False
            elif hook_filter == "-HOOK" and not negative_hook:
                return False
            elif hook_filter == "both" and not (positive_hook or negative_hook):
                return False
    
    return True

if __name__ == "__main__":
    test_comprehensive_ppo_hook_filtering()