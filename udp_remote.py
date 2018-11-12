#!/usr/bin/env python3

import argparse, socket, random, sys
from datetime import datetime

MAX_BYTES = 65535

def server(host, port):
    sSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sSock.bind((host, port))
    print('Listening at {}'.format(sSock.getsockname()))
    while True:
        msg, address = sSock.recvfrom(MAX_BYTES)
        if random.random() < 0.8:
            print('Dropped packet from {}'.format(address))
            continue
        sentence = msg.decode('ascii')
        print('Someone from {} said {!r}'.format(address, sentence))
        sentence = 'I received from you a message of {} bytes'.format(len(msg))
        msg = sentence.encode('ascii')
        sSock.sendto(msg, address)
    
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
    roles = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='send and receive UDP packets locally')
    parser.add_argument('role', choices=roles, help='set the role as server or client')
    parser.add_argument('host', help='ip address (network interface) of server')
    parser.add_argument('-port', type=int, default=1234, help='UDP port number (default 1234)')
    args = parser.parse_args()
    function = roles[args.role]
    function(args.host, args.port)
