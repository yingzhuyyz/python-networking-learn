#!/usr/bin/env python3
# First try at a basic asynchronous sphinx server
# by using the OS-provided poll() system call in the select library

import select, helpers

def poll_for_events(poller):
    while True:
        for fd, event in poller.poll():
            yield fd, event

def run_server(listenSock):
    # Maintain a dictionary of <key, value> pairs
    # where value is a socket and key is the socket's file descriptor.
    # Initialize it with the listener socket.
    # Also maintain a list of addresses for the sockets connecting to clients,
    # initially empty.

	sockets = {listenSock.fileno(): listenSock}
	addresses = {}
	data_recv = {}
	data_send = {}

	poller = select.poll()
	poller.register(listener, select.POLLIN)

	for fd, event in poll_for_events(poller):
		sock = sockets[fd]

if __name__ == '__main__':
	addr = helpers.get_address()
	listenSock = helpers.get_server_socket(addr)
	run_server(listenSock)
