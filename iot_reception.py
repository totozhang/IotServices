import socket
import threading


class IOTMsgReception(threading.Thread):

    def __init__(self, identifier, name, queue, ipaddr, port, buffersize):
        threading.Thread.__init__(self)
        self.identifier = identifier
        self.buffersize = buffersize
        self.name = name
        self.queue = queue
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((ipaddr, port))

    def __del__(self):
        self.close()

    def get(self):
        data, addr = self.sock.recvfrom(self.buffersize)
        return bytes.decode(data)

    def close(self):
        self.sock.close()

    def run(self):
        while True:
            msg = self.get()
            self.queue.put(msg)
