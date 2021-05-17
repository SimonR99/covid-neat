import random as rd
import pygame as pg
import os



class Enemy():

    def __init__(self, screen_width, screen_height):
        self.x = rd.randint(0,screen_width - 30)
        self.y = 0-30
        self.vel = 10
        self.img_virus = pg.image.load('./res/images/virus.png')
        self.rect_virus = pg.Rect(self.x,self.y, 30,30)

    def draw(self,screen):
        screen.blit(self.img_virus, (self.rect_virus.x, self.rect_virus.y))

    def move(self):
        self.y += self.vel
        self.rect_virus.y = self.y
        
    def getRect(self):
        return self.rect_virus
        
    def collide(self, player):
        return player.colliderect(self.rect_virus)