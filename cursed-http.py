import os.path
import socket
import threading
import argparse

class TCP:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def main(self, filepath):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.listen()

        print(f"Listening on http://{self.host}:{self.port}")

        try:
            while True:
                conn, _addr = server.accept()
                client_thread = threading.Thread(
                    target=self.handle_connection,
                    args=(conn, filepath),
                    daemon=True,
                )
                client_thread.start()
        except KeyboardInterrupt:
            server.close()


    def handle_connection(self, conn, filepath):
        request = conn.recv(1024).decode()
        print(request)

        lines = request.split("\r\n")
        method, path, http_ver = lines[0].split(" ")

        header = ""
        for line in lines:
            if line.startswith("User-Agent:"):
                header = line.split(": ")[1]

        if os.path.exists(filepath):
            with open(filepath, 'r') as file:
                file_exist = True
                file_content = file.read()
        else:
            file_exist = False

        if path == "/":
            response = self.build_response("200 OK", "200 OK\r\nThe request was successful.")

        elif (len(path_parts := path.split("/")) == 3
              and path_parts[1] == "echo"
              ):
            response = b"\r\n".join([
                b"HTTP/1.1 200 OK",
                b"Content-Type: text/plain",
                b"Content-Length: " + str(len(path_parts[2])).encode(),
                b"",
                path_parts[2].encode(),
                b"",
                ])

        elif path == "/user-agent":
            response = self.build_response("200 OK", header)
        elif path == f"/filename/{filepath}" and file_exist:
            if method == "GET":
                response = self.build_response("200 OK", file_content, "text/html")
            elif method == "POST":
                # Handle POST request body
                body_start = request.find("\r\n\r\n") + 4
                body = request[body_start:]
                print(f"POST request body:\n{body.decode()}")
                response = self.build_response("200 OK", "POST request received.", "text/plain")
        elif path == f"/display/{filepath}" and file_exist:
            response = self.build_response("200 OK", file_content, "text/html")
        elif path == "/secret":
            self.create_secret_file()
            response = self.build_response("200 OK", "", "text/plain", "Content-Disposition: attachment; filename=secret_file.txt")
        else:
            html = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>404 NOT FOUND</title><style>body{margin:0;padding:0;height:100vh;display:flex;align-items:center;justify-content:center;background-color:#111;font-family:"Arial",sans-serif;color:#fff;}.container{text-align:center;}h1{font-size:1.5em;margin:0;}p{font-size:1em;margin:0;}</style></head><body><div class="container"><h1>404 NOT FOUND</h1><p>Sorry, the page you are looking for might be in another universe.</p></div><script>// You can add inline JavaScript if neededconsole.log("404 Page Not Found");</script></body></html>'
            response = self.build_response("404 NOT FOUND", html, "text/html")

        conn.send(response)
        conn.close()

    def build_response(self, status, content, content_type="text/plain", additional_headers=""):
        response = f"HTTP/1.1 {status}\r\n"
        response += f"Content-Type: {content_type}\r\n"
        response += f"Content-Length: {len(content)}\r\n"
        response += f"{additional_headers}\r\n\r\n"
        response = response.encode() + content.encode()
        return response

    def create_secret_file(self):
        with open("secret_file.txt", "w") as f:
            f.write("This is a secret file. Do not share!")

def run_server():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, default="index.html", help="File path")
    parser.add_argument("-H", "--host", type=str, default="127.0.0.1", help="Host")
    parser.add_argument("-p", "--port", type=int, default=4222, help="Port")
    args = parser.parse_args()

    tcp = TCP(args.host, args.port)
    tcp.main(args.file)

if __name__ == "__main__":
    run_server()

