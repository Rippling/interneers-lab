#!/usr/bin/env python
import os
import sys
import subprocess
import argparse

def run_tests(test_type=None, verbose=False, coverage=True):
    """
    Run the test suite with the given parameters.
    
    Args:
        test_type (str): The type of tests to run ('unit' or None for all)
        verbose (bool): Whether to run tests in verbose mode
        coverage (bool): Whether to generate a coverage report
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
    
    # Build the pytest command
    cmd = ["pytest"]
    
    # Add markers if a specific test type is requested
    if test_type:
        cmd.append(f"-m {test_type}")
    
    # Add verbose flag if requested
    if verbose:
        cmd.append("-v")
    
    # Add coverage flags if requested
    if coverage:
        cmd.append("--cov=products")
        cmd.append("--cov-report=term")
        cmd.append("--cov-report=html:coverage_html")
    
    # Join the command parts
    cmd_str = " ".join(cmd)
    
    # Run the tests
    print(f"Running tests with command: {cmd_str}")
    result = subprocess.run(cmd_str, shell=True)
    
    # Return the exit code
    return result.returncode

def main():
    parser = argparse.ArgumentParser(description='Run ProductAPI tests')
    parser.add_argument('--type', choices=['unit', 'integration', 'all'], 
                        default='all', help='Type of tests to run')
    parser.add_argument('--verbose', '-v', action='store_true', 
                        help='Run tests in verbose mode')
    parser.add_argument('--no-coverage', action='store_true', 
                        help='Disable coverage reporting')
    
    args = parser.parse_args()
    
    # Map 'all' to None for run_tests function
    test_type = args.type if args.type != 'all' else None
    
    # Run the tests
    exit_code = run_tests(
        test_type=test_type,
        verbose=args.verbose,
        coverage=not args.no_coverage
    )
    
    # Exit with the same code as the tests
    sys.exit(exit_code)

if __name__ == "__main__":
    main() 