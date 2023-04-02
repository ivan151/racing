import random

import pygame
from config import width, height, snd_dir, img_dir


class Road(pygame.sprite.Sprite):
    def __init__(self):  # Функция, где указываем что будет у игрока
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img_dir + "road.jpg")
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, 0)
        self.max_speed = 50
        self.min_speed = 0
        self.speed = 0

    def update(self):  # Функция, действия которой будут выполняться каждый тик
        self.rect.y += self.speed  # Изменяем положение по вертикали

        keystate = pygame.key.get_pressed()  # Сохраняем нажатие на кнопку
        if keystate[pygame.K_UP] and self.speed < self.max_speed:  # Стрелка вверх
            self.speed += 1
        elif keystate[pygame.K_DOWN] and self.speed > self.min_speed:  # Стрелка вниз
            self.speed -= 1

        if self.rect.centery > height:  # Если центр достиг низа
            self.rect.centery = 0  # Переносим дорогу


class Board(pygame.sprite.Sprite):
    def __init__(self, type):  # Функция, где указываем что будет у игрока
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(img_dir + "board.png")
        self.rect = self.image.get_rect()
        self.speed = 0
        self.max_speed = 50
        self.min_speed = 0

        if type == 'right':
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect.centerx = width // 2 + 370
        else:
            self.rect.centerx = width // 2 - 370

    def update(self):  # Функция, действия которой будут выполняться каждый тик
        keystate = pygame.key.get_pressed()  # Сохраняем нажатие на кнопку
        if keystate[pygame.K_UP] and self.speed < self.max_speed:  # Стрелка вверх
            self.speed += 1
        elif keystate[pygame.K_DOWN] and self.speed > self.min_speed:  # Стрелка вниз
            self.speed -= 1

        self.rect.y += self.speed  # Изменяем положение по вертикали

        if self.rect.centery > height:  # Если центр достиг низа
            self.rect.centery = 0  # Переносим бортик


class Tree(pygame.sprite.Sprite):
    def __init__(self):  # Функция, где указываем что будет у игрока
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img_dir + f"trees/{random.randint(1, 16)}.png")

        self.rect = self.image.get_rect()

        self.rect.x = width // 2
        self.rect.y = random.randrange(-height, 0, 50)

        self.side = random.choice(['left', 'right'])
        if self.side == 'left':
            self.rect.x = self.rect.x - 450 - random.randint(10, 350)
        elif self.side == 'right':
            self.rect.x = self.rect.x + 380 + random.randint(10, 350)

        self.speed = 0
        self.max_speed = 50
        self.min_speed = 0

    def update(self):  # Функция, действия которой будут выполняться каждый тик
        keystate = pygame.key.get_pressed()  # Сохраняем нажатие на кнопку
        if keystate[pygame.K_UP] and self.speed < self.max_speed:  # Стрелка вверх
            self.speed += 1
        elif keystate[pygame.K_DOWN] and self.speed > self.min_speed:  # Стрелка вниз
            self.speed -= 1

        self.rect.y += self.speed  # Изменяем положение по вертикали

        # Если достигли одного из краев экрана
        if self.rect.top > height:
            self.rect.y = random.randrange(-height, 0, 50)
            self.side = random.choice(['left', 'right'])
            if self.side == 'left':
                self.rect.x = width // 2 - 450 - random.randint(10, 350)
            elif self.side == 'right':
                self.rect.x = width // 2 + 380 + random.randint(10, 350)