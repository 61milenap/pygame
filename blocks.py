import random


class Blocks:
    x = 0
    y = 0
    blocks = [[[1, 2, 6, 10],
               [5, 6, 7, 9],
               [2, 6, 10, 11],
               [3, 5, 6, 7]],
              [[6, 7, 9, 10],
               [1, 5, 6, 10]],
              [[1, 4, 5, 6],
               [1, 4, 5, 9],
               [4, 5, 6, 9],
               [1, 5, 6, 9]],
              [[1, 2, 5, 6]],
              [[1, 2, 5, 9],
               [0, 4, 5, 6],
               [1, 5, 9, 8],
               [4, 5, 6, 10]],
              [[1, 5, 9, 13],
               [4, 5, 6, 7]],
              [[4, 5, 9, 10],
               [2, 6, 5, 9]]]
    colors_block = [(255, 0, 0), (255, 125, 0), (255, 255, 0),
                    (0, 255, 0), (175, 214, 255), (0, 0, 255),
                    (170, 0, 255)]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.blocks) - 1)
        self.color = random.randint(1, len(self.colors_block) - 1)
        self.rotation = 0

    def image(self):
        return self.blocks[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.blocks[self.type])
