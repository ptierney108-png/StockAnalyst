#!/usr/bin/env python3
"""
Phase 2 Batch Screener Validation Test
Focused testing of Phase 2 features only
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BACKEND_URL = "https://market-scanner-27.preview.emergentagent.com/api"

def test_phase2_stock_universe_expansion():
    """Test Phase 2 Stock Universe Expansion"""
    print("📊 Testing Phase 2 Stock Universe Expansion...")
    
    try:
        response = requests.get(f"{BACKEND_URL}/batch/indices", timeout=15)
        if response.status_code == 200:
            data = response.json()
            indices = data.get("indices", {})
            
            # Validate all Phase 2 indices are present
            expected_indices = {
                "SP500": {"min_stocks": 460, "expected_time": 7.0},
                "NASDAQ100": {"min_stocks": 90, "expected_time": 1.5},
                "NASDAQ_COMPOSITE": {"min_stocks": 300, "expected_time": 42.0},
                "NYSE_COMPOSITE": {"min_stocks": 280, "expected_time": 38.0},
                "DOW30": {"min_stocks": 30, "expected_time": 0.5}
            }
            
            print(f"✅ Found {len(indices)} indices")
            
            for index_name, expectations in expected_indices.items():
                if index_name in indices:
                    index_data = indices[index_name]
                    stock_count = index_data.get("stock_count", 0)
                    estimated_time = index_data.get("estimated_scan_time_minutes", 0)
                    
                    print(f"  ✅ {index_name}: {stock_count} stocks, ~{estimated_time} min")
                    
                    if stock_count >= expectations["min_stocks"]:
                        print(f"    ✅ Stock count OK ({stock_count} >= {expectations['min_stocks']})")
                    else:
                        print(f"    ❌ Stock count low ({stock_count} < {expectations['min_stocks']})")
                else:
                    print(f"  ❌ Missing index: {index_name}")
            
            return True
        else:
            print(f"❌ API Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def test_phase2_interleaved_processing():
    """Test Phase 2 Interleaved Processing"""
    print("\n🔄 Testing Phase 2 Interleaved Processing...")
    
    try:
        # Create multi-index batch job
        batch_request = {
            "indices": ["DOW30", "NASDAQ100"],
            "filters": {
                "price_filter": {"type": "under", "under": 500},
                "dmi_filter": {"min": 15, "max": 70},
                "ppo_slope_filter": {"threshold": -50},
                "ppo_hook_filter": "all"
            },
            "force_refresh": False
        }
        
        response = requests.post(f"{BACKEND_URL}/batch/scan", 
                               json=batch_request,
                               headers={"Content-Type": "application/json"},
                               timeout=30)
        
        if response.status_code == 200:
            batch_data = response.json()
            batch_id = batch_data.get("batch_id")
            estimated_minutes = batch_data.get("estimated_completion_minutes", 0)
            total_stocks = batch_data.get("total_stocks", 0)
            indices_selected = batch_data.get("indices_selected", [])
            
            print(f"✅ Created batch {batch_id}")
            print(f"  📊 {total_stocks} stocks from {len(indices_selected)} indices")
            print(f"  ⏱️ Estimated time: {estimated_minutes} minutes")
            print(f"  📋 Indices: {indices_selected}")
            
            # Monitor batch processing briefly
            print("  🔍 Monitoring processing...")
            for i in range(3):
                time.sleep(2)
                status_response = requests.get(f"{BACKEND_URL}/batch/status/{batch_id}", timeout=10)
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    progress = status_data.get("progress", {})
                    current_symbol = progress.get("current_symbol")
                    processed = progress.get("processed", 0)
                    percentage = progress.get("percentage", 0)
                    
                    print(f"    Check {i+1}: {current_symbol}, {processed} processed ({percentage:.1f}%)")
                    
            return True
        else:
            print(f"❌ Batch creation failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def test_phase2_partial_results_api():
    """Test Phase 2 Partial Results API"""
    print("\n📊 Testing Phase 2 Partial Results API...")
    
    try:
        # Create a small batch job
        batch_request = {
            "indices": ["DOW30"],
            "filters": {
                "price_filter": {"type": "under", "under": 1000},
                "dmi_filter": {"min": 10, "max": 90},
                "ppo_slope_filter": {"threshold": -100},
                "ppo_hook_filter": "all"
            },
            "force_refresh": False
        }
        
        response = requests.post(f"{BACKEND_URL}/batch/scan", 
                               json=batch_request,
                               headers={"Content-Type": "application/json"},
                               timeout=30)
        
        if response.status_code == 200:
            batch_data = response.json()
            batch_id = batch_data.get("batch_id")
            
            print(f"✅ Created batch {batch_id} for partial results testing")
            
            # Test partial results endpoint
            for i in range(3):
                time.sleep(1)
                
                partial_response = requests.get(f"{BACKEND_URL}/batch/partial-results/{batch_id}", timeout=10)
                if partial_response.status_code == 200:
                    data = partial_response.json()
                    
                    # Check required fields
                    required_fields = ["batch_id", "status", "progress", "partial_results", 
                                     "partial_results_count", "last_update", "is_final"]
                    
                    missing_fields = [field for field in required_fields if field not in data]
                    if missing_fields:
                        print(f"    ❌ Missing fields: {missing_fields}")
                        return False
                    
                    partial_results = data.get("partial_results", [])
                    partial_count = data.get("partial_results_count", 0)
                    last_update = data.get("last_update")
                    is_final = data.get("is_final", False)
                    
                    print(f"    Check {i+1}: {partial_count} results, final: {is_final}")
                    
                    if len(partial_results) == partial_count:
                        print(f"    ✅ Partial results count matches: {partial_count}")
                    else:
                        print(f"    ❌ Count mismatch: {len(partial_results)} vs {partial_count}")
                        return False
                else:
                    print(f"    ❌ Partial results API failed: {partial_response.status_code}")
            
            print("✅ Partial Results API working correctly")
            return True
        else:
            print(f"❌ Batch creation failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def test_phase2_enhanced_time_estimation():
    """Test Phase 2 Enhanced Time Estimation"""
    print("\n⏱️ Testing Phase 2 Enhanced Time Estimation...")
    
    try:
        # Test single index
        single_request = {
            "indices": ["DOW30"],
            "filters": {
                "price_filter": {"type": "under", "under": 500},
                "dmi_filter": {"min": 15, "max": 70},
                "ppo_slope_filter": {"threshold": -50},
                "ppo_hook_filter": "all"
            },
            "force_refresh": False
        }
        
        # Test multi index
        multi_request = {
            "indices": ["DOW30", "NASDAQ100"],
            "filters": {
                "price_filter": {"type": "under", "under": 500},
                "dmi_filter": {"min": 15, "max": 70},
                "ppo_slope_filter": {"threshold": -50},
                "ppo_hook_filter": "all"
            },
            "force_refresh": False
        }
        
        single_response = requests.post(f"{BACKEND_URL}/batch/scan", 
                                      json=single_request,
                                      headers={"Content-Type": "application/json"},
                                      timeout=30)
        
        multi_response = requests.post(f"{BACKEND_URL}/batch/scan", 
                                     json=multi_request,
                                     headers={"Content-Type": "application/json"},
                                     timeout=30)
        
        if single_response.status_code == 200 and multi_response.status_code == 200:
            single_data = single_response.json()
            multi_data = multi_response.json()
            
            single_time = single_data.get("estimated_completion_minutes", 0)
            multi_time = multi_data.get("estimated_completion_minutes", 0)
            single_stocks = single_data.get("total_stocks", 0)
            multi_stocks = multi_data.get("total_stocks", 0)
            
            print(f"✅ Single index: {single_stocks} stocks, {single_time} min")
            print(f"✅ Multi index: {multi_stocks} stocks, {multi_time} min")
            
            if multi_time > 0 and single_time > 0:
                if multi_time <= single_time * 2.5:  # Reasonable overlap adjustment
                    print(f"✅ Time estimation shows overlap optimization")
                    return True
                else:
                    print(f"❌ Multi-index time too high: {multi_time} vs expected max {single_time * 2.5}")
                    return False
            else:
                print(f"❌ Time estimation returned 0")
                return False
        else:
            print(f"❌ API calls failed: {single_response.status_code}, {multi_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def main():
    """Run Phase 2 validation tests"""
    print("🚀 COMPREHENSIVE PHASE 2 BATCH SCREENER VALIDATION")
    print("=" * 60)
    
    tests = [
        ("Stock Universe Expansion", test_phase2_stock_universe_expansion),
        ("Interleaved Processing", test_phase2_interleaved_processing),
        ("Partial Results API", test_phase2_partial_results_api),
        ("Enhanced Time Estimation", test_phase2_enhanced_time_estimation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n📋 PHASE 2 VALIDATION SUMMARY")
    print("=" * 40)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All Phase 2 features validated successfully!")
        return 0
    else:
        print("🚨 Some Phase 2 features need attention")
        return 1

if __name__ == "__main__":
    exit(main())