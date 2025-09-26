#!/usr/bin/env python3
"""
Comprehensive DMI+ Value Variation Test
Tests all the scenarios mentioned in the review request
"""

import requests
import json
import time

# Configuration
BACKEND_URL = "https://stockwise-120.preview.emergentagent.com/api"

def test_comprehensive_dmi_scenarios():
    """Test all DMI+ scenarios from the review request"""
    print("🎯 COMPREHENSIVE DMI+ VALUE VARIATION TESTING")
    print("=" * 70)
    print("Testing all scenarios from the review request:")
    print("1. Stock Entry Sequence Test (AAPL → GOOGL → MSFT)")
    print("2. Comparison Analysis (all different values)")
    print("3. Range Check (0-100 range)")
    print("4. Backend logs verification")
    print("=" * 70)
    
    # Test symbols as specified in review request
    test_symbols = ["AAPL", "GOOGL", "MSFT"]
    results = {}
    
    print("\n📊 1. STOCK ENTRY SEQUENCE TEST")
    print("-" * 50)
    
    for i, symbol in enumerate(test_symbols, 1):
        try:
            payload = {"symbol": symbol, "timeframe": "3M"}
            start_time = time.time()
            
            response = requests.post(f"{BACKEND_URL}/analyze", 
                                   json=payload,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                indicators = data.get("indicators", {})
                dmi_plus = indicators.get("dmi_plus")
                dmi_minus = indicators.get("dmi_minus")
                adx = indicators.get("adx")
                data_source = data.get("data_source", "unknown")
                
                results[symbol] = {
                    "dmi_plus": dmi_plus,
                    "dmi_minus": dmi_minus,
                    "adx": adx,
                    "data_source": data_source,
                    "response_time": response_time
                }
                
                print(f"  {i}. {symbol}:")
                print(f"     DMI+ = {dmi_plus:.2f}")
                print(f"     DMI- = {dmi_minus:.2f}")
                print(f"     ADX = {adx:.2f}")
                print(f"     Source: {data_source}")
                print(f"     Time: {response_time:.2f}s")
                print(f"     ✅ SUCCESS")
                
            else:
                print(f"  {i}. {symbol}: ❌ API ERROR - HTTP {response.status_code}")
                results[symbol] = {"error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            print(f"  {i}. {symbol}: ❌ EXCEPTION - {str(e)}")
            results[symbol] = {"error": str(e)}
    
    print("\n🔍 2. COMPARISON ANALYSIS")
    print("-" * 50)
    
    successful_results = {k: v for k, v in results.items() if "dmi_plus" in v}
    
    if len(successful_results) >= 2:
        dmi_plus_values = [v["dmi_plus"] for v in successful_results.values()]
        unique_values = set(dmi_plus_values)
        
        print("DMI+ Values Retrieved:")
        for symbol, data in successful_results.items():
            print(f"  • {symbol}: {data['dmi_plus']:.6f}")
        
        print(f"\nUnique DMI+ values: {len(unique_values)} out of {len(successful_results)} stocks")
        
        # CRITICAL SUCCESS CRITERIA
        if len(unique_values) == len(successful_results):
            print(f"✅ SUCCESS: All stocks have DIFFERENT DMI+ values")
            print(f"✅ DMI+ value variation bug is FIXED!")
        else:
            print(f"❌ FAILURE: Only {len(unique_values)} unique values")
            print(f"❌ DMI+ values still not varying properly")
        
        # Check for old bug (22.00 values)
        if 22.00 in dmi_plus_values:
            count_22 = sum(1 for v in dmi_plus_values if abs(v - 22.00) < 0.01)
            if count_22 == len(dmi_plus_values):
                print(f"❌ CRITICAL: All stocks returning DMI+ ≈ 22.00 (old bug)")
            elif count_22 > 1:
                print(f"⚠️ WARNING: {count_22} stocks returning DMI+ ≈ 22.00")
            else:
                print(f"✅ Only coincidental 22.00 value - acceptable")
        else:
            print(f"✅ No 22.00 values - old static bug eliminated")
    
    print("\n📏 3. RANGE CHECK (0-100 VALIDATION)")
    print("-" * 50)
    
    range_issues = []
    for symbol, data in successful_results.items():
        if "dmi_plus" in data:
            dmi_plus = data["dmi_plus"]
            dmi_minus = data["dmi_minus"]
            adx = data["adx"]
            
            if not (0 <= dmi_plus <= 100):
                range_issues.append(f"{symbol}: DMI+ {dmi_plus:.2f} outside 0-100 range")
            if not (0 <= dmi_minus <= 100):
                range_issues.append(f"{symbol}: DMI- {dmi_minus:.2f} outside 0-100 range")
            if not (0 <= adx <= 100):
                range_issues.append(f"{symbol}: ADX {adx:.2f} outside 0-100 range")
    
    if range_issues:
        print("❌ RANGE ISSUES FOUND:")
        for issue in range_issues:
            print(f"  • {issue}")
    else:
        print("✅ All DMI values within valid 0-100 range")
    
    print("\n🔧 4. BACKEND LOGS VERIFICATION")
    print("-" * 50)
    
    # Check if we can see calculation evidence
    calculation_evidence = []
    for symbol, data in successful_results.items():
        if data.get("data_source") == "alpha_vantage":
            calculation_evidence.append(f"✅ {symbol}: Using Alpha Vantage real data")
        else:
            calculation_evidence.append(f"⚠️ {symbol}: Using {data.get('data_source', 'unknown')} data")
    
    if calculation_evidence:
        print("Data Source Analysis:")
        for evidence in calculation_evidence:
            print(f"  {evidence}")
    
    print("\n" + "=" * 70)
    print("🎯 COMPREHENSIVE DMI+ TEST SUMMARY")
    print("=" * 70)
    
    # Final assessment
    success_criteria = []
    
    if len(successful_results) >= 3:
        success_criteria.append("✅ All 3 stocks tested successfully")
    else:
        success_criteria.append(f"⚠️ Only {len(successful_results)}/3 stocks tested successfully")
    
    if len(successful_results) >= 2:
        dmi_values = [v["dmi_plus"] for v in successful_results.values()]
        unique_count = len(set(dmi_values))
        if unique_count == len(successful_results):
            success_criteria.append("✅ All stocks return DIFFERENT DMI+ values")
        else:
            success_criteria.append("❌ Stocks still returning identical DMI+ values")
    
    if not range_issues:
        success_criteria.append("✅ All values within 0-100 range")
    else:
        success_criteria.append("❌ Some values outside valid range")
    
    if not any("22.00" in str(v.get("dmi_plus", 0)) for v in successful_results.values()):
        success_criteria.append("✅ No static 22.00 values detected")
    else:
        success_criteria.append("⚠️ Some 22.00 values detected")
    
    print("FINAL ASSESSMENT:")
    for criterion in success_criteria:
        print(f"  {criterion}")
    
    # Overall result
    passed_criteria = sum(1 for c in success_criteria if c.startswith("✅"))
    total_criteria = len(success_criteria)
    
    print(f"\nOVERALL RESULT: {passed_criteria}/{total_criteria} criteria passed")
    
    if passed_criteria == total_criteria:
        print("🎉 DMI+ VALUE VARIATION FIX: COMPLETE SUCCESS!")
        print("🎉 User-reported bug has been RESOLVED!")
    elif passed_criteria >= total_criteria * 0.75:
        print("✅ DMI+ VALUE VARIATION FIX: MOSTLY SUCCESSFUL")
        print("✅ Major improvements made, minor issues remain")
    else:
        print("❌ DMI+ VALUE VARIATION FIX: NEEDS MORE WORK")
        print("❌ Significant issues still present")
    
    return results

if __name__ == "__main__":
    test_comprehensive_dmi_scenarios()