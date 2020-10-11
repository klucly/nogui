from nogui import *


w = Matrix([80, 40], " ", 60, True)

r = RectangleXYWH(w, [20, 4], [30, 20], "W")

def on_click():
    print(1)

hold = False

while 1:
    if r.mouse_down():
        hold = True
        r.symbol = "."

    if r.mouse_up():
        if hold:
            on_click()

    if w.mouse_up():
        r.symbol = "w"
        hold = False

    w.fill()
    r.draw()
    # r.fill()
    w.show()