# INFO

Thats the game engine where you can make programs
without gui `(Like in console)` very easy


## Installation

Well, you have to download this. There is no other ways, haha


## Configuring

In the `/nogui/__init__.py` in the top of file you will see those lines:

```python

install_packages = True
use_local_console = True

```

`install_packages` is to install packages, what the engine needs

`use_local_console` is to use special console for this engine
* If `True` you need [`pygame`](https://github.com/pygame/pygame), speed of programs will be increased by the few times
* If `False` you need [`keyboard`](https://github.com/boppreh/keyboard) and if you have linux you have to run files with a root `(not recommended to use)`

# Using

## "Window"

For the start we need to import an engine:
```python
import nogui
```

Then we need an object of class `Matrix`, it will be our window by the symbols and we will call it `matrix`:
```python
from nogui import Matrix

matrix = Matrix()
```

If we will start this, nothing will happen, because we will do not show 
our window, just create it, to show it you can write some code:

```python
from nogui import Matrix

matrix = Matrix()
matrix.show()
```

If you have ever used [`pygame`](https://github.com/pygame/pygame), it will be easy for you

So, our console opened and closed almost at the same time if you [use local console](#Configuring). 
We just need to put `.show()` to the loop and we will get that:

```python
from nogui import Matrix

matrix = Matrix()

while 1:
    matrix.show()
```

# API


## class `Matrix`
The main class. Its a window for engine

### method `__init__(size = [10, 5], bg = " ") -> None:`
Returning the object of class window called `Matrix`

* **Size** is the size of window in symbols first is X, second is Y
* **bg** is the symbol of background

### method `show(self) -> str:`
Update's interface

### method `fill(self, bg = None) -> None:`
Fill all the window with the symbol, 

* **bg** is the symbol to fill by. If `bg` is `None`, it just fill interface with a standart symbol in `Matrix.bg`

### variable `bg`
Its a 2D list of all the interface

### variable `size`
Its the size of window. `(Not recommended to touch)`

### variable `console`
Its a console. It exist only if you [use local console](#Configuring). `(Not recommended to touch)`


## function `clear_console`
Clear you console


## class `RectangleXY2`
Rectangle, uses `x` and `y` coords of 2 points to draw itself

### method `__init__(self, matrix: Matrix, coords: list, symbol: str) -> None:`
Returning the object of class rectangle

* **matrix** is the matrix of your program
* **coords** is the coordinates of two points between which will be drawed a rectangle
* **symbol** is the symbol, from which the square will be drawn

### method `draw(self) -> None:`
Drawing the rectangle on a matrix

### variable `matrix`
Its the matrix of your program

### variable `coords`
Its the coordinates of two points between which will be drawed a rectangle

### variable `symbol`
Its the symbol, from which the square will be drawn



## class `RectangleXYWH`
Rectangle, uses coordinates and size to be drawn

### method `__init__(self, matrix: Matrix, xywh: list, symbol: str) -> None:`
Returning the object of class rectangle

* **matrix** is the matrix of your program
* **xywh** is the coordinates of rectangle and the size of it
* **symbol** is the symbol, from which the square will be drawn

### method `draw(self) -> None:`
Drawing the rectangle on a matrix

### variable `matrix`
Its the matrix of your program

### variable `xywh`
Its the coordinates of rectangle and the size of it

### variable `symbol`
Its the symbol, from which the square will be drawn


## function `press(key: str):`
Reading the press of a key

* **key** is a key that a function will read


## function `collision(obj1, obj2):`
Returning True if `obj1` colliding with `obj2`

### Attension! This function read colliding between only objects of classes [`RectangleXYWH`](#class-rectanglexywh) and [`RectangleXY2`](#class-rectanglexy2)


## class `Sprite`

### method `__init__(self, matrix: Matrix, xy, sprite) -> None:`

* **matrix** is the matrix of your program
* **xy** is coordinates of sprite
* **sprite** is sprite `(string format)`

### method `draw(self) -> None:`
Drawing the sprite on a matrix

### variable `matrix`
Its the matrix of your program

### variable `xywh`
Its the coordinates of sprite and size of it

### variable `line_split`
Its the list of lines of sprite

### variable `coords`
Its the coordinates of sprite `(Not recommended to touch)`


## class `Polygon`
Polygon.

### method `__init__(self, matrix: Matrix, coords: list, symbol: str, angle = 0, fixed_out = False) -> None:`

* **matrix** is the matrix of your program
* **coords** is coordinates of the points to draw polygon
* **symbol** is the symbol, from which the polygon will be drawn
* **angle** is angle of a polygon `(Yes, you can rotate it)`
* **fixed_out** making your polygon looks as it must

### method `draw(self, to_return = False):`
Draws a polygon on a window

* **to_return**, if `True`, it will return the coordinates, not show itself

### method `get_line(coords) -> list:`
Returning coordinates of all the points of a line between 2 points from `coords`

* **coords** is coordinates of 2 points of a line

### method `fill(self, symbol: str, mode = "raycasting") -> None:`
Fill a polygon (Work in progress but can be used)

* **mode** is mode of filling
  Here's 2 modes now:
  * "raycasting"
  - "depthcopy"
  They both works awful, but differently awful