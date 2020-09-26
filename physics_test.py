from nogui import *
import time

class PRect:

    def __init__(self, matrix: Matrix, xywh: list, symbol: str, active: bool) -> None:

        self.matrix = matrix
        self.x = xywh[0]
        self.y = xywh[1]
        self.symbol = symbol
        self.active = active

        self.speedX = 0
        self.speedY = 0
        self.time = 0

        self.object = RectangleXYWH(matrix, xywh, symbol)

        self.draw = self.object.draw

    def update(self, time) -> None:

        if self.active:
            self._use_gravity(time)
        

    def _use_gravity(self, time):

        self.time += time

        self.speedY += 1*self.time

        self._update()
        

    def _update(self):
        
        self.x += self.speedX
        self.object.xywh[0] = self.x

        self.y += self.speedY
        self.object.xywh[1] = self.y




matrix = Matrix([40, 20], ".")

sq = PRect(matrix, [2, 2, 5, 5], "O", True)
floor = PRect(matrix, [1, 15, 7, 2], "#", False)

while 1:
    matrix.fill()

    sq.draw()
    floor.draw()

    if collision(sq.object, floor.object):
        sq.speedY *= -1

    if round(sq.speedY*100) > -10 and round(sq.speedY*100) < 10:
        sq.time = 0

    sq.update(1/60)

    clear_console()
    print(matrix.show())

    time.sleep(1/60)