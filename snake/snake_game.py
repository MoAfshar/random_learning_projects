import numpy as np
import time
import pygame
import random

def display_snake(snake_position):
    for position in snake_position:
        ## The snake is 3 unites with each unit a 5x5 block
        ## Position as left, top, width height
        pygame.draw.rect(display, snake_colour, pygame.Rect(position[0], position[1], 5, 5))

def display_food(display, food_position, food):
    display.blit(food, (food_position[0], food_position[1]))

## If snake collapses with iself or with boundaries, game over
def collision_with_boundaries(snake_head):
    if (snake_head[0] >= 300 or snake_head[0] < 0 or snake_head[1] >= 300 or snake_head[1] < 0):
        return 1
    return 0

def collision_with_self(snake_position):
    snake_head = snake_position[0]
    if snake_head in snake_position[1:]:
        return 1
    return 0

def collision_with_food(food_position, score):
    food_position = [random.randrange(1, 30) * 10, random.randrange(1, 30) * 10]
    score += 1
    return food_position, score

## After seeing which direction button is pressed we need to change our snakes head position
def generate_snake(snake_head, snake_position, food_position, btn_direction, score):
    ## Right
    if btn_direction == 1:
        snake_head[0] += 5
    ## Left
    elif btn_direction == 0:
        snake_head[0] -= 5
    ## Down
    elif btn_direction == 2:
        snake_head[1] += 5
    ## Up
    elif btn_direction == 3:
        snake_head[1] -= 5
    else:
        pass

    ## To make the snake keep moving in one direction, add one unit to the
    ## head and remove one unit from the tail
    if snake_head == food_position:
        food_position, score = collision_with_food(food_position, score)
        snake_position.insert(0, list(snake_head))
    else:
        snake_position.insert(0, list(snake_head))
        snake_position.pop()
    return snake_position, food_position, score

def is_direction_blocked(snake_position):
    snake_head = snake_position[0]
    if collision_with_boundaries(snake_head) == 1 or collision_with_self(snake_position) == 1:
        return 1
    return 0

def play_game(snake_head, snake_position, food_position, btn_direction, food, score):
    crashed = False
    prev_btn_direction = 1
    btn_direction = 1

    while crashed is not True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
            ## When button pressed to move in a direction (left, right, up, down)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and prev_btn_direction != 1:
                    btn_direction = 0
                elif event.key == pygame.K_RIGHT and prev_btn_direction != 0:
                    btn_direction = 1
                elif event.key == pygame.K_UP and prev_btn_direction != 2:
                    btn_direction = 3
                elif event.key == pygame.K_DOWN and prev_btn_direction != 3:
                    btn_direction = 2
                else:
                    btn_direction = btn_direction
        display.fill(window_colour)
        display_food(display, food_position, food)
        display_snake(snake_position)
        snake_position, food_position, score = generate_snake(snake_head, snake_position, food_position, btn_direction, score)
        pygame.display.set_caption("Snake Game" + " " + "Score: " + str(score))
        pygame.display.update()
        prev_btn_direction = btn_direction
        if is_direction_blocked(snake_position) == 1:
            crashed = True
        frame_rate.tick(20)
    return score

def display_final_score(display_text, final_score):
    large_text = pygame.font.Font('freesansbold.ttf', 35)
    text_surf = large_text.render(display_text, True, snake_colour)
    text_rect = text_surf.get_rect()
    text_rect.center = ((width/2), (height/2))
    display.blit(text_surf, text_rect)
    pygame.display.update()
    time.sleep(2)

if __name__ == '__main__':
    ## Display game objects
    width = 300
    height = 300
    window_colour = (0, 0, 0)
    snake_colour = (255, 255, 255)
    path = 'C:\\Users\\945970\\Desktop\\random_learning_projects\\snake\\cookie.png'
    food = pygame.image.load(path)
    food = pygame.transform.scale(food, (5, 5))
    ## Starting position of the snake
    snake_head = [150, 150]
    snake_position = [[150, 150], [145, 150], [140, 150]]
    ## Starting position of the food, select randomly
    food_position = [random.randrange(1, 30) * 10, random.randrange(1, 30) * 10]
    score = 0
    ## Frame rate of our game
    frame_rate = pygame.time.Clock()

    ## Initialise all the modules from pygame
    pygame.init()
    ## Display game windonw
    display = pygame.display.set_mode((width, height))
    display.fill(window_colour)
    ## Only allows a portion of the screen to be updated, instead of of the
    ## entire area, if no argument it updates the entire surface area
    pygame.display.update()
    final_score = play_game(snake_head, snake_position, food_position, 1, food, score)
    display = pygame.display.set_mode((width, height))
    display.fill(window_colour)
    pygame.display.update()
    display_text = 'Your score is: ' + str(final_score)
    display_final_score(display_text, final_score)
    pygame.quit()
