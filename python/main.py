import subprocess
import os
import sys


def run_pipeline():

    current_dir = os.path.dirname(__file__)

    for script in ["cleaning.py", "create_database.py", "analysis.py", "visualisation.py"]:
        print(f"\n>>> Running {script}")
        subprocess.run([sys.executable, os.path.join(current_dir, script)], check=True)

if __name__ == "__main__":
    run_pipeline()
