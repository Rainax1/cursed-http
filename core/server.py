import socket
import threading




class Server:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.make_conn()


    def handle_conn(self, client_connection):
        while True:
            recv_data = client_connection.recv(1024).decode("utf-8")
            print(recv_data)

    def make_conn(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server.bind((self.host, self.port))
        print("Listning...")
        print(f"{self.host}:{self.port}")
        while True:
            server.listen()
            client_connection, client_addr =  server.accept()
            print(f"Connected with {client_addr}")
            client_thread = threading.Thread(
                    target=self.handle_conn,
                    args=(client_connection, ),
                    daemon=True
                    )
            client_thread.start()

Server("127.0.0.1", 4322)


