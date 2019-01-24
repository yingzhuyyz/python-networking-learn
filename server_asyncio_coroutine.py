# Using the asyncio module to create a coroutine
# which pauses when it performs I/O and returns control to caller
# instead of blocking in an IO

import asyncio, helpers

@asyncio.coroutine
def communicate(receiver, sender):
	# address of client on the other end of this connection
	addr = sender.get_extra_info('peername')
	print('Connected to {}'.format(addr))
	while True:
		data = b''
		while not data.endswith(b'?'):
			more = yield from receiver.read(4096)
			if not more:
				if data:
					print('Client {} sent {} then closed connection'.format(addr,
data))
				else:	
					print('Client {} closed connection'.format(addr))
				return
			data += more
		reply = helpers.make_reply(data)
		sender.write(reply)

if __name__ == '__main__':
	addr = helpers.get_address()
	loop = asyncio.get_event_loop()
	coroutine = asyncio.start_server(communicate, *addr)
	server = loop.run_until_complete(coroutine)
	print('Listening for incoming connections at {}'.format(addr))
	try:
		loop.run_forever()
	finally:
		server.close()
		loop.close()
