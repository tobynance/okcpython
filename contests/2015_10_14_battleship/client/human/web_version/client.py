#!/usr/bin/env python
import os
import json
import BaseHTTPServer
from Queue import Queue, Empty

from_battleship_server = Queue()
to_battleship_server = Queue()


########################################################################
class WebServerRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    ####################################################################
    def send_head(self, content_type="text/html; charset=UTF-8"):
        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.send_header("Last-Modified", self.date_time_string())
        self.end_headers()

    ####################################################################
    def do_GET(self):
        # print "path:", self.path
        # print "request_version:", self.request_version
        # print "command:", self.command
        # print "client_address:", self.client_address
        if self.path == "/":
            self.send_head()
            self.wfile.write(open(os.path.join("www", "index.html")).read())
        elif self.path in ["/client.js", "/jquery.js"]:
            self.send_head(content_type="text/javascript; charset=UTF-8")
            self.wfile.write(open(os.path.join("www", self.path[1:])).read())
        elif self.path in ["/client.css"]:
            self.send_head(content_type="text/css")
            self.wfile.write(open(os.path.join("www", self.path[1:])).read())
        elif self.path == "/data.json":
            self.send_head(content_type="application/json; charset=UTF-8")
            self.wfile.write(json.dumps(self.get_messages_from_battleship_server()))
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.send_header("Last-Modified", self.date_time_string())
            self.end_headers()
            self.wfile.write("File not found")

    ####################################################################
    def do_POST(self):
        if self.path == "/data.json":
            print "handling POST to data.json"
            pass

    ####################################################################
    def get_messages_from_battleship_server(self):
        messages = []
        try:
            while True:
                messages.append(from_battleship_server.get_nowait())
        except Empty:
            pass
        return messages

    ####################################################################
    def send_message_to_battleship_server(self, message):
        to_battleship_server.put(message)


########################################################################
def main():
    server_address = ('', 8000)
    server = BaseHTTPServer.HTTPServer(server_address, WebServerRequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()


########################################################################
if __name__ == '__main__':
    main()
