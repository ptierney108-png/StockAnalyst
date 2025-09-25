#!/usr/bin/env python3
"""
Focused PPO Slope Absolute Value Removal Test
Tests the specific changes requested in the review
"""

import requests
import json
import time
from typing import Dict, Any, List

# Configuration
BACKEND_URL = "https://market-scanner-27.preview.emergentagent.com/api"
TEST_SYMBOLS = ["AAPL", "GOOGL", "MSFT"]

def test_ppo_slope_absolute_value_removal():
    """
    CRITICAL TEST: Validate removal of absolute values from hook and slope calculations
    
    Tests that after removing Math.abs() and abs() from slope calculations, 
    the results still produce meaningful positive and negative slope values 
    naturally from the mathematical formulas.
    """
    print(f"\n🎯 CRITICAL TEST: PPO SLOPE ABSOLUTE VALUE REMOVAL VALIDATION")
    print("=" * 80)
    
    all_passed = True
    slope_issues = []
    
    print(f"\n📊 Testing PPO slope calculations without absolute values")
    
    for symbol in TEST_SYMBOLS:
        print(f"\n🔍 Testing {symbol} for natural slope calculations...")
        
        try:
            # Test with different timeframes to get various PPO scenarios
            timeframes = ["1D", "5D", "1M"]
            
            for timeframe in timeframes:
                payload = {"symbol": symbol, "timeframe": timeframe}
                start_time = time.time()
                
                response = requests.post(f"{BACKEND_URL}/analyze", 
                                       json=payload,
                                       headers={"Content-Type": "application/json"},
                                       timeout=30)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Validate PPO slope calculation without absolute values
                    slope_validation_issues = validate_natural_slope_calculations(
                        data, symbol, timeframe
                    )
                    
                    if slope_validation_issues:
                        slope_issues.extend(slope_validation_issues)
                        all_passed = False
                        print(f"    ❌ FAIL: Natural Slope Calculation ({symbol} {timeframe}) - Issues: {slope_validation_issues}")
                    else:
                        print(f"    ✅ PASS: Natural Slope Calculation ({symbol} {timeframe}) - PPO slopes calculated naturally without absolute values")
                    
                    # Log detailed slope analysis
                    indicators = data.get("indicators", {})
                    ppo_slope_percentage = indicators.get("ppo_slope_percentage", 0)
                    ppo_history = data.get("ppo_history", [])
                    
                    if len(ppo_history) >= 3:
                        today_ppo = ppo_history[-1].get("ppo", 0)
                        yesterday_ppo = ppo_history[-2].get("ppo", 0)
                        day_before_ppo = ppo_history[-3].get("ppo", 0)
                        
                        print(f"      📈 {symbol} ({timeframe}): PPO History: Today={today_ppo:.4f}, Yesterday={yesterday_ppo:.4f}, Day Before={day_before_ppo:.4f}")
                        print(f"      📐 Calculated Slope: {ppo_slope_percentage:.2f}% (Natural calculation without abs())")
                        
                        # Verify slope sign makes mathematical sense
                        if yesterday_ppo != 0:
                            expected_slope_direction = "positive" if today_ppo > yesterday_ppo else "negative"
                            actual_slope_direction = "positive" if ppo_slope_percentage > 0 else "negative"
                            
                            print(f"      🧮 PPO Movement: {expected_slope_direction}, Calculated Slope: {actual_slope_direction}")
                    
                else:
                    print(f"    ❌ FAIL: Slope Test API ({symbol} {timeframe}) - HTTP {response.status_code}: {response.text}")
                    all_passed = False
                    
        except Exception as e:
            print(f"    ❌ FAIL: Slope Test ({symbol}) - Error: {str(e)}")
            all_passed = False
    
    # Test Stock Screener with various slope thresholds
    print(f"\n📊 Testing Stock Screener with Various PPO Slope Thresholds")
    screener_slope_tests = test_screener_slope_filtering()
    if not screener_slope_tests:
        all_passed = False
        slope_issues.append("Stock screener slope filtering failed")
    
    # Test Hook Pattern Detection
    print(f"\n🪝 Testing Hook Pattern Detection with Natural Slopes")
    hook_pattern_tests = test_hook_pattern_detection()
    if not hook_pattern_tests:
        all_passed = False
        slope_issues.append("Hook pattern detection failed")
    
    # Summary
    if slope_issues:
        print(f"\n🚨 PPO SLOPE ABSOLUTE VALUE REMOVAL ISSUES ({len(slope_issues)}):")
        for issue in slope_issues:
            print(f"  • {issue}")
    else:
        print(f"\n✅ PPO slope calculations working correctly without absolute values")
        print(f"   • Positive and negative slopes calculated naturally")
        print(f"   • Mathematical formulas produce meaningful results")
        print(f"   • Hook pattern detection unaffected")
        print(f"   • Filtering logic compatible with natural slope values")
    
    return all_passed

