from blocks import Blocks


class Tetris:
    level = 2
    score = 0
    poss = "НАЧАТЬ"
    x = 100
    y = 60
    cell_size = 20
    block = None
    high_score = 0

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
