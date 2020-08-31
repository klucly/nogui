from keyboard2 import play
from nogui import *

master = Matrix([100, 10])


# player_sprite = "|=-"


s = '''/-==
|+0
\-=='''

player = Sprite(master, [0, 0], s)
player.draw()
# print(player.xywh)


print(master.show())
