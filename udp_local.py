#!/usr/bin/env python3

import argparse, socket
from datetime import datetime

MAX_BYTES = 65535

def server(port):
    sSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sSock.bind(('127.0.0.1', port))
    print('Listening at {}'.format(sSock.getsockname()))

    while True:
        msg, address = sSock.recvfrom(MAX_BYTES)
        sentence = msg.decode('ascii')
        print('Someone from {} said {!r}'.format(address, sentence))
        sentence = 'I received from you a message of {} bytes'.format(len(msg))
        msg = sentence.encode('ascii')
        sSock.sendto(msg, address)
    
def client(port):
    cSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    address = ('127.0.0.1', port)
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
    roles = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='send and receive UDP packets locally')
    parser.add_argument('role', choices=roles, help='set the role as server or client')
    parser.add_argument('-port', type=int, default=1234, help='UDP port number (default 1234)')
    args = parser.parse_args()
    function = roles[args.role]
    function(args.port)
