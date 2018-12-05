#!/usr/bin/env python3

from socket import *
import argparse, sys

def recvall(sock, length):
    data = b''
    while len(data) < length:
        nextbytes= sock.recv(length - len(data))
        if not nextbytes:
                raise EOFError('was supposed to receive %d bytes'
                    ' but only received %d bytes' % (length, len(data)))
        data += nextbytes
    return data

def server(interface, port):
    serverSock = socket(AF_INET, SOCK_STREAM)
    serverSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSock.bind((interface, port))
    serverSock.listen(1)
    print('Listening at', serverSock.getsockname())
    while True:
        connSock, sockname = serverSock.accept()
        print('Accepted a connection from', sockname)
        print('--- Socket name:', connSock.getsockname())
        print('--- Socket peer:', connSock.getpeername())
        msg = recvall(connSock, 16)
        print('--- received 16-octet message:', repr(msg))
        connSock.sendall(b'Goodbye for now!')
        connSock.close()
        print('--- Sent bye to client')

def client(host, port):
    clientSock = socket(AF_INET, SOCK_STREAM)
    clientSock.connect((host, port))
    print('I am assigned', clientSock.getsockname())
    clientSock.sendall(b'Hello world!!!!!')
    reply = recvall(clientSock, 16)
    print('Got the reply', repr(reply))
    clientSock.close()

if __name__ == '__main__':
    roles = {'client': client, 'server': server}
    function = roles[sys.argv[1]]
    host = sys.argv[2]
    port = int(sys.argv[3])
    function(host, port)
