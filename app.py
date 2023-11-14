import socket
import select
from visualapp import ValueUpdater
import threading,csvcotroller
import queue
BATCHSIZE=20 #Speed for uodate statuses
APPENDBATCH=50
DATAFILENAME="data.csv"
Updatable=[]
Appendable=queue.Queue(APPENDBATCH+1)
# Function to set up the server socket
def setup_server_socket(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(125)
    return server_socket

# Function to handle incoming connections
def handle_new_connection(server_socket, inputs, buffers):
    client_socket, client_address = server_socket.accept()
    print(f"New connection from {client_address}")
    client_socket.setblocking(False)
    inputs.append(client_socket)
    buffers[client_socket] = b""

# Function to handle data from clients
def handle_client_data(sock, inputs, buffers):
    data = sock.recv(512)
    if data:
        print(f"Received data: {data} from {sock.getpeername()}")
        buffers[sock] += data
        data=data.decode()
        action=data[:6]
        values=data[6:].split(":")
        if "update" in action:
            Updatable.append(values)
            if len(Updatable) >BATCHSIZE:
                threading.Thread(target=csvcotroller.change_multiple_status_by_ip,args=(DATAFILENAME,Updatable,)).start()
                Updatable.clear()
        elif "append" in action:
            Appendable.put(values)
            if Appendable.qsize()>APPENDBATCH:
                threading.Thread(target=csvcotroller.append_batch_to_csv,args=(DATAFILENAME,[Appendable.get() for _ in range(Appendable.qsize())],)).start()
            
        if sock not in inputs:
            inputs.append(sock)
    else:
        # Connection closed by the client
        print(f"Connection closed by {sock.getpeername()}")
        inputs.remove(sock)
        sock.close()
        del buffers[sock]

# Function to send data to clients
def send_data(sock, inputs, buffers):
    if buffers[sock]:
        #print(f"Sending data to {sock.getpeername()}: {buffers[sock]}")
        #sent = sock.send(buffers[sock])
        #buffers[sock] = buffers[sock][sent:]
        if not buffers[sock]:
            # No more data to send, remove from inputs
            inputs.remove(sock)

# Main function to run the server
def run_server(host, port):
    server_socket = setup_server_socket(host, port)
    inputs = [server_socket]
    buffers = {}

    while inputs:
        readable, _, exceptional = select.select(inputs, [], inputs)

        for s in readable:
            if s is server_socket:
                # New connection
                handle_new_connection(server_socket, inputs, buffers)
            else:
                # Existing connection has data to be read
                handle_client_data(s, inputs, buffers)

        for s in exceptional:
            print(f"Handling exceptional condition for {s.getpeername()}")
            inputs.remove(s)
            s.close()
            del buffers[s]

if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 12345
    run_server(HOST, PORT)
