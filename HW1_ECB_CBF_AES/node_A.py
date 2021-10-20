import copy
import socket
import pickle

from Cryptodome.Cipher import AES
from ECB_CBF.ECB_CBF import aes_ecb_encrypt, aes_cfb_encrypt, ask_km_for_key, random_key_generator


if __name__ == '__main__':
    mode = input("Select a communication mode (ecb/cfb): ").lower()
    while mode != "ecb" and mode != "cfb":
        print("Error! Incorrect communication mode. ")
        mode = input("Select a communication mode (ecb/cfb): ")

    print("Selected communication mode: " + mode.upper())

    ip_A = socket.gethostbyname(socket.gethostname())
    port_A = 4445
    cl_A = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    K = ask_km_for_key(mode)
    cl_A.connect((ip_A, port_A))
    cl_A.sendall(mode.encode('utf-8'))

    res = cl_A.recv(4096).decode('utf-8')
    if res != "OK":
        print("Error from B!")

    if mode == 'ecb':
        _aes = AES.new(K, AES.MODE_ECB)
        crypto_text = aes_ecb_encrypt(input_file="input.txt", _aes=_aes)
    else:
        iv = bytes(random_key_generator(128), 'utf-8')
        with open("iv.txt", "wb") as f:
            pickle.dump(iv, f)
        cp_iv = copy.deepcopy(iv)
        _aes = AES.new(K, AES.MODE_CFB, iv=cp_iv)
        crypto_text = aes_cfb_encrypt(iv, input_file="input.txt", _aes=_aes)

    to_send = pickle.dumps(crypto_text)
    cl_A.sendall(to_send)
    cl_A.close()
