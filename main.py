from __future__ import print_function, unicode_literals

import os
import re
import socket
import sys
from builtins import input
from threading import Event, Thread
import socket
import logging
import json

logging.basicConfig(filename="server.log",
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')

with open("appsettings.json", "r") as read_file:
    config = json.load(read_file)


class TcpServer:

    def __init__(self, port, family_addr, persist=False):
        self.port = port
        self.socket = socket.socket(family_addr, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.settimeout(60.0)
        self.shutdown = Event()
        self.persist = persist
        self.family_addr = family_addr

    def __enter__(self):
        try:
            self.socket.bind(('', self.port))
        except socket.error as e:
            print('Bind failed:{}'.format(e))
            raise
        self.socket.listen(1)

        print('Starting server on port={} family_addr={}'.format(
            self.port, self.family_addr))
        self.server_thread = Thread(target=self.run_server)
        self.server_thread.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.persist:
            sock = socket.socket(self.family_addr, socket.SOCK_STREAM)
            sock.connect(('localhost', self.port))
            sock.sendall(b'Stop', )
            sock.close()
            self.shutdown.set()
        self.shutdown.set()
        self.server_thread.join()
        self.socket.close()

    def run_server(self):
        while not self.shutdown.is_set():
            try:
                conn, address = self.socket.accept()  # accept new connection
                print('Connection from: {}'.format(address))
                conn.setblocking(1)
                data = conn.recv(config["BUFFSIZE"])
                if not data:
                    return
                #ata = data.decode()
                print('Received data: ', data)
                reply = data
                conn.send(reply.encode())
                conn.close()
            except socket.error as e:
                print('Running server failed:{}'.format(e))
                raise
            if not self.persist:
                break


def printlog(message):
    print(message)
    logging.info(message)


def main():
    with TcpServer(config["PORT"], family_addr=socket.AF_INET, persist=True) as s:
        print(input('Press Enter stop the server...'))


if __name__ == "__main__":
    main()
