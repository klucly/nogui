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

        self.repeat()

    def repeat(self) -> None:

        self.matrix.fill()

        self.player.object.draw()

        print(self.matrix.show())


if __name__ == "__main__":
    Main()