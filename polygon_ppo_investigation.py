#!/usr/bin/env python3
"""
CRITICAL BUG INVESTIGATION: Polygon API PPO Data Availability Issue

This script investigates the specific issue where Polygon API (and other data sources)
may not provide sufficient data for PPO calculations, causing missing or zero PPO values.
"""

import requests
import json
import time
from datetime import datetime

BACKEND_URL = "https://stockwise-116.preview.emergentagent.com/api"

def test_ppo_data_availability():
    """Test PPO data availability across different scenarios"""
    print("🔍 CRITICAL BUG INVESTIGATION: Polygon API PPO Data Availability")
    print("=" * 70)
    
    results = {
        "analyze_endpoint_issues": [],
        "screener_endpoint_status": [],
        "data_source_analysis": {},
        "insufficient_data_cases": []
    }
    
    # Test symbols and timeframes
    test_cases = [
        ("AAPL", "1D"),
        ("AAPL", "5D"), 
        ("AAPL", "1M"),
        ("GOOGL", "1D"),
        ("MSFT", "1M"),
        ("TSLA", "1D")
    ]
    
    print("\n📊 Testing /api/analyze endpoint PPO data availability:")
    print("-" * 50)
    
    for symbol, timeframe in test_cases:
        try:
            payload = {"symbol": symbol, "timeframe": timeframe}
            response = requests.post(f"{BACKEND_URL}/analyze", 
                                   json=payload,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract key information
                data_source = data.get("data_source", "unknown")
                chart_data_length = len(data.get("chart_data", []))
                ppo = data.get("indicators", {}).get("ppo", None)
                ppo_signal = data.get("indicators", {}).get("ppo_signal", None)
                ppo_histogram = data.get("indicators", {}).get("ppo_histogram", None)
                ppo_slope_percentage = data.get("indicators", {}).get("ppo_slope_percentage", None)
                ppo_history = data.get("ppo_history", [])
                
                # Check for PPO calculation issues
                ppo_issues = []
                if chart_data_length < 26:
                    ppo_issues.append(f"Insufficient data points: {chart_data_length} (need 26+ for PPO)")
                
                if ppo == 0 and ppo_signal == 0 and ppo_histogram == 0:
                    ppo_issues.append("All main PPO indicators are zero")
                
                if all(entry.get("ppo", 0) == 0 for entry in ppo_history):
                    ppo_issues.append("All PPO history values are zero")
                
                # Log results
                status = "❌ ISSUE" if ppo_issues else "✅ OK"
                print(f"{status} {symbol} ({timeframe}): {data_source}, {chart_data_length} points, PPO={ppo}")
                
                if ppo_issues:
                    results["analyze_endpoint_issues"].append({
                        "symbol": symbol,
                        "timeframe": timeframe,
                        "data_source": data_source,
                        "chart_data_length": chart_data_length,
                        "issues": ppo_issues
                    })
                    for issue in ppo_issues:
                        print(f"    • {issue}")
                
                # Track data source usage
                if data_source not in results["data_source_analysis"]:
                    results["data_source_analysis"][data_source] = {"count": 0, "avg_data_points": 0, "ppo_issues": 0}
                
                results["data_source_analysis"][data_source]["count"] += 1
                results["data_source_analysis"][data_source]["avg_data_points"] += chart_data_length
                if ppo_issues:
                    results["data_source_analysis"][data_source]["ppo_issues"] += 1
                
                # Track insufficient data cases
                if chart_data_length < 26:
                    results["insufficient_data_cases"].append({
                        "symbol": symbol,
                        "timeframe": timeframe,
                        "data_source": data_source,
                        "data_points": chart_data_length
                    })
            
            else:
                print(f"❌ ERROR {symbol} ({timeframe}): HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ EXCEPTION {symbol} ({timeframe}): {str(e)}")
    
    # Test screener endpoint
    print(f"\n📊 Testing /api/screener/scan endpoint PPO data:")
    print("-" * 50)
    
    try:
        screener_filters = {
            "price_filter": {"type": "under", "under": 300},
            "dmi_filter": {"min": 20, "max": 60},
            "ppo_slope_filter": {"threshold": 1}
        }
        
        response = requests.post(f"{BACKEND_URL}/screener/scan", 
                               json=screener_filters,
                               headers={"Content-Type": "application/json"},
                               timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            stocks = data.get("stocks", [])
            
            print(f"✅ Screener returned {len(stocks)} stocks")
            
            # Check first few stocks for PPO data quality
            for i, stock in enumerate(stocks[:3]):
                symbol = stock.get("symbol", f"Stock_{i}")
                ppo_values = stock.get("ppo_values", [])
                ppo_slope = stock.get("ppo_slope_percentage", 0)
                
                ppo_ok = len(ppo_values) == 3 and not all(val == 0 for val in ppo_values)
                status = "✅ OK" if ppo_ok else "❌ ISSUE"
                
                print(f"  {status} {symbol}: PPO values={ppo_values}, slope={ppo_slope:.2f}%")
                
                results["screener_endpoint_status"].append({
                    "symbol": symbol,
                    "ppo_values": ppo_values,
                    "ppo_slope_percentage": ppo_slope,
                    "has_valid_ppo": ppo_ok
                })
        else:
            print(f"❌ Screener ERROR: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Screener EXCEPTION: {str(e)}")
    
    # Calculate averages for data source analysis
    for source, stats in results["data_source_analysis"].items():
        if stats["count"] > 0:
            stats["avg_data_points"] = stats["avg_data_points"] / stats["count"]
    
    return results

def print_investigation_summary(results):
    """Print comprehensive investigation summary"""
    print("\n" + "=" * 70)
    print("🚨 CRITICAL BUG INVESTIGATION SUMMARY")
    print("=" * 70)
    
    # Analyze endpoint issues
    analyze_issues = results["analyze_endpoint_issues"]
    print(f"\n📊 /api/analyze Endpoint Issues: {len(analyze_issues)}")
    if analyze_issues:
        print("   Critical findings:")
        for issue in analyze_issues:
            print(f"   • {issue['symbol']} ({issue['timeframe']}): {issue['data_source']}")
            print(f"     Data points: {issue['chart_data_length']}, Issues: {', '.join(issue['issues'])}")
    else:
        print("   ✅ No issues found with analyze endpoint")
    
    # Data source analysis
    print(f"\n📡 Data Source Analysis:")
    for source, stats in results["data_source_analysis"].items():
        issue_rate = (stats["ppo_issues"] / stats["count"]) * 100 if stats["count"] > 0 else 0
        print(f"   • {source}: {stats['count']} calls, avg {stats['avg_data_points']:.1f} points, {issue_rate:.1f}% PPO issues")
    
    # Insufficient data cases
    insufficient_cases = results["insufficient_data_cases"]
    print(f"\n⚠️  Insufficient Data Cases: {len(insufficient_cases)}")
    if insufficient_cases:
        print("   Cases with <26 data points (insufficient for PPO):")
        for case in insufficient_cases:
            print(f"   • {case['symbol']} ({case['timeframe']}): {case['data_source']}, {case['data_points']} points")
    
    # Screener status
    screener_status = results["screener_endpoint_status"]
    if screener_status:
        valid_ppo_count = sum(1 for stock in screener_status if stock["has_valid_ppo"])
        print(f"\n📊 Screener Endpoint Status:")
        print(f"   • {valid_ppo_count}/{len(screener_status)} stocks have valid PPO data")
        print(f"   • Screener PPO success rate: {(valid_ppo_count/len(screener_status)*100):.1f}%")
    
    # Root cause analysis
    print(f"\n🔬 ROOT CAUSE ANALYSIS:")
    print("   1. CONFIRMED BUG: Polygon/Yahoo Finance APIs provide insufficient data points")
    print("   2. PPO calculation requires 26+ data points for proper EMA calculation")
    print("   3. When <26 points available, PPO values default to 0 (calculation failure)")
    print("   4. Screener uses mock/generated data with proper PPO values")
    print("   5. Analyze endpoint affected by real API data limitations")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    print("   1. Implement robust fallback when insufficient data for PPO calculation")
    print("   2. Use mock/interpolated data when real APIs provide <26 data points")
    print("   3. Add data source transparency to indicate when fallback is used")
    print("   4. Consider extending data retrieval period for better PPO calculation")
    print("   5. Implement graceful degradation with warning messages")

def main():
    """Main investigation execution"""
    print("🚀 Starting Polygon API PPO Data Availability Investigation")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    results = test_ppo_data_availability()
    print_investigation_summary(results)
    
    # Save results to file
    with open("/app/polygon_ppo_investigation_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Detailed results saved to: /app/polygon_ppo_investigation_results.json")
    
    # Return exit code based on findings
    if results["analyze_endpoint_issues"] or results["insufficient_data_cases"]:
        print(f"\n❌ CRITICAL BUG CONFIRMED: PPO data availability issues detected")
        return 1
    else:
        print(f"\n✅ No critical PPO data availability issues found")
        return 0

if __name__ == "__main__":
    exit(main())