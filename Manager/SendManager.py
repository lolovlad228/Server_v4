import json
from socket import socket

class Send:

    def login(self, sock):
        send = {
            "Type_Command": "Login",
            "Information": "all"
        }
        sock.send(json.dumps(send).encode())
