import pygame

from auto import AutoForward, AutoBack
from config import width, img_dir, fps, height, snd_dir
from explosion import Explosion
from player import Bullet, Player, Arrow, Speedometer
from road import Tree, Board, Road
import time

pygame.init()

# Цвета
BLACK = "#000000"
WHITE = "#FFFFFF"
RED = "#FF0000"
GREEN = "#008000"
BLUE = "#0000FF"
CYAN = "#00FFFF"
GOLD = "#FFD700"

game_name = "Autoback"

# Создаем игровой экран
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption(game_name)  # Заголовок окна
icon = pygame.image.load(img_dir + 'icon.png')  # загружаем файл с иконкой
pygame.display.set_icon(icon)  # устанавливаем иконку в окно

timer = pygame.time.Clock()  # Создаем таймер pygame
run = True

all_sprites = pygame.sprite.Group()  # создаем группу спрайтов
players = pygame.sprite.Group()  # Создаем группу для игроков
bullets = pygame.sprite.Group()  # Создаем группу для пуль
cars = pygame.sprite.Group()  # Создаем группу для автомобилей
boards = pygame.sprite.Group()  # Создаем группу для бортиков
all_boards = pygame.sprite.Group()

player = Player()
speedometer = Speedometer()
arrow = Arrow()
road = Road()
board_left = Board("left")
board_right = Board("right")
auto_back = AutoBack()
auto_forward = AutoForward()

players.add(player)  # Добавляем игрока в группу
boards.add(board_left)
boards.add(board_right)
cars.add([auto_back, auto_forward])

all_sprites.add([road, board_left, board_right, auto_back, auto_forward, speedometer, arrow, player])

for i in range(20):
    tree = Tree()
    all_sprites.add(tree)


def get_hit_sprite(hits_dict):  # Функция возвращает спрайт с которым столкнулись
    for hit in hits_dict.values():
        return hit[0]


# pygame.mixer.Sound.set_volume()

pygame.mixer.music.load(snd_dir + 'music.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)


def draw_text(screen, text, size, x, y, color):  # Функция для отображения текста на экране
    font_name = 'font.ttf'
    font = pygame.font.Font(font_name, size)  # Шрифт выбранного типа и размера
    text_image = font.render(text, True, color)  # Превращаем текст в картинку
    text_rect = text_image.get_rect()  # Задаем рамку картинки с текстом
    text_rect.center = (x, y)  # Переносим центр текста в указанные координаты
    screen.blit(text_image, text_rect)  # Рисуем текст на экране


end_time = None

while run:  # Начинаем бесконечный цикл
    timer.tick(fps)  # Контроль времени (обновление игры)
    all_sprites.update()
    curr_time = time.time()
    player.score += player.speed // 10
    for event in pygame.event.get():  # Обработка ввода (события)
        if event.type == pygame.QUIT:  # Проверить закрытие окна
            run = False  # Завершаем игровой цикл
        if event.type == pygame.KEYDOWN and len(players) > 0:  # Если клавиша нажата
            if event.key == pygame.K_SPACE:
                player.snd_shoot.play()
                bullet = Bullet(player)  # Создаем пулю
                all_sprites.add(bullet)  # Добавляем пулю ко всем спрайтам
                bullets.add(bullet)  # Добавляем пулю ко всем пулям
    # Событие столкновения бортика и игрока
    hit_boards = pygame.sprite.groupcollide(players, boards, False, False)
    # Событие столкновения машин и игрока
    hit_cars = pygame.sprite.groupcollide(players, cars, False, False)
    if hit_boards or hit_cars:  # Если произошло события столкновения с бортом или авто
        player.speed = 0  # Скорость игрока на 0
        player.kill()  # Убиваем игрока
        end_time = time.time()
        player.snd_expl.play()  # Воспроизводим звук взрыва
        expl = Explosion(player.rect.center)
        all_sprites.add(expl)
        for sprite in all_sprites:
            try:
                sprite.speed = 0
                sprite.max_speed = 0
                sprite.min_speed = 0
            except Exception as e:
                print(e)

        end_time = time.time()

    hit_bullets = pygame.sprite.groupcollide(bullets, cars, True, False)
    if hit_bullets:  # Если произошло
        car = get_hit_sprite(hit_bullets)  # Определяем столкнувшееся авто
        car.sound.play()
        expl = Explosion(car.rect.center)
        all_sprites.add(expl)
        if car.type == 'forward':  # Определяем тип уничтоженного авто
            auto = AutoForward()  # Если попутка, создаем новую
            # auto.sound.play()  # Звук взрыва
            all_sprites.add(auto)
            cars.add(auto)
            player.score += 10
        else:
            auto = AutoBack()  # Если встречка, создаем новую
            # auto.sound.play()  # Звук взрыва
            all_sprites.add(auto)
            cars.add(auto)
            player.score += 50
        car.kill()  # Уничтожаем авто

    for car in cars:  # Перебираем в цикле все авто
        cars.remove(car)  # Удаляем одно авто из группы

        # Проверяем извлеченный авто на предмет столкновение с группой остальных спрайтов
        hit_another_car = pygame.sprite.spritecollide(car, cars, False)
        if hit_another_car:  # Если столкнулся
            car.sound.play()
            expl = Explosion(car.rect.center)
            all_sprites.add(expl)
            if car.type == 'forward':
                auto = AutoForward()
                all_sprites.add(auto)
                cars.add(auto)
            else:
                auto = AutoBack()
                all_sprites.add(auto)
                cars.add(auto)
            car.kill()  # Уничтожаем авто
        else:
            cars.add(car)  # Если не сталкивается, возвращаем обратно в группу

    # Рендеринг (прорисовка)
    screen.fill(GREEN)  # Заливка заднего фона
    all_sprites.draw(screen)  # отрисовка спрайтов
    draw_text(screen, f'Score = {player.score}', 50, 120, 20, GOLD)
    if not len(players):
        draw_text(screen, "GAME OVER", 100, width / 2, height / 2 - 50, WHITE)
        draw_text(screen, f"SCORE = {player.score}", 100, width / 2, height / 2 + 50, WHITE)

        if end_time:
            if curr_time - end_time > 3:
                run = False
                end_time = None

    pygame.display.update()  # Переворачиваем экран
pygame.quit()  # Корректно завершаем игру
