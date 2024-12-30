import socket
import threading

# A list to maintain active peers
active_peers = []

def handle_client(conn, addr):
    global active_peers
    try:
        data = conn.recv(1024).decode()
        if data.startswith("REGISTER"):
            # Expect format: "REGISTER:<peer_host>:<peer_port>"
            parts = data.split(":")
            if len(parts) == 3:
                _, peer_host, peer_port = parts
                peer_address = f"{peer_host}:{peer_port}"
                if peer_address not in active_peers:
                    active_peers.append(peer_address)
                    print(f"Registered peer: {peer_address}")
                conn.sendall(",".join(active_peers).encode())
            else:
                print(f"Malformed REGISTER request: {data}")
                conn.sendall(b"ERROR: Malformed REGISTER request")
        elif data.startswith("UNREGISTER"):
            # Expect format: "UNREGISTER:<peer_host>:<peer_port>"
            parts = data.split(":")
            if len(parts) == 3:
                _, peer_host, peer_port = parts
                peer_address = f"{peer_host}:{peer_port}"
                if peer_address in active_peers:
                    active_peers.remove(peer_address)
                    print(f"Unregistered peer: {peer_address}")
                conn.sendall(b"OK")
            else:
                print(f"Malformed UNREGISTER request: {data}")
                conn.sendall(b"ERROR: Malformed UNREGISTER request")
        else:
            print(f"Unknown command: {data}")
            conn.sendall(b"ERROR: Unknown command")
    except Exception as e:
        print(f"Error in handle_client: {e}")
    finally:
        conn.close()

def tracker_server(host='0.0.0.0', port=5000):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Tracker running on {host}:{port}")
    
    while True:
        conn, addr = server.accept()
        print(f"Connection from {addr}")
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    tracker_server()
