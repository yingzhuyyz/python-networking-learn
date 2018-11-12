#!/usr/bin/env python3

import sys, socket

# run udp_local.py client first
# then run this with the port number assigned to client

if __name__ == '__main__':
    port = int(sys.argv[1]) 
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto("I'm fake".encode('ascii'), ('127.0.0.1', port))
