import subprocess
import os
import sys


def run_pipeline():

    current_dir = os.path.dirname(__file__)

    subprocess.run([sys.executable, os.path.join(current_dir, "analysis.py")])
    subprocess.run([sys.executable, os.path.join(current_dir, 'visualisation.py')])

if __name__ == "__main__":
    run_pipeline()
    
    