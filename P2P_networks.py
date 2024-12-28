import socket
import threading
import os

# Constants for host and port
HOST = '127.0.0.1'  # Localhost
PORT = 65432        # Arbitrary non-privileged port

# Server code (Peer A)
def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"[SERVER] Listening on {HOST}:{PORT}")

    conn, addr = server_socket.accept()
    print(f"[SERVER] Connected by {addr}")

    # Receive file name
    file_name = conn.recv(1024).decode()
    print(f"[SERVER] Receiving file: {file_name}")

    # Receive file data
    with open(file_name, 'wb') as file:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            file.write(data)

    print(f"[SERVER] File '{file_name}' received successfully.")
    conn.close()
    server_socket.close()

# Client code (Peer B)
def client(file_path):
    if not os.path.exists(file_path):
        print("[CLIENT] File does not exist.")
        return

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print(f"[CLIENT] Connected to server at {HOST}:{PORT}")

    # Send file name
    file_name = os.path.basename(file_path)
    client_socket.sendall(file_name.encode())

    # Send file data
    with open(file_path, 'rb') as file:
        while chunk := file.read(1024):
            client_socket.sendall(chunk)

    print(f"[CLIENT] File '{file_name}' sent successfully.")
    client_socket.close()

# Multi-threading for running server and client simultaneously
def main():
    # Start server in a separate thread
    server_thread = threading.Thread(target=server)
    server_thread.start()

    # File to transfer (client side)
    file_to_send = input("Enter the path of the file to send: ")

    # Start client in the main thread
    client(file_to_send)

    # Wait for the server thread to finish
    server_thread.join()

if __name__ == "__main__":
    main()
