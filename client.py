import socket
import threading

class GilbClient:
    def __init__(self, host: str, port: int, server_identifier: str):
        self.host = host
        self.port = port
        self.server_identifier = server_identifier
        self.sock = None
        self.running = False
        self.on_message = None
    
    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.sock.sendall(f"lets gilb {self.server_identifier}\n".encode("ascii"))
        resp = self.sock.recv(1024).decode("ascii").strip()
        if resp != "OK LETS GILB":
            raise ConnectionError(f"handshake failed: {resp}")
        self.running = True
        threading.Thread(target=self._listen_loop, daemon=True).start()
    
    def _listen_loop(self):
        while self.running:
            data = self.sock.recv(1024)
            if not data:
                break
            message = data.decode("ascii").strip()
            if message.startswith("heres your ") and " gilberts " in message:
                parts = message.split(" ", 4)
                msg_len = int(parts[2], 16)
                msg_content = parts[4]
                self.sock.sendall(b"ok i gilbert\n")
                if self.on_message:
                    self.on_message(msg_content)
    
    def send_message(self, message: str):
        msg_bytes = message.encode("ascii")
        length_hex = f"0x{len(msg_bytes):08X}"
        full_msg = f"heres my {length_hex} gilberts {message}\n"
        self.sock.sendall(full_msg.encode("ascii"))

        while True:
            resp = self.sock.recv(1024).decode("ascii").strip()
            if resp == "ok i gilbert":
                break
            elif resp.startswith("heres your ") and " gilberts " in resp:
                parts = resp.split(" ", 4)
                if self.on_message:
                    self.on_message(parts[4])
            else:
                raise RuntimeError(f"unexpected response: {resp}")

    
    def disconnect(self):
        self.running = False
        if self.sock:
            self.sock.sendall(b"i want to disconnect my gilbbing\n")
            resp = self.sock.recv(1024).decode("ascii").strip()
            if resp != "ok":
                raise RuntimeError(f"unexpected response: {resp}")
            self.sock.close()
            self.sock = None