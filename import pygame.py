import os
import sys
import pygame
import random

pygame.display.set_caption("Тетрис")
pygame.init()
FPS = 25

#размеры самого экрана
WIDTH = 400
HEIGHT = 500
size = (WIDTH, HEIGHT)
#размеры поля
p_height = 600
p_width = 300
#крайние левые точки
top_left_x = (WIDTH - p_width) // 2
top_left_y = HEIGHT - p_height
#цвета блоков
colors_block = [(255, 0, 0), (255, 125, 0), (255, 255, 0),
          (0, 255, 0), (175, 214, 255), (0, 0, 255),
          (170, 0, 255)]

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
    font = pygame.font.SysFont('georgia', 60)
    name1 = font.render('ТЕТРИС', 1, ('white'))
    screen.blit(name1, (top_left_x + p_width / 2 - (name1.get_width() / 2), 20))
    font3 = pygame.font.SysFont('cambria', 80)
    name2 = font3.render('Играть', 2, ('yellow'))
    screen.blit(name2, (top_left_x + p_width / 2 - (name2.get_width() / 2), HEIGHT // 2 - 50))
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
                return # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)

start_screen()

class Blocks:
    x = 0
    y = 0
    blocks = [ [ [1, 2, 6, 10], 
                 [5, 6, 7, 9], 
                 [2, 6, 10, 11], 
                 [3, 5, 6, 7] ],
               [ [6, 7, 9, 10],
                 [1, 5, 6, 10] ],
               [ [1, 4, 5, 6], 
                 [1, 4, 5, 9], 
                 [4, 5, 6, 9], 
                 [1, 5, 6, 9]] ,
               [ [1, 2, 5, 6] ],
               [ [1, 2, 5, 9],
                 [0, 4, 5, 6], 
                 [1, 5, 9, 8], 
                 [4, 5, 6, 10] ],
               [ [1, 5, 9, 13],
                 [4, 5, 6, 7] ],
               [[4, 5, 9, 10], 
                [2, 6, 5, 9] ] ]
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.blocks) - 1)
        self.color = random.randint(1, len(colors_block) - 1)
        self.rotation = 0

    def image(self):
        return self.blocks[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.blocks[self.type])


class Tetris:
    level = 2
    score = 0
    poss = "НАЧАТЬ"
    field = []
    height = 0
    width = 0
    x = 100
    y = 60
    cell_size = 20
    block = None

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.board = []
        self.score = 0
        self.poss = "НАЧАТЬ"
        for _ in range(height):
            new_line = []
            for _ in range(width):
                new_line.append(0)
            self.board.append(new_line)

    def new_block(self):
        self.block = Blocks(3, 0)

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.block.image():
                    if i + self.block.y > self.height - 1 or \
                            j + self.block.x > self.width - 1 or \
                            j + self.block.x < 0 or \
                            self.board[i + self.block.y][j + self.block.x] > 0:
                        intersection = True
        return intersection

    def break_lines(self):
        line = 0
        for i in range(1, self.height):
            zero = 0
            for j in range(self.width):
                if self.board[i][j] == 0:
                    zero += 1
            if zero == 0:
                line += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.board[i1][j] = self.board[i1 - 1][j]
        self.score += line ** 2

    def go_space(self):
        while not self.intersects():
            self.block.y += 1
        self.block.y -= 1
        self.freeze()

    def go_down(self):
        self.block.y += 1
        if self.intersects():
            self.block.y -= 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.block.image():
                    self.board[i + self.block.y][j + self.block.x] = self.block.color
        self.break_lines()
        self.new_block()
        if self.intersects():
            self.poss = "ИГРА ОКОНЧЕНА"

    def go_side(self, dx):
        old_x = self.block.x
        self.block.x += dx
        if self.intersects():
            self.block.x = old_x

    def rotate(self):
        old_rotation = self.block.rotation
        self.block.rotate()
        if self.intersects():
            self.block.rotation = old_rotation

running = True
game = Tetris(20, 10)
counter = 0
pressing_down = False

while running:
    if game.block is None:
        game.new_block()
    counter += 1
    if counter > 100000:
        counter = 0

    if counter % (FPS // game.level // 2) == 0 or pressing_down:
        if game.poss == "НАЧАТЬ":
            game.go_down()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:
                game.go_side(1)
            if event.key == pygame.K_SPACE:
                game.go_space()
            if event.key == pygame.K_ESCAPE:
                game.__init__(20, 10)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False
        
        if event.type == pygame.QUIT:
                terminate()

    screen.fill('black')

    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, 'white', [game.x + game.cell_size * j, game.y + game.cell_size * i, game.cell_size, game.cell_size], 1)
            if game.board[i][j] > 0:
                pygame.draw.rect(screen, colors[game.board[i][j]],
                                 [game.x + game.cell_size * j + 1, game.y + game.cell_size * i + 1, game.cell_size - 2, game.cell_size - 1])

    if game.block is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.block.image():
                    pygame.draw.rect(screen, colors_block[game.block.color],
                                     [game.x + game.cell_size * (j + game.block.x) + 1,
                                      game.y + game.cell_size * (i + game.block.y) + 1,
                                      game.cell_size - 2, game.cell_size - 2])

    font = pygame.font.SysFont('cambria', 25, True, False)
    font1 = pygame.font.SysFont('cambria', 35, True, False)

    text = font.render("СЧЁТ " + str(game.score), True, 'red')
    
    gameover1 = font1.render("Press ESC", True, 'red')
    gameover= font1.render("ИГРА ОКОНЧЕНА", True, 'red')

    screen.blit(text, [0, 0])
    if game.poss == "ИГРА ОКОНЧЕНА":
        screen.blit(gameover, [20, 200])
        screen.blit(gameover1, [25, 265])

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()