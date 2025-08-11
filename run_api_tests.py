#!/usr/bin/env python3
"""
Test runner for API endpoints with detailed results and summary
"""

import sys
import subprocess
import json
from datetime import datetime


def run_tests():
    """Run API tests against live server and provide summary"""
    print("=" * 70)
    print("Flask Calculator API Test Suite (Live Server Testing)")
    print("=" * 70)
    print("ℹ️  These tests make real HTTP requests to http://localhost:8080")
    print("ℹ️  Make sure the server is running before running tests!")
    print("ℹ️  Start server with: ./docker-start.sh or python run.py")
    print()
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run pytest with verbose output and JSON report
    cmd = [
        sys.executable, '-m', 'pytest',
        'tests/test_routes.py',
        'tests/test_calculator.py',
        '-v',
        '--tb=short',
        '--json-report',
        '--json-report-file=test_report.json'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Print test output
        print("TEST OUTPUT:")
        print("-" * 40)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        # Try to load JSON report for detailed summary
        try:
            with open('test_report.json', 'r') as f:
                report = json.load(f)
            
            print("\n" + "=" * 60)
            print("TEST SUMMARY")
            print("=" * 60)
            
            summary = report.get('summary', {})
            total = summary.get('total', 0)
            passed = summary.get('passed', 0)
            failed = summary.get('failed', 0)
            skipped = summary.get('skipped', 0)
            error = summary.get('error', 0)
            
            print(f"Total Tests:    {total}")
            print(f"✅ Passed:      {passed}")
            print(f"❌ Failed:      {failed}")
            print(f"⏭️  Skipped:     {skipped}")
            print(f"🚨 Errors:      {error}")
            
            if total > 0:
                success_rate = (passed / total) * 100
                print(f"Success Rate:   {success_rate:.1f}%")
            
            # Show failed tests if any
            if failed > 0:
                print("\nFAILED TESTS:")
                print("-" * 40)
                for test in report.get('tests', []):
                    if test.get('outcome') == 'failed':
                        print(f"❌ {test.get('nodeid', 'Unknown test')}")
                        if 'call' in test and 'longrepr' in test['call']:
                            print(f"   Error: {test['call']['longrepr'][:100]}...")
            
            # Show test categories
            print("\nTEST CATEGORIES:")
            print("-" * 40)
            route_tests = [t for t in report.get('tests', []) if 'test_routes' in t.get('nodeid', '')]
            calculator_tests = [t for t in report.get('tests', []) if 'test_calculator' in t.get('nodeid', '')]
            
            route_passed = len([t for t in route_tests if t.get('outcome') == 'passed'])
            route_total = len(route_tests)
            
            calc_passed = len([t for t in calculator_tests if t.get('outcome') == 'passed'])
            calc_total = len(calculator_tests)
            
            print(f"Routes/API:     {route_passed}/{route_total} tests passed")
            print(f"Calculator:     {calc_passed}/{calc_total} tests passed")
            
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"\nNote: Could not load detailed test report: {e}")
            
            # Fallback to parsing stdout
            lines = result.stdout.split('\n')
            summary_line = None
            for line in lines:
                if 'passed' in line or 'failed' in line:
                    if '==' in line:
                        summary_line = line
                        break
            
            if summary_line:
                print(f"\nSummary: {summary_line.strip()}")
        
        print("\n" + "=" * 60)
        print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Clean up report file
        try:
            import os
            os.remove('test_report.json')
        except:
            pass
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"Error running tests: {e}")
        return False


def main():
    """Main function"""
    success = run_tests()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()