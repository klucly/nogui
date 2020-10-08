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

            size = round(size[0]*10), size[1] * 19

        self.FPS = fps
        self.size = size
        self.show_fps = show_fps
        self.event_list = []

        self.screen = pygame.display.set_mode(size)
        set_caption("Console")

        self.clock = pygame.time.Clock()
        

    def update(self, text: str) -> None:
        self.event_list = pygame.event.get()
        
        for i in self.event_list:
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

    def mouse_up(self) -> bool:
        # print(2)
        for event in self.event_list:
            # print(pygame.event.get())
            if event.type == pygame.MOUSEBUTTONUP:
                return True
        return False
            

    def mouse_down(self) -> bool:
        for event in self.event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True
        return False

    def mouse_coords(self) -> list:
        pos = pygame.mouse.get_pos()
        return (pos[0]/9, pos[1]/19) if os.name == "nt" else (pos[0]/10, pos[1]/19)
