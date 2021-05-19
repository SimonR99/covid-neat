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

        #Game parameters
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.game_speed = 3000
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pg.time.Clock()
        self.largeTextFont = pg.font.Font('freesansbold.ttf',90)
        self.smallTextFont = pg.font.Font("freesansbold.ttf",20)
        self.start = False
        self.is_playing = False
        self.smallText = pg.font.SysFont("cominnercolorsansms",20)
        self.img_background = pg.image.load("./res/images/background.png")
        self.img_virus = pg.image.load('./res/images/virus.png')
        self.img_player = pg.image.load('./res/images/player.png')
        self.next_page = 0
        self.virus_rate = 15
        pg.display.set_caption("Covid vs AI (NEAT)")
        self.count_to_new_virus = 0
        self.config_path = os.path.join('./neatbot/config-feedforward.txt')

    def screenManager(self):
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
        self.clock.tick(self.game_speed)
        self.screen.fill((0, 150, 255))
        self.screen.blit(self.img_background, (0, 0))
        

    def menuWindow(self):
        while not self.start:
            self.screenManager()
            self.textSurfb1, self.textRectb1 = self.TextObj("Covid vs AI", self.largeTextFont)
            self.textRectb1.center = (self.screen_width/2, self.screen_height/2-100)
            self.screen.blit(self.textSurfb1, self.textRectb1)

            if self.button("Play", int(2*self.screen_width/9),300,100,50,(0,200,0),(0,255,0)):    #(msg,x,y,w,h,idlecolor,activecolor):
                self.start = True
                self.next_page = 1

            if self.button("Neat robot", int(4*self.screen_width/9),300,100,50,(0,200,0),(0,255,0)):    #(msg,x,y,w,h,idlecolor,activecolor):
                self.start = True
                self.next_page = 2
            
            if self.button("Settings", int(6*self.screen_width/9),300,100,50,(0,200,0),(0,255,0)):    #(msg,x,y,w,h,idlecolor,activecolor):
                self.start = True
                self.next_page = 3
          

            
        self.start = False
        return self.next_page

    def playPlayer(self):
        self.player = Player(self.screen_width,self.screen_height)
        self.enemies = []
        self.first_enemy = Enemy(self.screen_width, self.screen_height)

        self.is_playing = True
        while self.is_playing:
            self.screenManager()

            keys = pg.key.get_pressed()
            if keys[pg.K_a]:  #move left
                self.player.direction = -1
            elif keys[pg.K_d]: #move right
                self.player.direction = 1
            else:
                self.player.direction = 0
            
            self.player.move()
            self.player.draw(self.screen)
            self.first_enemy.y = 100
            self.first_enemy.x = 100
            self.first_enemy.draw(self.screen)
            

            self.count_to_new_virus += 1
            if self.count_to_new_virus == self.virus_rate:
                self.count_to_new_virus = 0
                self.enemies.append(Enemy(self.screen_width, self.screen_height))

            if len(self.enemies) > 0:
                for x in range (0,len(self.enemies)):
                    self.enemies[x].move()
                    self.enemies[x].draw(self.screen)
                    if self.enemies[x].collide(self.player.getRect()):
                        self.is_playing = False
       
    def playNeat(self): 
        neat_manager = NeatManager(self.screen, self.screen_width, self.screen_height, self.game_speed)

        self.is_playing = True
        
        neat_manager.run(self.config_path)
        


       

       
    
    def settings(self):
        self.is_playing = True
        while self.is_playing:
            self.screen.fill((0, 150, 255))
            self.textSurfb1, self.textRectb1 = self.TextObj("Covid vs AI", self.largeTextFont)
            self.textRectb1.center = (self.screen_width/2, self.screen_height/2-100)
            self.screen.blit(self.textSurfb1, self.textRectb1)

    
    
    def setGameSpeed(self, speed):
        #Allow user to change game speed
        #Make the AI training faster is speed is higher
        self.game_speed = speed
        return self.game_speed

    def TextObj(self,text, font):
        textSurface = font.render(text, True, (0,0,0))
        return textSurface, textSurface.get_rect()

    def button(self,msg,x,y,w,h,idlecolor,activecolor):
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


    

