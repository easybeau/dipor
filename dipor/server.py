import http.server
import socketserver
from os import listdir
import os

PORT = 5050

class CustomHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        path = self.path.strip('/')
        for file in listdir('public/'):
            if file == path and os.path.isdir('public/'+file):
                self.path = 'public/'+file+"/main.html"

        return http.server.SimpleHTTPRequestHandler.do_GET(self)


handler = CustomHttpRequestHandler
socketserver.TCPServer.allow_reuse_address = True

with socketserver.TCPServer(("", PORT), handler) as httpd:
    print("server is running...")
    httpd.serve_forever()