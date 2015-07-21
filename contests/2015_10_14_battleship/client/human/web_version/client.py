from web_socket_server import WebSocketServer


########################################################################
def on_message(self, message):
    # do something with message here
    print "Modified message action: " + message


########################################################################
if __name__ == "__main__":
    WebSocketServer(9999, on_message).serve()