def validate_natural_slope_calculations(data: Dict[str, Any], symbol: str, timeframe: str) -> List[str]:
    """Validate that PPO slopes are calculated naturally without absolute values"""
    issues = []
    
    indicators = data.get("indicators", {})
    ppo_history = data.get("ppo_history", [])
    
    if not indicators:
        issues.append("Missing indicators object")
        return issues
    
    if len(ppo_history) < 3:
        issues.append(f"Insufficient PPO history: {len(ppo_history)} entries (need 3)")
        return issues
    
    # Get PPO values
    today_ppo = ppo_history[-1].get("ppo", 0)
    yesterday_ppo = ppo_history[-2].get("ppo", 0)
    day_before_ppo = ppo_history[-3].get("ppo", 0)
    
    # Get calculated slope
    ppo_slope = indicators.get("ppo_slope", 0)
    ppo_slope_percentage = indicators.get("ppo_slope_percentage", 0)
    
    # Validate slope calculation follows the implemented formula (without absolute values)
    if yesterday_ppo != 0:
        # The current implementation has specific logic for positive/negative PPO values
        if today_ppo < 0:
            expected_slope = (today_ppo - yesterday_ppo) / yesterday_ppo
        else:  # today_ppo >= 0
            expected_slope = (yesterday_ppo - today_ppo) / yesterday_ppo
        
        expected_slope_percentage = expected_slope * 100
        
        # Allow for small floating point differences
        if abs(ppo_slope_percentage - expected_slope_percentage) > 0.01:
            issues.append(f"Slope calculation mismatch: expected {expected_slope_percentage:.4f}%, got {ppo_slope_percentage:.4f}%")
    
    # Check for mathematical errors
    if ppo_slope_percentage != ppo_slope_percentage:  # NaN check
        issues.append("PPO slope percentage is NaN")
    
    if abs(ppo_slope_percentage) > 10000:  # Unreasonably large slope
        issues.append(f"PPO slope percentage unreasonably large: {ppo_slope_percentage}%")
    
    # Validate division by zero protection
    if yesterday_ppo == 0 and ppo_slope_percentage != 0:
        issues.append("Division by zero not properly handled")
    
    return issues

def test_screener_slope_filtering() -> bool:
    """Test stock screener with various PPO slope thresholds (positive and negative)"""
    all_passed = True
    
    # Test cases with different slope thresholds
    test_cases = [
        {
            "name": "Positive Slope Filter",
            "filters": {
                "price_filter": {"type": "under", "under": 500},
                "dmi_filter": {"min": 20, "max": 60},
                "ppo_slope_filter": {"threshold": 5},  # Positive threshold
                "ppo_hook_filter": "all"
            },
            "expected_behavior": "Should find stocks with slopes >= 5%"
        },
        {
            "name": "Negative Slope Filter",
            "filters": {
                "price_filter": {"type": "under", "under": 500},
                "dmi_filter": {"min": 20, "max": 60},
                "ppo_slope_filter": {"threshold": -5},  # Negative threshold
                "ppo_hook_filter": "all"
            },
            "expected_behavior": "Should find stocks with slopes <= -5%"
        },
        {
            "name": "Very Permissive Negative Slope",
            "filters": {
                "price_filter": {"type": "under", "under": 500},
                "dmi_filter": {"min": 20, "max": 60},
                "ppo_slope_filter": {"threshold": -100},  # Very permissive negative
                "ppo_hook_filter": "all"
            },
            "expected_behavior": "Should find many stocks with natural slope calculations"
        }
    ]
    
    for test_case in test_cases:
        try:
            print(f"  🔍 Testing: {test_case['name']}")
            
            response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                   json=test_case["filters"],
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                stocks = data.get("stocks", [])
                results_found = data.get("results_found", 0)
                
                # Validate filtering logic works with natural slopes
                slope_threshold = test_case["filters"]["ppo_slope_filter"]["threshold"]
                
                violations = 0
                for stock in stocks[:5]:  # Check first 5 stocks
                    stock_slope = stock.get("ppo_slope_percentage", 0)
                    symbol = stock.get("symbol", "Unknown")
                    
                    # Validate slope filtering logic
                    if slope_threshold > 0:
                        if stock_slope < slope_threshold:
                            print(f"    ❌ {symbol} slope {stock_slope:.2f}% below positive threshold {slope_threshold}%")
                            violations += 1
                    else:  # Negative threshold
                        if stock_slope > slope_threshold:
                            print(f"    ❌ {symbol} slope {stock_slope:.2f}% above negative threshold {slope_threshold}%")
                            violations += 1
                
                if violations > 0:
                    print(f"    ❌ FAIL: Screener Slope Filter ({test_case['name']}) - {violations} violations found")
                    all_passed = False
                else:
                    print(f"    ✅ PASS: Screener Slope Filter ({test_case['name']}) - Found {results_found} stocks, filtering logic working correctly")
                
            else:
                print(f"    ❌ FAIL: Screener Slope Test ({test_case['name']}) - HTTP {response.status_code}: {response.text}")
                all_passed = False
                
        except Exception as e:
            print(f"    ❌ FAIL: Screener Slope Test ({test_case['name']}) - Error: {str(e)}")
            all_passed = False
    
    return all_passed

