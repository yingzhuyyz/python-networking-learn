#!/usr/bin/env python3
# Multi-threaded sphinx server

import helpers
from threading import Thread

def start_threads(listener, numThreads=5):
    param = (listener,)
    for i in range(numThreads):
        Thread(target=helpers.setup_connections, args=param).start()

if __name__ == '__main__':
    address = helpers.get_address()
    listener = helpers.get_server_socket(address)
    start_threads(listener)
