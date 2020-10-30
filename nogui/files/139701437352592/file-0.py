from math import acos, acosh, asin, cos, degrees, dist, radians, sin, sqrt
from typing import Union
import nogui
from nogui import Vec2, Matrix, collision, press
import math


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
            for coords in nogui.Polygon.get_line(None, [point1, point2]):
                if min(coords>=0):
                    try: self.matrix.matrix[coords[1]][coords[0]] = self.symbol
                    except IndexError: pass

        return point1, point2

class Camera:

    def __repr__(self) -> str: return "rayc.Camera"

    def __init__(self, main, i_count = 5, coords: Vec2 = Vec2(0), resolution: int = 10, viewing_angle: int = 60, rotation: int = 0, **args) -> None:

        self._main = main
        self.matrix = main.matrix
        self.coords = coords
        self.i_count = i_count
        self.show_rays = False
        self._objectlist = main.objectlist
        self.resolution = resolution
        self.rotation = rotation
        self.viewing_angle = viewing_angle
        self.attr = {}
        self._vectors = []
        self._vectors.append(Vector(main.matrix, self.coords, rotation-viewing_angle/2, 5, "H"))
        self._vectors.append(Vector(main.matrix, self.coords, rotation+viewing_angle/2, 5, "H"))

        if "symbol" in args: self.symbol = args["symbol"]
        else: self.symbol = "#"
        if "size" in args: self.size = args["size"]
        else: self.size = 5
        if "output_coords" in args: self.output_size = args["output_coords"]
        else: self.output_coords = Vec2(0)
        if "output_weight" in args: self.output_size = args["output_weight"]
        else: self.output_weight = 2


    def draw(self) -> None:
        output = []
        distances = {}
        _distances = {}
        coords_list = []
        ray_num = 0

        for vector in self._vectors:
            vector.direction = self.rotation+(self.viewing_angle/2*(-1)**self._vectors.index(vector))
            vector.lenght = self.size
            vector.symbol = self.symbol
            vector.coords = self.coords
            vector.update()

        for ray_direction in range(self.rotation-self.viewing_angle//2, self.rotation+self.viewing_angle//2, round(self.viewing_angle/self.resolution)):
            coords = self.coords
            stop = False
            
            for i in range(self.i_count):

                for obj in self._objectlist:
                    if obj.__class__ == nogui.Circle:
                        distancex, distancey = coords-obj.coords
                        distance = sqrt(distancex**2+distancey**2)-obj.radius
                        distances[distance] = obj
                # print(distances, 1)

                if distances != {} and not stop:
                    lenght = min(distances)
                    coords = Vector(self.matrix, coords, ray_direction, lenght, f"{i}").update(self.show_rays)[1]
                    
                    if (coords[0] > self.matrix.size[0] or coords[1] > self.matrix.size[1]
                        or coords[0] < 0 or coords[1] < 0):
                        stop = True
                        output.append(False)

                    elif lenght < 1:
                        stop = True
                        output.append(True)

                    _distances[ray_num] = distances[lenght]
                    distances = {}

            if not stop: output.append(False)
            coords_list.append(coords)
            ray_num += 1


        for i in range(len(output)):
            for w in range(self.output_weight):
                try:
                    obj = _distances[i]
                    # if nogui.press("k"):
                    if output[i]: self.matrix.matrix[i+self.output_coords[1]][self.output_coords[w+self.output_coords[0]]] = shader(self._main, obj, coords_list[i])
                    else: self.matrix.matrix[i+self.output_coords[1]][self.output_coords[w+self.output_coords[0]]] = " "
                except: ...

    def rotate_to_mouse(self, main):
        mouse_coords = Vec2(self.matrix.mouse_coords())

        distanceX, distanceY = self.coords-mouse_coords
        distance = sqrt(distanceX**2+distanceY**2)
        angle = math.degrees(math.asin(distanceX/distance)) * (-1 if distanceY >= 0 else 1) + (0 if distanceY >= 0 else 180) - 90
        main.command(f"c 0.rotation {round(angle)}")


            
class Nothing:
    def __repr__(self) -> str: return "nothing"


def shader(main, obj, coords) -> str:
    distanceX, distanceY = main.objectlist[0].coords-obj.coords
    distance = sqrt(distanceX**2+distanceY**2)
    
    return str(round(distance/3))[-1]



def start(main):
    main.objectlist = []
    main.objectlist = [Camera(main, 5, Vec2(4, 4), 20, 60, 1, size = 5), Nothing()]
    main.command("add circle 25 10 3 K")
    main.command("add circle 30 1 2 K")
    main.objectlist[0]._objectlist = main.objectlist

def loop(main):
    coords = main.objectlist[0].coords
    try:
        if nogui.press("d"):
            main.command("c 0.coords "+str(Vec2(coords[0]+1, coords[1])).replace(" ", ""))
        elif nogui.press("a"):
            main.command("c 0.coords "+str(Vec2(coords[0]-1, coords[1])).replace(" ", ""))
    except: ...
    try:
        if nogui.press("w"):
            main.command("c 0.coords "+str(Vec2(coords[0], coords[1]-1)).replace(" ", ""))
        elif nogui.press("s"):
            main.command("c 0.coords "+str(Vec2(coords[0], coords[1]+1)).replace(" ", ""))
    except: ...

    try: main.objectlist[0].rotate_to_mouse(main)
    except: pass