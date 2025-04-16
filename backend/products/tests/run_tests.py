#!/usr/bin/env python
# run_tests.py
import os
import sys
import pytest

def run_integration_tests():
    
    print("Starting MongoDB integration tests...")
   
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, project_root)
    
    # Define test arguments
    args = [
        '--verbose',
        'tests/test_api_integration.py',
        '-v'
    ]
    
    # Run the tests
    result = pytest.main(args)
    
    # Return the exit code
    return result

if __name__ == "__main__":
    sys.exit(run_integration_tests())