import pygame
import random
import socket
import threading
import queue
import pickle
from config import *


class Player():
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.rect = (x, y, PLAYER_SIZE, PLAYER_SIZE)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.x -= PLAYER_SPEED
            if self.x <= 0:
                self.x = 0
        elif keys[pygame.K_d]:
            self.x += PLAYER_SPEED
            if self.x + PLAYER_SIZE >= WINDOW_WIDTH:
                self.x = WINDOW_WIDTH - PLAYER_SIZE
        elif keys[pygame.K_w]:
            self.y -= PLAYER_SPEED
            if self.y <= 0:
                self.y = 0
        elif keys[pygame.K_s]:
            self.y += PLAYER_SPEED
            if self.y + PLAYER_SIZE >= WINDOW_HEIHGT:
                self.y = WINDOW_HEIHGT - PLAYER_SIZE

        self.rect = (self.x, self.y, PLAYER_SIZE, PLAYER_SIZE)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


def drawing(screen, players):
    screen.fill((0,0,0))
    for player in players:
        player.draw(screen)
    pygame.display.update()


def receive_data(client_socket, message_queue):
    while True:
        try:
            raw_data = client_socket.recv(1024)
            if raw_data:
                data = pickle.loads(raw_data)
                message_queue.put(data)

        except socket.error as e:   # handle non-blocking socket error
            pass


def send_data(client_socket, data):
    serialized_data = pickle.dumps(data)
    client_socket.send(serialized_data)


def main():
    run = True
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIHGT))
    pygame.display.set_caption("Pygame Multiplayer Example")
    clock = pygame.time.Clock()
    players = []
    my_player = Player(random.randint(0, WINDOW_WIDTH - PLAYER_SIZE), random.randint(0, WINDOW_HEIHGT - PLAYER_SIZE),(0,0,255))
    players.append(my_player)
    players.append(my_player)

    # connect to server
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(SERVER_ADDRESS)
        client_socket.setblocking(False)
        message_queue = queue.Queue()
        receive_thread = threading.Thread(target=receive_data, args=(client_socket, message_queue,))
        receive_thread.start()
        print("[*] Connected to the server")
    except ConnectionRefusedError:
        print("[!] Failed to connect to the server")
        run = False
        pygame.quit()

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                run = False

        my_player.move()
        data = [my_player.x, my_player.y]
        send_data(client_socket, data)

        while not message_queue.empty():
            position = message_queue.get()
            opponent = Player(position[0], position[1], (255,0,0))
            players[1] = opponent

        drawing(screen, players)

    client_socket.close()


if __name__ == "__main__":
    main()