import os
import sys
import pygame
from tetris import Tetris

pygame.mixer.music.load("sounds/tetris.mp3")

pygame.display.set_caption("Тетрис")
pygame.init()
FPS = 25

# размеры самого экрана
WIDTH = 400
HEIGHT = 500
size = (WIDTH, HEIGHT)
# размеры поля
p_height = 400
p_width = 200
# крайние левые точки
top_left_x = (WIDTH - p_width) // 2
top_left_y = HEIGHT - p_height


# цвета блоков
colors_block = [(255, 0, 0), (255, 125, 0), (255, 255, 0),
                (0, 255, 0), (175, 214, 255), (0, 0, 255),
                (170, 0, 255)]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    clock.tick(FPS)

pygame.mixer.music.play(-1)


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
    screen.blit(name1, (top_left_x + p_width /
                2 - (name1.get_width() / 2), 20))
    font3 = pygame.font.SysFont('cambria', 80)
    name2 = font3.render('Играть', 2, ('yellow'))
    screen.blit(name2, (top_left_x + p_width / 2 -
                (name2.get_width() / 2), HEIGHT // 2 - 50))
    intro_text = ["Цель игры:",
                  "заполнить как можно больше горизонтальных линий",
                  "на игровом поле, размещая опускающиеся фигуры",
                  "и не оставляя пустых пространств между ними."]
    font2 = pygame.font.SysFont('impact', 16)
    text_coord = HEIGHT // 1.4
    for line in intro_text:
        string_rendered = font2.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 5
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


start_screen()


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
            pygame.draw.rect(screen, 'white', [
                             game.x + game.cell_size * j, game.y + game.cell_size * i, game.cell_size, game.cell_size], 1)
            if game.board[i][j] > 0:
                pygame.draw.rect(screen, colors_block[game.board[i][j]],
                                 [game.x + game.cell_size * j + 1, game.y + game.cell_size * i + 1, game.cell_size - 2, game.cell_size - 1])

    if game.block is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.block.image():
                    pygame.draw.rect(screen, colors_block[game.block.color],
                                     [game.x + game.cell_size * (j + game.block.x) + 1,
                                      game.y + game.cell_size *
                                      (i + game.block.y) + 1,
                                      game.cell_size - 2, game.cell_size - 2])

    font = pygame.font.SysFont('cambria', 25, True, False)
    font1 = pygame.font.SysFont('cambria', 35, True, False)

    text = font.render("СЧЁТ " + str(game.score), True, 'red')

    gameover1 = font1.render("Press ESC", True, 'red')
    gameover = font1.render("ИГРА ОКОНЧЕНА", True, 'red')

    screen.blit(text, [0, 0])
    if game.poss == "ИГРА ОКОНЧЕНА":
        screen.blit(gameover, [20, 200])
        screen.blit(gameover1, [25, 265])

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
