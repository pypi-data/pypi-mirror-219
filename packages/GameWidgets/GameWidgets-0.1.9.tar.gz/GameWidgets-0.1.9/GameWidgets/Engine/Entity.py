import pygame
import time

pygame.init()


class Entity:
    def __init__(self,Screen):
        self.frame = 0
        self.stime = 0
        self.ctime = 0
        self.screen = Screen
        self.animationStart = False
        self.xyanituple = (0,0)

    def createAnimation(self, frameCycle: tuple, size=(50, 50)):
        self.images = []
        for i in frameCycle:
            img = pygame.image.load(i)
            img = pygame.transform.scale(img, size)
            self.images.append(img)

    def StartAnimation(self):
        self.animationStart = True
        self.stime = time.time()

    def Animate(self, Speed: int, xy: tuple):
        self.xyanituple = xy
        if self.animationStart:
            self.ctime = time.time()
            if self.ctime - self.stime >= Speed:
                try:
                    self.stime = time.time()
                    self.frame += 1
                    c = self.images[self.frame]
                except:
                    self.stime = time.time()
                    self.frame = 0
        else:
            return
    def Draw(self):
        self.screen.blit(self.images[self.frame],self.xyanituple)

