from math import sin
from nogui import *

w = Matrix([80, 40], " ", 60, True)

c = Circle(w, [40, 20], 1, "O", True)

tick = 0
while 1:
    tick += 1
    c.radius = abs(sin(tick/100)*40)
    w.fill()
    c.fill()
    c.draw()
    w.show()