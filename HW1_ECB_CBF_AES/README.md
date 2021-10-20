# Installation
`pip3 install pycryptodomex`

#Intro
Implementation in Python 3.9 of a multithreaded client/server application which utilizes AES cryptosystem and ECB and 
CBF modes for traffic encryption between two nodes A(lice) and B(ob).

#Libraries
`socket` - BSD interface for socket programming and TCP server <br>
`threading` - multithreaded TCP server <br>
`pycryptodome` - for AES
`pickle` - sending and loading that as objects

# Usage
Application encrypts the contents of file `input.txt`, `node_A` requests from `node_KM` the `K` key which is encrypted
and decrypts it with `K_prime` key. `node_A` sends the encryption chosen to `node_b` and sends the encrypted content of
`input.txt` to `node_b`. `node_b` requests `node_KM` the `K` and decrypts it with `K_prime` key. Using `K` attempts to
decrypt the message from `node_A`.

First - `python3 node_KM.py` <br>
Second - `python3 node_A.py` <br>
Third - `python3 node_B.py` <br>
Fourth - `choose encryption ECB or CBF (in node_A.py terminal)`
