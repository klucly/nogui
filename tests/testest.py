from math import sin
from nogui import *

w = Matrix([80, 40], " ", 60, True)

r = RectangleXYWH(w, [20, 4, 40, 20], "I")

while 1:
    if r.mouse_down():
        r.symbol = "0"
    if w.mouse_up() != None:
        print(1)
        r.symbol = "I"
    w.fill()
    r.draw()
    w.show()