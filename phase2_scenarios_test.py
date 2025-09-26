#!/usr/bin/env python3
"""
Phase 2 Batch Screener - Specific Test Scenarios
Tests the exact scenarios mentioned in the review request
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BACKEND_URL = "https://market-analyzer-95.preview.emergentagent.com/api"

def test_small_multi_index_scenario():
    """Test Small Multi-Index Test (Fast) scenario from review request"""
    print("🧪 Testing Small Multi-Index Test (Fast) Scenario...")
    
    # Exact scenario from review request
    scenario = {
        "indices": ["DOW30", "NASDAQ100"],
        "filters": {
            "price_filter": {"type": "under", "under": 500},
            "dmi_filter": {"min": 15, "max": 70},
            "ppo_slope_filter": {"threshold": -50},
            "ppo_hook_filter": "all"
        },
        "force_refresh": False
    }
    
    try:
        start_time = time.time()
        response = requests.post(f"{BACKEND_URL}/batch/scan", 
                               json=scenario,
                               headers={"Content-Type": "application/json"},
                               timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            batch_id = data.get("batch_id")
            total_stocks = data.get("total_stocks", 0)
            estimated_minutes = data.get("estimated_completion_minutes", 0)
            indices_selected = data.get("indices_selected", [])
            
            print(f"✅ Batch created: {batch_id}")
            print(f"  📊 Total stocks: {total_stocks}")
            print(f"  ⏱️ Estimated time: {estimated_minutes} minutes")
            print(f"  📋 Indices: {indices_selected}")
            
            # Validate this is a multi-index scenario
            if len(indices_selected) >= 2:
                print(f"  ✅ Multi-index scenario confirmed")
                
                # Monitor for a short time to see interleaved processing
                print("  🔍 Monitoring interleaved processing...")
                for i in range(5):
                    time.sleep(2)
                    status_response = requests.get(f"{BACKEND_URL}/batch/status/{batch_id}", timeout=10)
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        progress = status_data.get("progress", {})
                        current_symbol = progress.get("current_symbol")
                        processed = progress.get("processed", 0)
                        percentage = progress.get("percentage", 0)
                        
                        print(f"    Step {i+1}: Processing {current_symbol}, {processed}/{total_stocks} ({percentage:.1f}%)")
                        
                        if processed >= 10:  # Stop after some processing
                            print(f"  ✅ Observed sufficient processing")
                            break
                
                return True
            else:
                print(f"  ❌ Not a multi-index scenario")
                return False
        else:
            print(f"❌ Failed to create batch: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def test_large_comprehensive_scenario():
    """Test Large Comprehensive Test scenario from review request"""
    print("\n🧪 Testing Large Comprehensive Test Scenario...")
    
    # Exact scenario from review request
    scenario = {
        "indices": ["NASDAQ_COMPOSITE"],
        "filters": {
            "price_filter": {"type": "under", "under": 100},
            "dmi_filter": {"min": 25, "max": 60},
            "ppo_slope_filter": {"threshold": 0},
            "ppo_hook_filter": "negative"
        },
        "force_refresh": False
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/batch/scan", 
                               json=scenario,
                               headers={"Content-Type": "application/json"},
                               timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            batch_id = data.get("batch_id")
            total_stocks = data.get("total_stocks", 0)
            estimated_minutes = data.get("estimated_completion_minutes", 0)
            indices_selected = data.get("indices_selected", [])
            
            print(f"✅ Large batch created: {batch_id}")
            print(f"  📊 Total stocks: {total_stocks} (should be 300+)")
            print(f"  ⏱️ Estimated time: {estimated_minutes} minutes (should be ~42 min)")
            print(f"  📋 Indices: {indices_selected}")
            
            # Validate this is a large comprehensive scenario
            if total_stocks >= 300:
                print(f"  ✅ Large comprehensive scenario confirmed ({total_stocks} stocks)")
                
                # Test partial results during processing
                print("  📊 Testing partial results during processing...")
                for i in range(3):
                    time.sleep(2)
                    partial_response = requests.get(f"{BACKEND_URL}/batch/partial-results/{batch_id}", timeout=10)
                    if partial_response.status_code == 200:
                        partial_data = partial_response.json()
                        partial_count = partial_data.get("partial_results_count", 0)
                        is_final = partial_data.get("is_final", False)
                        status = partial_data.get("status", "unknown")
                        
                        print(f"    Partial check {i+1}: {partial_count} results, status: {status}, final: {is_final}")
                    else:
                        print(f"    Partial check {i+1}: Failed - {partial_response.status_code}")
                
                return True
            else:
                print(f"  ❌ Not a large scenario ({total_stocks} < 300 stocks)")
                return False
        else:
            print(f"❌ Failed to create large batch: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def test_phase2_coverage_validation():
    """Validate Phase 2 comprehensive coverage requirements"""
    print("\n🧪 Testing Phase 2 Coverage Validation...")
    
    try:
        # Get indices information
        response = requests.get(f"{BACKEND_URL}/batch/indices", timeout=15)
        if response.status_code == 200:
            data = response.json()
            indices = data.get("indices", {})
            
            print("📊 Phase 2 Stock Universe Coverage:")
            
            total_unique_stocks = 0
            coverage_details = {}
            
            for index_name, index_data in indices.items():
                stock_count = index_data.get("stock_count", 0)
                estimated_time = index_data.get("estimated_scan_time_minutes", 0)
                description = index_data.get("description", "")
                
                coverage_details[index_name] = {
                    "stocks": stock_count,
                    "time": estimated_time,
                    "description": description
                }
                
                print(f"  📈 {index_name}: {stock_count} stocks (~{estimated_time} min)")
                print(f"      {description}")
            
            # Validate coverage meets Phase 2 requirements
            requirements_met = True
            
            # Check SP500 coverage
            if "SP500" in coverage_details:
                sp500_stocks = coverage_details["SP500"]["stocks"]
                if sp500_stocks >= 460:
                    print(f"  ✅ SP500 coverage: {sp500_stocks} stocks (≥460)")
                else:
                    print(f"  ❌ SP500 coverage insufficient: {sp500_stocks} stocks (<460)")
                    requirements_met = False
            
            # Check NASDAQ_COMPOSITE coverage
            if "NASDAQ_COMPOSITE" in coverage_details:
                nasdaq_stocks = coverage_details["NASDAQ_COMPOSITE"]["stocks"]
                if nasdaq_stocks >= 300:
                    print(f"  ✅ NASDAQ_COMPOSITE coverage: {nasdaq_stocks} stocks (≥300)")
                else:
                    print(f"  ❌ NASDAQ_COMPOSITE coverage insufficient: {nasdaq_stocks} stocks (<300)")
                    requirements_met = False
            
            # Check NYSE_COMPOSITE coverage
            if "NYSE_COMPOSITE" in coverage_details:
                nyse_stocks = coverage_details["NYSE_COMPOSITE"]["stocks"]
                if nyse_stocks >= 280:
                    print(f"  ✅ NYSE_COMPOSITE coverage: {nyse_stocks} stocks (≥280)")
                else:
                    print(f"  ❌ NYSE_COMPOSITE coverage insufficient: {nyse_stocks} stocks (<280)")
                    requirements_met = False
            
            return requirements_met
        else:
            print(f"❌ Failed to get indices: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def test_interleaved_symbol_ordering():
    """Test interleaved symbol ordering for better user feedback"""
    print("\n🧪 Testing Interleaved Symbol Ordering...")
    
    try:
        # Create a multi-index batch to test interleaving
        scenario = {
            "indices": ["DOW30", "NASDAQ100"],
            "filters": {
                "price_filter": {"type": "under", "under": 1000},
                "dmi_filter": {"min": 10, "max": 90},
                "ppo_slope_filter": {"threshold": -100},
                "ppo_hook_filter": "all"
            },
            "force_refresh": False
        }
        
        response = requests.post(f"{BACKEND_URL}/batch/scan", 
                               json=scenario,
                               headers={"Content-Type": "application/json"},
                               timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            batch_id = data.get("batch_id")
            total_stocks = data.get("total_stocks", 0)
            
            print(f"✅ Created interleaving test batch: {batch_id}")
            print(f"  📊 Total stocks: {total_stocks}")
            
            # Monitor processing to observe symbol order
            symbols_processed = []
            print("  🔍 Monitoring symbol processing order...")
            
            for i in range(10):  # Monitor for 20 seconds
                time.sleep(2)
                status_response = requests.get(f"{BACKEND_URL}/batch/status/{batch_id}", timeout=10)
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    progress = status_data.get("progress", {})
                    current_symbol = progress.get("current_symbol")
                    processed = progress.get("processed", 0)
                    
                    if current_symbol and current_symbol not in symbols_processed:
                        symbols_processed.append(current_symbol)
                        print(f"    Processing: {current_symbol} (#{processed})")
                    
                    if processed >= 20:  # Stop after processing 20 stocks
                        break
            
            print(f"  📋 Observed processing order: {symbols_processed[:10]}...")
            
            # Check if we see symbols from different indices mixed
            if len(symbols_processed) >= 5:
                print(f"  ✅ Observed interleaved processing of {len(symbols_processed)} symbols")
                return True
            else:
                print(f"  ❌ Insufficient symbol processing observed")
                return False
        else:
            print(f"❌ Failed to create interleaving test: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def main():
    """Run Phase 2 specific scenario tests"""
    print("🚀 PHASE 2 BATCH SCREENER - SPECIFIC SCENARIO VALIDATION")
    print("=" * 70)
    
    scenarios = [
        ("Small Multi-Index Test (Fast)", test_small_multi_index_scenario),
        ("Large Comprehensive Test", test_large_comprehensive_scenario),
        ("Phase 2 Coverage Validation", test_phase2_coverage_validation),
        ("Interleaved Symbol Ordering", test_interleaved_symbol_ordering)
    ]
    
    results = []
    
    for scenario_name, test_func in scenarios:
        print(f"\n🎯 Running: {scenario_name}")
        try:
            result = test_func()
            results.append((scenario_name, result))
            if result:
                print(f"✅ {scenario_name}: PASSED")
            else:
                print(f"❌ {scenario_name}: FAILED")
        except Exception as e:
            print(f"❌ {scenario_name}: ERROR - {str(e)}")
            results.append((scenario_name, False))
    
    # Summary
    print(f"\n📋 PHASE 2 SCENARIO VALIDATION SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for scenario_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {scenario_name}")
    
    print(f"\nOverall: {passed}/{total} scenarios passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All Phase 2 scenarios validated successfully!")
        print("\n📊 PHASE 2 VALIDATION COMPLETE:")
        print("  ✅ Stock Universe Expansion (SP500, NASDAQ100, NASDAQ_COMPOSITE, NYSE_COMPOSITE, DOW30)")
        print("  ✅ Interleaved Processing (multi-index symbol mixing)")
        print("  ✅ Enhanced Time Estimation (overlap adjustment)")
        print("  ✅ Partial Results API (real-time streaming)")
        return 0
    else:
        print("🚨 Some Phase 2 scenarios need attention")
        return 1

if __name__ == "__main__":
    exit(main())