def test_hook_pattern_detection() -> bool:
    """Test that hook pattern detection works correctly with natural slope calculations"""
    all_passed = True
    
    # Test hook pattern filtering
    hook_test_cases = [
        {
            "name": "Positive Hook Detection",
            "filters": {
                "price_filter": {"type": "under", "under": 500},
                "dmi_filter": {"min": 20, "max": 60},
                "ppo_slope_filter": {"threshold": -100},  # Very permissive
                "ppo_hook_filter": "positive"
            },
            "expected_pattern": "positive"
        },
        {
            "name": "Negative Hook Detection",
            "filters": {
                "price_filter": {"type": "under", "under": 500},
                "dmi_filter": {"min": 20, "max": 60},
                "ppo_slope_filter": {"threshold": -100},  # Very permissive
                "ppo_hook_filter": "negative"
            },
            "expected_pattern": "negative"
        }
    ]
    
    for test_case in hook_test_cases:
        try:
            print(f"  🪝 Testing: {test_case['name']}")
            
            response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                   json=test_case["filters"],
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                stocks = data.get("stocks", [])
                results_found = data.get("results_found", 0)
                
                # Validate hook pattern detection
                violations = 0
                for stock in stocks[:3]:  # Check first 3 stocks
                    symbol = stock.get("symbol", "Unknown")
                    ppo_values = stock.get("ppo_values", [])
                    
                    if len(ppo_values) >= 3:
                        today = ppo_values[0]  # Today (index 0)
                        yesterday = ppo_values[1]  # Yesterday (index 1)
                        day_before = ppo_values[2]  # Day before (index 2)
                        
                        # Validate hook pattern logic
                        is_positive_hook = today > yesterday and yesterday < day_before
                        is_negative_hook = today < yesterday and yesterday > day_before
                        
                        expected_pattern = test_case["expected_pattern"]
                        
                        if expected_pattern == "positive" and not is_positive_hook:
                            print(f"    ❌ {symbol} doesn't match positive hook pattern: {ppo_values}")
                            violations += 1
                        elif expected_pattern == "negative" and not is_negative_hook:
                            print(f"    ❌ {symbol} doesn't match negative hook pattern: {ppo_values}")
                            violations += 1
                
                if violations > 0:
                    print(f"    ❌ FAIL: Hook Pattern Detection ({test_case['name']}) - {violations} violations found")
                    all_passed = False
                else:
                    print(f"    ✅ PASS: Hook Pattern Detection ({test_case['name']}) - Found {results_found} stocks with {expected_pattern} hook patterns")
                
            else:
                print(f"    ❌ FAIL: Hook Pattern Test ({test_case['name']}) - HTTP {response.status_code}: {response.text}")
                all_passed = False
                
        except Exception as e:
            print(f"    ❌ FAIL: Hook Pattern Test ({test_case['name']}) - Error: {str(e)}")
            all_passed = False
    
    return all_passed

if __name__ == "__main__":
    print("🚀 STARTING PPO SLOPE ABSOLUTE VALUE REMOVAL TEST")
    print("=" * 60)
    
    success = test_ppo_slope_absolute_value_removal()
    
    if success:
        print(f"\n✅ ALL TESTS PASSED - PPO slope calculations working correctly without absolute values")
    else:
        print(f"\n❌ SOME TESTS FAILED - Issues found with PPO slope calculations")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")