import copy
import os
import socket
import pickle
from Cryptodome.Cipher import AES
from fileutilities.fileutilities import write_to_file, read_into_hex


def aes_ecb_encrypt(input_file=None, output_file=None, to_encrypt=None, _aes=AES):
    cryptotext = list()
    if input_file and not to_encrypt:
        to_encrypt = read_into_hex(input_file)

    if len(to_encrypt[-1]) < 16:
        to_encrypt[-1] = pad(to_encrypt[-1], 8)

    print("Encrypting with ECB: ", to_encrypt)
    # AES for every block
    for i in range(len(to_encrypt)):
        cryptotext.append(_aes.encrypt(bytes(to_encrypt[i], 'utf-8')))

    if output_file:
        write_to_file(output_file, cryptotext)

    return cryptotext


def aes_ecb_decrypt(input_file=None, output_file=None, to_decrypt=None, _aes=AES):
    decrypted = list()
    if input_file and not to_decrypt:
        to_decrypt = read_into_hex(input_file)
    # decrypt block by block
    for i in range(len(to_decrypt)):
        decrypted.append(_aes.decrypt(to_decrypt[i]))
    decrypted[-1] = unpad(decrypted[-1])
    print("ECB DECRYPTED: ", decrypted)
    if output_file:
        write_to_file(output_file, decrypted)
        if output_file:
            write_to_file(output_file, decrypted)
            with open(output_file, "r") as f:
                plaintext = f.read()
    for i in range(len(decrypted)):
        decrypted[i] = decrypted[i].decode('utf-8')
    return plaintext


def aes_cfb_encrypt(iv, input_file=None, output_file=None, to_encrypt=None, _aes=AES):
    cryptotext = list()
    if input_file and not to_encrypt:
        to_encrypt = read_into_hex(input_file)

    if len(to_encrypt[-1]) < 16:
        to_encrypt[-1] = pad(to_encrypt[-1], 8)

    print("Encrypting with CFB: ", to_encrypt)
    xor_with = iv
    for i in range(len(to_encrypt)):
        xor_msg = xor_block(bytes(to_encrypt[i], 'utf-8'), _aes.encrypt(xor_with))
        xor_with = copy.deepcopy(xor_msg)
        cryptotext.append(xor_msg)

    if output_file:
        write_to_file(output_file, cryptotext)

    return cryptotext


def aes_cfb_decrypt(iv, input_file=None, output_file=None, to_decrypt=None, _aes=AES):
    decrypted = list()
    if input_file and not to_decrypt:
        to_decrypt = read_into_hex(input_file)
    # decrypt block by block
    xor_with = copy.deepcopy(iv)
    for i in range(len(to_decrypt)):
        xor_msg = xor_block(to_decrypt[i], _aes.encrypt(xor_with))
        xor_with = copy.deepcopy(to_decrypt[i])
        decrypted.append(xor_msg)
    print("DECRYPTED CFB: ", decrypted)
    decrypted[-1] = unpad(decrypted[-1])
    if output_file:
        write_to_file(output_file, decrypted)
        with open(output_file, "r") as f:
            plaintext = f.read()

    return plaintext


def pad(block, length):
    for_pad = length - len(block) // 2
    for i in range(for_pad):
        block += format(for_pad, '02x')
    return block


def unpad(block):
    for_unpad = int(block[-2:], 16)
    return block[:-2 * for_unpad]


def xor_block(block_1, block_2):
    return bytes([i ^ j for i, j in zip(block_1, block_2)])


def random_key_generator(bits_length):
    return bytes.hex(os.urandom(bits_length // 16))


def ask_km_for_key(mode):
    IP = socket.gethostbyname(socket.gethostname())
    PORT = 4444

    cl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cl.connect((IP, PORT))
    cl.sendall(mode.encode('utf-8'))

    res = cl.recv(4096)
    print("Recieved from KM: ", res)

    cl.close()
    with open("k_prime.txt", "rb") as f:
        K_prime = pickle.load(f)

    _aes = AES.new(K_prime, AES.MODE_ECB)
    K = _aes.decrypt(res)
    print("Decrypted key K: ", K)
    return K
