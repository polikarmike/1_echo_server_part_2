import socket


def start_server():
    host = ''
    port = 9090

    print("[INFO] Starting server...")
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"[INFO] Server is listening on port {port}")

    conn, addr = server_socket.accept()
    print(f"[INFO] Connection established with {addr}")

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                print("[INFO] No data received. Closing connection.")
                break

            message = data.decode()
            print(f"[INFO] Received from client: {message}")

            if message.strip().lower() == "exit":
                print("[INFO] Exit command received. Closing connection.")
                conn.send("Goodbye!".encode())
                break

            conn.send(data)  # Echo back to client
            print(f"[INFO] Sent to client: {message}")

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()
        print("[INFO] Connection closed.")
        server_socket.close()
        print("[INFO] Server stopped.")


if __name__ == "__main__":
    start_server()
