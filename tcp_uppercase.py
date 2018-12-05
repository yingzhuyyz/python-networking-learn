#!/usr/bin/env python3
# TCP server receives unlimited stream of characters from client and converts them to upper case.

from socket import *
import sys

def server(interface, port, numBytes):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind((interface, port))
    sock.listen(1)
    print('Waiting for incoming connection at', sock.getsockname())
    while True:
        connSock, sockname = sock.accept()
        print('Receiving data from', sockname)
        bytesSent = 0
        while True:
            data = connSock.recv(1024)
            if not data:
                break
            processedData = data.decode('ascii').upper().encode('ascii')
            connSock.sendall(processedData)
            bytesSent += len(data)
            print('  {} bytes already capitalized'.format(bytesSent))
            sys.stdout.flush()
        print()
        connSock.close()
        print('  Closed socket')

def client(host, port, numBytes):
    sock = socket(AF_INET, SOCK_STREAM)
    numBytes = (numBytes + 15) // 16 * 16   # round up to a multiple of 16
    data = b'hello foobar bye'   # 16-byte message to be repeatedly sent
    print('Going to send %d bytes in total, 16 bytes at a time')
    sock.connect((host, port))
    sent = 0
    while sent < numBytes:
        sock.sendall(data)
        sent += len(data)
        print('  {} bytes sent'.format(sent))
        sys.stdout.flush()
    print()
    sock.shutdown(SHUT_WR)

    recvBytes = 0
    while True:
        data = sock.recv(42)
        if not recvBytes:
            print('  First received:', repr(data))
        if not data:
            break
        recvBytes += len(data)
        print('  {} bytes received'.format(recvBytes))

    print()
    sock.close()

if __name__ == '__main__':
    functions = {'client': client, 'server': server}
    role = sys.argv[1]
    host = sys.argv[2]
    port = int(sys.argv[3])
    n = int(sys.argv[4])    # number of bytes
    function = functions[role]
    function(host, port, n)
