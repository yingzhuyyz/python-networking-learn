#!/usr/bin/env python3
# Some helper methods for buliding a server

from socket import *
import sys, time, random

replies = [b'Yes definitely.', b'Very likely.', b'Maybe.', b'Not likely.', b'Nope.']

example_questions = [b'Will I be happy tomorrow?', 
                     b'Is general artificial intelligence possible?', 
                     b'Is there true free will?']

def make_reply(question):
    time.sleep(0.0) # tune sleep time to simulate processing time
    reply = question + b'  ' + replies[random.randint(0, 4)]
    return reply

def get_address():
    host = sys.argv[1]
    port = int(sys.argv[2])
    address = (host, port)
    return address

def get_server_socket(address):
    # create and return a listening socket
    listenSock = socket(AF_INET, SOCK_STREAM)
    listenSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    listenSock.bind(address)
    listenSock.listen(64)   # set number of unaccepted connections before refusal
    print('Listening at', str(address))
    return listenSock

def setup_connections(listenSock):
    # accept connections on listening socket
    while True:
        serverSock, address = listenSock.accept()
        print('Connection set up from', str(address))
        process_connection(serverSock, address)

def process_connection(serverSock, address):
    # reply to client questions until client closes connection
    try:
        while True:
            process_request(serverSock)
    except EOFError:
        print('Client socket to {} has closed'.format(address))
    except Exception as e:
        print('Client {} error: {}'.format(address, e))
    finally:
        serverSock.close()

def process_request(sock):
    # reply to a single request from client
    # receive bytes until the '?' delimiter
    question = recv_upto(sock, b'?')
    reply = make_reply(question)
    sock.sendall(reply)

def recv_upto(sock, delim):
    # receive bytes until the delimiter is seen
    data = sock.recv(4096)
    if not data:
        raise EOFError('socket closed')
    while not data.endswith(delim):
        more = sock.recv(4096)
        if not more:
            raise IOError('before socket closed, received', repr(more))
        data += more
    return data
