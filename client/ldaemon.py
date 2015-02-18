import SocketServer
import logging
import getuser

class RequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        name = getuser.lookup_username()
        logging.debug("Returning that user is %s", name)
        self.request.send(name + '\n')

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Starting ldaemon in test mode")
    logging.info("Attempting to bind to port")
    server = SocketServer.TCPServer(("localhost", 3200), RequestHandler)
    server.serve_forever()
