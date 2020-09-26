import pygame
import sys
from pygame.display import set_caption
import pygame.freetype

class Console:

    def __init__(self, size: list, fps = 480) -> None:

        pygame.init()
        pygame.font.init()

        self.myfont = pygame.font.SysFont('notomono', 16)

        size = round(size[0]*9.8), size[1] * 19

        self.FPS = fps
        self.size = size

        self.screen = pygame.display.set_mode(size)
        set_caption("Console")

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
            text_split[text_split.index(line)] = None





        pygame.display.update()

        self.clock.tick(self.FPS)

# w = ""
# for i in range(10):
#     w += (f"{i//2}"*10+"\n")

# c = Console([10, 10])

# while 1:
    
#     c.update(w)