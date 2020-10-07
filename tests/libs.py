from nogui import *
from math import *
from random import *

def middle(l: list) -> float:
    r = 0
    for i in l: r += i
    return r/len(l)

class Plate:

    def __init__(self, matrix, _tick, tick, speed, difficulty) -> None:

        self.x = randint(0, 35)
        self.y = 5
        self.wh = 5
        self.tick = tick
        self._tick = _tick
        self.speed = speed
        self.is_pressed = False
        self.difficulty = difficulty

        self.object = RectangleXYWH(matrix, [self.x, self.y, self.wh, self.wh], "#")

    def update(self):
        self.y += ((self._tick*10+(self.tick/100000)**2)*self.speed+(self.difficulty-1)/10)/10+.02

        self.object.xywh[1] = self.y

        self.object.draw()

score_sprite = '''/--------------------------------------\\
|||/                                \\|||
|||                                  |||
|||\\                                /|||
\\--------------------------------------/'''

class Score:
    def __init__(self, matrix, score) -> None:
        self.x = 0
        self.y = 0
        self.score = score
        self.w = Sprite(matrix, [0, 2], "")

        self.object = Sprite(matrix, [0, 0], score_sprite)

    def update(self, score):
        self.object.draw()
        score = round(score)

        score_lenght = str(score).__len__()
        line = "|||"+" "*((34-score_lenght)//2)+str(score)+" "*((34-score_lenght)//2)+"|||"
        if line.__len__() % 2 == 1:
            line = line[:-3]+" |||"

        self.w.sprite = line
        self.w.draw()

start_sign = '''
._.....|.....__....._.....|.
|.\...-+-......|.../..\..-+-
.\.....|..../--|...|......|.
..\....|...|...|...|......|.
\_/....|....\--|...|......|.
'''

options_sign = '''
/-\.|-\._|_.`./-\.|\..|./-\.
|.|.|-/..|..|.|.|.|.\.|.\-\.
\-/.|....|..|.\-/.|..\|.__/.
'''

right_arrow = '''
.-\\
--|
.-/
'''

left_arrow = '''
/-.
|--
\-.
'''

class Selection:

    def __init__(self, matrix) -> None:

        self.matrix = matrix
        self.x = 0
        self.y = 0
        self.selection = 0

        self.left = Sprite(matrix, [2, 11], left_arrow)
        self.right = Sprite(matrix, [34, 11], right_arrow)

    def update(self):

        self.left.draw()
        self.right.draw()

    def go_down(self):

        self.left = Sprite(self.matrix, [2, 16], left_arrow)
        self.right = Sprite(self.matrix, [34, 16], right_arrow)

        self.selection = 1

    def go_up(self):

        self.left = Sprite(self.matrix, [2, 11], left_arrow)
        self.right = Sprite(self.matrix, [34, 11], right_arrow)

        self.selection = 0