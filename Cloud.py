import random, os, pygame, sys
from pygame.locals import *
from GameCharacter import GameCharacter

class Cloud(GameCharacter):
    def __init__(self, game):
        # Game to which this snoopy belongs to
        self.game = game

        # The woodstock image
        self.image = pygame.image.load(os.path.join("assets/images", "cloud.png"))
        
        # Resize the woodstock
        self.rect = self.image.get_rect()
        height = self.rect.height
        width = self.rect.width
        # self.image = pygame.transform.scale(self.image, (width/5, height/5))
        self.mainimage = self.image

        # Get the woodstock rect
        self.rect = self.image.get_rect()

        # Get a random y axis location
        height = self.rect.height
        xcoordinate = random.randint(height/2, self.game.height - height/2)

        # Set the woodstock to the top of the game at the x location
        self.rect.left = self.game.width
        self.rect.centery = xcoordinate

        # Set default vertical speed (arbitrarily decided)
        self.vspeed = 0

        # hspeed: horizontal speed
        self.hspeed = random.randint(-10,-4)
        
        # The current rotated degrees
        # self.currentRotation = 0

    
    def move(self):
        # oldcenter = self.rect.center
        # self.currentRotation = (self.currentRotation + self.rspeed) % 360
        # self.image = pygame.transform.rotate(self.mainimage, self.currentRotation)
        # self.rect = self.image.get_rect()
        # self.rect.center = oldcenter
        
        self.rect = self.rect.move([self.hspeed, self.vspeed])
        
        # if(self.isAtRightEdge() and self.isGoingRight() or self.isAtLeftEdge() and self.isGoingLeft()):
            # self.turnAround()