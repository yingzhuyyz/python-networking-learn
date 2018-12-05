from socket import *
import sys

serverSock = socket(AF_INET, SOCK_STREAM)

# Prepare a server socket
# Fill in begin

# Fill in end

while True:
    # Establish the connection
    print('Listening at', getsockname())
    connectionSocket, addr = # Fill in begin        # Fill in end
    try:
        message = # Fill in begin       # Fill in end
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = # Fill in start        # Fill in end
        # Send one HTTP header line into socket
        # Fill in begin

        # Fill in end

        # Send content of requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()
    except IOError:
        # Send response message for file not found
        # Fill in begin

        # Fill in end

        # Close client socket
        # Fill in begin

        # Fill in end

serverSocket.close()
sys.exit()
