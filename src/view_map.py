#!/usr/bin/env python3
"""
Simple script to view the interactive risk map in a web browser.
Opens the HTML file using Python's built-in HTTP server if needed.
"""

import os
import sys
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

def open_map_direct(file_path):
    """Try to open the map file directly in browser."""
    file_path = os.path.abspath(file_path)
    if not os.path.exists(file_path):
        print(f"ERROR: File not found: {file_path}")
        return False
    
    print(f"Opening map: {file_path}")
    print("If the map doesn't load, try the HTTP server option below.")
    
    # Open in default browser
    webbrowser.open(f'file://{file_path}')
    return True

def serve_map_http(file_path, port=8000):
    """Serve the map via HTTP server."""
    file_path = os.path.abspath(file_path)
    file_dir = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)
    
    if not os.path.exists(file_path):
        print(f"ERROR: File not found: {file_path}")
        return False
    
    # Change to the directory containing the file
    os.chdir(file_dir)
    
    # Create a custom handler that serves the specific file
    class MapHandler(SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/' or self.path == f'/{file_name}':
                self.path = f'/{file_name}'
            return SimpleHTTPRequestHandler.do_GET(self)
    
    server_address = ('', port)
    httpd = HTTPServer(server_address, MapHandler)
    
    url = f'http://localhost:{port}/{file_name}'
    print(f"\n{'='*60}")
    print(f"Serving map at: {url}")
    print(f"{'='*60}")
    print(f"\nMap will open in your browser automatically.")
    print(f"Press Ctrl+C to stop the server.\n")
    
    # Open browser
    webbrowser.open(url)
    
    # Start server
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
        httpd.shutdown()
    
    return True

def main():
    """Main function."""
    # Default map file
    map_file = 'data/processed/nyc_risk_map.html'
    
    # Check if file exists
    if not os.path.exists(map_file):
        print(f"ERROR: Map file not found: {map_file}")
        print("\nPlease run the risk mapping script first:")
        print("  python src/example_risk_map_real_data.py")
        return
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == '--http' or sys.argv[1] == '-s':
            # Use HTTP server
            port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000
            serve_map_http(map_file, port)
        elif sys.argv[1] == '--help' or sys.argv[1] == '-h':
            print("Usage:")
            print("  python src/view_map.py           # Open directly in browser")
            print("  python src/view_map.py --http    # Serve via HTTP (recommended)")
            print("  python src/view_map.py --http 8080  # Use custom port")
        else:
            map_file = sys.argv[1]
            open_map_direct(map_file)
    else:
        # Try direct open first, suggest HTTP if it doesn't work
        print("Opening map directly in browser...")
        print("If it doesn't work, try: python src/view_map.py --http")
        print()
        open_map_direct(map_file)

if __name__ == '__main__':
    main()

