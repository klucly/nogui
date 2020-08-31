from nogui import *
import time

s = '''/-==
|+0
\-=='''

matrix = Matrix([100, 10], ".")
# rect = RectangleXYWH(matrix, [1, 8, 3, 3], "2")
rect = Sprite(matrix, [10, 4], s)
rect2 = RectangleXYWH(matrix, [3, 2, 3, 3], "#")
i = 0
fps1 = 0

while 1:
    # time1 = time.perf_counter()
    x=1

    if press("d"):
        rect.xywh[0] += .4/x
        if collision(rect, rect2): rect.xywh[0] -= .4/x

    elif press("a"):
        rect.xywh[0] -= .4/x
        if collision(rect, rect2): rect.xywh[0] += .4/x

    if press("s"):
        rect.xywh[1] += .2/x
        if collision(rect, rect2): rect.xywh[1] -= .2/x

    elif press("w"):
        rect.xywh[1] -= .2/x
        if collision(rect, rect2): rect.xywh[1] += .2/x

    # time2 = time.perf_counter()
        
    matrix.fill()

    # time21 = time.perf_counter()

    rect.draw()
    
    # time22 = time.perf_counter()

    rect2.draw()

    # time3 = time.perf_counter()

    print(matrix.show())
    # time4 = time.perf_counter()
    # print(time2-time1, time3-time2, time4-time3)
    # print(time3-time22, time22-time21, time21-time2)
    # print(time4-fps1)

    
    wait(1/60)
    clear_console()
    i += 1

    # fps1 = time.perf_counter()