import pygame as pg
import os



class Player():
    def __init__(self, width, height):
        self.width = 30
        self.height = 60
        self.x_pos = width/2
        self.y_pos = height - self.height - 40
        self.rect_player = pg.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.direction = 0                                      # 0 = neutre // 1 = gauche // 2 = droite
        self.speed = 4
        self.rect_player.x = width/2
        self.img_player = pg.image.load('./res/images/player.png')

        self.line = list()
        for i in range(-5,4):
            self.line.append(pg.Rect(self.x_pos - i*30 -15,200,1,self.height-200))
    
    def draw(self, screen):
        screen.blit(self.img_player, (self.rect_player.x, self.rect_player.y))


    def move(self):
        if self.direction == 1:
            self.rect_player.x += self.speed
            self.x_pos += self.speed
        elif self.direction == -1:
            self.rect_player.x -= self.speed
            self.x_pos -= self.speed

    def moveVisionBox(self):
        for i in range(-5,4):
            self.line[i] = pg.Rect(self.x_pos - i*30 -15,50,1,self.height-50)
