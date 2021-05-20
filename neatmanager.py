import os
import neat
import pygame as pg
import visualize

from player import Player
from enemy import Enemy



class NeatManager():
    def __init__(self, screen, screen_width, screen_height, game_speed):

        # Window settings
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        

        # Game settings
        self.players = []
        self.nets = []
        self.ge = []
        self.enemies = []
        self.generation =0
        self.count_to_new_enemy = 0
        self.game_speed = game_speed
        
        
        #Ressources
        self.img_background = pg.image.load("./res/images/background.png")
        self.base_font = pg.font.Font('freesansbold.ttf', 32)
        self.black = (0, 0, 0) 


    def eval_genomes(self, genomes, config):
        global screen, gen
        global count_to_new_enemy

        self.generation +=1
        self.enemies = []

        for genome_id, genome in genomes:
            genome.fitness = 0  # start with fitness level of 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            self.nets.append(net)
            self.players.append(Player(self.screen_width, self.screen_height))
            self.ge.append(genome)

        self.clock = pg.time.Clock()

        run = True

        while run and len(self.players)>0:
            self.clock.tick(self.game_speed)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                    pg.quit()
                    quit()
                    break

            for x, player in enumerate(self.players):
                
                data = player.getSmartVision(self.enemies)
                self.position = (player.rect_player.x)/self.screen_width # give x position between 0.0 and 1.0
                self.ge[x].fitness += 1
                
                # The output is list compose of 3 elements base
                output = self.nets[self.players.index(player)].activate((self.position*2,0.2*data[1]+0.5*data[2] + data[3],data[4],0.2*data[7] + 0.5*data[6] +data[5]))

                max_value = max(output)
                max_index = output.index(max_value)
                player.move(max_index)
                


            rem = [] # List enemy to remove
            add_enemy = False 
            self.count_to_new_enemy+=1
            if(self.count_to_new_enemy >= 20):
                add_enemy= True
                self.count_to_new_enemy = 10
            if add_enemy:
                self.enemies.append(Enemy(self.screen_width,self.screen_height))
            for enemy in self.enemies: # Detect collision between enemies and players
                enemy.move()
                for player in self.players:
                    if enemy.collide(player.getRect()):
                        self.nets.pop(self.players.index(player))
                        self.ge.pop(self.players.index(player))
                        self.players.pop(self.players.index(player))
                if enemy.y > self.screen_height: # Detect if virus outside the screen
                    rem.append(enemy)

            for r in rem: # Remove virus (free space)
                self.enemies.remove(r)

            for player in self.players:
                if player.rect_player.x < 5 or player.rect_player.x > self.screen_width -30:
                    self.nets.pop(self.players.index(player))
                    self.ge.pop(self.players.index(player))
                    self.players.pop(self.players.index(player))

            self.draw_screen(self.screen, self.players, self.enemies)

    def draw_screen(self,screen, players, enemies):
        # Background
        self.screen.fill((0, 150, 255)) # Blue
        self.screen.blit(self.img_background, (0,0))
        
        #Text
        self.text = self.base_font.render('Generation : ' + str(self.generation), True, self.black)
        self.screen.blit(self.text, (20,20)) # Top left corner

        # Draw players and enemies
        for enemy in enemies:
            enemy.draw(screen)
        for player in players:
            player.draw(screen)

        # Update all the window
        pg.display.update()

    def run(self, config_file, generation):

        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                            neat.DefaultSpeciesSet, neat.DefaultStagnation,
                            config_file) #Load the configuration

        p = neat.Population(config)
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)
        winner = p.run(self.eval_genomes , generation)

        # Produce graphics at the end.
        visualize.plot_stats(stats, ylog=False, view=True, filename="feedforward-fitness.svg")
        visualize.plot_species(stats, view=True, filename="feedforward-speciation.svg")


        # show final stats
        print('\nBest genome:\n{!s}'.format(winner))
