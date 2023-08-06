from __future__ import absolute_import

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

import algocash_sdk
from algocash_sdk.callback import SignatureVerificationException

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("Hello", "utf-8"))
    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))
        
        try:
            print("Signature: %s\n" % self.headers['Signature'])
            callback = algocash_sdk.Callback()
            data = callback.construct_callback(post_data.decode('utf-8'), self.headers['Signature'], '4q4epHrbUHykQwnc')
            logging.info(data)
            print(data)
        except SignatureVerificationException as e:
            print("SignatureVerificationException when listening callback: %s\n" % e)
            self.send_response(401)
        except ValueError as e:
            print("ValueError Exception when listening callback: %s\n" % e)
            self.send_response(500)
            
        self.send_response(200)

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")