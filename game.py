from neatmanager import NeatManager
import pygame as pg
import sys
import os
import neat

from player import Player
from enemy import Enemy


class Game:
    def __init__(self, screen_width=640, screen_height=480, resizable=True):
        
        #Pygame initialisation
        pg.init()

        #Window parameters
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.game_speed = 100
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pg.time.Clock()
        pg.display.set_caption("Covid vs AI (NEAT)")
        self.next_page = 0

        #Text font parameters
        self.largeTextFont = pg.font.Font('freesansbold.ttf',90)
        self.smallTextFont = pg.font.Font("freesansbold.ttf",20)
        self.smallText = pg.font.SysFont("cominnercolorsansms",20)

        #Images and ressources
        self.img_background = pg.image.load("./res/images/background.png")
        self.config_path = os.path.join('./neatbot/confcovid.txt') # path to NEAT paramters
        
        
        # Game settings
        self.count_to_new_virus = 0
        self.start = False
        self.is_playing = False
        self.virus_rate = 15 # Low = more virus
        self.n_generation = 30

    def screenManager(self): #Call at each game to refresh the drawing and allow user to quit
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

        self.clock.tick(self.game_speed) #FPS
        self.screen.fill((0, 150, 255)) #blue
        self.screen.blit(self.img_background, (0, 0)) #Adjust to the size of the screen
        

    def menuWindow(self):
        while not self.start:
            self.screenManager()

            self.textSurfb1, self.textRectb1 = self.TextObj("Covid vs AI", self.largeTextFont)
            self.textRectb1.center = (self.screen_width/2, self.screen_height/2-100)
            self.screen.blit(self.textSurfb1, self.textRectb1)

            if self.button("Play", int(3*self.screen_width/9) - 100/2,300,100,50,(0,200,0),(0,255,0)):    #(msg,x,y,w,h,idlecolor,activecolor):
                self.start = True # Get out of the loop
                self.next_page = 1 # page 1 = human player

            if self.button("Neat robot", int(6*self.screen_width/9) - 100/2,300,100,50,(0,200,0),(0,255,0)):    #(msg,x,y,w,h,idlecolor,activecolor):
                self.start = True # Get out of the loop
                self.next_page = 2 # page 2 = neat player
            
          

            
        self.start = False #Reset for next time
        return self.next_page

    def playPlayer(self):

        self.player = Player(self.screen_width,self.screen_height) # Create a unique player
        self.enemies = [] # Create an array of virus (enemy)

        self.is_playing = True
        while self.is_playing:
            self.screenManager() 

            keys = pg.key.get_pressed()
            if keys[pg.K_a]:  #move left
                self.player.direction = 1
            elif keys[pg.K_d]: #move right
                self.player.direction = 0
            elif keys[pg.K_s]: #pause the game for debuging
                self.clock.tick(1)
                self.player.direction = 2
            else:
                self.player.direction = 2 #If no key, no move (direction 2 = stop)
            

            self.player.move(self.player.direction) # move the object player
            self.player.draw(self.screen) # draw the result on the screen
            
            self.count_to_new_virus += 1

            if self.count_to_new_virus == self.virus_rate: # Add new virus if true
                self.count_to_new_virus = 0
                self.enemies.append(Enemy(self.screen_width, self.screen_height))

            if len(self.enemies) > 0: # Move and draw each virus
                for x in range (0,len(self.enemies)):
                    self.enemies[x].move()
                    self.enemies[x].draw(self.screen)
                    if self.enemies[x].collide(self.player.getRect()):
                        self.is_playing = False # Stop the game if the virus touch the player
       
    def playNeat(self): 
        neat_manager = NeatManager(self.screen, self.screen_width, self.screen_height, self.game_speed) # The neat manager will manage the AI
        neat_manager.run(self.config_path, self.n_generation)
        
    def setGameSpeed(self, speed):
        #Allow user to change game speed
        #Make the AI training faster is speed is higher
        self.game_speed = speed
        return self.game_speed

    def TextObj(self,text, font): # Add by Daniel Bilodeau to make it easier to add text
        textSurface = font.render(text, True, (0,0,0))
        return textSurface, textSurface.get_rect()

    def button(self,msg,x,y,w,h,idlecolor,activecolor): # Add by Daniel Bilodeau to make it easier to add button
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pg.draw.rect(self.screen, activecolor,(x,y,w,h))
            if click[0] == 1:
                return True
        else:
            pg.draw.rect(self.screen, idlecolor,(x,y,w,h))

        self.smallText = pg.font.SysFont("cominnercolorsansms",20)
        self.textSurf, self.textRect = self.TextObj(msg, self.smallText)
        self.textRect.center = ( (x+(w/2)), (y+(h/2)) )
        self.screen.blit(self.textSurf, self.textRect)
        return False


    

