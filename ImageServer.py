from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime
import configparser
import os

config = configparser.ConfigParser()
config.read("config.ini")

# directory to store the frontend
static_dir = config["Slideshow"]["website_dir"]
# directory to store the images
upload_dir = config["Slideshow"]["img_dir"]

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
            # disable cors
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            # Sende den Inhalt der Datei als Response
            self.wfile.write(content)
        except FileNotFoundError:
            # Wenn die Datei nicht gefunden wurde, sende einen 404 Fehler
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        # parse the content type header to get the boundary
        content_type = self.headers['Content-Type']
        boundary = content_type.split("=")[1].encode()
        
        # read the content length
        content_length = int(self.headers['Content-Length'])        
        # read the raw POST data
        post_data = self.rfile.read(content_length)
        
        # find the position of the boundary
        boundary_pos = post_data.find(boundary)
        image_data = post_data[boundary_pos:]
        
        # find the position of the image data within the boundary
        image_pos = image_data.find(b'\r\n\r\n') + 4
        
        # extract the image data
        image_data = image_data[image_pos:]

        # setup filename containing the timestamp
        file_name = "Image " + datetime.now().strftime("%d-%m-%Y %H-%M-%S.%f") + ".jpg"
        
        # write the image data to a new file
        with open(os.path.join(upload_dir, file_name), 'wb') as f:
            f.write(image_data)
        
        # Send a response
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        # disable cors
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write('{"msg": "Success"}'.encode())
        
def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print("Server running on Port", port)
    httpd.serve_forever()

if __name__ == "__main__":
    port = int(config["Slideshow"]["port"])
    run_server(port)