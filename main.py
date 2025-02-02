import socket
import threading

HOST = None # Будет запрошен у пользователя
PORT = 12345

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break  # Если соединение закрыто
            print("\nПолучено: " + message)
        except Exception as e:
            print(f"Ошибка при получении сообщения: {e}")
            break

def send_messages(client_socket):
    while True:
        message = input("Вы: ")
        try:
            client_socket.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Ошибка при отправке сообщения: {e}")
            break

def start_server():
    global HOST
    HOST = input("Введите свой IP-адрес (если вы сервер) или нажмите Enter: ")
    if not HOST:
        HOST = socket.gethostbyname(socket.gethostname())  # Получение IP-адреса локально
        print(f"Ваш IP-адрес: {HOST}. Начнем прослушивание...")
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print("Ожидание подключения...")
        client_socket, addr = server_socket.accept()
        print(f"Подключено {addr[0]}:{addr[1]}")
        
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        send_thread = threading.Thread(target=send_messages, args=(client_socket,))

        receive_thread.start()
        send_thread.start()

        receive_thread.join()
        send_thread.join()
        
        client_socket.close()
        server_socket.close()


    else: # Клиент
        
        peer_host = input("Введите IP-адрес другого участника: ")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((peer_host, PORT))
            print("Подключено!")
            
            receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
            send_thread = threading.Thread(target=send_messages, args=(client_socket,))
            
            receive_thread.start()
            send_thread.start()
            
            receive_thread.join()
            send_thread.join()
        except Exception as e:
            print(f"Не удалось подключиться: {e}")
        finally:
            client_socket.close()


if __name__ == "__main__":
    start_server()
