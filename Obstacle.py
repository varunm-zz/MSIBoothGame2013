import random, os, pygame, sys
from pygame.locals import *
from GameCharacter import GameCharacter

class Obstacle(GameCharacter):
    def __init__(self, game, balloon1, balloon2, balloon3, bird):
        # Game to which this snoopy belongs to
        self.game = game

        num = random.randint(1,4)
        if num == 4:
            imagename = "bird11.png"
            self.image = bird
        else:
            imagename = "balloon" + str(num) + ".png"
            
            # The woodstock image
            if num == 1:
                # self.image = pygame.image.load(os.path.join("assets/images", imagename))
                self.image = balloon1
            elif num == 2:
                self.image = balloon2
            else:
                self.image = balloon3
        
        # Resize the woodstock
        # self.rect = self.image.get_rect()
        # height = self.rect.height
        # width = self.rect.width
        # if imagename == "balloon1.png":
        #     self.image = pygame.transform.scale(self.image, (width/5, height/5))
        # elif imagename == "balloon2.png":
        #     self.image = pygame.transform.scale(self.image, (width/30, height/30))
        # elif imagename == "balloon3.png":
        #     self.image = pygame.transform.scale(self.image, (width/35, height/35))
        # self.mainimage = self.image

        # Get the woodstock rect
        self.rect = self.image.get_rect()

        # Get a random y axis location
        height = self.rect.height
        ycoordinate = random.randint(height/2, self.game.height - height/2)

        # Set the woodstock to the top of the game at the x location
        self.rect.left = self.game.width
        self.rect.centery = ycoordinate

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