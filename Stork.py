import random, os, pygame, sys
from pygame.locals import *
from GameCharacter import GameCharacter

LEFT_KEY = pygame.K_LEFT
RIGHT_KEY = pygame.K_RIGHT

class Stork(GameCharacter):
    def __init__(self, game, dumbo1):
        # Game to which this stork belongs to
        self.game = game

        # Get stork's image
        # self.image = pygame.image.load(os.path.join("assets/images", "stork-1.jpg"))
        self.image = dumbo1

        # Resize the huge stork
        self.rect = self.image.get_rect()
        height = self.rect.height
        width = self.rect.width
        # self.image = pygame.transform.flip(self.image, True, False)
        # self.image = pygame.transform.scale(self.image, (width/2, height/2))

        # Reset the rect to the resized image's rect
        self.rect = self.image.get_rect()

        # Position him at the bottom of the game screen
        self.rect.left = 0
        self.rect.centery = self.game.height/2

        self.speed = 10
        self.bobbingAmplitude = 2
        self.bobbingSpeed = self.bobbingAmplitude*2

    def move(self, keys, joyStick):
        # if keys and (self.isGoingLeft() and keys[RIGHT_KEY] or self.isGoingRight() and keys[LEFT_KEY]):
            # self.turnAround()

        self.moveVertical(keys, self.game.height, self.game.width, joyStick)
        self.moveHorizontal(keys, self.game.height, self.game.width, joyStick)
        
        # if (self.isGoingLeft() and self.joyStick_isRight(joyStick) or self.isGoingRight() and self.joyStick_isLeft(joyStick)):
        #     self.turnAround()

        # self.keepFlying()

    def moveVertical(self, keys, height, width, joyStick):
        vertical = joyStick.get_axis(1)
        selfMove = self.rect
        if (keys[pygame.K_DOWN] and not(keys[pygame.K_UP])) or vertical > 0.00390625:
            self.rect = self.rect.move([0,self.speed])
        elif (keys[pygame.K_UP] and not(keys[pygame.K_DOWN])) or vertical < 0.00390625:
                self.rect = self.rect.move([0,-self.speed])
        
        if (self.rect.top < 0) or (self.rect.bottom > height):
            self.rect = selfMove
        
        selfMove = self.rect
        
    def moveHorizontal(self, keys, height, width, joyStick):
        horizontal = joyStick.get_axis(0)
        selfMove = self.rect
        if (keys[pygame.K_LEFT] and not(keys[pygame.K_RIGHT])) or horizontal < 0.00390625:
            self.rect = self.rect.move([-self.speed,0])
        elif keys[pygame.K_RIGHT] and not(keys[pygame.K_LEFT]) or horizontal > 0.00390625:
            self.rect = self.rect.move([self.speed,0])
    
        if (self.rect.right > width) or (self.rect.left < 0):
            self.rect = selfMove

    def keepFlying(self):
        bob = random.randint(1,3)

        newRect = self.rect.move([self.hspeed, 0])#self.bobbingSpeed])
        if bob == 3:
            newRect = self.rect.move([self.hspeed, 0])#self.bobbingSpeed])
            self.bobbingSpeed = -self.bobbingSpeed
        else:
            newRect = self.rect.move([self.hspeed,0])

        self.rect = newRect

        if(self.isAtRightEdge() and self.isGoingRight() or self.isAtLeftEdge() and self.isGoingLeft()):
            self.turnAround()
