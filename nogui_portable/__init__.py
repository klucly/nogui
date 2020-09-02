# -*- coding: utf-8 -*-

keyboard_lib = True

import os
import time
import math

if keyboard_lib:
    from keyboard import is_pressed as _is_pressed

class Matrix:

    def __init__(self, size = [10, 5], bg = " ") -> None:
        '''The main class, uses like a screen, called matrix'''

        self.matrix = []
        self.bg = bg
        self.size = size

        for i in range(size[1]):
            element = []

            for ii in range(size[0]):
                element.append(bg)
            self.matrix.append(element)

    def show(self) -> str:
        '''Returns the "image"'''
        buffer_matrix = self.matrix
        out = ""

        for line in buffer_matrix:

            out += "".join(line)+"\n"

        return out

    def fill(self, bg = None) -> None:
        '''Fill a matrix in with bg'''
        
        if bg == None:
            bg = self.bg

        #This makes 2d array
        self.matrix = [[self.bg for i in range(self.size[0])] for j in range(self.size[1])] 


clear_console = lambda: os.system("cls" if os.name == "nt" else "clear")


def wait(time_seconds = 1): time.sleep(time_seconds)


class __Object2D__:
    
    def __get_global_coords__(self):


        if self.__class__ == RectangleXY2:
            x_min = min(self.coords[0], self.coords[2])
            x_max = max(self.coords[0], self.coords[2])

            y_min = min(self.coords[1], self.coords[3])
            y_max = max(self.coords[1], self.coords[3])

            self.__figure_init__ = True

        elif self.__class__ == RectangleXYWH or self.__class__ == Sprite:

            x1 = self.xywh[0]
            x2 = self.xywh[0]+self.xywh[2]

            y1 = self.xywh[1]
            y2 = self.xywh[1]+self.xywh[3]

            x_min = min(x1, x2)
            x_max = max(x1, x2)

            y_min = min(y1, y2)
            y_max = max(y1, y2)
            
            self.__figure_init__ = True

        if hasattr(self , "__figure_init__"):
            return x_min, x_max, y_min, y_max
        else: return None


class __Rectangle__(__Object2D__):

    def __init__(self) -> None:

        self.coords = [0, 0]
        self.matrix = Matrix()
        self.symbol = " "

    def draw(self) -> None:

        buffer_matrix = self.matrix.matrix

        x_min, x_max, y_min, y_max = self.__get_global_coords__()

        lines = range(round(y_min), round(y_max))
        pixels = range(round(x_min), round(x_max))

        for line_index in lines:

            for pixel_index in pixels:

                try:
                    buffer_matrix[line_index][pixel_index] = self.symbol
                except: ...


class RectangleXY2(__Rectangle__):

    def __init__(self, matrix: Matrix, coords: list, symbol: str) -> None:
        '''Rectangle, that uses 2 global points on the matrix to be drawed'''
        
        self.coords = coords
        self.symbol = symbol
        self.matrix = matrix


class RectangleXYWH(__Rectangle__):

    def __init__(self, matrix: Matrix, xywh: list, symbol: str) -> None:
        '''Rectangle, that uses x, y, width, height to be drawed'''

        self.matrix = matrix
        self.xywh = xywh
        self.symbol = symbol


def press(key):
    if keyboard_lib: return _is_pressed(key) 
    else: return False


def collision(obj1, obj2):

    coords1 = obj1.__get_global_coords__()
    coords2 = obj2.__get_global_coords__()

    if coords1[0] <= coords2[1] and coords1[1] >= coords2[0]:

        if coords1[2] <= coords2[3] and coords1[3] >= coords2[2]:

            return True

    return False


class Sprite(__Object2D__):

    def __init__(self, matrix: Matrix, xy, sprite) -> None:

        sprite_lines_split = sprite.split("\n")
        buffer = []

        for line in sprite_lines_split:
            buffer.append(line.__len__())

        width = max(buffer)

        height = sprite_lines_split.__len__()

        self.xywh = [xy[0], xy[1], width, height]
        self.matrix = matrix
        self.line_split = sprite_lines_split
        self.coords = self.xywh[0], self.xywh[1], self.xywh[0]+self.xywh[2], self.xywh[1]+self.xywh[3]

    def draw(self) -> None:

        buffer_matrix = self.matrix.matrix
        x_min, x_max, y_min, y_max = self.__get_global_coords__()

        
        lines = range(round(y_min), round(y_max))
        pixels = range(round(x_min), round(x_max))

        lines_sprite = range(round(y_max-y_min))
        pixel_sprite = range(round(x_max-x_min))

        for line_index in lines:

            for pixel_index in pixels:

                try:
                    a = self.line_split[lines.index(line_index)][pixels.index(pixel_index)]
                    buffer_matrix[line_index][pixel_index] = a
                except: ...

