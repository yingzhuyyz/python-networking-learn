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
        data = msg.decode('ascii')
        reqID = int(data.split(';')[0])
        if random.random() < 0.5:
            print('Drop packet {} from {}'.format(reqID, address))
            continue
        print('Packet with request ID {} from {}'.format(reqID, address))
        data = '{}; reply'.format(reqID)
        msg = data.encode('ascii')
        sSock.sendto(msg, address)
    
def client(host, port):
    cSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print('I was assigned the address {}'.format(cSock.getsockname()))
    address = (host,  port)
    cSock.connect((host, port))
    while True:
        reqID = int(random.random() * 1000000)   # random request ID
        print('generated request ID {}'.format(reqID))
        data = str(reqID) + ';' + ' request'
        msg = data.encode('ascii')
        cSock.send(msg)
        print('sent request {}'.format(reqID))
        delay = 0.1
        keep = True
        while True:
            cSock.send(msg)
            print('sent request {}'.format(reqID))
            cSock.settimeout(delay)
            try:
                msg = cSock.recv(MAX_BYTES)
            except socket.timeout:
                delay *= 2  # exponential waiting time
                print('setting delay to {}'.format(delay))
                if delay > 2.0:
                    print('waiting too long for reply to {}, giving up'.format(reqID))
                    keep = False 
                    break
            else:
                break
        if keep:
            data = msg.decode('ascii')
            reqID = int(data.split(';')[0])
            print('Reply for request ID {}'.format(reqID))

if __name__ == '__main__':
    roles = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='send and receive UDP packets locally')
    parser.add_argument('role', choices=roles, help='set the role as server or client')
    parser.add_argument('host', help='ip address (network interface) of server')
    parser.add_argument('-port', type=int, default=1234, help='UDP port number (default 1234)')
    args = parser.parse_args()
    function = roles[args.role]
    function(args.host, args.port)
