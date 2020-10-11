from typing import Any
from vector import Vector
from nogui import *

class Ray2D:

    def __init__(self, matrix: Matrix, coords: Vec2, direction: int, obj: Any, sections: int, min_closeness: Union[int, float] = 1) -> None:

        self.direction = direction
        self.obj = obj
        self.matrix = matrix
        self.sections = sections
        self.coords = coords
        self.min_closeness = min_closeness
        self.o = True

    def update(self, show_circles: bool = False, show: bool = True) -> bool:
        if self.obj.__class__ == Circle:
            vec = Vector(self.matrix, self.coords, self.direction, 1, "0")
            if show_circles: c = Circle(self.matrix, self.coords, 1, "O", 0)
            coords = self.coords

            for i in range(self.sections):
                distancex = self.obj.coords[0] - coords[0]
                distancey = self.obj.coords[1] - coords[1]
                center_distance = math.sqrt(distancex**2+distancey**2)
                distance = center_distance-self.obj.radius

                if distance < self.min_closeness:
                    return True, coords
                if max(Vec2(coords) > Vec2(self.matrix.size)) or max(Vec2(coords) < Vec2(0)):
                    return False, coords

                vec.lenght = distance
                if show_circles:
                    c.radius = distance
                    c.draw()

                vec.symbol = str(i)
                coords1 = vec.update(show)
                vec.coords = coords1[1]
                if show_circles: c.coords = round(coords1[1])
                coords = coords1[1]

        return False, None



class Camera2D:

    def _degrees_from_coords(self, coords: list) -> float:
        coords1 = Vec2(coords[0])
        coords2 = Vec2(coords[1])

        distanceX, distanceY = coords2-coords1
        distance = sqrt(distanceX**2+distanceY**2)
        angle = math.degrees(math.asin(distanceX/distance)) * (-1 if distanceY >= 0 else 1) + (0 if distanceY >= 0 else 180) + 180
        return angle

    def __init__(self, matrix: Matrix, coords: Vec2, rotation: int, size: Vec2,
                 symbol: str, fixed_out = False, obj: Any = None, sections: int = 4,
                 min_closeness: Union[int, float] = 2, resolution: int = 5, viewing_angle: Union[int, float] = 45,
                 show_rays: bool = True) -> None:

        self.coords = coords
        self.min_closeness = min_closeness
        self.rotation = rotation
        self.show_rays = show_rays
        self.matrix = matrix
        self.fixed_out = fixed_out
        self.symbol = symbol
        self.sections = sections
        self.size = size
        self.obj = obj
        self.viewing_angle = viewing_angle
        self.resolution = resolution
        self.figure = Polygon(matrix, [coords], self.symbol, fixed_out = fixed_out)
        self.ray = Ray2D(self.matrix, self.coords, self.rotation, self.obj, sections, min_closeness)
        self.symbol_list = ".,-/=!UO0#@"


    def update(self) -> list:
        self.ray.min_closeness = self.min_closeness
        self.ray.sections = self.sections
        rotation = -self.rotation+180
        r = self.size
        offset = (math.pi*r*2)*2/3
        points_coords = [self.coords]

        for sign in range(2):

            Sin = math.sin ( math.radians(rotation + offset * (-1)**sign) ) * r
            Cos = math.cos ( math.radians(rotation + offset * (-1)**sign) ) * r / (self.fixed_out+1)

            x = round(Sin+self.coords[0])
            y = round(Cos+self.coords[1])

            try: self.matrix.matrix[y][x] = self.symbol
            except: pass
            points_coords.append((x, y))

        self.figure.coords = points_coords
        self.figure.draw()
        self.ray.direction = self.rotation-90
        res = self.resolution
        self.ray.direction -= self.viewing_angle//2
        out = []

        for i in range(res):
            self.ray.direction += self.viewing_angle/res
            ray_output = self.ray.update(0, self.show_rays)

            if ray_output[0]:
                angle = self._degrees_from_coords([self.obj.coords, ray_output[1]])
                symbol = self.symbol_list[(round(math.cos(math.radians(angle))*5)+5)]

            else: symbol = " "

            out.append(symbol)
        try: self.matrix.matrix[round(self.coords[1])][round(self.coords[0])] = "O"
        except: pass
        return out


if __name__ == "__main__":
    
    win = Matrix(Vec2(80, 40), ".", show_fps = 1)

    circle = Circle(win, Vec2(50, 30), 5, "0", 0)
    camera1 = Camera2D(win, Vec2(10, 10), 90, 5, "H", 0, circle, 10, .5, win.size[1], 60, 0)
    step = .03
    speed = 0
    tick = 0
    s_r = 0
    delay = 0
    show_rays = False
    while 1:
        tick += 1
        camera1.rotation = Camera2D._degrees_from_coords(None, [camera1.coords, win.mouse_coords()])
        
        if press("f") and delay == 0:
            delay = 1
            show_rays = not show_rays

        if press("d"):
            s_r = 1
            speed += step
            camera1.coords[0] -=- speed * (3 if show_rays else 1)
        elif press("a"):
            s_r = 1
            speed += step
            camera1.coords[0] -= speed * (3 if show_rays else 1)
        else: s_r = 0

        if press("w"):
            speed += step
            camera1.coords[1] -= speed/2 * (3 if show_rays else 1)
        elif press("s"):
            speed += step
            camera1.coords[1] -=- speed/2 * (3 if show_rays else 1)
        
        elif not s_r and speed != 0: speed = 0
        if speed >= .5: speed = .5

        if delay > 0: delay -= .1
        if delay < 0: delay = 0

        camera1.show_rays = show_rays
            
        win.fill()
        points = camera1.update()
        circle.fill()

        for i in range(len(points)):
            for j in range(10):
                win.matrix[i-1][win.size[0]-1-j] = points[i]

        win.show()
