import ipaddress
import socket
import sys
import threading

# initialize empty list to keep track of incoming and outgoing connections
all_connections = []
connection_id =1
def start_server(port):
    """
    Function to start a server and listen for incoming connections
    """
    #get computer running the program's ip
    local_ip = get_local_ip()

    #set connection_id variable
    global connection_id

    #access the list 
    global all_connections

     # create a TCP socket 
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind to the address of computer running program and specified port number
    server_socket.bind((local_ip, port))

    # allow one connection at a time
    server_socket.listen(1)

    while True:
        client_socket, address = server_socket.accept()

        # use f string to print ip address (address[0]) and port number (address[1])
        print(f"\nAccepted connection from {address[0]}:{address[1]}")

        # add the client socket to the appropriate list
        all_connections.append({'id': connection_id, 'ip': address[0], 'port no.': address[1], 'socket': client_socket})

        #increment id for next connection
        connection_id += 1

        # create a new thread to handle communication with the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address,all_connections,server_socket))
        client_thread.start()

def remove_connection(connections, address):
    """
    Function to remove a connection from the list of connections
    """
    for connection in connections:
        if connection['ip'] == address[0] and connection['port no.'] == address[1]:
            connections.remove(connection)
            break
    else:
        print(f"Client {address[0]}:{address[1]} not found in connections list.")




# Handles server-to-client communication
def handle_client(client_socket, address, connections, server_socket):
    """
    Function to handle communication with a client
    """
    # calls to .recv won't block program
    client_socket.setblocking(False)

    while True:
        try:
            # get the message client inputs into command line from Line 73
            message = client_socket.recv(1024).decode()
            if not message:
                
                print(f"Connection from {address[0]}:{address[1]} terminated.")
                msg = (f"Connection from {address[0]}:{address[1]} terminated.")
                client_socket.sendall(msg.encode())
                client_socket.close()
                remove_connection(connections,address)
                break
                # the host server client sent message to will print the message to console 
            else:
                print(f"\nReceived message from {address[0]}:{address[1]} Message: {message}")
                
        # error handling
        except BlockingIOError:
            continue
        except ConnectionResetError:
            print(f"Client {address[0]}:{address[1]} disconnected.")
            remove_connection(connections, address)
            break
        except BrokenPipeError:
            print(f"Client socket {address[0]}:{address[1]} terminated.")
            remove_connection(connections, address)
            break
        except socket.error:
            print(f"Socket error with client {address[0]}:{address[1]}.")
            remove_connection(connections, address)
            break
        except ValueError:
            print(f"Empty message received from client {address[0]}:{address[1]}.")
            remove_connection(connections, address)




def list_connections():
    """
    Function to list all connections in all_connections dictionary
    """
    print("All connections:")

    # i is used as an index, connection represents each dictionary, enumerate allows us to iterate through list of dictionaries
    for i, connection in enumerate(all_connections):
     print(f"ID: {connection['id']}, IP: {connection['ip']}, Port: {connection['port no.']}")

def send():
    """
    Function to send a message to a connection ID
    """
    connection_id = int(input("Enter the connection ID to send message to: "))
    message = input("Enter message to send: ")

    # find the connection with the given ID
    for connection in all_connections:
        if connection['id'] == connection_id:
            try:
                # send the message to the connection
                connection['socket'].sendall(message.encode())
                print(f"\nMessage sent to connection {connection_id}")
            except OSError:
                print(f"\nError sending message to connection {connection_id}")
            return

    # if no connection with the given ID is found
    print(f"\nNo connection found with ID {connection_id}")

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


def myPort(port):
    """
    Function to display the current process's port
    """
    print("Current port number:", port)


def help(port):
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
        try:
         if choice ==1:
            help()
         elif choice == 2:
            myIp()
         elif choice == 3:
            myPort(port)
         elif choice == 4:
            connect()
         elif choice == 5:
            list_connections()
         elif choice == 6:
            terminate(all_connections)
         elif choice == 7:
            send()
         elif choice == 8:
            exit()
         else:
                print("\nInvalid choice. Please enter a valid option number.")
        except ValueError:
            print("\nInvalid input. Please enter a valid integer.")
def exit():
    """
    Function to close all connections and terminate the program
    """
    global all_connections
    
    # Close all connections
    for connection in all_connections:
        try:
            connection['socket'].shutdown(socket.SHUT_RDWR)
            connection['socket'].close()
        except OSError:
            pass
    
    # Remove all connections from the list
    all_connections = []

    # Terminate the program
    print("Exiting program...")
    sys.exit(0)


def get_local_ip():
    """
    Function to get the local IP address of the machine
    """
    return socket.gethostbyname(socket.gethostname())

            
def is_valid_ip(ip):
    if ip == 'localhost':
        return True
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False
    
def terminate(all_connections):
    """
    Function to terminate a connection
    """
    id = int(input("Enter the ID of the connection to terminate: "))
    for connection in all_connections:
        #find connection in list using id
        if connection['id'] == id:
            try:

                #shut down socket 
                connection['socket'].shutdown(socket.SHUT_RDWR)
                
                #close socket
                connection['socket'].close()

                #remove from list
                all_connections.remove(connection)
                print(f"Connection with ID {id} terminated.")
            except OSError:
                print(f"Error terminating connection with ID {id}")
            return
    print(f"No connection with ID {id} found.")

          

def connect():
    global connection_id
    while True:
        # get host address
        host = input("Enter host address: ")
        if is_valid_ip(host):
            break  # exit loop if IP is valid
        else:
            print("Invalid IP address, please input a valid IP address!")

    while True:
        try:
            port = int(input("Enter port number: "))
            break  # Exit the loop if input is valid
        except ValueError:
            print("Invalid port number, please enter a valid integer.")

    # create the client socket and connect to the server
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host,port))
        client_socket.setblocking(False)
        print(f"Connected to {host}:{port}")
        # add the client socket to the all_connections list
        all_connections.append({'id': connection_id, 'ip': host, 'port no.': port, 'socket': client_socket})
        # increment id for next connection
        
        connection_id += 1
    except ConnectionRefusedError:
        print("Connection refused. Please check the host and port number.")
    except OSError as e:
        print(f"Error connecting to {host}:{port}: {e}")
    # return the client socket object to the main program loop
    return client_socket

    
            

# if program is main program run on command line this block of code will be executed first
if __name__ == '__main__':

    #get the first argument given after argv[0], (name of program itself)
    port = int(sys.argv[1])
    
    #seperate thread for server, and handling clients
    server_thread = threading.Thread(target=start_server, args=(port,))
    server_thread.start()

    #check if thread is alive, then call for options
    if server_thread.is_alive():
        print("Server started... ")
        help(port)

        
    
    