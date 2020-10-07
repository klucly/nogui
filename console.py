import pygame
import sys
from pygame.display import set_caption
import pygame.freetype
import os

class Console:

    def __init__(self, size: list, fps = 60, show_fps = False) -> None:

        pygame.init()
        pygame.font.init()

        if os.name == "nt":

            self.myfont = pygame.font.SysFont(pygame.font.get_fonts()[8], 16)

            size = round(size[0]*9), size[1] * 19

        else:
            self.myfont = pygame.font.SysFont('notomono', 16)

            size = round(size[0]*10.), size[1] * 19

        self.FPS = fps
        self.size = size
        self.show_fps = show_fps

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
        set_caption(f"Console {round(self.clock.get_fps())}fps" if self.show_fps else "Console")

        self.clock.tick(self.FPS)
