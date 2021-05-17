import os
import neat
from player import Player

class NeatManager():
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.config_path = os.path.join('./neatbot/config-feedforward.txt')
        self.generation =0

        self.players = []
        self.nets = []
        self.ge = []


    def initiateGenomes(self,genomes, config):
        self.generation +=1
        
        for genome_id, genome in genomes:
            genome.fitness = 0  # start with fitness level of 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            self.nets.append(net)
            self.players.append(Player(self.screen_width/2, self.screen_height))
            self.ge.append(genome)

    def evalGenomes(self,genomes, config, enemies):
        for x, player in enumerate(self.players):
            self.ge[x].fitness += 0.1
            direction = 0
            data = Check_Vision(player, enemies)
            output = nets[players.index(player)].activate((player.x, data[0], data[1], data[2],data[3],data[4],data[5],data[6],data[7],data[8]))
            if output[0] > 0.5:
                direction = -1
            elif output[1] > 0.5:
                direction = 0
            elif output[2] >0.5:
                direction = 1
            player.move(direction)


        rem = []
        add_enemy = False
        count_to_new_enemy+=1
        if(count_to_new_enemy >= 20):
            add_enemy= True
            count_to_new_enemy = 10
        if add_enemy:
            enemies.append(Enemy(screen_width))

        for enemy in enemies:
            enemy.move()
            for player in players:
                if enemy.collide(player, win):
                    ge[players.index(player)].fitness -= 1
                    nets.pop(players.index(player))
                    ge.pop(players.index(player))
                    players.pop(players.index(player))

            if enemy.y > screen_height:
                rem.append(enemy)



        for r in rem:
            enemies.remove(r)

        for player in self.players:
            if player.x < 5 or player.x > screen_width -30:
                nets.pop(players.index(player))
                ge.pop(players.index(player))
                players.pop(players.index(player))