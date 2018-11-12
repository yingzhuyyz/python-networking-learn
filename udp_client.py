#!/usr/bin/env python3

import socket, sys
from datetime import datetime

MAX_BYTES = 65535

def client(host, port):
    cSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    address = (host, port)
    sentence = 'Current time is {}'.format(datetime.now())
    msg = sentence.encode('ascii')
    cSock.sendto(msg, address)
    print('I was assigned the address {}'.format(cSock.getsockname()))

    msg, msgSender = cSock.recvfrom(MAX_BYTES)    # not safe!
    sentence = msg.decode('ascii')
    print('The server said: {}'.format(sentence))

    # one option is to check if sender address matches server address
    # if msgSender == address:
    #     sentence = msg.decode('ascii')
    #     print('The server said: {}'.format(sentence))
    # else:
    #     print('Message received from stranger at {}'.format(msgSender))

if __name__ == '__main__':
    # pass to client the server ip address and port number
    client(sys.argv[1], int(sys.argv[2]))
