import socket
import threading

stop_receiving = False  # Флаг для остановки потока получения сообщений


def receive_messages(client_socket):
    """Поток для получения сообщений от сервера."""
    global stop_receiving
    while not stop_receiving:  # Поток завершится, если флаг установлен в True
        try:
            data, _ = client_socket.recvfrom(1024)
            print(data.decode())
        except OSError:
            break  # Прекращаем цикл, если сокет был закрыт
        except Exception:
            print("[ERROR] Connection error.")
            break


def start_udp_chat_client():
    global stop_receiving
    server_host = 'localhost'  # Замените на IP сервера
    server_port = 9090

    # Создание UDP-сокета
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Регистрируем клиента на сервере и получаем никнейм
    print(f"[INFO] Connecting to the server...")
    client_socket.sendto("JOIN".encode(), (server_host, server_port))
    data, _ = client_socket.recvfrom(1024)
    nickname = data.decode()

    # Выводим сообщение с никнеймом
    print(f"[INFO] Your nickname is: {nickname}")

    # Поток для получения сообщений
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.daemon = True  # Поток завершится с завершением программы
    receive_thread.start()

    try:
        while True:
            message = input()
            if message.strip().lower() == "exit":
                client_socket.sendto(f"{nickname} left the chat.".encode(), (server_host, server_port))
                print("[INFO] Disconnected from the chat.")
                stop_receiving = True  # Сигнал для завершения потока
                break
            client_socket.sendto(f"{nickname}: {message}".encode(), (server_host, server_port))
    except KeyboardInterrupt:
        client_socket.sendto(f"{nickname} left the chat.".encode(), (server_host, server_port))
        print("\n[INFO] Disconnected from the chat.")
        stop_receiving = True  # Сигнал для завершения потока
    finally:
        client_socket.close()


if __name__ == "__main__":
    start_udp_chat_client()
