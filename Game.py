import random, os, pygame, sys
from pygame.locals import *
# from Snoopy import Snoopy
from Stork import Stork
# from Woodstock import Woodstock
from Cloud import Cloud
from Obstacle import Obstacle

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

# Pygame Keys
Q = pygame.K_q
R = pygame.K_r
ESCAPE = pygame.K_ESCAPE

# Colors
COLOR_BLACK = (0,0,0)

# Events
TIME_UP = pygame.USEREVENT + 1

class Game(object):
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode([width, height])
        self.balloon1 = pygame.image.load(os.path.join("assets/images", "balloon1.png"))
        self.balloon2 = pygame.image.load(os.path.join("assets/images", "balloon2.png"))
        self.balloon3 = pygame.image.load(os.path.join("assets/images", "balloon3.png"))
        self.bird_init = pygame.image.load(os.path.join("assets/images", "bird11.png"))
        self.bird = pygame.transform.flip(self.bird_init, True, False)
        self.bird2 = pygame.image.load(os.path.join("assets/images", "bird12.png"))
        self.bird2 = pygame.transform.flip(self.bird2, True, False)
        self.dumbo1 = pygame.image.load(os.path.join("assets/images", "dumbo_frame1.png"))
        self.dumbo2 = pygame.image.load(os.path.join("assets/images", "dumbo_frame2.png"))
        self.dumbo3 = pygame.image.load(os.path.join("assets/images", "dumbo_frame3.png"))
        # self.dumbo1 = pygame.transform.flip(self.dumbo1, True, False)
        # self.dumbo2 = pygame.transform.flip(self.dumbo2, True, False)
        # self.dumbo3 = pygame.transform.flip(self.dumbo3, True, False)

        self.balloon1 = pygame.transform.scale(self.balloon1, (self.balloon1.get_rect().width/5, self.balloon1.get_rect().height/5))
        self.balloon2 = pygame.transform.scale(self.balloon2, (self.balloon2.get_rect().width/30, self.balloon2.get_rect().height/30))
        self.balloon3 = pygame.transform.scale(self.balloon3, (self.balloon3.get_rect().width/35, self.balloon3.get_rect().height/35))
        self.bird = pygame.transform.scale(self.bird, (self.bird.get_rect().width/2, self.bird.get_rect().height/2))
        self.bird2 = pygame.transform.scale(self.bird2, (self.bird2.get_rect().width/2, self.bird2.get_rect().height/2))
        self.dumbo1 = pygame.transform.scale(self.dumbo1, (self.dumbo1.get_rect().width/10, self.dumbo1.get_rect().height/10))
        self.dumbo2 = pygame.transform.scale(self.dumbo2, (self.dumbo2.get_rect().width/10, self.dumbo2.get_rect().height/10))
        self.dumbo3 = pygame.transform.scale(self.dumbo3, (self.dumbo3.get_rect().width/10, self.dumbo3.get_rect().height/10))


        
        self.re_init()
    
    def re_init(self):
        self.score = 0
        self.lives = 3
        self.totalTime = 10
        highscore = open("highscore.txt", "r")
        currentHighScore = highscore.readline()

        self.score = 0
        self.totalTime = 25

        # Start a timer to figure out when the game ends (60 seconds)
        pygame.time.set_timer(TIME_UP,25000)
        self.startTime = pygame.time.get_ticks()

        # font = pygame.font.Font(os.path.join("assets/fonts", "peanuts.tff"), 28)
        self.fontRegular = pygame.font.Font(os.path.join("assets/fonts", "cella.otf"), 28)
        self.fontSmall = pygame.font.Font(os.path.join("assets/fonts", "cella.otf"), 20)
        
        # Render the text with Anti-aliasing
        self.scoreText = self.fontRegular.render("Score: " + str(self.score), True, COLOR_BLACK)
        self.scorepos = self.scoreText.get_rect(left = 40, top = 20)
        # self.timerText = self.fontRegular.render("Time Left: " + str(self.time_left()), True, COLOR_BLACK)
        self.timerText = self.fontRegular.render("Lives: " + str(self.lives), True, COLOR_BLACK)
        self.timerpos = self.timerText.get_rect(left = 40, top = 50)
        self.highscoreText = self.fontRegular.render("High Score: " + currentHighScore, True, COLOR_BLACK)
        self.highscorepos = self.highscoreText.get_rect(left = self.width-400, top = 20)
        
        # Initialize snoopy and the woodstocks
        self.dumbo = Stork(self, self.dumbo1)
        self.clouds = self.createClouds()
        self.obstacles = self.createObstacles()
        
        
        pygame.joystick.init()
        
        
        
    def time_left(self):
        return self.totalTime - self.current_time()
    
    # Returns time since startTime in seconds
    def current_time(self):
        return (pygame.time.get_ticks() - self.startTime)/1000

    def run(self):
        runGame = True
        
        while runGame:
            joyStick = pygame.joystick.Joystick(0)
            joyStick.init()
            # Define colors
            black = (0,0,0)
            end = True
            self.gameOver = False
            timerIsRunning = True
            while not self.gameOver:
                self.score += 1
                self.resetClouds()
                self.resetObstacles()

                keys = pygame.key.get_pressed()

                for event in pygame.event.get():
                    if  self.lives <= 0 or event.type == QUIT or keys and keys[Q]:#timerIsRunning and event.type == TIME_UP
                        self.gameOver = True
                        highscore = open("highscore.txt", "r")
                        currentHighScore = int(highscore.readline())
                        
                        #Write the highscore
                        if currentHighScore < self.score:
                            highscore = open("highscore.txt", "w")
                            highscore.write(str(self.score))
                        
                        # highscore.write(str(self.score))
                        break

                self.moveClouds()
                self.moveObstacles()
                self.dumbo.move(keys, joyStick)#(joyStick, keys)
            
                self.draw()
                pygame.display.update()
        
            # Game End State
            self.dumbo.stop()
            while end:
                #print "drawing the end"
                self.drawTheEnd()
                
                keys = pygame.key.get_pressed()
                if joyStick.get_button(0):
                    runGame = True
                    self.re_init()
                    end = False
                    break
                for event in pygame.event.get():
                    if event.type == QUIT or keys and keys[Q]:
                        return
                    if keys and keys[R]: #Restart game
                        runGame = True
                        self.re_init()
                        end = False
                        break
                pygame.display.update()
        
    def createClouds(self):
        # There is one woodstock for each speed
        # The first one is vertical speed. Second one is the rotational speed
        clouds = []

        for i in xrange(3):
            c = Cloud(self)
            c.setVSpeed(0)
            clouds += [c]

        return clouds

    #	Checks if any of the woodstocks have collided with snoopy
    def resetClouds(self):
        for c in self.clouds:
            # Woodstock is dead if he hits the bottom or if Snoopy catches him
            if c.isAtLeftEdge():
                self.clouds.remove(c)
                c = Cloud(self)
                c.setVSpeed(0)
                self.clouds.append(c)

    def createObstacles(self):
        # There is one woodstock for each speed
        # The first one is vertical speed. Second one is the rotational speed
        obstacles = []

        for i in xrange(8):
            o = Obstacle(self, self.balloon1, self.balloon2, self.balloon3, self.bird)
            o.setVSpeed(0)
            obstacles += [o]

        return obstacles

    #   Checks if any of the woodstocks have collided with snoopy
    def resetObstacles(self):
        for o in self.obstacles:
            # Woodstock is dead if he hits the bottom or if Snoopy catches him
            if o.isAtLeftEdge():
                self.obstacles.remove(o)
                o = Obstacle(self, self.balloon1, self.balloon2, self.balloon3, self.bird)
                o.setVSpeed(0)
                self.obstacles.append(o)

            if o.hasCollidedWith(self.dumbo):
                self.lives -= 1
                self.obstacles.remove(o)
                o = Obstacle(self, self.balloon1, self.balloon2, self.balloon3, self.bird)
                o.setVSpeed(0)
                self.obstacles.append(o)
                

    def moveClouds(self):
        for w in self.clouds:
            w.move()

    def moveObstacles(self):
        for o in self.obstacles:
            o.move()

    def draw(self):
        # Redraw the background and the game characters
        self.drawBackground()
        for w in self.clouds:
            self.screen.blit(w.image, w.rect)
        for o in self.obstacles:
            if o.image == self.bird:
                o.image = self.bird2
            elif o.image == self.bird2:
                o.image = self.bird
            self.screen.blit(o.image, o.rect)

        if self.dumbo.image == self.dumbo1:
            self.dumbo.image = self.dumbo2
        elif self.dumbo.image == self.dumbo2:
            self.dumbo.image = self.dumbo3
        elif self.dumbo.image == self.dumbo3:
            self.dumbo.image = self.dumbo1
        self.screen.blit(self.dumbo.image, self.dumbo.rect)
        
        highscore = open("highscore.txt", "r")
        currentHighScore = highscore.readline()
        
        self.scoreText = self.fontRegular.render("Score: " + str(self.score), True, COLOR_BLACK)
        self.screen.blit(self.scoreText, self.scorepos)
        # self.timerText = self.fontRegular.render("Time Left: " + str(self.time_left()), True, COLOR_BLACK)
        self.timerText = self.fontRegular.render("Lives: " + str(self.lives), True, COLOR_BLACK)
        self.screen.blit(self.timerText, self.timerpos)
        self.highscoreText = self.fontRegular.render("High Score: " + currentHighScore, True, COLOR_BLACK)
        self.screen.blit(self.highscoreText, self.highscorepos)

        pygame.display.update()

    def drawBackground(self):
      self.drawSky()
    
    def drawSky(self):
        skyimage = pygame.image.load(os.path.join("assets/images/sky", "sky2.jpg"))
        skyimage = pygame.transform.scale(skyimage, (self.width, self.height))
        skyrect = skyimage.get_rect()
        self.screen.blit(skyimage, skyrect)
    
    def drawTheEnd(self):

        # Draw the background
        self.drawBackground()
        
        # Draw the final score
        self.scoreText = self.fontRegular.render("Score: " + str(self.score), True, COLOR_BLACK)
        self.scorepos = self.scoreText.get_rect(centerx = self.width/2, centery = self.height/2 - 50)
        self.screen.blit(self.scoreText, self.scorepos)

        # Draw "The End"
        theEnd = self.fontRegular.render("The End", True, COLOR_BLACK)
        theEndpos = theEnd.get_rect(centerx = self.width/2, centery = self.height/2)
        self.screen.blit(theEnd, theEndpos)
        
        # Draw Instructions Text
        self.instructions = self.fontSmall.render("[R] to start a new game, [ESC] to quit", True, COLOR_BLACK)
        self.instructionsPos = self.instructions.get_rect(centerx = self.width/2, centery = self.height/2 + 50)
        self.screen.blit(self.instructions, self.instructionsPos)
        
        pygame.display.update()
        

game = Game(1250, 750)
game.run()
