#!/usr/bin/env python3
"""
URGENT BATCH FILTERING DEBUG TEST
Tests batch processing with extremely permissive filters to debug why 0 results are being returned.
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any, List

# Configuration
BACKEND_URL = "https://stockwise-120.preview.emergentagent.com/api"

class BatchFilteringDebugTester:
    def __init__(self):
        self.results = {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "test_details": [],
            "critical_issues": [],
            "debug_issues": []
        }
        
    def log_test(self, test_name: str, passed: bool, details: str, is_critical: bool = False):
        """Log test results"""
        self.results["total_tests"] += 1
        if passed:
            self.results["passed_tests"] += 1
            status = "✅ PASS"
        else:
            self.results["failed_tests"] += 1
            status = "❌ FAIL"
            if is_critical:
                self.results["critical_issues"].append(f"{test_name}: {details}")
        
        self.results["test_details"].append({
            "test": test_name,
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
        print(f"{status}: {test_name} - {details}")

    def test_batch_filtering_debug(self) -> bool:
        """
        URGENT BATCH FILTERING DEBUG TEST
        
        Tests batch processing with extremely permissive filters to debug why 0 results 
        are being returned. Uses ultra-permissive filters that should definitely return results.
        
        Debug Investigation:
        1. Monitor debug logs for filtering issues
        2. Data structure validation 
        3. Filter logic testing
        4. Sample data analysis
        """
        print(f"\n🔧 URGENT BATCH FILTERING DEBUG TEST")
        print("=" * 70)
        print("Testing with ultra-permissive filters that should return most DOW30 stocks")
        
        all_passed = True
        debug_issues = []
        
        # Ultra-permissive filters from the review request
        ultra_permissive_filters = {
            "indices": ["DOW30"],
            "filters": {
                "price_filter": {"type": "under", "under": 1000},
                "dmi_filter": {"min": 0, "max": 100}, 
                "ppo_slope_filter": {"threshold": -1000},
                "ppo_hook_filter": "all"
            },
            "force_refresh": False
        }
        
        print(f"🎯 ULTRA-PERMISSIVE FILTER TEST:")
        print(f"  • Price: Under $1000 (should include all stocks)")
        print(f"  • DMI: 0-100 range (should include all stocks)")
        print(f"  • PPO Slope: >-1000% (should include all stocks)")
        print(f"  • Hook Filter: All (should include all stocks)")
        print(f"  • Index: DOW30 (30 stocks total)")
        
        try:
            # 1. First check available indices
            print(f"\n📊 Step 1: Checking available indices...")
            indices_response = requests.get(f"{BACKEND_URL}/batch/indices", timeout=10)
            
            if indices_response.status_code == 200:
                indices_data = indices_response.json()
                dow30_info = indices_data.get("indices", {}).get("DOW30", {})
                stock_count = dow30_info.get("stock_count", 0)
                
                self.log_test("Batch Indices Check", True, 
                            f"DOW30 has {stock_count} stocks available")
                print(f"  ✅ DOW30 Index: {stock_count} stocks available")
                
                if stock_count == 0:
                    debug_issues.append("DOW30 index has 0 stocks - data loading issue")
                    all_passed = False
            else:
                self.log_test("Batch Indices Check", False, 
                            f"HTTP {indices_response.status_code}: {indices_response.text}", True)
                debug_issues.append("Cannot access batch indices endpoint")
                all_passed = False
                return False
            
            # 2. Start batch scan with ultra-permissive filters
            print(f"\n🚀 Step 2: Starting batch scan with ultra-permissive filters...")
            start_time = time.time()
            
            scan_response = requests.post(f"{BACKEND_URL}/batch/scan", 
                                        json=ultra_permissive_filters,
                                        headers={"Content-Type": "application/json"},
                                        timeout=30)
            
            if scan_response.status_code == 200:
                scan_data = scan_response.json()
                batch_id = scan_data.get("batch_id")
                total_stocks = scan_data.get("total_stocks", 0)
                
                self.log_test("Batch Scan Start", True, 
                            f"Batch {batch_id} started for {total_stocks} stocks")
                print(f"  ✅ Batch ID: {batch_id}")
                print(f"  ✅ Total stocks to process: {total_stocks}")
                
                if total_stocks == 0:
                    debug_issues.append("Batch scan started with 0 stocks - symbol collection issue")
                    all_passed = False
                
            else:
                self.log_test("Batch Scan Start", False, 
                            f"HTTP {scan_response.status_code}: {scan_response.text}", True)
                debug_issues.append(f"Batch scan failed to start: {scan_response.status_code}")
                all_passed = False
                return False
            
            # 3. Monitor batch progress and wait for completion
            print(f"\n⏳ Step 3: Monitoring batch progress...")
            max_wait_time = 300  # 5 minutes max wait
            check_interval = 10   # Check every 10 seconds
            elapsed_time = 0
            
            while elapsed_time < max_wait_time:
                status_response = requests.get(f"{BACKEND_URL}/batch/status/{batch_id}", timeout=10)
                
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    batch_status = status_data.get("status", "unknown")
                    progress = status_data.get("progress", {})
                    processed = progress.get("processed", 0)
                    total = progress.get("total", 0)
                    percentage = progress.get("percentage", 0)
                    current_symbol = progress.get("current_symbol", "")
                    
                    print(f"  📈 Status: {batch_status}, Progress: {processed}/{total} ({percentage:.1f}%), Current: {current_symbol}")
                    
                    if batch_status == "completed":
                        self.log_test("Batch Processing", True, 
                                    f"Batch completed: {processed}/{total} stocks processed")
                        break
                    elif batch_status == "failed":
                        error = status_data.get("error", "Unknown error")
                        self.log_test("Batch Processing", False, 
                                    f"Batch failed: {error}", True)
                        debug_issues.append(f"Batch processing failed: {error}")
                        all_passed = False
                        break
                    
                    time.sleep(check_interval)
                    elapsed_time += check_interval
                else:
                    debug_issues.append(f"Cannot check batch status: {status_response.status_code}")
                    break
            
            if elapsed_time >= max_wait_time:
                self.log_test("Batch Processing", False, 
                            "Batch processing timed out after 5 minutes", True)
                debug_issues.append("Batch processing timed out")
                all_passed = False
            
            # 4. Get batch results and analyze filtering
            print(f"\n📋 Step 4: Analyzing batch results...")
            results_response = requests.get(f"{BACKEND_URL}/batch/results/{batch_id}", timeout=10)
            
            if results_response.status_code == 200:
                results_data = results_response.json()
                results = results_data.get("results", [])
                results_count = len(results)
                
                print(f"  📊 Results Analysis:")
                print(f"    • Total results returned: {results_count}")
                print(f"    • Expected: Most of 30 DOW30 stocks (with ultra-permissive filters)")
                
                if results_count == 0:
                    self.log_test("Batch Results Analysis", False, 
                                "CRITICAL: 0 results with ultra-permissive filters", True)
                    debug_issues.append("CRITICAL: Ultra-permissive filters returned 0 results")
                    all_passed = False
                    
                    # This is the core issue - investigate why
                    print(f"\n🚨 CRITICAL ISSUE DETECTED: 0 results with ultra-permissive filters")
                    print(f"🔍 DEBUGGING INVESTIGATION:")
                    print(f"  • Filters should allow ALL stocks (price <$1000, DMI 0-100, slope >-1000%)")
                    print(f"  • DOW30 has 30 stocks, most should pass these criteria")
                    print(f"  • This indicates a fundamental filtering or data conversion issue")
                    
                elif results_count < 10:
                    self.log_test("Batch Results Analysis", False, 
                                f"Too few results: {results_count}/30 with ultra-permissive filters", True)
                    debug_issues.append(f"Ultra-permissive filters returned only {results_count} results")
                    all_passed = False
                else:
                    self.log_test("Batch Results Analysis", True, 
                                f"Good results: {results_count} stocks passed ultra-permissive filters")
                
                # 5. Analyze individual stock data for debugging
                if results:
                    print(f"\n🔬 Step 5: Sample data analysis...")
                    self.analyze_batch_sample_data(results[:5], debug_issues)
                else:
                    print(f"\n🔬 Step 5: No results to analyze - investigating data conversion...")
                    # Try to get individual stock data to see if convert_to_batch_format is working
                    self.investigate_data_conversion_issue(debug_issues)
                
            else:
                self.log_test("Batch Results Retrieval", False, 
                            f"HTTP {results_response.status_code}: {results_response.text}", True)
                debug_issues.append(f"Cannot retrieve batch results: {results_response.status_code}")
                all_passed = False
            
        except Exception as e:
            self.log_test("Batch Filtering Debug", False, f"Error: {str(e)}", True)
            debug_issues.append(f"Test execution error: {str(e)}")
            all_passed = False
        
        # Store debug issues for summary
        self.results["debug_issues"] = debug_issues
        
        # Summary of debug findings
        print(f"\n📋 BATCH FILTERING DEBUG SUMMARY:")
        if debug_issues:
            print(f"🚨 ISSUES FOUND ({len(debug_issues)}):")
            for i, issue in enumerate(debug_issues, 1):
                print(f"  {i}. {issue}")
        else:
            print(f"✅ No critical issues found - batch filtering working correctly")
        
        return all_passed
    
    def analyze_batch_sample_data(self, sample_results: List[Dict], debug_issues: List[str]):
        """Analyze sample batch results for debugging"""
        print(f"  🔍 Analyzing {len(sample_results)} sample results:")
        
        for i, stock in enumerate(sample_results, 1):
            symbol = stock.get("symbol", f"Stock_{i}")
            price = stock.get("price", 0)
            dmi = stock.get("dmi", 0)
            ppo_slope = stock.get("ppo_slope_percentage", 0)
            hook_type = stock.get("ppo_hook_type")
            
            print(f"    {i}. {symbol}: Price=${price:.2f}, DMI={dmi:.2f}, PPO_Slope={ppo_slope:.2f}%, Hook={hook_type}")
            
            # Check if data looks reasonable
            if price == 0:
                debug_issues.append(f"{symbol} has zero price - data conversion issue")
            if dmi == 0:
                debug_issues.append(f"{symbol} has zero DMI - calculation issue")
            if ppo_slope == 0:
                debug_issues.append(f"{symbol} has zero PPO slope - calculation issue")
    
    def investigate_data_conversion_issue(self, debug_issues: List[str]):
        """Investigate if convert_to_batch_format is returning None"""
        print(f"  🔍 Investigating data conversion issues...")
        
        # Try to get individual stock analysis for a DOW30 stock
        test_symbols = ["AAPL", "MSFT", "JPM"]  # Common DOW30 stocks
        
        for symbol in test_symbols:
            try:
                response = requests.get(f"{BACKEND_URL}/analyze/{symbol}", timeout=15)
                if response.status_code == 200:
                    data = response.json()
                    price = data.get("current_price", 0)
                    indicators = data.get("indicators", {})
                    ppo_slope = indicators.get("ppo_slope_percentage", 0)
                    dmi_plus = indicators.get("dmi_plus", 0)
                    dmi_minus = indicators.get("dmi_minus", 0)
                    
                    print(f"    • {symbol} individual analysis: Price=${price:.2f}, PPO_Slope={ppo_slope:.2f}%, DMI+={dmi_plus:.2f}, DMI-={dmi_minus:.2f}")
                    
                    if price == 0:
                        debug_issues.append(f"{symbol} individual analysis returns zero price")
                    if ppo_slope == 0 and dmi_plus == 0:
                        debug_issues.append(f"{symbol} individual analysis has zero technical indicators")
                    
                    # This data should be convertible to batch format
                    if price > 0 and (dmi_plus > 0 or dmi_minus > 0):
                        print(f"    ✅ {symbol} has valid data that should convert to batch format")
                    else:
                        print(f"    ❌ {symbol} has invalid data that might cause conversion to return None")
                        debug_issues.append(f"{symbol} has invalid data for batch conversion")
                        
                else:
                    debug_issues.append(f"Cannot get individual analysis for {symbol}: {response.status_code}")
                    
            except Exception as e:
                debug_issues.append(f"Error testing individual analysis for {symbol}: {str(e)}")

    def print_summary(self):
        """Print comprehensive summary"""
        print(f"\n" + "=" * 80)
        print(f"🏁 BATCH FILTERING DEBUG TEST COMPLETE")
        print("=" * 80)
        
        success_rate = (self.results["passed_tests"] / self.results["total_tests"]) * 100 if self.results["total_tests"] > 0 else 0
        
        print(f"📊 OVERALL RESULTS:")
        print(f"  • Total Tests: {self.results['total_tests']}")
        print(f"  • Passed: {self.results['passed_tests']} ✅")
        print(f"  • Failed: {self.results['failed_tests']} ❌")
        print(f"  • Success Rate: {success_rate:.1f}%")
        
        if self.results["critical_issues"]:
            print(f"\n🚨 CRITICAL ISSUES REQUIRING ATTENTION ({len(self.results['critical_issues'])}):")
            for i, issue in enumerate(self.results["critical_issues"], 1):
                print(f"  {i}. {issue}")
        
        if self.results["debug_issues"]:
            print(f"\n🔍 DEBUG FINDINGS ({len(self.results['debug_issues'])}):")
            for i, issue in enumerate(self.results["debug_issues"], 1):
                print(f"  {i}. {issue}")
        
        # Final recommendation
        if success_rate >= 90:
            print(f"\n✅ EXCELLENT: Batch filtering is working correctly with {success_rate:.1f}% success rate")
        elif success_rate >= 75:
            print(f"\n⚠️ GOOD: Batch filtering is mostly functional with {success_rate:.1f}% success rate")
        elif success_rate >= 50:
            print(f"\n🔧 NEEDS WORK: Batch filtering has issues with {success_rate:.1f}% success rate")
        else:
            print(f"\n🚨 CRITICAL: Batch filtering has major issues with {success_rate:.1f}% success rate")
        
        print("=" * 80)


if __name__ == "__main__":
    print("🔧 URGENT: Running Batch Filtering Debug Test as requested in review")
    
    tester = BatchFilteringDebugTester()
    success = tester.test_batch_filtering_debug()
    tester.print_summary()
    
    # Exit with appropriate code
    if not success:
        exit(1)
    else:
        exit(0)