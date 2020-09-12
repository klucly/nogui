from nogui import *
from math import sin

doFill = True

def out(matrix: Matrix, tick: int) -> None:
    
    clear_console()
    print(matrix.show())
    matrix.fill()

x, y = 30, 4

w, h = 10, 10

rawcoords = [[x, y], [x, y+h], [x+w, y+h], [x+w, y]]

matrix = Matrix([50, 20], " ")

obj = Polygon(matrix, rawcoords, "@", fixed_out = True)

tick = 0

fill = " .,*^O0#@"

while 1:

    for coords in obj.coords[:2]:
        coords[0] = sin(tick/200)*(w/2)+x
    for coords in obj.coords[2:]:
        coords[0] = sin(-tick/200)*(w/2)+x+w

    obj.angle = sin(tick/1000)*360

    if doFill:
        Acoords = sin(tick/200)*(w/2)+x
        Bcoords = sin(-tick/200)*(w/2)+x+w
        numberOfFillSymbol = (Bcoords-Acoords)/2.5+2
        obj.fill(fill[-int(numberOfFillSymbol)])
    obj.draw()
    out(matrix, tick)
    tick += 1