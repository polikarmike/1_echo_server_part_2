import socket

def start_client():
    host = 'localhost'
    port = 9090

    print("[INFO] Connecting to the server...")
    client_socket = socket.socket()
    client_socket.connect((host, port))
    print("[INFO] Connected to the server.")

    try:
        while True:
            message = input("Enter message (type 'exit' to quit): ")
            client_socket.send(message.encode())
            print(f"[INFO] Sent to server: {message}")

            if message.strip().lower() == "exit":
                print("[INFO] Exit command sent. Closing connection.")
                break

            data = client_socket.recv(1024)
            print(f"[INFO] Received from server: {data.decode()}")

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        client_socket.close()
        print("[INFO] Connection closed.")

if __name__ == "__main__":
    start_client()
