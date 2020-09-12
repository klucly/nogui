from nogui import *

matrix = Matrix([40, 20], ".")
space = Space()

cube = RectangleFULL(matrix, [10, -6], [10, 10], "M", 40)
cube.physics_init(space)

floor = RectangleFULL(matrix, [5, 6], [10, 4], "=", 10)
floor.physics_init(space, obj_type = STATIC)

floor1 = RectangleFULL(matrix, [30, 16], [10, 4], "=", -10)
floor1.physics_init(space, obj_type = STATIC)

while 1:
    space.update(1/30)

    matrix.fill()
    floor.draw()
    floor1.draw()
    cube.draw()

    # floor._body.angle += math.radians(10)

    clear_console()
    print(matrix.show())

    if cube._body.position[1] > 30:
        cube = RectangleFULL(matrix, [10, -2], [10, 10], "M", 40)
        cube.physics_init(space)

    wait(1/30)