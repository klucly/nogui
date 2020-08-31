from nogui import *

matrix = Matrix([60, 30])

xy = 10, 10
wh = 10, 10

rect = RectangleFULL(matrix, xy, wh, "$", 0)
rect1 = RectangleFULL(matrix, [30, 10], wh, "$", 0)

while 1:
    matrix.fill()

    rect.draw()

    rect.angle += 5

    rect1.draw()
    
    rect1.angle += 5

    clear_console()

    print(matrix.show())

    wait(.05)