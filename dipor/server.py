import http.server
import socketserver
from os import listdir
import os

PORT = 5050

def runserver(public_folder):
    class CustomHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super(CustomHttpRequestHandler, self).__init__(*args, **kwargs)
            self.public = public_folder
        def do_GET(self):
            path = self.path.strip('/')
            for file in listdir(self.public):
                if file == path and os.path.isdir(os.path.join(self.public, file)):
                    self.path = os.path.join(self.public, file, "index.html")

            return http.server.SimpleHTTPRequestHandler.do_GET(self)
    handler = CustomHttpRequestHandler
    socketserver.TCPServer.allow_reuse_address = True

    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print("server is running...")
        httpd.serve_forever()