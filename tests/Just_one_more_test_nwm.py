from nogui import *


matrix = Matrix([80, 40], " ")

a = RectangleFULL(matrix, [20, 0], [40, 40], "O", 0, True)
a1 = RectangleFULL(matrix, [12, -8], [56, 56], "O", 0, True)

c = Circle(matrix, [40, 20], 28, "M", 100, True)
c1 = Circle(matrix, [40, 20], 20, "M", fixed_out = True)

tick = 0
while 1:
    tick += .5

    a.angle += (math.sin(tick/50))*2
    a1.angle += -(math.sin(tick/50))*2
    
    matrix.fill()
    a1.draw()
    c.draw()
    a.draw()
    a.figure.fill("u")
    c1.draw()

    clear_console()
    matrix.show()
