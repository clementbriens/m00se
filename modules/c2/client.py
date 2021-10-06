import base64
import socket
import rsa
import json

class C2_Client():

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connected = False
        # self.private_key = rsa.PrivateKey.load_pkcs1(open("./private.key", "r").read())
        # self.public_key =  rsa.PublicKey.load_pkcs1_openssl_pem(open("./public.key", "rb").read())

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.connected = True
        print('Connected by', self.host, self.port)
        return self.socket

    def send_message(self, msg):
        print('sent msg:', msg)
        if self.connected:
            if isinstance(msg, dict):
                encoded_msg = base64.b64encode(json.dumps(msg).encode('utf-8'))
            else:
                encoded_msg = base64.b64encode(str(msg).encode('utf-8'))
            # encrypted_message = rsa.encrypt(encoded_msg,
            #              self.public_key)
            self.socket.sendall(encoded_msg)
            # self.socket.close()

    def receive_message(self):
        while True:
            data = self.socket.recv(1024)
            # dec_msg = rsa.decrypt(data, self.private_key).decode()
            msg = base64.b64decode(data)
            print('received msg:', msg.decode('utf-8'))
            # self.socket.close()
            return msg


if __name__ == '__main__':
    c2 = C2_Client("127.0.0.1", 5555)
    c2.connect()
    while True:
        c2.receive_message()
