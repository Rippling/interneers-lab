import os
import subprocess
import sys

def run_tests():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)
    
    try:
        subprocess.check_call(["coverage", "run", "--source=.", "-m", "unittest", "discover", "-s", "tests"])
        subprocess.check_call(["coverage", "report", "-m"])
        subprocess.check_call(["coverage", "html"])
    except subprocess.CalledProcessError as e:
        print("Error while running tests or generating coverage report", e)
        sys.exit(1)

if __name__ == '__main__':
    run_tests()