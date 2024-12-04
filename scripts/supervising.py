import subprocess
import time
import requests

def run_script():
    """Runs the main script and waits for it to complete."""
    while True:
        # Start the main script
        process = subprocess.Popen(["python3", "demo1.py"])
        
        # Wait for the script to complete
        process.wait()

        # Add delay or condition to avoid rapid restarts (optional)
        print("Restarting script...")
        time.sleep(1)

if __name__ == "__main__":
    run_script()