# INFO

Thats the game engine where you can make programs
without gui `(Like in console)` very easy


# Installation

Well, you have to download this. There is no other ways, haha


# Configuring

In the `/nogui/__init__.py` in the up of file you will see this lines:

```python

install_packages = True
use_local_console = True

```

`install_packeges` is to install packages, what the engine needs
`use_local_console` is to use special console for this engine
* If `True` you need [`pygame`,](https://github.com/pygame/pygame) speed of programs will be increased by the few times
* If `False` you need [`keyboard`](https://github.com/boppreh/keyboard) and if you have linux you have to run files with a root `(not recommended to use)`

# Using

## "Window"

For the start we need to import an engine:
```python
import nogui
```

Then we need an object of class Matrix, it will be our window by the symbols:
```python
from nogui import Matrix

matrix = Matrix()
```

If we will start this, nothing will happen, because will do not show our window, to show it you can write some code:

```python
from nogui import Matrix

matrix = Matrix()
matrix.show()
```