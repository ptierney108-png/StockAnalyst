#!/usr/bin/env python3
"""
Focused DMI+ Value Variation Test
Tests the exact scenario reported by the user: "DMI component values for DMI+ do not change when another stock is entered"
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BACKEND_URL = "https://market-analyzer-95.preview.emergentagent.com/api"

def test_dmi_value_variation():
    """Test DMI+ value variation between different stocks"""
    print("🎯 CRITICAL DMI+ VALUE VARIATION FIX TESTING")
    print("=" * 70)
    print("Testing the exact user scenario: 'DMI component values for DMI+ do not change when another stock is entered'")
    print()
    
    # Test the exact symbols mentioned in the review request
    test_symbols = ["AAPL", "GOOGL", "MSFT"]
    dmi_plus_values = {}
    
    print("📊 Stock Entry Sequence Test (as specified in review request)")
    print("-" * 50)
    
    # Test each stock and record DMI+ values
    for i, symbol in enumerate(test_symbols, 1):
        try:
            payload = {"symbol": symbol, "timeframe": "3M"}  # Using 3M as specified
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
                
                # Record DMI+ value for comparison
                dmi_plus_values[symbol] = dmi_plus
                
                print(f"  {i}. {symbol}: DMI+ = {dmi_plus}, DMI- = {dmi_minus}, ADX = {adx}")
                print(f"     Source: {data_source}, Response time: {response_time:.2f}s")
                
                # Validate DMI+ value is reasonable
                if dmi_plus is None:
                    print(f"     ❌ ERROR: DMI+ value is null")
                elif not (0 <= dmi_plus <= 100):
                    print(f"     ❌ ERROR: DMI+ value {dmi_plus} outside valid range (0-100)")
                else:
                    print(f"     ✅ DMI+ value is valid")
                
            else:
                print(f"  {i}. {symbol}: ❌ API ERROR - HTTP {response.status_code}")
                print(f"     Response: {response.text}")
                
        except Exception as e:
            print(f"  {i}. {symbol}: ❌ EXCEPTION - {str(e)}")
    
    print()
    print("🔍 Comparison Analysis (Critical Success Criteria)")
    print("-" * 50)
    
    if len(dmi_plus_values) >= 2:
        # Check if all values are different (the core fix requirement)
        unique_values = set(dmi_plus_values.values())
        
        print("DMI+ Values Retrieved:")
        for symbol, value in dmi_plus_values.items():
            print(f"  • {symbol}: {value}")
        
        print(f"\nUnique DMI+ values: {len(unique_values)} out of {len(dmi_plus_values)} stocks")
        
        # CRITICAL TEST: All stocks should have DIFFERENT DMI+ values
        if len(unique_values) == len(dmi_plus_values):
            print(f"✅ SUCCESS: All {len(dmi_plus_values)} stocks have DIFFERENT DMI+ values")
            print("✅ DMI+ value variation bug has been FIXED!")
        else:
            print(f"❌ FAILURE: Only {len(unique_values)} unique values out of {len(dmi_plus_values)} stocks")
            print("❌ DMI+ values are still NOT varying between stocks")
        
        # Check for the specific bug: all stocks returning 22.00
        if 22.00 in dmi_plus_values.values():
            count_22 = sum(1 for v in dmi_plus_values.values() if v == 22.00)
            if count_22 == len(dmi_plus_values):
                print(f"❌ CRITICAL: All stocks still returning DMI+ = 22.00 (original bug persists)")
            elif count_22 > 1:
                print(f"⚠️ WARNING: {count_22} stocks still returning DMI+ = 22.00")
            else:
                print(f"✅ Only one stock returning 22.00 - acceptable variation")
        else:
            print(f"✅ No 22.00 values found - static value bug eliminated")
    else:
        print("❌ FAILURE: Could not retrieve enough DMI+ values for comparison")
    
    print()
    print("=" * 70)
    print("🎯 DMI+ VALUE VARIATION TEST COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    test_dmi_value_variation()