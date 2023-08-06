import pygame

pygame.init()


class Player:
    def __init__(self, screen):
        self.screen = screen

    def StartUp(self, img: str, xy=(100, 100)):
        self.Surf = pygame.image.load(img)
        self.Rect = self.Surf.get_rect(topleft=xy)

    def Scale(self, ScaleSize=(50, 50)):
        self.Surf = pygame.transform.scale(self.Surf, ScaleSize)

    def Draw(self):
        self.screen.blit(self.Surf, self.Rect)
