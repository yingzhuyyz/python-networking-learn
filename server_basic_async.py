#!/usr/bin/env python3
# First try at a basic asynchronous sphinx server
# by using the OS-provided poll() system call in the select library

import select, helpers

def poll_for_events(poller):
    while True:
        for fd, event in poller.poll():
            yield fd, event

def run_server(listener):
    # Maintain a dictionary of <key, value> pairs
    # where value is a socket and key is the socket's file descriptor.
    # Initialize it with the listener socket.
    # Also maintain a list of addresses for the sockets connecting to clients,
    # initially empty.
    sockets = {listener.fileno(): listener}
    addresses = {}

    # create the poll object for polling the sockets
    poller = select.poll()
    # register listener socket with the poll object to receive data only
    poller.register(listener, select.POLLIN)

    for fd, event in poll_for_events(poller):
        # find socket for file descriptor returned by poll object
        sock = sockets[fd]

        # new client, add new socket to list
        if sock is listener:
            
        # data ready to receive
        
        # socket ready to send data

if __name__ == '__main__':
    address = helpers.get_address()
    listener = helpers.get_server_socket(address)
    run_server(listener)
