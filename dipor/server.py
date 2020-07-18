import http.server
import socketserver
from os import listdir
import os

PORT = 5050

# def runserver(public_folder):
#     class CustomHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
#         def __init__(self, *args, **kwargs):
#             self.public = public_folder
#             super(CustomHttpRequestHandler, self).__init__(*args, **kwargs)
            
#         def do_GET(self):
#             path = self.path.strip('/')
#             if path == "":
#                 self.path = os.path.join(self.public, 'index.html')
#                 # return http.server.SimpleHTTPRequestHandler.do_GET(self)

#             for file in listdir(self.public):
#                 if file == path and os.path.isdir(os.path.join(self.public, file)):
#                     print(path, "-->", os.path.join(self.public, file, "index.html"))
#                     self.path = os.path.join(self.public, file, "index.html")

#             return http.server.SimpleHTTPRequestHandler.do_GET(self)
#     handler = CustomHttpRequestHandler
#     socketserver.TCPServer.allow_reuse_address = True

#     with socketserver.TCPServer(("", PORT), handler) as httpd:
#         print("server is running...")
#         httpd.serve_forever()


def runserver():
    web_dir = os.path.join(os.path.dirname(__file__), 'public')
    os.chdir(web_dir)

    Handler = http.server.SimpleHTTPRequestHandler
    socketserver.TCPServer.allow_reuse_address = True
    # httpd = socketserver.TCPServer(("", PORT), Handler)
    print("serving at port", PORT)
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()

