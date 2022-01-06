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
p_widht = 300
p_height = 600
#верхние левые точки
top_left_x = (WIDTH - p_widht) // 2
top_left_y = HEIGHT - p_height

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

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
    font = pygame.font.SysFont('comicsans', 60)
    name1 = font.render('ТЕТРИС', 1, ('white'))
    screen.blit(name1, (top_left_x + p_widht / 2 - (name1.get_width() / 2), 20))
    font3 = pygame.font.Font(None, 80)
    name2 = font3.render('Играть', 2, ('yellow'))
    screen.blit(name2, (top_left_x + p_widht / 2 - (name2.get_width() / 2), HEIGHT // 2 - 50))
    intro_text = ["Цель игры",
                  "заполнить как можно больше горизонтальных линий",
                  "на игровом поле, размещая опускающиеся фигуры",
                  "и не оставляя пустых пространств между ними."]

    font2 = pygame.font.Font(None, 40)
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

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]
S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]
L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]
O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]
I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]
J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]
T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]
blocks = [S, T, I, J, O, Z, L]
colors_blocks = ['blue', 'orange', 'red', 'purple', 'yellow', 'aqua', 'green']


start_screen()
def draw(surface)

class Board:
        def __init__(self, p_width, p_height):
            self.p_width = p_width
            self.p_height = p_height
            self.board = [[0] * p_width for _ in range(p_height)]
            self.left = 10
            self.top = 10
            self.cell_size = 30

        def set_view(self, left, top, cell_size):
            self.left = left
            self.top = top
            self.cell_size = cell_size

        def render(self, screen):
            for x in range(self.p_width):
                for y in range(self.p_height):
                    pygame.draw.rect(screen, (255, 255, 255), (
                        x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size),
                                     1)


board = Board(10, 20)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    board.render(screen)
    pygame.display.flip() 
