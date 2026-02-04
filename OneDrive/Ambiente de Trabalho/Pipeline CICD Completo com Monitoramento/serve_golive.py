#!/usr/bin/env python3
"""
Simple HTTP server to serve GO_LIVE.html locally
Allows the buttons to work correctly with file serving
"""

import http.server
import socketserver
import os
import webbrowser
from urllib.parse import urljoin

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/GO_LIVE.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)
    
    def end_headers(self):
        # Add headers to prevent caching
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()
    
    def log_message(self, format, *args):
        # Custom logging
        if '200' in str(args):
            print(f"✅ {args[0]}")
        elif '404' in str(args):
            print(f"❌ {args[0]}")
        else:
            print(f"ℹ️  {args[0]}")

def run_server():
    """Run the HTTP server"""
    os.chdir(DIRECTORY)
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        server_url = f"http://localhost:{PORT}"
        
        print("\n" + "="*60)
        print("🚀 GO LIVE Dashboard Server")
        print("="*60)
        print(f"✅ Servidor iniciado em: {server_url}")
        print(f"📁 Diretório: {DIRECTORY}")
        print(f"🌐 Abrindo navegador em 2 segundos...")
        print("="*60)
        print("Pressione Ctrl+C para parar o servidor\n")
        
        # Wait a moment then open browser
        import time
        time.sleep(2)
        
        try:
            webbrowser.open(server_url)
        except Exception as e:
            print(f"⚠️  Não conseguiu abrir o navegador automaticamente")
            print(f"   Abra manualmente: {server_url}")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n✋ Servidor parado")
            httpd.shutdown()

if __name__ == "__main__":
    run_server()
