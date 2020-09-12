from nogui_portable import *

matrix = Matrix([80, 15], ".")

triangle_coords = [[11, 5], [25, 5], [18, 10]]
triangle_coords1 = [[11+30, 5], [25+30, 5], [18+30, 10]]

triangle = Polygon(matrix, triangle_coords, "%")
triangle1 = Polygon(matrix, triangle_coords1, "$", fixed_out = 1)

while 1:

    matrix.fill()

    triangle.angle += 10
    triangle1.angle += 10

    triangle.draw()
    triangle1.draw()

    clear_console()

    print(matrix.show())

    wait(1/30)

