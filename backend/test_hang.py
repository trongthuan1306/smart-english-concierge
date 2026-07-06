import sys
import threading
import time
import traceback

def dump_tracebacks():
    print("Dumping...")
    for t, f in sys._current_frames().items():
        print(f"Thread {t}")
        print("".join(traceback.format_stack(f)))
    sys.exit(1)

def main():
    timer = threading.Timer(3.0, dump_tracebacks)
    timer.start()
    try:
        from fastapi.testclient import TestClient
        from main import app
        client = TestClient(app)
        print("Testing /docs...")
        client.get("/docs")
        print("Done")
    finally:
        timer.cancel()

if __name__ == "__main__":
    main()
