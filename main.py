import pygame as pg
import random as rdaa
import time
import neat
import os
import visualize



from game import Game


game = Game()

while True:
    next_step = game.menuWindow()

    if next_step == 1:
        game.playPlayer()
    elif next_step == 2:
        game.playNeat()
    elif next_step == 3:
        game.settings()
    elif next_step == 4:
        break
    else:
        pass



    