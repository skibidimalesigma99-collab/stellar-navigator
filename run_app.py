import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
        
    def log_message(self, format, *args):
        # Quiet log
        pass

def start_server():
    os.chdir(DIRECTORY)
    port = PORT
    for p in range(PORT, PORT + 20):
        try:
            httpd = socketserver.TCPServer(("", p), Handler)
            port = p
            break
        except OSError:
            continue
            
    url = f"http://localhost:{port}/index.html"
    print("=" * 65)
    print("  3D STELLAR CARTOGRAPHY & GRID NAVIGATOR")
    print("=" * 65)
    print(f"  Server running locally at: {url}")
    print(f"  Serving directory: {DIRECTORY}")
    print("  Press Ctrl+C to stop server at any time.")
    print("=" * 65)
    
    webbrowser.open(url)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        httpd.server_close()

if __name__ == "__main__":
    start_server()
