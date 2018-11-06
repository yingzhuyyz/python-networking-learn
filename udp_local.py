#!/usr/bin/env python3

import argparse

def client(port):
    print("I'm the client, send UDP packets to port %d of the server." % port)

def server(port):
    print("I'm the server, listening at port %d." % port)

if __name__ == '__main__':
    roles = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='send and receive UDP packets locally')
    parser.add_argument('role', choices=roles, help='set the role as server or client')
    parser.add_argument('-port', type=int, default=1234, help='UDP port number (default 1234)')
    args = parser.parse_args()
    function = roles[args.role]
    function(args.port)

