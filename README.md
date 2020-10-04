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

## `Matrix`

### method `__init__(size = [10, 5], bg = " ") -> None:`
Making the object of class window called `Matrix`

* **Size** is the size of window in symbols first is X, second is Y
* **bg** is the symbol of background

### method `show(self) -> str:`
Update's interface

### method `fill(self, bg = None) -> None:`
Fill all the window with the symbol, 

* **bg** is the symbol to fill by. If `bg` is `None`, it just fill interface with a standart symbol in `Matrix.bg`

### variable `bg`
Background of the window