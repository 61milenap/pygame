import os
import sys
import pygame
from pygame import surface

pygame.init()
FPS = 50
#размеры самого экрана
WIDTH = 800
HEIGHT = 700
#размеры поля игры
color_blocks = ['red', 'orange', 'yellow','green', 'blue', 'indigo', 'purple']

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class blocks:
    blocks = [ [ [1, 2, 6, 10], 
                [5, 6, 7, 9], 
                [2, 6, 10, 11], 
                [3, 5, 6, 7] ],
               [ [6, 7, 9, 10],
                 [1, 5, 6, 10]],

    ]
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)

    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    pygame.font.init()
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('georgia', 60)
    name1 = font.render('ТЕТРИС', 1, ('white'))
    screen.blit(name1, (top_left_x + p_widht / 2 - (name1.get_width() / 2), 20))
    font3 = pygame.font.SysFont('cambria', 80)
    name2 = font3.render('Играть', 2, ('yellow'))
    screen.blit(name2, (top_left_x + p_widht / 2 - (name2.get_width() / 2), HEIGHT // 2 - 50))
    intro_text = ["Цель игры:",
                  "заполнить как можно больше горизонтальных линий",
                  "на игровом поле, размещая опускающиеся фигуры",
                  "и не оставляя пустых пространств между ними."]

    font2 = pygame.font.SysFont('impact', 30)
    text_coord = HEIGHT // 1.4
    for line in intro_text:
        string_rendered = font2.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)

