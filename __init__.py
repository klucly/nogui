# -*- coding: utf-8 -*-

install_packages = True
use_local_console = True



import os
import time
import math

if install_packages:
    try: from keyboard import is_pressed as _is_pressed
    except ImportError: os.system("pip install keyboard") if os.name == "nt" else os.system("sudo pip3 install keyboard")

    try: import pygame
    except ImportError: os.system("pip install pygame") if os.name == "nt" else os.system("sudo pip3 install pygame")



class Matrix:

    def __init__(self, size = [10, 5], bg = " ") -> None:
        '''The main class, uses like a screen, called matrix'''

        if use_local_console:
            import nogui.console as console
            self.console = console.Console(size)


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
        
        if use_local_console: self.console.update(out)
        else: print(out)

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


def press(key: str):
    if use_local_console:
        import pygame

        if len(key) == 1: key = key.lower()
        else: key = key.upper()

        key_ = pygame.constants.__dict__["K_"+key]

        events = pygame.key.get_pressed()

        if events[key_]:
            return True

        return False

    else:
        from keyboard import is_pressed as _is_pressed
        return _is_pressed(key)


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


    def draw(self, to_return = False):
        self.__out = []

        coords = self.coords
        self.lines = []

        xs, ys = [], []

        for coord in coords:
            xs.append(coord[0])
            ys.append(coord[1])

        max_x = max(xs) if xs != [] else 0
        min_x = min(xs) if xs != [] else 0
        max_y = max(ys) if ys != [] else 0
        min_y = min(ys) if ys != [] else 0

        self.max_x, self.max_y, self.min_x, self.min_y = max_x, max_y, min_x, min_y

        self.__width_x__ = max_x-min_x

        centerx = (max_x+min_x)/2
        centery = (max_y+min_y)/2

        center = [centerx, centery]
        self.center = center

        coords = self._rotate(coords, self.angle, center)

        if self.fixed_out:
            coords = self._fix_coords(coords)

        if coords != []:
            coords.append(coords[0])

        self.coords = coords

        coords_lenght = coords.__len__()
        
        for i in range(coords_lenght):
            
            if i+2 <= coords_lenght:

                line = self.get_line(coords[i:i+2])
                self.lines.append(line)

                for pixel in line:
                    if pixel[1] >= 0 and pixel[0] >= 0:

                        try:
                            if not to_return:
                                self.matrix.matrix[pixel[1]][pixel[0]] = self.symbol

                            else:
                                self.__out.append(pixel)
                        except IndexError: pass

            if to_return:
                out = []
                for ii in range(coords.__len__()-2):
                    to_add1 = [self.coords[ii][0], self.coords[ii][1]]
                    to_add2 = [self.coords[ii+1][0], self.coords[ii+1][1]]
                    out.append(self.get_line([to_add1, to_add2]))
                return out


    def get_line(coords) -> list:

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

    def _fix_coords(self, coords):
        y_s = []

        for coord in coords:
            y_s.append(coord[1])

        max_y = max(y_s) if y_s != [] else 0
        min_y = min(y_s) if y_s != [] else 0

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

    def fill(self, symbol: str, mode = "raycasting") -> None:
        '''Function works awful, but can be used
        theres 2 modes now: "raycasting" and "depthcopy"
        they both works bad, but differently bad'''

        if mode == "raycasting":
            out_coords = []

            if hasattr(self, "lines"):
                
                class Searcher:

                    def __init__(self, coords: list) -> None:
                        self.coords = coords
                        self.inside = False
                        self.passed_lines = []


                searchers: list = []


                for i in range(round(self.max_y-self.min_y)):
                    searchers.append(Searcher((round(self.min_x), round(self.min_y+i))))


                for x in range(round(self.max_x-self.min_x)):

                    coords1 = []
                    for coord in self.coords:
                        coords1.append(tuple(coord))


                    for searcher in searchers:

                        for line in self.lines:
                            if searcher.coords in line and searcher.coords not in coords1:

                                if line not in searcher.passed_lines:

                                    searcher.inside = not searcher.inside
                                    searcher.passed_lines.append(line)
                                    

                        searcher.coords = searcher.coords[0]+1, searcher.coords[1]

                        if searcher.inside:
                            self.matrix.matrix[searcher.coords[1]][searcher.coords[0]] = symbol

        if mode == "depthcopy":
            out_coords1 = []

            center = [round((self.min_x+self.max_x)/2), round((self.min_y+self.max_y)/2)]

            for i in range(round((((self.max_x-self.min_x)+(self.max_y-self.min_y))/2)/2)):
                coords = []

                rotated = self._rotate(self.coords, self.angle, self.center)
                for coord in rotated:
                        
                    # for j in range(round((self.max_x-self.min_x)/5)):

                    if coord[0] >= center[0]:
                        coords.append([coord[0]-i])
                    
                    elif coord[0] < center[0]:
                        coords.append([coord[0]+i])
                    
                    if coord[1] >= center[1]:
                        coords[-1].append(coord[1]-i)
                    
                    elif coord[1] < center[1]:
                        coords[-1].append(coord[1]+i)
            
                pol = Polygon(self.matrix, coords, symbol, fixed_out = self.fixed_out)

                pol.draw()
                    
            print(out_coords1)

                # for coords1 in self.get_line(coords):
                #     self.matrix.matrix[coords1[1]][coords1[0]] = "%"



    # def fill(self):

    #     if hasattr(self, "lines"):
            
    #         class Searcher:

    #             def __init__(self, coords: list) -> None:
    #                 self.coords = coords
    #                 self.inside = False
    #                 self.passed_lines = []

    #         def _area() -> int:
                
    #             S: int

    #             result1 = 0
    #             result2 = 0


    #             for coord_index in range(self.coords.__len__()-1):
    #                 result1 += self.coords[coord_index][0]*self.coords[coord_index+1][1]
                    
    #             for coord_index in range(self.coords.__len__()-1):
    #                 result2 += self.coords[coord_index][1]*self.coords[coord_index+1][0]

                    
    #             return -round((result1-result2)/2)

            

            
    #         searcher = Searcher((round(self.min_x), round((self.max_y+self.min_y)/2)))
    #         for step in range(round(self.max_x-self.min_x)):

    #             for line in self.lines:

    #                 if searcher.coords in line and line not in searcher.passed_lines:

    #                     searcher.passed_lines.append(line)
    #                     searcher.inside = not searcher.inside

    #                     break


    #         coords = searcher.coords[0]+1, searcher.coords[1]


    #         area = _area()
    #         lines = []


    #         for line in self.lines:
    #             for coord in line:
    #                 lines.append(coord)

    #         i = 0

    #         # for move in range(area):
    #         def go(self, coords, lines, i) -> None:
    #             coordsUp = coords[0], coords[1]+1
    #             coordsLeft = coords[0]+1, coords[1]
    #             coordsDown = coords[0], coords[1]-1
    #             coordsRight = coords[0]-1, coords[1]
    #             i += 1

    #             if i < 5:

    #                 try:
                        
    #                     if (coordsUp not in lines 
    #                         and coordsUp[1] > -1
    #                         and coordsUp[1] < self.matrix.size[1]
    #                         and coordsUp[0] > -1
    #                         and coordsUp[0] < self.matrix.size[0]):
                            
    #                         self.matrix.matrix[coordsUp[1]][coordsUp[0]] = "9"
    #                         coords = coordsUp
    #                         go(self, coords, lines, i)
                        
    #                     if (coordsLeft not in lines 
    #                         and coordsLeft[1] > -1
    #                         and coordsLeft[1] < self.matrix.size[1]
    #                         and coordsLeft[0] > -1
    #                         and coordsLeft[0] < self.matrix.size[0]):

    #                         self.matrix.matrix[coordsLeft[1]][coordsLeft[0]] = "9"
    #                         coords = coordsLeft
    #                         go(self, coords, lines, i)
                        
    #                     if (coordsDown not in lines 
    #                         and coordsDown[1] > -1
    #                         and coordsDown[1] < self.matrix.size[1]
    #                         and coordsDown[0] > -1
    #                         and coordsDown[0] < self.matrix.size[0]):

    #                         self.matrix.matrix[coordsDown[1]][coordsDown[0]] = "9"
    #                         coords = coordsDown
    #                         go(self, coords, lines, i)
                            
    #                     if (coordsRight not in lines 
    #                         and coordsRight[1] > -1
    #                         and coordsRight[1] < self.matrix.size[1]
    #                         and coordsRight[0] > -1
    #                         and coordsRight[0] < self.matrix.size[0]):

    #                         self.matrix.matrix[coordsRight[1]][coordsRight[0]] = "9"
    #                         coords = coordsRight
    #                         go(self, coords, lines, i)

    #                 except: print("err")


    #         go(self, coords, lines, i)
            

