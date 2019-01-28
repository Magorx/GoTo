#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
from worlds import *


def main():
    s = socket.socket()
    s.connect(('192.168.0.155', 10001))
    message = ''
    while message != b' stop':
        message = b'.'
        message = message + input().encode()
        s.send(message)
        data = s.recv(1024).decode()
        print(data)


if __name__ == "__main__":
    main()

