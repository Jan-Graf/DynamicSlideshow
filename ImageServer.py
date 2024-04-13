from http.server import BaseHTTPRequestHandler, HTTPServer
import os

# directory to store the frontend
static_dir = "C:\\Users\\Jan\\Documents\\Python Scripts\\DynamicSlideshow"
# directory to store the images
upload_dir = "C:\\Users\\Jan\\Documents\\Python Scripts\\DynamicSlideshow\\Images"

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        try:
            # Öffne die angeforderte Datei
            with open(static_dir + self.path, 'rb') as file:
                # Lese den Inhalt der Datei
                content = file.read()
            # Setze den Statuscode und die Content-Type-Header
            self.send_response(200)
            if self.path.endswith(".html"):
                self.send_header('Content-type', 'text/html')
            elif self.path.endswith(".css"):
                self.send_header('Content-type', 'text/css')
            elif self.path.endswith((".js", ".mjs")):
                self.send_header('Content-type', 'text/javascript')
            self.end_headers()
            # Sende den Inhalt der Datei als Response
            self.wfile.write(content)
        except FileNotFoundError:
            # Wenn die Datei nicht gefunden wurde, sende einen 404 Fehler
            self.send_error(404, 'File Not Found: %s' % self.path)

    
def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print("Server running on Port", port)
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()