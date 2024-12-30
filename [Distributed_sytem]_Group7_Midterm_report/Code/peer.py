import socket
import threading
import time
import os
from chunk_handler import split_file, merge_chunks

# Configuration
TRACKER_HOST = '127.0.0.1'
TRACKER_PORT = 5000
PEER_HOST = '127.0.0.1'
PEER_PORT = 6002

# Peer Functions
def register_with_tracker():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tracker_socket:
            tracker_socket.connect((TRACKER_HOST, TRACKER_PORT))
            tracker_socket.sendall(f"{PEER_HOST}:{PEER_PORT}".encode('utf-8'))
            print(f"Registered with tracker at {TRACKER_HOST}:{TRACKER_PORT}")
    except Exception as e:
        print(f"Failed to register with tracker: {e}")

def handle_peer_connection(conn, addr):
    print(f"Connected by {addr}")
    try:
        data = conn.recv(1024).decode('utf-8')
        if data.startswith("REQUEST_FILE"):
            filename = data.split()[1]
            if os.path.exists(filename):
                chunks = split_file(filename)
                conn.sendall(f"CHUNKS {len(chunks)}".encode('utf-8'))
                for chunk in chunks:
                    conn.sendall(chunk)
                print(f"Sent file '{filename}' in {len(chunks)} chunks to {addr}")
            else:
                conn.sendall(b"ERROR File not found")
        else:
            conn.sendall(b"ERROR Invalid request")
    except Exception as e:
        print(f"Error handling peer connection: {e}")
    finally:
        conn.close()

def start_peer_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as peer_socket:
        peer_socket.bind((PEER_HOST, PEER_PORT))
        peer_socket.listen()
        print(f"Peer server running on {PEER_HOST}:{PEER_PORT}")
        while True:
            conn, addr = peer_socket.accept()
            threading.Thread(target=handle_peer_connection, args=(conn, addr)).start()

# Main Logic
def main():
    # Register with tracker
    register_with_tracker()

    # Start peer server
    threading.Thread(target=start_peer_server, daemon=True).start()

    # Simulate file sharing
    try:
        filename = "example_file.txt"
        if not os.path.exists(filename):
            raise FileNotFoundError(f"The file '{filename}' does not exist. Please ensure the file is in the correct location.")

        print(f"Splitting file '{filename}'...")
        chunks = split_file(filename)
        print(f"File '{filename}' split into {len(chunks)} chunks.")

        # Example: Simulate merging chunks back into the original file
        merged_filename = "reconstructed_" + filename
        merge_chunks(chunks, merged_filename)
        print(f"File successfully reconstructed as '{merged_filename}'")

    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
