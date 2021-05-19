import pygame as pg
import os



class Player():
    def __init__(self, screen_width, screen_height):
        self.width = 30
        self.height = 60
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.x_pos = self.screen_width/2
        self.y_pos = self.screen_height - self.height - 40
        self.rect_player = pg.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.direction = 0                                      # 0 = neutre // 1 = gauche // 2 = droite
        self.speed = 4
        self.rect_player.x = self.screen_width/2
        self.img_player = pg.image.load('./res/images/player.png')

        self.line = list()
        for i in range(-5,4):
            self.line.append(pg.Rect(self.x_pos - i*30 -15,200,1,self.height-200))
    
    def draw(self, screen):
        screen.blit(self.img_player, (self.rect_player.x, self.rect_player.y))


    def move(self, direction):
        if direction == 1:
            self.rect_player.x += self.speed
            self.x_pos += self.speed
        elif direction == -1:
            self.rect_player.x -= self.speed
            self.x_pos -= self.speed
    
    def getSmartVision(self,enemy):
        table = [0,0,0,0,0,0,0,0,0]
        for i in range (0, len(enemy)):
            #if True:

            for j in range (-4,5):
                pos = self.rect_player.x + j*30 + 15
                if (pos in range(enemy[i].x, enemy[i].x + 30)) and (enemy[i].y in range(50,self.screen_height)):
                    table[j+4] = (enemy[i].y)/self.screen_height
                    if pos > self.width:
                        table[j+4] = 0.6
                    if pos < 0:
                        table[j+4] = 0.6
                else:
                    pass
        
        return [ round(i, 1) for i in table ]

    def moveVisionBox(self):
        for i in range(-5,4):
            self.line[i] = pg.Rect(self.x_pos - i*30 -15,50,1,self.height-50)

    def getRect(self):
        return self.rect_player