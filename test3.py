#!/usr/bin/env python3
import socket, select, base64, os

def recvline(s):
    buf = b''
    while True:
        c = s.recv(1)
        buf += c
        if c == b'' or c == b'\n':
            return buf
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 7000))
def myrand(n=512):
    return base64.b32encode(os.urandom(n))

s.send(myrand(200))
r,_,_=select.select([s],[],[],0.5)
assert r==[], 'O servidor não deveria responder enquanto não chegar uma linha inteira'

s.send(myrand(200) + b'\n')
assert recvline(s) == b'/error\n'

nick = myrand(8).decode()
s.send('/nick {}\n'.format(nick).encode())
assert recvline(s) == '/joined {}\n'.format(nick).encode()

msg = myrand().decode()
s.send(msg.encode() + b'\n')
assert recvline(s) == '{}: {}\n'.format(nick, msg).encode()

oldnick = nick
nick = myrand(8).decode()
s.send('/nick {}\n'.format(nick).encode())
assert recvline(s) == '/renamed {} {}\n'.format(oldnick, nick).encode()

msg = myrand().decode()
s.send(msg.encode() + b'\n')
assert recvline(s) == '{}: {}\n'.format(nick, msg).encode()

msg = myrand().decode()
s.send(msg.encode() + b'\n')
assert recvline(s) == '{}: {}\n'.format(nick, msg).encode()

s.close()
