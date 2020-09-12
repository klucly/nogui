from nogui import *

space = Space()

matrix = Matrix([80, 20], ".")
obj_list = [RectangleFULL(matrix, [30, 5], [5, 5], "J", 20), RectangleFULL(matrix, [10, 20], [40, 5], "W", 0)]
obj_list[0].physics_init(space)
for obj in obj_list[1:]:
    obj.physics_init(space, obj_type = STATIC)

while 1:

    space.update(1/30)

    matrix.fill()

    for obj in obj_list:
        obj.draw()

    clear_console()
    print(matrix.show())

    wait(1/30)
