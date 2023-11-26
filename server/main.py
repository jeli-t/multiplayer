from config import *
import socket
import threading


clients = []


def handle_client(client_socket):
    while True:
        try:
            raw_data = client_socket.recv(1024)
            if not raw_data:
                break

            for c in clients:
                if c != client_socket:
                    c.send(raw_data)

        except Exception as e:
            print(f"[!] Error {e}")
            break

    clients.remove(client_socket)
    client_socket.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(ADDRESS)
    server_socket.listen(5)

    print(f"[*] Listening on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"[*] New connection from {client_address}")

        clients.append(client_socket)
        client_handler = threading.Thread(target=handle_client, args=(client_socket, ))
        client_handler.start()

if __name__ == "__main__":
    main()