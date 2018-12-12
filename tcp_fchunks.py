#!/usr/bin/env python3
# TCP server receives chunks of data from client, each chunk is prefixed with the length of the data in that chunk.
# Client reads lines from a file, converts each line to a byte string (Python bytes object) and sends it to server.

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
    data = recvall(serverSock, header.size)
    (chunk_length,) = header.unpack(data)
    return recvall(serverSock, chunk_length)

def send_chunk(clientSock, chunk):
    chunk_length = len(chunk)
    clientSock.send(header.pack(chunk_length))
    clientSock.send(chunk)

def server(interface, port, fn):
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

def client(host, port, fn):
    cs = socket(AF_INET, SOCK_STREAM)
    cs.connect((host, port))
    cs.shutdown(SHUT_RD)
    with open(fn) as f:
        for line in f:
            line = line.rstrip('\n')
            send_chunk(cs, bytes(line, 'utf-8'))
    send_chunk(cs, b'')
    cs.close()

if __name__ == '__main__':
    functions = {'client': client, 'server': server}
    role = sys.argv[1]
    host = sys.argv[2]
    port = int(sys.argv[3])
    fn = sys.argv[4]
    function = functions[role]
    function(host, port, fn)
