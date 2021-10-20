import socket
import pickle

from Cryptodome.Cipher import AES
from threading import Thread
from ECB_CBF.ECB_CBF import random_key_generator


class ClientThread(Thread):
    def __init__(self, ip, port, connection):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.connection = connection
        print(f'New thread: {ip}:{port}')

    def run(self):
        data = self.connection.recv(4096)
        data = data.decode('utf-8')
        print("Recieved data: " + data)
        _aes = AES.new(K_prime, AES.MODE_ECB)

        if data.lower() == "ecb" or data.lower() == "cfb":
            res = _aes.encrypt(K)

        print("Sending: ", res)
        self.connection.send(res)
        self.connection.close()


IP = socket.gethostbyname(socket.gethostname())
PORT = 4444

tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp_server.bind((IP, PORT))

threads = []
K = bytes(random_key_generator(128), 'utf-8')
print("K: ", K)

K_prime = bytes(random_key_generator(128), 'utf-8')
print("K'(prime): ", K_prime)

with open("k_prime.txt", "wb") as f:
    pickle.dump(K_prime, f)


try:
    while True:
        tcp_server.listen(4)
        (connection, (ip, port)) = tcp_server.accept()
        new_thread = ClientThread(ip, port, connection)
        new_thread.start()
        threads.append(new_thread)
except Exception as e:
    print("ERROR!! ", e)
    for _th in threads:
        _th.join()
