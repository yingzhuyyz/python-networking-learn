#!/usr/bin/env python3
# TCP server receives chunks of data from client, each chunk is prefixed with the length of the data in that chunk.

from socket import *
import sys, struct

# A header is a struct, of 4 bytes
# The symbol 'I' means a 32-bit unsigned integer
# Each message chunk can be up to 2^32 in length
header = struct.Struct('!I')

def recvall(serverSock, length):
    parts = []
    while length:
        data = serverSock.recv(length)
        if not data:
            break
        length -= len(data)
        parts.append(data)
    return b''.join(parts)

def recv_chunk(serverSock):
    message = recvall(serverSock, header.size)
    (chunk_length,) = header.unpack(message)
    return recvall(serverSock, chunk_length)

def send_chunk(clientSock, chunk):
    chunk_length = len(chunk)
    clientSock.send(header.pack(chunk_length))
    clientSock.send(chunk)

def server(interface, port):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind((interface, port))
    sock.listen(1)
    print('Waiting for incoming connection at', sock.getsockname())
    ss, sockname = sock.accept()
    print('Connection accepted from', sockname)
    ss.shutdown(SHUT_WR)
    while True:
        chunk = recv_chunk(ss)
        if not chunk:
            break
        print('Received chunk:', repr(chunk))
    ss.close()
    sock.close()

def client(host, port):
    cs = socket(AF_INET, SOCK_STREAM)
    cs.connect((host, port))
    cs.shutdown(SHUT_RD)
    send_chunk(cs, b'Never let truth get in the way of a good story.')
    send_chunk(cs, b'Eighty percent of success is showing up.')
    send_chunk(cs, b'Pursue what is meaningful, not what is expedient.')
    send_chunk(cs, b'')
    cs.close()

if __name__ == '__main__':
    functions = {'client': client, 'server': server}
    role = sys.argv[1]
    host = sys.argv[2]
    port = int(sys.argv[3])
    function = functions[role]
    function(host, port)
