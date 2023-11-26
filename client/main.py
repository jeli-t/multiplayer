import pygame
import random
import socket
import threading
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


def drawing(screen, player):
    screen.fill((0,0,0))
    player.draw(screen)
    pygame.display.update()


def receive_data(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"Received from server: {data.decode('utf-8')}")

        except Exception as e:
            print(f"Error: {e}")
            break


def send_data(client_socket):
    while True:
        message = input("Enter a message: ")
        client_socket.send(message.encode('utf-8'))


def main():
    # connect to server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(SERVER_ADDRESS)
    receive_thread = threading.Thread(target=receive_data, args=(client_socket,))
    send_thread = threading.Thread(target=send_data, args=(client_socket,))
    receive_thread.start()
    send_thread.start()
    receive_thread.join()
    send_thread.join()

    # game logic
    run = True
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIHGT))
    clock = pygame.time.Clock()
    player = Player(0,0,(random.randint(50,255),random.randint(50,255),random.randint(50,255)))

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                run = False

        player.move()
        drawing(screen, player)

    client_socket.close()


if __name__ == "__main__":
    main()