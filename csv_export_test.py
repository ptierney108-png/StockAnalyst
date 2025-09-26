#!/usr/bin/env python3
"""
Focused CSV Export Functionality Testing
Tests the newly implemented CSV export functionality for batch scanner results
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any, List, Optional

# Configuration
BACKEND_URL = "https://market-analyzer-95.preview.emergentagent.com/api"

class CSVExportTester:
    def __init__(self):
        self.results = {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "test_details": [],
            "critical_issues": []
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
    
    def test_csv_export_error_cases(self) -> bool:
        """Test CSV export error handling"""
        print(f"\n🚨 Testing CSV export error cases...")
        all_passed = True
        
        # Test 1: Invalid batch ID
        try:
            response = requests.get(f"{BACKEND_URL}/batch/export/invalid-batch-id", timeout=10)
            if response.status_code == 404:
                self.log_test("CSV Export - Invalid Batch ID", True, 
                            "Correctly returned 404 for invalid batch ID")
            else:
                self.log_test("CSV Export - Invalid Batch ID", False, 
                            f"Expected 404, got {response.status_code}", True)
                all_passed = False
        except Exception as e:
            self.log_test("CSV Export - Invalid Batch ID", False, f"Error: {str(e)}", True)
            all_passed = False
        
        # Test 2: Non-existent batch ID (valid UUID format)
        try:
            fake_uuid = "12345678-1234-1234-1234-123456789012"
            response = requests.get(f"{BACKEND_URL}/batch/export/{fake_uuid}", timeout=10)
            if response.status_code == 404:
                self.log_test("CSV Export - Non-existent Batch ID", True, 
                            "Correctly returned 404 for non-existent batch ID")
            else:
                self.log_test("CSV Export - Non-existent Batch ID", False, 
                            f"Expected 404, got {response.status_code}", True)
                all_passed = False
        except Exception as e:
            self.log_test("CSV Export - Non-existent Batch ID", False, f"Error: {str(e)}", True)
            all_passed = False
        
        return all_passed
    
    def test_batch_infrastructure(self) -> bool:
        """Test batch infrastructure endpoints"""
        print(f"\n🔍 Testing batch infrastructure...")
        all_passed = True
        
        # Test batch indices endpoint
        try:
            response = requests.get(f"{BACKEND_URL}/batch/indices", timeout=10)
            if response.status_code == 200:
                data = response.json()
                indices = data.get("indices", {})
                if indices:
                    self.log_test("Batch Indices Endpoint", True, 
                                f"Retrieved {len(indices)} indices")
                    print(f"  Available indices: {list(indices.keys())}")
                else:
                    self.log_test("Batch Indices Endpoint", False, 
                                "No indices returned", True)
                    all_passed = False
            else:
                self.log_test("Batch Indices Endpoint", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                all_passed = False
        except Exception as e:
            self.log_test("Batch Indices Endpoint", False, f"Error: {str(e)}", True)
            all_passed = False
        
        # Test batch stats endpoint
        try:
            response = requests.get(f"{BACKEND_URL}/batch/stats", timeout=10)
            if response.status_code == 200:
                data = response.json()
                batch_processor = data.get("batch_processor", {})
                total_jobs = batch_processor.get("total_jobs", 0)
                completed_jobs = batch_processor.get("completed_jobs", 0)
                self.log_test("Batch Stats Endpoint", True, 
                            f"Total jobs: {total_jobs}, Completed: {completed_jobs}")
            else:
                self.log_test("Batch Stats Endpoint", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                all_passed = False
        except Exception as e:
            self.log_test("Batch Stats Endpoint", False, f"Error: {str(e)}", True)
            all_passed = False
        
        return all_passed
    
    def create_small_batch_job(self) -> Optional[str]:
        """Create a small batch job for testing"""
        try:
            # Create a very small batch job with minimal filters
            batch_request = {
                "indices": ["DOW30"],  # Smallest index
                "filters": {
                    "price_filter": {"type": "under", "under": 10000},  # Very permissive
                    "dmi_filter": {"min": 0, "max": 100},  # Very permissive
                    "ppo_slope_filter": {"threshold": -1000},  # Very permissive
                    "ppo_hook_filter": "all"
                },
                "force_refresh": False
            }
            
            print(f"Creating small test batch job...")
            response = requests.post(f"{BACKEND_URL}/batch/scan", 
                                   json=batch_request,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                batch_id = data.get("batch_id")
                print(f"✅ Created batch job: {batch_id}")
                return batch_id
            else:
                print(f"❌ Failed to create batch job: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error creating batch job: {e}")
            return None
    
    def wait_for_batch_completion(self, batch_id: str, timeout_minutes: int = 3) -> bool:
        """Wait for batch job to complete with shorter timeout"""
        start_time = time.time()
        timeout_seconds = timeout_minutes * 60
        
        print(f"⏳ Waiting for batch job completion (max {timeout_minutes} minutes)...")
        
        while time.time() - start_time < timeout_seconds:
            try:
                response = requests.get(f"{BACKEND_URL}/batch/status/{batch_id}", timeout=10)
                if response.status_code == 200:
                    status_data = response.json()
                    status = status_data.get("status")
                    progress = status_data.get("progress", {})
                    
                    if isinstance(progress, dict):
                        percentage = progress.get("percentage", 0)
                        processed = progress.get("processed", 0)
                        total = progress.get("total", 0)
                        print(f"  Status: {status}, Progress: {processed}/{total} ({percentage:.1f}%)")
                    else:
                        print(f"  Status: {status}, Progress: {progress}%")
                    
                    if status == "completed":
                        return True
                    elif status in ["failed", "cancelled"]:
                        print(f"❌ Batch job failed or was cancelled: {status}")
                        return False
                    
                    time.sleep(5)  # Check every 5 seconds
                else:
                    print(f"Error checking batch status: {response.status_code}")
                    time.sleep(5)
                    
            except Exception as e:
                print(f"Error waiting for batch completion: {e}")
                time.sleep(5)
        
        print(f"⚠️ Timeout waiting for batch completion")
        return False
    
    def test_csv_export_with_batch(self, batch_id: str) -> bool:
        """Test CSV export with a specific batch ID"""
        try:
            print(f"📄 Testing CSV export for batch ID: {batch_id}")
            
            start_time = time.time()
            response = requests.get(f"{BACKEND_URL}/batch/export/{batch_id}", timeout=30)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                # Validate response headers
                content_type = response.headers.get("content-type", "")
                content_disposition = response.headers.get("content-disposition", "")
                content_length = response.headers.get("content-length", "")
                
                header_issues = []
                if "text/csv" not in content_type:
                    header_issues.append(f"Wrong content-type: {content_type}")
                if "attachment" not in content_disposition:
                    header_issues.append(f"Missing attachment in content-disposition: {content_disposition}")
                if not content_length:
                    header_issues.append("Missing content-length header")
                
                if header_issues:
                    self.log_test("CSV Export Headers", False, 
                                f"Header issues: {header_issues}", True)
                    return False
                
                # Validate CSV content
                csv_content = response.text
                csv_lines = csv_content.split('\n')
                
                if len(csv_lines) < 2:  # At least header + 1 data row
                    self.log_test("CSV Export Content", False, 
                                f"Insufficient CSV content: {len(csv_lines)} lines", True)
                    return False
                
                # Validate CSV headers (31 columns)
                header_line = csv_lines[0]
                headers = [h.strip('"') for h in header_line.split(',')]
                
                expected_headers = [
                    "Symbol", "Company Name", "Sector", "Industry", "Price",
                    "Volume Today", "Volume Avg 3M", "Volume Year",
                    "1D Return %", "5D Return %", "2W Return %", "1M Return %", "1Y Return %",
                    "DMI", "ADX", "DI+", "DI-",
                    "PPO Day 1", "PPO Day 2", "PPO Day 3", "PPO Slope %", "PPO Hook",
                    "Optionable", "Call Bid", "Call Ask", "Put Bid", "Put Ask", "Options Expiration",
                    "Last Earnings", "Next Earnings", "Days to Earnings"
                ]
                
                if len(headers) != 31:
                    self.log_test("CSV Export Headers Count", False, 
                                f"Expected 31 headers, got {len(headers)}", True)
                    return False
                
                missing_headers = [h for h in expected_headers if h not in headers]
                if missing_headers:
                    self.log_test("CSV Export Headers Content", False, 
                                f"Missing headers: {missing_headers}", True)
                    return False
                
                # Validate data rows
                data_rows = [line for line in csv_lines[1:] if line.strip()]
                if len(data_rows) == 0:
                    self.log_test("CSV Export Data", False, "No data rows in CSV", True)
                    return False
                
                # Validate first data row format
                first_row = data_rows[0].split(',')
                if len(first_row) != 31:
                    self.log_test("CSV Export Data Format", False, 
                                f"First data row has {len(first_row)} columns, expected 31", True)
                    return False
                
                self.log_test("CSV Export Endpoint", True, 
                            f"CSV export successful: {len(data_rows)} stocks, {response_time:.2f}s")
                
                # Log sample data for verification
                print(f"    📊 CSV Export Details:")
                print(f"      • File size: {len(csv_content)} bytes")
                print(f"      • Data rows: {len(data_rows)}")
                print(f"      • Headers: {len(headers)} columns")
                print(f"      • Sample symbol: {first_row[0] if first_row else 'N/A'}")
                print(f"      • Sample headers: {', '.join(headers[:5])}...")
                
                return True
                
            elif response.status_code == 400:
                # Check if it's because batch job is not completed
                error_text = response.text
                if "not completed" in error_text:
                    self.log_test("CSV Export - Batch Not Completed", True, 
                                "Correctly returned 400 for non-completed batch job")
                    return True
                else:
                    self.log_test("CSV Export Endpoint", False, 
                                f"HTTP {response.status_code}: {response.text}", True)
                    return False
            else:
                self.log_test("CSV Export Endpoint", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                return False
                
        except Exception as e:
            self.log_test("CSV Export Endpoint", False, f"Error: {str(e)}", True)
            return False
    
    def run_csv_export_tests(self):
        """Run focused CSV export tests"""
        print("🚀 STARTING CSV EXPORT FUNCTIONALITY TESTING")
        print("=" * 70)
        
        # Test 1: Error handling (doesn't require batch jobs)
        error_handling_passed = self.test_csv_export_error_cases()
        
        # Test 2: Batch infrastructure
        infrastructure_passed = self.test_batch_infrastructure()
        
        # Test 3: Try to create and test with a batch job
        print(f"\n📊 Testing CSV export with actual batch job...")
        batch_id = self.create_small_batch_job()
        
        if batch_id:
            # Wait a short time for processing to start
            time.sleep(10)
            
            # Test CSV export (might return 400 if not completed, which is expected)
            csv_export_passed = self.test_csv_export_with_batch(batch_id)
            
            # Try waiting for completion if we have time
            if self.wait_for_batch_completion(batch_id, timeout_minutes=2):
                print(f"✅ Batch job completed! Testing CSV export...")
                csv_export_passed = self.test_csv_export_with_batch(batch_id)
            else:
                print(f"⚠️ Batch job still processing, but CSV endpoint error handling tested")
        else:
            print(f"⚠️ Could not create batch job for CSV export testing")
            csv_export_passed = False
        
        # Summary
        print(f"\n📋 CSV EXPORT TEST SUMMARY")
        print("=" * 50)
        print(f"Total tests: {self.results['total_tests']}")
        print(f"Passed: {self.results['passed_tests']}")
        print(f"Failed: {self.results['failed_tests']}")
        
        if self.results['critical_issues']:
            print(f"\n🚨 CRITICAL ISSUES:")
            for issue in self.results['critical_issues']:
                print(f"  • {issue}")
        else:
            print(f"\n✅ No critical issues found")
        
        success_rate = (self.results['passed_tests'] / self.results['total_tests']) * 100 if self.results['total_tests'] > 0 else 0
        print(f"\nSuccess rate: {success_rate:.1f}%")
        
        return self.results

if __name__ == "__main__":
    tester = CSVExportTester()
    results = tester.run_csv_export_tests()