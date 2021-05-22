import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self,ai_Settings, screen):
        "Initialize the alien and set its starting position"
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_Settings

        #lOAD THE ALIEN IMAGE AND SET ITS POSITION

        self.image = pygame.image.load('space-ship-of-aliens.bmp.png')
        self.image = pygame.transform.scale(self.image, (50, 50))

        self.rect = self.image.get_rect()

        #Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Store the alien's exact position
        self.x = float(self.rect.x)

    def update(self):
        "Move the alien right or left"
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        "Return true if alien is at edge if screen."
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True


    def blitme(self):
        "Draw the alien at its current location"
        self.screen.blit(self.image, self.rect)

