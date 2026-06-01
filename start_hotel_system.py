import webbrowser
import threading
import time
import os
from app import create_app

def open_browser():
    # Wait a bit for the server to start
    time.sleep(1.5)
    print("\n[SYSTEM] Opening Eastay Hotel System in your browser...")
    webbrowser.open("http://127.0.0.1:5000/")

if __name__ == "__main__":
    print("[SYSTEM] Starting Eastay Hotel Management System...")
    
    # Start browser in a separate thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Run the app
    app = create_app()
    app.run(host='127.0.0.1', port=5000, debug=False)
