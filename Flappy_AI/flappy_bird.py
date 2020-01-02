### Objects Needed: Ground, Bird and Pipe ###
import pygame
import neat
import time
import os
import random
import pygame

pygame.font.init()

## Screen Size
WIN_WIDTH = 500
WIN_HEIGHT = 800
GEN = 0
filepath = os.path.dirname(__file__)

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join(filepath, 'imgs\\bird1.png'))),
              pygame.transform.scale2x(pygame.image.load(os.path.join(filepath, 'imgs\\bird2.png'))),
              pygame.transform.scale2x(pygame.image.load(os.path.join(filepath, 'imgs\\bird3.png')))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join(filepath, 'imgs\\pipe.png')))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join(filepath, 'imgs\\base.png')))
BACKGROUND_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join(filepath, 'imgs\\bg.png')))

SCORE_FONT = pygame.font.SysFont('comicsans', 50)

class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATIONS = 25 ## How much is the bird gonna tilt
    ROTATION_VEL = 20 ## How much we're going to rotate each frame
    ANIMATION_TIME = 5 ## How long we're showing each aninmation

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0 ## Start from centre
        self.tick_count = 0 ## Physics
        self.velocity = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.velocity = -10.5 ## Negative velocity to move upwards
        self.tick_count = 0 ## Keep track of when we last jumped
        self.height = self.y ## Where the bird jumped from or moving from

    def move(self):
        self.tick_count += 1 ## Increase counter to show that we've moved

        ## How many pixels we're moving up or down this frame
        ## e.g -10.5 + 11.5 = -9 total velocity
        displacement = self.velocity * self.tick_count + 1.5 * self.tick_count ** 2

        if displacement >= 16:
            displacement = 16 ## Don't move down too fast - Don't accelarate anymore
        if displacement < 0:
            displacement -= 2 ## If we're moving upwards, move a little bit more upwards

        self.y = self.y + displacement ## Update the current position of the bird

        if displacement < 0 or self.y < self.height+50:
            if self.tilt < self.MAX_ROTATIONS:
                self.tilt = self.MAX_ROTATIONS
        else:
            if self.tilt > -90:
                self.tilt -= self.ROTATION_VEL

    def draw(self, window):
        self.img_count += 1 ## How many times have we shown one image
        ## Check what image to show based on the image count
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0] ## If less than 5 show first pic
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1] ## If less than 10 show second and so on..
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4+1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        rotated_image = pygame.transform.rotate(self.img, self.tilt) ## Rotate
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center) ## And centre our image
        window.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        ## Collisions for our objects
        return pygame.mask.from_surface(self.img)

class Pipe():
    GAP = 200
    VELOCITY = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        ## How the pipes are drawn
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height() ## Where the bottom and top of our pipe is

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        ## Move the pipe to the left a little bit, change the x position
        ## Everytime we call the move method, we're moving the pipe based on the velocity
        self.x -= self.VELOCITY

    def draw(self, window):
        window.blit(self.PIPE_TOP, (self.x, self.top))
        window.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def get_mask(self):
        bot_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        return bot_mask, top_mask

    def collide(self, bird):
        bird_mask = bird.get_mask()
        bot_mask, top_mask = self.get_mask()

        ## Offset - Checking the pixels with each other
        ## How far away the top two corners are from each other
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bot_offset = (self.x - bird.x, self.bottom - round(bird.y))
        ## If no collision returns None
        b_point = bird_mask.overlap(bot_mask, bot_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if b_point or t_point:
            return True

        return False

class Base():
    VELOCITY = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
         self.y = y
         self.x1 = 0
         self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VELOCITY
        self.x2 -= self.VELOCITY

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, window):
        window.blit(self.IMG, (self.x1, self.y))
        window.blit(self.IMG, (self.x2, self.y))


def draw_window(window, birds, pipes, base, score, gen):
    window.blit(BACKGROUND_IMG, (0, 0))
    for pipe in pipes:
        pipe.draw(window)

    text = SCORE_FONT.render('Score: ' + str(score), 1, (255, 255, 255))
    gen_text = SCORE_FONT.render('Gen: ' + str(gen), 1, (255, 255, 255))

    window.blit(text, (WIN_WIDTH-10-text.get_width(), 10))
    window.blit(gen_text, (10, 10))

    base.draw(window)
    for bird in birds:
        bird.draw(window)
    pygame.display.update()

def main(genomes, config):
    #bird = Bird(230, 350) ## Centre our bird
    global GEN
    GEN += 1
    birds = []
    nets = []
    ge = []
    ids = []

    ## we have genome id and object hence the _
    for id, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)
        ids.append(id)
    print(ids)

    base = Base(730) ## At the very bottom of our screen
    pipes = [Pipe(700)]
    score = 0
    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(25)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        ## Moving the bird
        pipe_indx = 0
        if len(birds) > 0:
            ## If we passed the first pipe, start looking at the second pipe in the list
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_indx = 1
        else:
            run = False
            break

        for idx, bird in enumerate(birds):
            bird.move()
            ## Add some fitness
            ge[idx].fitness += 0.1

            bird_top_pipe_dist = abs(bird.y - pipes[pipe_indx].height)
            bird_bott_pipe_dist =  abs(bird.y - pipes[pipe_indx].bottom)
            output = nets[idx].activate((bird.y, bird_top_pipe_dist, bird_bott_pipe_dist))
            print(bird.y, bird_top_pipe_dist, bird_bott_pipe_dist)
            ## Output of neuron is in a list, in our case we just have 1 output neuron
            if output[0] > 0.5:
                bird.jump()

        add_pipe = False
        removed_pipes = []
        for pipe in pipes:
            for idx, bird in enumerate(birds):
                if pipe.collide(bird):
                    ## If a bird hits a pipe reduce fitness
                    ge[idx].fitness -= 1
                    birds.pop(idx)
                    nets.pop(idx)
                    ge.pop(idx)

                if not pipe.passed and pipe.x + 75 < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0: ## If pipe off the screen
                removed_pipes.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            ## Since all the dead birds are removed we can just increase the
            ## fitness for all the birds
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(620))

        for p in removed_pipes:
            pipes.remove(p)

        ## we hit the floor
        for idx, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(idx)
                nets.pop(idx)
                ge.pop(idx)

        base.move()
        draw_window(window, birds, pipes, base, score, GEN)

def run(conf_file):
    ## Read the config file
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        config_file)

    ## Generate a population based on the config file
    population = neat.Population(config)
    ## Optional Stats within the console
    stats = neat.StatisticsReporter()
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(stats)
    ## Set the fitness function to run 50 generations
    ## Call the main function 50 times and pass all the genomes and the config file
    ## Generate a game based on all the genomes
    ## You can save this genome using pickle if needed
    winner = population.run(main, 50)

if __name__ == '__main__':
    config_file = os.path.join(filepath, 'config-feedforward.txt')
    run(config_file)
