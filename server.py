import socket
import threading

class GilbServer:
    def __init__(self, host: str, port: int, server_identifier: str):
        self.host = host
        self.port = port
        self.server_identifier = server_identifier
        self.sock = None
        self.clients = {}
        self.on_message = None
    
    def start(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        while True:
            conn, addr = self.sock.accept()
            t = threading.Thread(target=self.handle_client, args=(conn,))
            t.daemon = True
            t.start()
    
    def handle_client(self, conn):
        data = conn.recv(1024).decode("ascii").strip()
        if not data.startswith("lets gilb ") or data.split(" ", 2)[2] != self.server_identifier:
            conn.sendall(b"sorry no\n")
            conn.close()
            return
        conn.sendall(b"OK LETS GILB\n")
        self.clients[conn] = True
        while self.clients.get(conn):
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode("ascii").strip()
            if message == "i want to disconnect my gilbbing":
                conn.sendall(b"ok\n")
                break
            if message.startswith("heres my ") and " gilberts " in message:
                conn.sendall(b"ok i gilbert\n")
                parts = message.split(" ", 4)
                if self.on_message:
                    self.on_message(conn, parts[4])
        conn.close()
        self.clients.pop(conn, None)
    
    def send_message(self, conn, message: str):
        msg_bytes = message.encode("ascii")
        length_hex = f"0x{len(msg_bytes):08X}"
        full_msg = f"heres your {length_hex} gilberts {message}\n"
        conn.sendall(full_msg.encode("ascii"))
        resp = conn.recv(1024).decode("ascii").strip()
        if resp != "ok i gilbert":
            raise RuntimeError(f"unexpected response: {resp}")