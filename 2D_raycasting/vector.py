from nogui import *

class Vector:

    def __init__(self, matrix: Matrix, coords: Vec2, direction: Union[int, float] = 0, lenght: Union[int, float] = 10, symbol: str = "#", fixed_out: bool = False) -> None:
        self.coords = coords
        self.matrix = matrix
        self.direction = direction
        self.lenght = lenght
        self.symbol = symbol
        self.fixed_out = fixed_out
        

    def update(self, show: bool = True) -> tuple:

        point1 = self.coords

        xlenght = math.cos(math.radians(self.direction))*self.lenght
        ylenght = math.sin(math.radians(self.direction))*self.lenght/(1.9 if self.fixed_out else 1)
        lenghtxy = Vec2(xlenght, ylenght)

        point2 = lenghtxy+self.coords

        if show:
            for coords in Polygon.get_line(None, [point1, point2]):
                if min(coords>=0):
                    try: self.matrix.matrix[coords[1]][coords[0]] = self.symbol
                    except IndexError: pass

        return point1, point2

        
# matrix = Matrix(Vec2(40, 20), " ", 60, True)

# vec = Vector(matrix, Vec2(20, 10), 0, 10, "0")

# while 1:
#     if matrix.mouse_up(): vec.coords = matrix.mouse_coords()
#     if press("a"): vec.lenght -= .1
#     elif press("d"): vec.lenght -=- .1
#     vec.direction += 1
#     vec.symbol = f"{vec.direction//360}"[-1]
#     # matrix.fill()
#     vec.update()
#     matrix.show()