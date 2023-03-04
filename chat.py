import socket
import sys
import threading


def start_server(port):
    """
    Function to start a server and listen for incoming connections
    """
    # create a TCP socket 
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #bind to the address of computer running program and specified port number
    server_socket.bind(('localhost', port))

    #allow one connection at a time
    server_socket.listen(1)
    

    while True:
        client_socket, address = server_socket.accept()

        #use f string to print ip address (address[0]) and port number (address[1])
        print(f"Accepted connection from {address[0]}:{address[1]}")

        # Create a new thread to handle communication with the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

# Handles client - to - server communication
def handle_client(client_socket):
    """
    Function to handle communication with a client
    """
    #calls to .recv won't block program
    client_socket.setblocking(False)

    while True:
        try:
            # get the message client inputs into command line from Line 73
            message = client_socket.recv(1024).decode()
            if message:
            # the host server client sent message to will print the message to console 
                print(f"Received message: {message}")
            
            # this sends client's message to line 79 to be printed on client's console
                client_socket.sendall(f"Echo: {message}".encode())

            #error handling
        except BlockingIOError:
            continue
        except ConnectionResetError:
            print("Client disconnected")
            break

    client_socket.close()

#handles server - to - client communication 
def connect_to_peer(host, port):
    """
    Function to connect to a peer and send/receive messages
    """

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.setblocking(False)
    print(f"Connected to {host}:{port}")

    while True:
        try:
            message = input("Enter message (or type 'exit' to quit): ")
            if message.lower() == 'exit':
                break  # Exit the loop if user enters 'exit'
            client_socket.sendall(message.encode())
        except BlockingIOError:
            continue

        try:
            # decodes data sent from Line 46
            response = client_socket.recv(1024).decode()
            if response:
                print(f"Received response: {response}")
        except BlockingIOError:
            continue
        except ConnectionResetError:
            print("Server disconnected")
            break

    client_socket.close()

def myIp():
    """
    Function to display the current process's IP address
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # connect to public ip address, port 80 is commonly used for HTTP web traffic
    s.connect(('8.8.8.8', 80))

    #getsockname() returns tuple containing ip address and port number, getsockname()[0] for ip
    print("Current IP address:", s.getsockname()[0])
    s.close()   

def help1():
    """
    Function to display available options to the user
    """
    print("Options:")
    print("1) Help")
    print("2) myIp")
    print("3) myPort")
    print("4) connect")
    print("5) list")
    print("6) terminate")
    print("7) send")
    print("8) exit")

    while True:
        choice = int(input("Please enter your choice: "))
        if choice == 1:
            myIp()

     



# if program is main program run on command line this block of code will be executed first
if __name__ == '__main__':

    #get the first argument given after argv[0], (name of program itself)
    port = int(sys.argv[1])
    help1()
    #seperate thread for server, and handling clients
    server_thread = threading.Thread(target=start_server, args=(port,))
    server_thread.start()

    while True:
        host = input("Enter host IP address: ")
        if host.lower() == 'exit':
            break
        try:
            port = int(input("Enter port number: "))
            connect_to_peer(host, port)
        except ValueError:
            print("Invalid port number. Please enter a valid integer.")
