import pygame as pg


from game import Game


game = Game() #Create a new game. It's possible to create multiple game at the same time to fight agains't the AI

while True: # Main Game Loop
    next_step = game.menuWindow() # Return to menu at the end of each game
    if next_step == 1:#This option is selected to let the user play
        game.playPlayer()
    elif next_step == 2:#This option is selected to let the AI play
        game.playNeat()
    elif next_step == 3:#TO DO
        game.settings()# Settings are to implement to let a user decide the speed of the game, the number of generation and the size of the population. (And more)
    else: # Add else because of MISRA
        pass



    