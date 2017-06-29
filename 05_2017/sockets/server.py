#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import socketserver
from worlds import *
from random import randint, choice


HOST, PORT = "0.0.0.0", 10001
PLAYERS = {'ip': 'class_player'}
BUTTON_TO_COMMAND_DICT = {'w': 'move up',
                          'a': 'move left',
                          's': 'move down',
                          'd': 'move right',
                          'f': 'attack',
                          ' ': ''}


# button to command function
def btc(button):
    if button in BUTTON_TO_COMMAND_DICT:
        return BUTTON_TO_COMMAND_DICT[button]
    else:
        return 'wait'


def get_text_map(world):
    text = ''
    for x in range(world.width):
        for y in range(world.height):
            text = text + world.map[x][y].symb
        text = text + '\n'
    return text


class MyHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global WORLD
        while True:
            data = self.request.recv(1024).decode()
            print('{}: {}'.format(self.client_address[0], data))
            if data == '.':
                self.request.sendall(b'You waited')
            data = data[1:]
            adr = self.client_address[0]
            print('{}: {}'.format(adr, data))
            if len(data) > 1:
                self.request.sendall(b'You can send only 1 command(button)')
                return None

            if adr in PLAYERS:
                player = PLAYERS[adr]
            else:
                player = StandardCreature(WORLD, randint(2, 8), randint(2, 8))
                PLAYERS[adr] = player

            self.handle_command(player, data)

            texted_map = get_text_map(WORLD)
            self.request.sendall(texted_map.encode())

    def handle_command(self, player, button):
        command = btc(button).split()
        if len(command) == 1:
            pass
        if len(command) == 2:
            if command[0] == 'move':
                move_ret = player.move(command[1])
                if move_ret == 'full':
                    return 'This field is full'
                else:
                    return ''


class MyServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True


def main():
    global WORLD
    WORLD = World(10, 10)
    WORLD.GenerateWorld()

    server = MyServer((HOST, PORT), MyHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()

