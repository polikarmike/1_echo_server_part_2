import socket
import random

def generate_nickname():
    """Генерация случайного никнейма."""
    adjectives = ['Pink', 'Blue', 'Green', 'Red', 'Yellow', 'Purple']
    animals = ['Elephant', 'Tiger', 'Cat', 'Panda', 'Lion', 'Rabbit', 'Fox']
    number = random.randint(1000, 9999)
    return f"{random.choice(adjectives)}-{random.choice(animals)}-{number}"


def start_udp_chat_server():
    host = ''  # Слушаем все интерфейсы
    port = 9090
    buffer_size = 1024

    # Создание UDP-сокета
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    print(f"[INFO] Server is listening on port {port}")

    clients = {}

    try:
        while True:
            try:
                # Получаем данные от клиента
                data, addr = server_socket.recvfrom(buffer_size)
                message = data.decode()

                # Если клиент отправил команду 'JOIN', генерируем никнейм и отправляем его клиенту
                if message == "JOIN":
                    nickname = generate_nickname()
                    clients[addr] = nickname
                    server_socket.sendto(nickname.encode(), addr)
                    join_message = f"{nickname} has joined the chat!"
                    for client in clients:
                        if client != addr:
                            server_socket.sendto(join_message.encode(), client)
                    print(f"[INFO] New client {nickname} connected from {addr}")
                    continue

                # Получаем никнейм клиента
                nickname = clients[addr]

                print(f"[INFO] {message}")

                # Если клиент отправил команду 'exit', удаляем его из списка
                if message.strip().lower() == "exit":
                    print(f"[INFO] {nickname} disconnected.")
                    del clients[addr]
                    continue

                # Отправляем сообщение всем подключенным клиентам, добавляя никнейм
                for client in clients:
                    if client != addr:  # Не отправляем обратно отправителю
                        server_socket.sendto(f"{message}".encode(), client)
                print(f"[INFO] Message sent to all clients.")
            except ConnectionResetError:
                print(f"[ERROR] Connection with client {addr} was forcibly closed.")
    except KeyboardInterrupt:
        print("\n[INFO] Server shutting down.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_udp_chat_server()
