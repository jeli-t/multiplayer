import pygame
import random
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


def main():
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


if __name__ == "__main__":
    main()