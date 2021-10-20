import copy
import socket
import pickle

from Cryptodome.Cipher import AES
from ECB_CBF.ECB_CBF import aes_ecb_decrypt, aes_cfb_decrypt, ask_km_for_key


if __name__ == '__main__':
    ip_b = socket.gethostbyname(socket.gethostname())
    port_b = 4445

    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_server.bind((ip_b, port_b))
    tcp_server.listen(2)

    connection, address = tcp_server.accept()
    mode = connection.recv(4096)
    mode = mode.decode('utf-8')
    print("From A received mode: " + mode)    # receiving mode from A

    K = ask_km_for_key(mode)

    connection.send("OK".encode('utf-8'))
    data = []
    while True:
        packet = connection.recv(4096)
        if not packet:
            break
        data.append(packet)

    to_decrypt = pickle.loads(b"".join(data))

    if mode == "ecb":
        _aes = AES.new(K, AES.MODE_ECB)
        plaintext = aes_ecb_decrypt(output_file="out_ecb_out_dec.txt", to_decrypt=to_decrypt, _aes=_aes)
    else:
        with open("iv.txt", "rb") as f:
            iv = pickle.load(f)
        cp_iv = copy.deepcopy(iv)
        _aes = AES.new(K, AES.MODE_CFB, iv=cp_iv)
        plaintext = aes_cfb_decrypt(iv, to_decrypt=to_decrypt, output_file="out_cfb_out_dec.txt", _aes=_aes)

    print("Decrypted plaintext: ", plaintext)
    connection.close()

