import os


def read_into_hex(file_name):
    hex_arr = list()
    with open(file_name, "rb") as f:
        for i in range(0, os.path.getsize(file_name), 8):
            hex_arr.append(bytes.hex(f.read(8)))
            f.seek(i + 8)
    return hex_arr


def write_to_file(file_name, hex_arr):
    with open(file_name, "wb") as f:
        for i in range(len(hex_arr)):
            f.write(bytes.fromhex(hex_arr[i].decode('utf-8')))
