import http.server
import socketserver
from os import listdir
import os

PORT = 5050

def runserver(public_folder):
    class CustomHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            self.public = public_folder
            super(CustomHttpRequestHandler, self).__init__(*args, **kwargs)
            
        def do_GET(self):
            print(self.public)
            path = self.path.strip('/')
            print(path)
            if path == "":
                self.path = os.path.join(self.public, 'index.html')
            else:
                for file in listdir(self.public):
                    print(file)
                    if file == path and os.path.isdir(os.path.join(self.public, file)):
                        self.path = os.path.join(self.public, file, "index.html")

            return http.server.SimpleHTTPRequestHandler.do_GET(self)
    handler = CustomHttpRequestHandler
    socketserver.TCPServer.allow_reuse_address = True

    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print("server is running...")
        httpd.serve_forever()