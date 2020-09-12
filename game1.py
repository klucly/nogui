from random import randint
from nogui import *
import random


class player_control:

    def w(player: Sprite) -> None:
        player.xywh[1] -=  1

    def a(player: Sprite) -> None:
        player.xywh[0] -=  2

    def s(player: Sprite) -> None:
        player.xywh[1] -=- 1

    def d(player: Sprite) -> None:
        player.xywh[0] -=- 2

    def player_shoot(player: Sprite, buttet_list: list) -> None:
        xy = player.xywh[:2]
        xy[0] += 2
        buttet_list.append(Sprite(player.matrix, xy, Sprites.player_bullet))

    def main_control(player: Sprite, tick, bullet_list) -> None:
        if press("w") and player.xywh[1] != 0:
            player_control.w(player)
        elif press("s") and player.xywh[1] != 9:
            player_control.s(player)

        if press("a") and player.xywh[0] != 0:
            player_control.a(player)
        elif press("d") and player.xywh[0] != 78:
            player_control.d(player)

        if press(" "):
            if tick % 3 == 0:
                player_control.player_shoot(player, bullet_list)


class Sprites:

    player = "|=-"
    player_bullet = "-"

    star1 = "*"
    star2 = "`"
    star3 = "."
    star4 = ","
    starlist = ["*", "`", ".", ","]

    enemyF = "=<|"
    enemyE = "==|\\\n==|/"
    enemyD = "-=|>"
    enemyC = "x-<>"
    enemyB = "--~~>=<>"
    enemyA = "===--\\\n  +|  /\nx==  >-)\n  +|  \\\n===--/"


# class Enemy:
#     moves = ["foreward", "backward", "left", "right"]
    
#     class Standart:
        
#         def __init__(self, matrix, xy, speed) -> None:

#             self.next_move = ""
#             self.matrix = matrix
#             self.xy = xy
#             self.speed = speed
#             self.shoot = False

#         def step(self):

#             if self.next_move == "foreward":
#                 self.xy[0] -= 2
                
#             elif self.next_move == "backward":
#                 self.xy[0] -=- 2
                
#             elif self.next_move == "left":
#                 self.xy[1] -=- 1
                
#             elif self.next_move == "right":
#                 self.xy[1] -= 1

#             self.next_move = ""
#             self.shoot = False



#     class F(Standart):
        
#         def __init__(self, matrix, xy) -> None:

#             super().__init__(matrix, xy, 5)
#             self.sprite = Sprite(matrix, xy, Sprites.enemyF)
#             self.hp = 5

#         def step(self, tick, number):
#             if (tick+number) % 20 == 0:

#                 self.next_move = random.choice(Enemy.moves)

#                 if self.next_move == "right" and self.xy[1] <= 0:
#                     self.next_move = ""

#                 elif self.next_move == "left" and self.xy[1] >= 9:
#                     self.next_move = ""

#                 elif self.next_move == "forward" and self.xy[0] <= 0:
#                     self.next_move = ""

#                 elif self.next_move == "backward" and self.xy[0] >= 77:
#                     self.next_move = ""

#                 super().step()

#                 self.sprite.xywh[0] = self.xy[0]
#                 self.sprite.xywh[1] = self.xy[1]

class Enemy:
    moves = ["foreward", "backward", "left", "right"]
    ships_parts = "=<|\\/<>-x+~"

    class Default:

        def __init__(self, matrix, xy, number) -> None:

            self.matrix = matrix
            self.xy = xy
            self.sprite = Sprite(matrix, xy, Sprites.enemyF)
            self.number = number
            self.move = ""
            self.shoot = False

        def step(self, around, tick):
            
            if self.move == "foreward":
                self.xy[0] -= 2
            
            elif self.move == "backward":
                self.xy[0] -=- 2
            
            elif self.move == "left":
                self.xy[1] -= 1
            
            elif self.move == "right":
                self.xy[1] -=- 1


    class F(Default):

        def __init__(self, matrix, xy, number) -> None:

            super().__init__(matrix, xy, number)
            self.hp = 5


        def step(self, tick):
            
            if (tick+self.number) % 20:

                    
                move = random.choice(Enemy.moves)
                around = self.sprite.matrix.matrix

                foreward = around[self.xy[1]][self.xy[0]-1]
                backward = around[self.xy[1]][self.xy[0]+3]
                

                if move == "foreward" and foreward not in Enemy.ships_parts and self.xy[0] != 0:
                    self.move = move

                if move == "backward" and backward not in Enemy.ships_parts and self.xy[0] != 0:
                    self.move = move



def stars_init(matrix, starlist) -> None:
    for i in range(10):
        xy = [random.randint(0, 80), random.randint(0, 9)]
        sprite = random.choice(Sprites.starlist)
        starlist.append(Sprite(matrix, xy, sprite))


def Wave(matrix, difficult) -> None:

    enemylist = []

    for i in range(difficult):
        enemylist.append(Enemy.F(matrix, [random.randint(20, 79), random.randint(0, 9)], i))

    return enemylist


def stars_update(starlist) -> None:

    for star in starlist:
        if star.xywh[0] < 0:
            star.xywh[0] = 80
            star.xywh[1] = random.randint(0, 9)
            star.line_split = [random.choice(Sprites.starlist)]

        star.xywh[0] -= .1
        
    for star in starlist:
        star.draw()


def bullet_update(bullet_list) -> None:
    
    for bullet in bullet_list:
        if bullet.xywh[0] > 80:
            bullet_list.remove(bullet)
        bullet.xywh[0] += 4
        bullet.draw()


def score_update(bullet_list, score) -> None:
    
    score_str = f"||{str(len(bullet_list))}"
    score_str += " "*(6-len(score_str))+"||"
    score_str_top = "|======|"
    score_str_bottom = score_str_top
    score.line_split = [score_str_top, score_str, score_str_bottom]
    score.draw()


def enemy_update(enemylist, bullet_list, tick) -> None:

    for enemy in enemylist:
        for bullet in bullet_list:
            if collision(bullet, enemy.sprite):
                enemy.hp -= 1
                bullet_list.remove(bullet)

        if enemy.hp <= 0:
            enemylist.remove(enemy)
        
        enemy.step(tick)
        
        enemy.sprite.draw()


class Main:

    def init(self):

        self.matrix = Matrix([80, 10], " ")

        self.bullet_list = []
        self.starlist = []
        self.enemylist = []
        self.wave = 1
        self.tick = 0
        self.score = Sprite(self.matrix, [0, 0], "\n--------\n")

        self.player = Sprite(self.matrix, [0, 5], Sprites.player)

        stars_init(self.matrix, self.starlist)


    def __init__(self):

        self.init()

        matrix = self.matrix
        starlist = self.starlist
        player = self.player
        tick = self.tick
        bullet_list = self.bullet_list
        score = self.score
        wave = self.wave
        enemylist = self.enemylist

        while 1:
                
            matrix.fill()

            stars_update(starlist)
            
            player_control.main_control(player, tick, bullet_list)

            bullet_update(bullet_list)

            player.draw()

            score_update(bullet_list, score)

            enemy_update(enemylist, bullet_list, tick)

            wave1 = random.randint(10*(wave+2), 10*(wave+2)**2)
            if tick % wave1 == 0:
                for wave_ in Wave(matrix, wave*random.randint(round(wave/2), round(wave**2/10+1))):
                    enemylist.append(wave_)
                wave += 1


            clear_console()
            print(matrix.show())

            tick += 1
            wait(1/30)

if __name__ == "__main__":
    Main()