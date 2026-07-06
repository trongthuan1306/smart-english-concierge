import subprocess
import time
import requests
import sys

def test_uvicorn():
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    try:
        # Wait for startup
        time.sleep(5)
            
        print("Making request...")
        try:
            r = requests.get("http://127.0.0.1:8000/docs", timeout=5)
            print("Status:", r.status_code)
        except requests.exceptions.Timeout:
            print("Request timed out (hung)!")
        except Exception as e:
            print("Request failed:", e)
            
        # Print uvicorn output
        process.terminate()
        out, _ = process.communicate()
        print("Uvicorn Output:\n", out)
            
    finally:
        process.terminate()
        process.wait()
        
if __name__ == "__main__":
    test_uvicorn()
