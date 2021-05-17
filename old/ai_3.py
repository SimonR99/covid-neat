import pygame as pg
import random as rd
import time
import neat
import os
import visualize


pg.font.init()


screen_width = 640   #define screen width
screen_height = 480  #define screen height
player_height = 90

screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("AI playing agains covid")

config_path = os.path.join('./config-feedforward.txt')
img_virus = pg.image.load('./virus_1.png')
img_bg = pg.image.load('./background.png')
img_player = pg.image.load('./happy_1.png')

gen = 0

count_to_new_enemy = 25


class Player():

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.vel = 4
        self.drawing = pg.Rect(self.x, self.y, self.width, self.height)


    def move(self, direction):
        if direction == 1:
            self.x += self.vel
        elif direction == -1:
            self.x -= self.vel
    def draw(self, screen):
        screen.blit(img_player, (self.x, self.y))


class Enemy():

    def __init__(self, screen_width):
        self.x = rd.randint(0,screen_width - 30)
        self.y = 0-30
        self.vel = 4

    def move(self):
        self.y += self.vel
    def draw(self, screen):
        screen.blit(img_virus, (self.x, self.y))
    def collide(self, player, screen):
        x_player = player.x
        y_player = player.y
        if self.x +30 > x_player and self.x < x_player + 30 and self.y +30 > y_player:
            return True
        else:
            return False

def draw_screen(screen, players, enemies):

    screen.fill((0, 150, 255))
    screen.blit(img_bg, (0,0))

    for enemy in enemies:
        enemy.draw(screen)
        #pass

    for player in players:
        player.draw(screen)

    pg.display.update()


def Check_Vision(player, enemy):
    table = [0,0,0,0,0,0,0,0,0]
    for i in range (0, len(enemy)):
        #if True:

        for j in range (-4,5):
            pos = player.x + j*30 + 15
            if (pos in range(enemy[i].x, enemy[i].x + 30)) and (enemy[i].y in range(50,screen_height)):
                table[j+4] = (enemy[i].y)/480
            else:
                pass
    return table

def eval_genomes(genomes, config):
    global screen, gen
    global count_to_new_enemy

    win = screen
    gen +=1

    #print("generation en cours :", gen)

    nets = []
    players = []
    ge = []
    enemies = []

    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        players.append(Player(screen_width/2, screen_height - player_height))
        ge.append(genome)

    clock = pg.time.Clock()

    run = True

    while run and len(players)>0:
        clock.tick(30)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()
                quit()
                break

        for x, player in enumerate(players):
            ge[x].fitness += 0.1
            direction =0
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

        for player in players:
            if player.x < 5 or player.x > screen_width -30:
                nets.pop(players.index(player))
                ge.pop(players.index(player))
                players.pop(players.index(player))

        draw_screen(screen, players, enemies)

def run(config_file):

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)


    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)



    winner = p.run(eval_genomes, 50)

    visualize.plot_stats(stats, ylog=True, view=True, filename="feedforward-fitness.svg")
    visualize.plot_species(stats, view=True, filename="feedforward-speciation.svg")


    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))



if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
