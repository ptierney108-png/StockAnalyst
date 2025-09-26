#!/usr/bin/env python3
"""
Debug DMI+ Calculation Issue
Detailed analysis of why DMI+ values are not varying between stocks
"""

import requests
import json
import time

# Configuration
BACKEND_URL = "https://stockwise-120.preview.emergentagent.com/api"

def debug_dmi_calculation():
    """Debug DMI calculation to understand why values are not varying"""
    print("🔍 DEBUG: DMI+ CALCULATION ANALYSIS")
    print("=" * 70)
    
    # Test the exact symbols mentioned in the review request
    test_symbols = ["AAPL", "GOOGL", "MSFT"]
    
    for symbol in test_symbols:
        print(f"\n📊 Analyzing {symbol}")
        print("-" * 40)
        
        try:
            payload = {"symbol": symbol, "timeframe": "3M"}
            response = requests.post(f"{BACKEND_URL}/analyze", 
                                   json=payload,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # Analyze chart data
                chart_data = data.get("chart_data", [])
                print(f"Chart data points: {len(chart_data)}")
                
                if chart_data:
                    # Show first few data points
                    print("First 3 data points:")
                    for i, point in enumerate(chart_data[:3]):
                        print(f"  {i+1}. Date: {point.get('date')}, High: {point.get('high')}, Low: {point.get('low')}, Close: {point.get('close')}")
                    
                    # Show last few data points
                    print("Last 3 data points:")
                    for i, point in enumerate(chart_data[-3:]):
                        print(f"  {i+1}. Date: {point.get('date')}, High: {point.get('high')}, Low: {point.get('low')}, Close: {point.get('close')}")
                
                # Analyze indicators
                indicators = data.get("indicators", {})
                print(f"\nIndicators:")
                print(f"  DMI+: {indicators.get('dmi_plus')}")
                print(f"  DMI-: {indicators.get('dmi_minus')}")
                print(f"  ADX: {indicators.get('adx')}")
                
                # Analyze DMI history
                dmi_history = data.get("dmi_history", [])
                print(f"\nDMI History ({len(dmi_history)} entries):")
                for i, entry in enumerate(dmi_history):
                    print(f"  {i+1}. Date: {entry.get('date')}, DMI+: {entry.get('dmi_plus')}, DMI-: {entry.get('dmi_minus')}, ADX: {entry.get('adx')}")
                
                # Check data source
                data_source = data.get("data_source", "unknown")
                print(f"\nData source: {data_source}")
                
                # Check if we have enough data for DMI calculation (need 15+ points)
                if len(chart_data) >= 15:
                    print(f"✅ Sufficient data for DMI calculation ({len(chart_data)} >= 15)")
                    
                    # Manual DMI calculation check
                    print("\n🔧 Manual DMI calculation check:")
                    highs = [float(point["high"]) for point in chart_data[-15:]]
                    lows = [float(point["low"]) for point in chart_data[-15:]]
                    closes = [float(point["close"]) for point in chart_data[-15:]]
                    
                    print(f"  Using last 15 data points for calculation")
                    print(f"  High range: {min(highs):.2f} - {max(highs):.2f}")
                    print(f"  Low range: {min(lows):.2f} - {max(lows):.2f}")
                    print(f"  Close range: {min(closes):.2f} - {max(closes):.2f}")
                    
                    # Check if prices are varying (not static)
                    high_variation = max(highs) - min(highs)
                    low_variation = max(lows) - min(lows)
                    close_variation = max(closes) - min(closes)
                    
                    print(f"  Price variations:")
                    print(f"    High variation: {high_variation:.2f}")
                    print(f"    Low variation: {low_variation:.2f}")
                    print(f"    Close variation: {close_variation:.2f}")
                    
                    if high_variation > 0 and low_variation > 0 and close_variation > 0:
                        print(f"  ✅ Prices are varying - DMI should calculate properly")
                    else:
                        print(f"  ❌ Prices are static - DMI calculation will return zeros")
                        
                else:
                    print(f"❌ Insufficient data for DMI calculation ({len(chart_data)} < 15)")
                    print(f"   This explains why DMI+ = 0.0")
                
            else:
                print(f"❌ API ERROR - HTTP {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ EXCEPTION - {str(e)}")
    
    print("\n" + "=" * 70)
    print("🎯 DEBUG ANALYSIS COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    debug_dmi_calculation()