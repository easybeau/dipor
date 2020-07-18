import http.server
import socketserver
from os import listdir
import os
import pathlib

PORT = 5050

def runserver():
    web_dir = os.path.join(pathlib.Path().absolute(), 'public')
    os.chdir(web_dir)
    class CustomHttpRequestHandler(http.server.SimpleHTTPRequestHandler):            
        def do_GET(self):
            path = self.path.strip('/')
            if path == "":
                self.path = os.path.join(web_dir, 'index.html')
            else:
                if os.path.isfile(os.path.join(web_dir, path+".html")):
                    print(os.path.join(web_dir, path+".html"))
                    self.path = os.path.join(web_dir, path+".html")
                elif os.path.isfile(os.path.join(path, "index.html")):
                    print(os.path.join(web_dir, path, "index.html"))
                    self.path = os.path.join(path, "index.html")
                
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
    handler = CustomHttpRequestHandler
    socketserver.TCPServer.allow_reuse_address = True

    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print("server is running...")
        httpd.serve_forever()