class Polygon:

    def __init__(self, matrix: Matrix, coords: list, symbol: str, angle = 0, fixed_out = False) -> None:

        self.coords = coords
        self.matrix = matrix
        self.symbol = symbol
        self.fixed_out = fixed_out
        self.angle = angle


    def draw(self):

        coords = self.coords

        xs, ys = [], []

        for coord in coords:
            xs.append(coord[0])
            ys.append(coord[1])

        max_x = max(xs)
        min_x = min(xs)
        max_y = max(ys)
        min_y = min(ys)

        centerx = (max_x+min_x)/2
        centery = (max_y+min_y)/2

        center = [centerx, centery]

        coords = self._rotate(coords, self.angle, center)

        if self.fixed_out:
            coords = self._fix_coords(coords)

        coords.append(coords[0])

        coords_lenght = coords.__len__()
        
        for i in range(coords_lenght):
            
            if i+2 <= coords_lenght:
                for pixel in self.get_line(coords[i:i+2]):
                    if pixel[1] >= 0 and pixel[0] >= 0:
                        try:
                            self.matrix.matrix[pixel[1]][pixel[0]] = self.symbol
                        except IndexError: pass


    def _fix_coords(self, coords):
        y_s = []

        for coord in coords:
            y_s.append(coord[1])

        max_y = max(y_s)
        min_y = min(y_s)

        middle_y = (max_y + min_y) /2

        for coord in coords:
            coord[1] = (coord[1]+middle_y)/2

        return coords
        

    def _rotate(self, points, angle, center):
        angle = math.radians(angle)
        cos_val = math.cos(angle)
        sin_val = math.sin(angle)
        cx, cy = center
        new_points = []
        for x_old, y_old in points:
            x_old -= cx
            y_old -= cy
            x_new = x_old * cos_val - y_old * sin_val
            y_new = x_old * sin_val + y_old * cos_val
            new_points.append([x_new + cx, y_new + cy])
        return new_points


    def get_line(self, coords) -> list:

        coords0 = coords[0]
        coords1 = coords[1]

        distanceX = coords1[0]-coords0[0]
        distanceY = coords1[1]-coords0[1]

        distance = math.sqrt(distanceX**2 + distanceY**2)
        distance = round(distance)
        points = {}
        out = []

        for step in range(distance):
            
            x = round( distanceX / distance * step +coords0[0] )
            y = round( distanceY / distance * step +coords0[1] )

            points[x, y] = None

        for point in points:
            out.append(point)
        

        return out


    def get_line(self, coords) -> list:

        coords0 = coords[0]
        coords1 = coords[1]

        distanceX = coords1[0]-coords0[0]
        distanceY = coords1[1]-coords0[1]

        distance = math.sqrt(distanceX**2 + distanceY**2)
        distance = round(distance)
        points = {}
        out = []

        for step in range(distance):
            
            x = round( distanceX / distance * step +coords0[0] )
            y = round( distanceY / distance * step +coords0[1] )

            points[x, y] = None

        for point in points:
            out.append(point)
        

        return out


class RectangleFULL:

    def __init__(self, matrix: Matrix, xy: list, wh: list, symbol: str, angle: int, fixed_out = False) -> None:

        self.matrix = matrix
        self.xy = xy
        self.wh = wh
        self.angle = angle
        self.symbol = symbol
        self.fixed_out = fixed_out
        self._coords = []


    def draw(self) -> None:
        if hasattr(self, "_body"):
            xy = self._body.position
            angle = math.degrees(self._body.angle)
            self.angle = angle

        else:
            angle = self.angle
            xy = self.xy

        wh = self.wh

        x, y, w, h = xy[0], xy[1], wh[0], wh[1]

        if self._coords != []:
            y_s = []

            for coord in self._coords:
                y_s.append(coord[1])

            y_min = min(y_s)
            y_max = max(y_s)

            y -= y_max - y_min

        coords = [[x, y], [x, y+h], [x+w, y+h], [x+w, y]]

        # center = x+w/2, y+h/2

        # coords = self._rotate(coords, angle, center)
        Polygon(self.matrix, coords, self.symbol, angle, self.fixed_out)

        self.figure.angle = self.angle
        self.figure.fixed_out = self.fixed_out
        self.figure.symbol = self.symbol
        self.figure.coords = coords
        self._coords = self.figure.coords

        self.figure.draw()