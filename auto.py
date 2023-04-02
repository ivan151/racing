import random

import pygame

from config import width, img_dir, height, snd_dir


class AutoForward(pygame.sprite.Sprite):
    def __init__(self):  # Функция, где указываем что будет у игрока
        pygame.sprite.Sprite.__init__(self)
        self.type = 'forward'
        self.image = pygame.image.load(img_dir + f"/auto/{random.randint(0, 4)}.png")
        self.rect = self.image.get_rect()
        self.points = [(width / 2 + 50),  # Точки спауна по горизонтали
                       (width / 2 + 130),
                       (width / 2 + 210),
                       (width / 2 + 290)]
        self.rect.centerx = random.choice(self.points)  # Случайное значение центра рамки по оси X
        self.rect.centery = random.randrange(-height, 0, 300)

        self.max_speed = 25
        self.min_speed = 2
        self.speed = -random.randint(self.min_speed, self.max_speed)

        self.global_speed = 0  # Общая скорость движения
        self.global_min_speed = 0  # Общая минимальная скорость движения
        self.global_max_speed = 50  # Общая максимальная скорость движения
        self.sound = pygame.mixer.Sound(snd_dir + 'explosion_car.mp3')

    def update(self):  # Функция, действия которой будут выполняться каждый тик
        keystate = pygame.key.get_pressed()  # Сохраняем нажатие на кнопку
        if keystate[pygame.K_UP] and self.global_speed < self.global_max_speed:
            self.global_speed += 1
        elif keystate[pygame.K_DOWN] and self.global_speed > self.global_min_speed:
            self.global_speed -= 1
        self.rect.y += self.speed + self.global_speed  # Изменяем положение по вертикали
        if self.rect.top > height * 2:  # Если осталась далеко позади
            self.speed = -random.randint(self.min_speed, self.max_speed)
            self.rect.centerx = random.choice(self.points)
            self.rect.y = random.randrange(-height, 0, 300)  # Спауним сверху


class AutoBack(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.type = 'backward'
        self.image = pygame.image.load(img_dir + f"/auto/{random.randint(0, 4)}.png")
        self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()
        self.points = [(width / 2 - 50),  # Точки спауна по горизонтали
                       (width / 2 - 130),
                       (width / 2 - 210),
                       (width / 2 - 290)]
        self.rect.centerx = random.choice(self.points)  # Случайное значение центра рамки по оси X
        self.rect.y = random.randrange(-height, 0, 300)

        self.max_speed = 25
        self.min_speed = 5
        self.speed = random.randint(self.min_speed, self.max_speed)

        self.global_speed = 0  # Общая скорость движения
        self.global_min_speed = 0  # Общая минимальная скорость движения
        self.global_max_speed = 50  # Общая максимальная скорость движения
        self.sound = pygame.mixer.Sound(snd_dir + 'explosion_car.mp3')

    def update(self):  # Функция, действия которой будут выполняться каждый тик
        keystate = pygame.key.get_pressed()  # Сохраняем нажатие на кнопку
        if keystate[pygame.K_UP] and self.global_speed < self.global_max_speed:
            self.global_speed += 1
        elif keystate[pygame.K_DOWN] and self.global_speed > self.global_min_speed:
            self.global_speed -= 1
        self.rect.y += self.speed + self.global_speed  # Изменяем положение по вертикали
        if self.rect.top > height:  # Если осталась далеко позади
            self.speed = random.randint(self.min_speed, self.max_speed)
            self.rect.centerx = random.choice(self.points)
            self.rect.y = random.randrange(-height, 0, 300)  # Спауним сверху
