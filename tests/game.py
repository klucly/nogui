from libs import *


class Main:

    def __init__(self) -> None:

        self.matrix = Matrix([40, 40], ".")
        self.sq = RectangleXYWH(self.matrix, [3, 35, 4, 2], "I")
        self.tick = 100
        self._tick = 0.001
        self.first_ticks = []
        self.score = 0
        self.combo_score = 1
        self.speed_label = Sprite(self.matrix, [0, 8], "Speed:       ")
        self.hp_label = Sprite(self.matrix, [0, 7], "Health:           ")
        self.score_multiplier = Sprite(self.matrix, [0, 6], "Score: x      ")
        self.combo = Sprite(self.matrix, [0, 5], "Combo: x          ")
        self.start_button = Sprite(self.matrix, [6, 10], start_sign)
        self.options_button = Sprite(self.matrix, [6, 16], options_sign)
        self.selection = Selection(self.matrix)

        self.x = 0
        self.y = 32
        self.is_pressed = False
        self.objlist = [Score(self.matrix, self.score),
                        RectangleXYWH(self.matrix, [0, 30, 40, 10], ".")]

        self.speed = 5
        self.sensivity = 1
        self.difficulty = 10
        self.hp = 5

        self.spawn_speed = 500/20

        while 1:
            self.menu_update()
            self.main_update()

    def menu_update(self) -> None:
        self.matrix.bg = "."
        self._menu_update()

        while 1: 
            if press("s") and not(self.selection.selection):
                self.selection.go_down()

            elif press("w") and self.selection.selection:
                self.selection.go_up()

            if press("space"):
                if not(self.selection.selection): break

            self._menu_update()
            

    def _menu_update(self):

            self.matrix.fill(".")

            self.start_button.draw()
            self.options_button.draw()
            self.selection.update()

            clear_console()
            self.matrix.show()



    def main_update(self) -> None:
        self.matrix.bg = " "

        while 1:
            self.score += self._tick*self.speed*10*self.difficulty
            self.combo.sprite = "Combo: x"+str(self.combo_score)
            self.hp_label.sprite = "Health: "+str(self.hp)
            self.speed_label.sprite = "Speed: "+str((((self._tick*10+(self.tick/100000)**2)*self.speed+(self.difficulty-1)/10)/10+.02)/self._tick)
            self.score_multiplier.sprite = "Score: x"+str(round(sqrt(self.combo_score)))

            if self.tick <= 1000: a = time.perf_counter()

            if self.tick % int((self.spawn_speed-(self.tick/100000)**2)*self.speed-(self.difficulty-1)) == 0:
                self.objlist.append(Plate(self.matrix, self._tick, self.tick, self.speed, self.difficulty))


            if press("d"):
                self.x += .1*self.speed*self.sensivity if self.x < 36 else 0
            elif press("a"):
                self.x -= .1*self.speed*self.sensivity if self.x > 0 else 0

            if press("w"):
                self.y -= .05*self.speed*self.sensivity if self.y > 30 else 0
            elif press("s"):
                self.y += .05*self.speed*self.sensivity if self.y < 38 else 0

            if press("space"):
                if not(self.is_pressed):
                    for obj in self.objlist:
                        
                        if hasattr(obj, "object"):
                            if collision(self.sq, obj.object) and not(obj.is_pressed):

                                obj.object.symbol = "-"
                                self.combo_score += 1
                                self.score += 100*self.difficulty*sqrt(self.combo_score)
                                obj.is_pressed = True

                    self.is_pressed = True

            else: self.is_pressed = False


            if press("escape"): break


            self.matrix.fill(" ")

            self.obj_update()
            self.sq_update()
            self.combo.draw()
            self.hp_label.draw()
            self.speed_label.draw()
            self.score_multiplier.draw()


            clear_console()
            self.matrix.show()


            self.tick += 1


            if self.tick <= 1000:
                self.first_ticks.append(time.perf_counter()-a)

                if self.tick % 100 == 0:
                    self._tick = middle(self.first_ticks)


            if self.hp <= 0:
                while not(press("escape")): pass
                break


    def sq_update(self):
        self.sq.xywh[0] = self.x
        self.sq.xywh[1] = self.y

        self.sq.draw()


    def obj_update(self):

        for obj in self.objlist:
            if hasattr(obj, "update"):
                try: obj.update()
                except TypeError: obj.update(self.score)
                if obj.y > 40:
                    self.objlist.remove(obj)

                    if not(obj.is_pressed):
                        self.combo_score = round(self.combo_score/2)
                        self.hp -= 1

            elif hasattr(obj, "draw"): obj.draw()


if __name__ == "__main__":
    Main()