import pygame
import sys

class Console:

    def __init__(self, size: list, fps = 30) -> None:

        pygame.init()
        pygame.font.init()

        self.myfont = pygame.font.SysFont('notomono', 16)

        size = round(size[0]*9.8), size[1] * 19

        self.FPS = fps
        self.size = size

        self.screen = pygame.display.set_mode(size)

        self.clock = pygame.time.Clock()

    def update(self, text: str) -> None:
            
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                sys.exit()


        self.screen.fill((0, 0, 0))


        text_split = text.split("\n")

        for line in text_split:
            
            textsurface = self.myfont.render(line, False, (255, 255, 255))

            self.screen.blit(textsurface,(0,text_split.index(line)*19))



        pygame.display.update()

        self.clock.tick(self.FPS)
