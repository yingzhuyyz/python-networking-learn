#!/usr/bin/env python3
# Simple single-threaded sphinx server

import helpers

if __name__ == '__main__':
    address = helpers.get_address()
    listener = helpers.get_server_socket(address)
    helpers.setup_connections(listener)
