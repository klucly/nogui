from nogui import *

class Object2D:

    class Player:

        def __init__(self, matrix: Matrix) -> None:

            self.sprite = "^"
            self.object = Sprite(matrix, [1, 1], self.sprite)

    

class Main:
    def __init__(self) -> None:

        matrix = Matrix([80, 20], "-")

        player = Object2D.Player(matrix)
    
        self.matrix = matrix
        self.player = player

    def repeat(self) -> None:

        self.matrix.fill()

        self.player.object.draw()