#!/usr/bin/env python3

import socket, sys
from datetime import datetime

MAX_BYTES = 65535

def client(host, port):
    cSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print('I was assigned the address {}'.format(cSock.getsockname()))
    address = (host,  port)
    cSock.connect((host, port))
    sentence = 'Current time is {}'.format(datetime.now())
    msg = sentence.encode('ascii')
    delay = 0.1     # start with waiting 0.1 seconds
    while True:
        cSock.send(msg)
        print('Delay set at {} seconds to wait to hear from server'.format(delay))
        cSock.settimeout(delay)
        try:
            msg = cSock.recv(MAX_BYTES)
        except socket.timeout:
            delay *= 2  # exponential waiting time
            if delay > 2.0:
                raise RuntimeError('Cannot receive data from server')
        else:
            break
    sentence = msg.decode('ascii')
    print('The server said: {}'.format(sentence))

if __name__ == '__main__':
    # pass to client the server IP address and port number
    client(sys.argv[1], int(sys.argv[2]))
