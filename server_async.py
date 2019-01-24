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
    data_recvd = {}
    data_send = {}

	for fd, event in poll_for_events(poller):
		sock = sockets[fd]	# poller returned this socket with its event
        # new client, add new socket to list
		if sock is listener:
       		connSock, addr = sock.accept()
            print('New connection set up from ' + address)
            connSock.setblocking(False)
            sockets[connSock.fileno()] = connSock
            addresses[connSock] = addr
            poller.register(connSock, select.POLLIN)

        # socket ready to receive data
        elif event & select.POLLIN:
            new_data = sock.recv(4096)
            if not new_data:    # no more data incoming
                sock.close()
                continue
            # pop bytes received earlier for this socket
            # if nothing popped, then default to empty byte string b''
            # append newly received bytes to these previously received bytes
            data = data_recvd.pop(sock, b'') + new_data
            if data.endswith(b'?'):     # question entirely received
                data_send[sock] = helpers.make_reply(data)
                # change this socket to be ready for sending data
                poller.modify(sock, select.POLLOUT)
	    else:
		# haven't seen '?' yet so store data for future
		data_recvd[sock] = data

	# socket ready to send data
	elif event & select.POLLOUT:
		data = data_send.pop(sock)
		numBytes = sock.send(data)
		if numBytes < len(data):
			# only numBytes sent, keep the rest in data_send to send later
			data_send[sock] = data[n:]
	    else:
			# sent out all the data, switch back to be ready to receive
			poller.modify(sock, select.POLLIN)

if __name__ == '__main__':
    address = helpers.get_address()
    listener = helpers.get_server_socket(address)
    run_server(listener)
