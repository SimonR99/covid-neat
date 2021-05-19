import os
import neat
import pygame as pg
from pygame.display import get_active
from player import Player
from enemy import Enemy
import visualize

class NeatManager():
    def __init__(self, screen, screen_width, screen_height, game_speed):
        self.game_speed = game_speed
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.config_path = os.path.join('./neatbot/config-feedforward.txt')
        self.generation =0
        self.count_to_new_enemy = 0
        self.img_background = pg.image.load("./res/images/background.png")
        self.players = []
        self.nets = []
        self.ge = []
        self.enemies = []

    def eval_genomes(self, genomes, config):
        global screen, gen
        global count_to_new_enemy

        self.generation +=1

        #print("generation en cours :", gen)

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
                self.ge[x].fitness += 0.1
                direction =0
                data = player.getSmartVision(self.enemies)
                #if x ==1:
                 #   print(data)
                output = self.nets[self.players.index(player)].activate((player.rect_player.x/self.screen_width, data[0], data[1], data[2],data[3],data[4],data[5],data[6],data[7],data[8]))
                if output[0] > 0.5:
                    direction = -1
                elif output[1] > 0.5:
                    direction = 0
                elif output[2] >0.5:
                    direction = 1
                player.move(direction)


            rem = []
            add_enemy = False
            self.count_to_new_enemy+=1
            if(self.count_to_new_enemy >= 20):
                add_enemy= True
                self.count_to_new_enemy = 10
            if add_enemy:
                self.enemies.append(Enemy(self.screen_width,self.screen_height))

            for enemy in self.enemies:
                enemy.move()
                for player in self.players:
                    if enemy.collide(player.getRect()):
                        self.ge[self.players.index(player)].fitness -= 1
                        self.nets.pop(self.players.index(player))
                        self.ge.pop(self.players.index(player))
                        self.players.pop(self.players.index(player))

                if enemy.y > self.screen_height:
                    rem.append(enemy)



            for r in rem:
                self.enemies.remove(r)

            for player in self.players:
                if player.rect_player.x < 5 or player.rect_player.x > self.screen_width -30:
                    self.nets.pop(self.players.index(player))
                    self.ge.pop(self.players.index(player))
                    self.players.pop(self.players.index(player))

            self.draw_screen(self.screen, self.players, self.enemies)

    def draw_screen(self,screen, players, enemies):
        self.screen.fill((0, 150, 255))
        self.screen.blit(self.img_background, (0,0))

        font = pg.font.Font('freesansbold.ttf', 32)
        green = (0, 255, 0)
        blue = (0, 0, 128)
        black = (0, 0, 0)  
        text = font.render('Generation : ' + str(self.generation), True, black)
        
        

        self.screen.blit(text, (20,20))


        for enemy in enemies:
            enemy.draw(screen)
            

        for player in players:
            player.draw(screen)

        pg.display.update()
    def run(self, config_file):

        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                            neat.DefaultSpeciesSet, neat.DefaultStagnation,
                            config_file)


        p = neat.Population(config)

        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)



        winner = p.run(self.eval_genomes, 10)

        visualize.plot_stats(stats, ylog=True, view=True, filename="feedforward-fitness.svg")
        visualize.plot_species(stats, view=True, filename="feedforward-speciation.svg")


        # show final stats
        print('\nBest genome:\n{!s}'.format(winner))
