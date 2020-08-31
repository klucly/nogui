from nogui import *

matrix = Matrix([21, 11], ".")

coords = [[10, 0], [2, 2], [10, 5], [2, 10], [18, 10], [10, 5], [18, 2]]


a = Polygon(matrix, coords, "%")

a.draw()

print(matrix.show())