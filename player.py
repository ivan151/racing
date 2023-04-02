import pygame
from config import width, height, snd_dir, img_dir


class Player(pygame.sprite.Sprite):
    def __init__(self):  # Функция, где указываем что будет у игрока
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img_dir + "player.png")
        self.rect = self.image.get_rect()
        self.rect.x = width // 2
        self.rect.y = height - 150
        self.max_speed = 50
        self.min_speed = 0
        self.snd_move = pygame.mixer.Sound(snd_dir + 'motor.mp3') # урок 16
        self.snd_shoot = pygame.mixer.Sound(snd_dir + 'shoot.mp3')
        self.snd_expl = pygame.mixer.Sound(snd_dir + 'explosion_player.mp3')
        self.speed = 0
        self.score = 0

    def update(self):  # Функция, действия которой выполнятся каждый тик
        keystate = pygame.key.get_pressed()  # Сохраняем нажатие на кнопку
        if keystate[pygame.K_RIGHT]:  # Если нажата стрелка вправо
            self.rect.x += 15  # Изменяем координату Х на 5
        elif keystate[pygame.K_LEFT]:  # Если нажата стрелка влево
            self.rect.x -= 15  # Изменяем координату Х на -5
        elif keystate[pygame.K_UP] and self.speed < self.max_speed:  # Стрелка вверх
            self.speed += 1
        elif keystate[pygame.K_DOWN] and self.speed > self.min_speed:  # Стрелка вниз
            self.speed -= 1
        # урок 16
        if self.speed > 0 and not pygame.mixer.get_busy():
            self.snd_move.play()
        if self.speed == 0:
            self.snd_move.stop()


class Speedometer(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img_dir + 'speedometr.png')
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.rect = self.image.get_rect()
        self.rect.center = (100, height - 100)  # Левый нижний угол


class Arrow(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img_dir + 'arrow.png')
        self.image = pygame.transform.rotate(self.image, -200)
        self.rect = self.image.get_rect()
        self.copy = self.image
        self.rect.center = (100, height - 100)  # Располагаем стрелку

        self.max_speed = 50
        self.min_speed = 0
        self.speed = 0

    def rotate(self, rotate):
        self.image = pygame.transform.rotate(self.copy, rotate)  # Поворачиваем копию
        self.rect = self.image.get_rect(center=self.rect.center)  # Изменяем рамку

    def update(self):
        keystate = pygame.key.get_pressed()  # Сохраняем нажатие на кнопку
        if keystate[pygame.K_UP] and self.speed < self.max_speed:  # Стрелка вверх
            self.speed += 1
        elif keystate[pygame.K_DOWN] and self.speed > self.min_speed:  # Стрелка вниз
            self.speed -= 1

        self.rotate(-self.speed * 6)  # Крутим стрелку


class Bullet(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img_dir + 'shell.png')
        self.image = pygame.transform.scale(self.image, (4, 15))

        self.rect = self.image.get_rect()
        self.rect.center = player.rect.center  # Располагаем пулю там же где и игрок
        self.speed = 50

    def update(self):
        self.rect.y -= self.speed  # Полет пули против оси Y
        if self.rect.y < 0:  # Если залетела за верхний край экрана
            self.kill()
