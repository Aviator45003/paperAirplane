import threading
import Queue

# Non Standard
import gui
import ldaemon

class ClientControl():
    def __init__(self):
        self.countQueue = Queue.Queue()

        self.threads = []
        self.threads.append(threading.Thread(target=gui.run_window, args=(self.countQueue,)))

        for thread in self.threads:
            thread.daemon = True
            thread.start()

        for thread in self.threads:
            thread.join()

if __name__ == "__main__":
    test = ClientControl()