class RectangleFULL:

    def __init__(self, matrix: Matrix, xy: list, wh: list, symbol: str, angle: int, fixed_out = False) -> None:

        self.matrix = matrix
        self.xy = xy
        self.wh = wh
        self.angle = angle
        self.symbol = symbol
        self.fixed_out = fixed_out
        self._coords = []
        x, y, w, h = xy[0], xy[1], wh[0], wh[1]
        self.figure = Polygon(self.matrix, [[x, y], [x+w, y], [x+w, y+h], [x, y+h]], self.symbol, angle, self.fixed_out)


    def draw(self) -> None:

        xy = self.xy
        wh = self.wh

        x, y, w, h = xy[0], xy[1], wh[0], wh[1]
        
        coords = [[x, y], [x+w, y], [x+w, y+h], [x, y+h]]

        self.figure.angle = self.angle
        self.figure.fixed_out = self.fixed_out
        self.figure.symbol = self.symbol
        self.figure.coords = coords
        self._coords = self.figure.coords

        self.figure.draw()

class Circle:

    def __init__(self, matrix: Matrix, coords: list, radius: int, symbol: str, resolution = 50, fixed_out = False) -> None:

        self.matrix = matrix
        self.coords = coords
        self.radius = radius
        self.symbol = symbol
        self.resolusion = resolution
        self.fixed_out = fixed_out

    def draw(self):

        # x^2+y^2=r^2
        r = self.radius
        res = self.resolusion
        for boool in range(2):
            for step in range(-r*res, r*res, 1):

                x = step/res

                try:
                    y = math.sqrt(r**2-x**2)*(-1)**boool/(self.fixed_out+1)
                    
                    self.matrix.matrix[round(y+self.coords[1])][round(x+self.coords[0])] = self.symbol

                except: pass


        # x = cos(t); y = sin(t)

        # for i in range()
