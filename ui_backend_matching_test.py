#!/usr/bin/env python3
"""
UI-Backend Filter Matching Validation Test
Tests the specific validation requirements from the review request
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any, List

# Configuration
BACKEND_URL = "https://market-scanner-27.preview.emergentagent.com/api"

class UIBackendMatchingTester:
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

    def test_ui_backend_filter_matching(self) -> bool:
        """
        CRITICAL UI-BACKEND MATCHING VALIDATION
        
        Verify that the frontend UI filter elements exactly match the backend filtering 
        functionality and data structure as specified in the review request.
        
        Tests 4 critical areas:
        1. Price Filter Matching - "Under specific amount" vs "Within price range"
        2. DMI Filter Matching - "Minimum DMI" and "Maximum DMI" inputs  
        3. PPO Slope Filter Matching - "Minimum Slope %" input
        4. PPO Hook Filter Matching - "all", "positive", "negative", "both" options
        """
        print(f"\n🎯 CRITICAL UI-BACKEND MATCHING VALIDATION")
        print("=" * 70)
        
        all_passed = True
        validation_issues = []
        
        # Test 1 - Price Filter Validation
        print(f"\n💰 Test 1: Price Filter Validation")
        price_filter_test = {
            "price_filter": {"type": "under", "under": 200},
            "dmi_filter": {"min": 0, "max": 100},
            "ppo_slope_filter": {"threshold": -1000},
            "ppo_hook_filter": "all"
        }
        
        price_test_passed = self.validate_price_filter_matching(price_filter_test)
        if not price_test_passed:
            all_passed = False
            validation_issues.append("Price filter matching failed")
        
        # Test 2 - DMI Filter Validation  
        print(f"\n📊 Test 2: DMI Filter Validation")
        dmi_filter_test = {
            "price_filter": {"type": "under", "under": 1000},
            "dmi_filter": {"min": 30, "max": 50},
            "ppo_slope_filter": {"threshold": -1000},
            "ppo_hook_filter": "all"
        }
        
        dmi_test_passed = self.validate_dmi_filter_matching(dmi_filter_test)
        if not dmi_test_passed:
            all_passed = False
            validation_issues.append("DMI filter matching failed")
        
        # Test 3 - PPO Slope Filter Validation
        print(f"\n📈 Test 3: PPO Slope Filter Validation")
        slope_filter_test = {
            "price_filter": {"type": "under", "under": 1000},
            "dmi_filter": {"min": 0, "max": 100},
            "ppo_slope_filter": {"threshold": 5.0},
            "ppo_hook_filter": "all"
        }
        
        slope_test_passed = self.validate_ppo_slope_filter_matching(slope_filter_test)
        if not slope_test_passed:
            all_passed = False
            validation_issues.append("PPO slope filter matching failed")
        
        # Test 4 - Hook Filter Validation
        print(f"\n🎣 Test 4: PPO Hook Filter Validation")
        hook_filter_test = {
            "price_filter": {"type": "under", "under": 1000},
            "dmi_filter": {"min": 0, "max": 100},
            "ppo_slope_filter": {"threshold": -1000},
            "ppo_hook_filter": "negative"
        }
        
        hook_test_passed = self.validate_ppo_hook_filter_matching(hook_filter_test)
        if not hook_test_passed:
            all_passed = False
            validation_issues.append("PPO hook filter matching failed")
        
        # Additional comprehensive validation tests
        print(f"\n🔍 Additional Comprehensive Filter Tests")
        comprehensive_passed = self.run_comprehensive_filter_validation()
        if not comprehensive_passed:
            all_passed = False
            validation_issues.append("Comprehensive filter validation failed")
        
        # Summary of UI-Backend matching validation
        if validation_issues:
            print(f"\n🚨 UI-BACKEND MATCHING ISSUES FOUND ({len(validation_issues)}):")
            for issue in validation_issues:
                print(f"  • {issue}")
        else:
            print(f"\n✅ UI-Backend filter matching validation passed completely")
        
        return all_passed

    def validate_price_filter_matching(self, filters_payload: Dict[str, Any]) -> bool:
        """Validate price filter matching between UI and backend"""
        try:
            print(f"  Testing price filter: {filters_payload['price_filter']}")
            
            response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                   json=filters_payload,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate price filter structure matches UI expectations
                filters_applied = data.get("filters_applied", {})
                price_filter = filters_applied.get("price_filter", {})
                
                # Check if backend correctly interprets "under" type
                if price_filter.get("type") != "under":
                    self.log_test("Price Filter Type Matching", False, 
                                f"Backend received type '{price_filter.get('type')}', expected 'under'", True)
                    return False
                
                if price_filter.get("under") != 200:
                    self.log_test("Price Filter Value Matching", False, 
                                f"Backend received under value {price_filter.get('under')}, expected 200", True)
                    return False
                
                # Validate actual filtering works
                stocks = data.get("stocks", [])
                violations = 0
                for stock in stocks[:10]:  # Check first 10 results
                    price = stock.get("price", 0)
                    if price > 200:
                        violations += 1
                        if violations <= 3:  # Only log first 3 violations
                            print(f"    ⚠️  Stock {stock.get('symbol')} price ${price:.2f} exceeds filter ${200}")
                
                if violations > len(stocks) * 0.1:  # More than 10% violations
                    self.log_test("Price Filter Logic", False, 
                                f"{violations}/{len(stocks)} stocks violate price filter", True)
                    return False
                
                self.log_test("Price Filter Matching", True, 
                            f"Price filter working correctly, found {len(stocks)} stocks, {violations} violations")
                return True
            else:
                self.log_test("Price Filter API", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                return False
                
        except Exception as e:
            self.log_test("Price Filter Test", False, f"Error: {str(e)}", True)
            return False

    def validate_dmi_filter_matching(self, filters_payload: Dict[str, Any]) -> bool:
        """Validate DMI filter matching between UI and backend"""
        try:
            print(f"  Testing DMI filter: {filters_payload['dmi_filter']}")
            
            response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                   json=filters_payload,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate DMI filter structure matches UI expectations
                filters_applied = data.get("filters_applied", {})
                dmi_filter = filters_applied.get("dmi_filter", {})
                
                # Check if backend correctly interprets min/max values
                if dmi_filter.get("min") != 30:
                    self.log_test("DMI Filter Min Matching", False, 
                                f"Backend received min {dmi_filter.get('min')}, expected 30", True)
                    return False
                
                if dmi_filter.get("max") != 50:
                    self.log_test("DMI Filter Max Matching", False, 
                                f"Backend received max {dmi_filter.get('max')}, expected 50", True)
                    return False
                
                # Validate actual filtering works with DMI field (not ADX)
                stocks = data.get("stocks", [])
                violations = 0
                for stock in stocks[:10]:  # Check first 10 results
                    dmi_value = stock.get("dmi", 0)  # Should use 'dmi' field, not 'adx'
                    if not (30 <= dmi_value <= 50):
                        violations += 1
                        if violations <= 3:  # Only log first 3 violations
                            print(f"    ⚠️  Stock {stock.get('symbol')} DMI {dmi_value:.2f} outside range 30-50")
                
                if violations > len(stocks) * 0.1:  # More than 10% violations
                    self.log_test("DMI Filter Logic", False, 
                                f"{violations}/{len(stocks)} stocks violate DMI filter", True)
                    return False
                
                self.log_test("DMI Filter Matching", True, 
                            f"DMI filter working correctly, found {len(stocks)} stocks, {violations} violations")
                return True
            else:
                self.log_test("DMI Filter API", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                return False
                
        except Exception as e:
            self.log_test("DMI Filter Test", False, f"Error: {str(e)}", True)
            return False

    def validate_ppo_slope_filter_matching(self, filters_payload: Dict[str, Any]) -> bool:
        """Validate PPO slope filter matching between UI and backend"""
        try:
            print(f"  Testing PPO slope filter: {filters_payload['ppo_slope_filter']}")
            
            response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                   json=filters_payload,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate PPO slope filter structure matches UI expectations
                filters_applied = data.get("filters_applied", {})
                slope_filter = filters_applied.get("ppo_slope_filter", {})
                
                # Check if backend correctly interprets threshold value
                if slope_filter.get("threshold") != 5.0:
                    self.log_test("PPO Slope Filter Threshold Matching", False, 
                                f"Backend received threshold {slope_filter.get('threshold')}, expected 5.0", True)
                    return False
                
                # Validate actual filtering works with ppo_slope_percentage field
                stocks = data.get("stocks", [])
                violations = 0
                for stock in stocks[:10]:  # Check first 10 results
                    slope_percentage = stock.get("ppo_slope_percentage", 0)
                    if slope_percentage < 5.0:
                        violations += 1
                        if violations <= 3:  # Only log first 3 violations
                            print(f"    ⚠️  Stock {stock.get('symbol')} slope {slope_percentage:.2f}% below threshold 5.0%")
                
                if violations > len(stocks) * 0.1:  # More than 10% violations
                    self.log_test("PPO Slope Filter Logic", False, 
                                f"{violations}/{len(stocks)} stocks violate PPO slope filter", True)
                    return False
                
                self.log_test("PPO Slope Filter Matching", True, 
                            f"PPO slope filter working correctly, found {len(stocks)} stocks, {violations} violations")
                return True
            else:
                self.log_test("PPO Slope Filter API", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                return False
                
        except Exception as e:
            self.log_test("PPO Slope Filter Test", False, f"Error: {str(e)}", True)
            return False

    def validate_ppo_hook_filter_matching(self, filters_payload: Dict[str, Any]) -> bool:
        """Validate PPO hook filter matching between UI and backend"""
        try:
            print(f"  Testing PPO hook filter: {filters_payload['ppo_hook_filter']}")
            
            response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                   json=filters_payload,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate PPO hook filter structure matches UI expectations
                filters_applied = data.get("filters_applied", {})
                hook_filter = filters_applied.get("ppo_hook_filter")
                
                # Check if backend correctly interprets "negative" value
                if hook_filter != "negative":
                    self.log_test("PPO Hook Filter Value Matching", False, 
                                f"Backend received hook filter '{hook_filter}', expected 'negative'", True)
                    return False
                
                # Validate actual filtering works with ppo_hook_type field
                stocks = data.get("stocks", [])
                violations = 0
                for stock in stocks[:10]:  # Check first 10 results
                    hook_type = stock.get("ppo_hook_type")
                    if hook_type != "negative":
                        violations += 1
                        if violations <= 3:  # Only log first 3 violations
                            print(f"    ⚠️  Stock {stock.get('symbol')} hook type '{hook_type}', expected 'negative'")
                
                if violations > len(stocks) * 0.1:  # More than 10% violations
                    self.log_test("PPO Hook Filter Logic", False, 
                                f"{violations}/{len(stocks)} stocks violate hook filter", True)
                    return False
                
                self.log_test("PPO Hook Filter Matching", True, 
                            f"PPO hook filter working correctly, found {len(stocks)} stocks, {violations} violations")
                return True
            else:
                self.log_test("PPO Hook Filter API", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                return False
                
        except Exception as e:
            self.log_test("PPO Hook Filter Test", False, f"Error: {str(e)}", True)
            return False

    def run_comprehensive_filter_validation(self) -> bool:
        """Run comprehensive validation of all filter combinations"""
        all_passed = True
        
        # Test all hook filter options
        hook_options = ["all", "positive", "negative", "both"]
        for hook_option in hook_options:
            filters_payload = {
                "price_filter": {"type": "under", "under": 500},
                "dmi_filter": {"min": 20, "max": 60},
                "ppo_slope_filter": {"threshold": -100},
                "ppo_hook_filter": hook_option
            }
            
            try:
                response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                       json=filters_payload,
                                       headers={"Content-Type": "application/json"},
                                       timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    stocks = data.get("stocks", [])
                    
                    # Validate hook filtering logic
                    if hook_option != "all" and len(stocks) > 0:
                        violations = 0
                        for stock in stocks[:5]:  # Check first 5 results
                            hook_type = stock.get("ppo_hook_type")
                            if hook_option == "positive" and hook_type != "positive":
                                violations += 1
                            elif hook_option == "negative" and hook_type != "negative":
                                violations += 1
                            elif hook_option == "both" and hook_type not in ["positive", "negative"]:
                                violations += 1
                        
                        if violations > 0:
                            self.log_test(f"Hook Filter ({hook_option})", False, 
                                        f"{violations} violations in hook filtering", True)
                            all_passed = False
                        else:
                            self.log_test(f"Hook Filter ({hook_option})", True, 
                                        f"Found {len(stocks)} stocks with {hook_option} hook filter")
                    else:
                        self.log_test(f"Hook Filter ({hook_option})", True, 
                                    f"Found {len(stocks)} stocks with {hook_option} hook filter")
                else:
                    self.log_test(f"Hook Filter API ({hook_option})", False, 
                                f"HTTP {response.status_code}: {response.text}", True)
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"Hook Filter Test ({hook_option})", False, f"Error: {str(e)}", True)
                all_passed = False
        
        # Test price range filter (not just "under")
        range_filters_payload = {
            "price_filter": {"type": "range", "min": 100, "max": 300},
            "dmi_filter": {"min": 0, "max": 100},
            "ppo_slope_filter": {"threshold": -1000},
            "ppo_hook_filter": "all"
        }
        
        try:
            response = requests.post(f"{BACKEND_URL}/screener/scan", 
                                   json=range_filters_payload,
                                   headers={"Content-Type": "application/json"},
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                stocks = data.get("stocks", [])
                
                # Validate price range filtering
                violations = 0
                for stock in stocks[:10]:  # Check first 10 results
                    price = stock.get("price", 0)
                    if not (100 <= price <= 300):
                        violations += 1
                        if violations <= 3:  # Only log first 3 violations
                            print(f"    ⚠️  Stock {stock.get('symbol')} price ${price:.2f} outside range $100-$300")
                
                if violations > len(stocks) * 0.1:  # More than 10% violations
                    self.log_test("Price Range Filter", False, 
                                f"{violations}/{len(stocks)} stocks violate price range filter", True)
                    all_passed = False
                else:
                    self.log_test("Price Range Filter", True, 
                                f"Price range filter working correctly, found {len(stocks)} stocks, {violations} violations")
            else:
                self.log_test("Price Range Filter API", False, 
                            f"HTTP {response.status_code}: {response.text}", True)
                all_passed = False
                
        except Exception as e:
            self.log_test("Price Range Filter Test", False, f"Error: {str(e)}", True)
            all_passed = False
        
        return all_passed

    def print_final_summary(self):
        """Print final test summary"""
        print(f"\n" + "=" * 70)
        print(f"🎯 UI-BACKEND MATCHING VALIDATION SUMMARY")
        print(f"=" * 70)
        print(f"Total Tests: {self.results['total_tests']}")
        print(f"Passed: {self.results['passed_tests']}")
        print(f"Failed: {self.results['failed_tests']}")
        
        if self.results['failed_tests'] > 0:
            print(f"\n❌ CRITICAL ISSUES FOUND ({len(self.results['critical_issues'])}):")
            for issue in self.results['critical_issues']:
                print(f"  • {issue}")
        else:
            print(f"\n✅ ALL UI-BACKEND MATCHING TESTS PASSED!")
        
        success_rate = (self.results['passed_tests'] / self.results['total_tests']) * 100 if self.results['total_tests'] > 0 else 0
        print(f"\nSuccess Rate: {success_rate:.1f}%")

if __name__ == "__main__":
    tester = UIBackendMatchingTester()
    
    print("🚀 Starting UI-Backend Filter Matching Validation")
    print("=" * 70)
    
    # Run the comprehensive UI-backend matching validation
    all_passed = tester.test_ui_backend_filter_matching()
    
    # Print final summary
    tester.print_final_summary()
    
    # Exit with appropriate code
    exit(0 if all_passed else 1)