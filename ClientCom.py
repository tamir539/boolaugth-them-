import socket
import threading
import queue
import sys
from my_AES import AESCipher
from my_RSA import RSAClass


class ClientCom:
    def __init__(self,server_ip, port, msg_q):
        self.running = False
        self.my_socket = socket.socket()
        self.server = server_ip
        self.port = port
        self.msg_q = msg_q
        self.key = None
        self.cry = None
        self.connect()


    

    def sendTo(self, msg):
        try:
            self.my_socket.send(msg.encode())
        except:
            self.running = False


    def sendEnc(self, msg):
        try:


            msg = self.cry.encrypt(msg)

            self.my_socket.send(msg)
        except Exception as e:
            print(2222, str(e))
            self.running = False





    def connect(self):
        try:
            self.my_socket.connect((self.server, self.port))
            self.running = True
        except:
            pass

    def recv(self):
        while self.running:
            try:

                data = self.my_socket.recv(1024).decode()

            except:
                self.running = False
            else:

                self.msg_q.put(data)



    def server_status(self):
        return self.running

    def switch_keys(self):
        try:
            myRsa = RSAClass()
            public_key = myRsa.get_public_key_pem()

            self.my_socket.send(public_key)
            key = self.my_socket.recv(1024)

            self.key = myRsa.decrypt_msg(key).decode()

            self.cry = AESCipher(self.key)
        except Exception as e:
            print(str(e))
            self.running = False

        threading.Thread(target=self.recv).start()







