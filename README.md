# gilb-protocol-python
A python implementation of the [gilb-protocol](https://github.com/skibidihomer123/gilb-protocol)

# Example Usage
```py
from gilb-protocol-python import GilbServer, GilbClient
import threading

server = GilbServer(host="127.0.0.1", port=12345, server_identifier="myserver123")

def server_handler(conn, message):
    print(f"[Server] Received: {message}")
    server.send_message(conn, f"Echo: {message}")

server.on_message = server_handler
threading.Thread(target=server.start, daemon=True).start()

client = GilbClient(host="127.0.0.1", port=12345, server_identifier="myserver123")

def client_handler(message):
    print(f"[Client] Received: {message}")

client.on_message = client_handler
client.connect()
client.send_message("hello world!")
client.disconnect()
```