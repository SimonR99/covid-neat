import pygame as pg
import os



class Player():
    def __init__(self, screen_width, screen_height):

        # Base settings
        self.width = 30
        self.height = 60
        self.speed = 4
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.x_pos = self.screen_width/2
        self.y_pos = self.screen_height - self.height - 40
        self.rect_player = pg.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.rect_player.x = self.screen_width/2

        # Images
        self.img_player = pg.image.load('./res/images/player.png')

        # Create line that represent the vision of the AI (use for debug only)
        self.line = list()
        for i in range(-5,4):
            self.line.append(pg.Rect(self.x_pos - i*30 -15,200,1,self.height-200))
    
    def draw(self, screen):
        screen.blit(self.img_player, (self.rect_player.x, self.rect_player.y))


    def move(self, direction): # 0 = right // 1 = left // 2 = do nothing
        if direction == 0:
            self.rect_player.x += self.speed
            self.x_pos += self.speed
        elif direction == 1:
            self.rect_player.x -= self.speed
            self.x_pos -= self.speed
        elif direction == 2:
            pass

    def getSmartVision(self,enemy): # create virtual vertical line that the AI will use to "see" if there's a virus in the way.
        table = [0,0,0,0,0,0,0,0,0] # each value of the table represent a line. Each line have a value between 0 and 1. 1 means that the 
        for i in range (0, len(enemy)):
            for j in range (-4,5):
                pos = self.rect_player.x + j*30 + 15
                if (pos in range(enemy[i].x, enemy[i].x + 30)) and (enemy[i].y in range(0,self.screen_height-50)):
                    table[j+4] = ((enemy[i].y) - 50)/self.screen_height
                else:
                    if pos > self.screen_width:
                        table[j+4] = 0.6
                    if pos < 0:
                        table[j+4] = 0.6
                    
        
        return [ round(i, 1) for i in table ]

    def moveVisionBox(self): # Use for debug, allow user to see the line
        for i in range(-5,4):
            self.line[i] = pg.Rect(self.x_pos - i*30 -15,50,1,self.height-50)

    def getRect(self):
        return self.rect_player