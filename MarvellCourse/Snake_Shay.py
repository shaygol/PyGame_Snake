#############################
## (C) Shay Goldshmit 2022 ##
#############################

import random
import color_constants as Colors
from os import environ as env_var
import tkinter.messagebox
import tkinter

env_var['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'  # for hiding an annoying message from Pygame
import pygame

pygame.init()
pygame.display.set_caption('Shay\'s Snake')

# constants
KEYBOARD_PRESSED = pygame.KEYDOWN
GAME_SPEED_START = 35
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_COLOR = Colors.SEAGREEN4
SNAKE_SIZE = SCREEN_HEIGHT // 100
STEP_LENGTH = SNAKE_SIZE
SNAKE_COLOR = Colors.YELLOW1

# global variables
game_screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
food_size = 2 * SNAKE_SIZE
food_color = Colors.BANANA
game_over = None
game_speed = None
snake_dir = None
head_pos_x = None
head_pos_y = None
snake_pos_lst = None
is_space = None
snake_len = None
pos_food_x = SCREEN_HEIGHT // 2
pos_food_y = SCREEN_WIDTH // 2
score = None


def draw_food(rand_new=False):
    global pos_food_x
    global pos_food_y
    global food_color
    global food_size

    if rand_new:
        pos_food_x = random.randint(10, SCREEN_WIDTH - 5)
        pos_food_x -= pos_food_x % SNAKE_SIZE
        pos_food_y = random.randint(10, SCREEN_HEIGHT - 5)
        pos_food_y -= pos_food_y % SNAKE_SIZE
        while True:
            colo = Colors.get_rand_color()
            food_color = colo[0]
            food_color_name = colo[1]
            if (food_color != SCREEN_COLOR) and ('green' not in food_color_name):
                break


        food_size_factor = 2 * random.random() + 1
        food_size = int(food_size_factor * SNAKE_SIZE)
        print(f'Food: ({pos_food_x}, {pos_food_y}), Size - {food_size}, Color - {colo[1]}')

    if food_size % 3 == 0:
        pygame.draw.rect(game_screen, food_color, [pos_food_x, pos_food_y, food_size, food_size])
    elif food_size % 3 == 1:
        pygame.draw.circle(game_screen, food_color, center=(pos_food_x, pos_food_y), radius=food_size)
    else:
        pygame.draw.polygon(game_screen, food_color, ((pos_food_x - food_size, pos_food_y),
                                                      (pos_food_x, pos_food_y - food_size),
                                                      (pos_food_x + food_size, pos_food_y),
                                                      (pos_food_x, pos_food_y + food_size)))


def init_game():
    global game_over
    global game_speed
    global snake_dir
    global head_pos_x
    global head_pos_x
    global head_pos_y
    global head_pos_y
    global snake_pos_lst
    global game_screen
    global is_space
    global score

    game_over = False
    game_speed = GAME_SPEED_START
    snake_dir = ''
    head_pos_x = random.randint(SCREEN_WIDTH // 2 - SCREEN_WIDTH // 4, SCREEN_WIDTH // 2 + SCREEN_WIDTH // 4)
    head_pos_x -= (head_pos_x % SNAKE_SIZE)
    head_pos_y = random.randint(SCREEN_HEIGHT // 2 - SCREEN_HEIGHT // 4, SCREEN_HEIGHT // 2 + SCREEN_HEIGHT // 4)
    head_pos_y -= (head_pos_y % SNAKE_SIZE)
    snake_pos_lst = [(head_pos_x, head_pos_y)]  # list of tuples
    is_space = True
    score = 0
    draw_food(True)


def finish_game():
    global game_over

    while not game_over:
        draw_score()
        font = pygame.font.Font('freesansbold.ttf', SCREEN_HEIGHT // 15)
        text = font.render('Game Over!', True, Colors.RED1, Colors.BLUE)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        game_screen.blit(text, textRect)
        pygame.display.update()

        for game_event in pygame.event.get():
            if game_event.type == pygame.QUIT:
                game_over = True
            elif game_event.type == KEYBOARD_PRESSED:
                if game_event.key == pygame.K_ESCAPE:
                    game_over = True
                else:
                    init_game()
                    return


def draw_score():
    global score

    font = pygame.font.Font('freesansbold.ttf', SCREEN_HEIGHT // 30)
    text = font.render(f'Score: {score}', True, Colors.BLACK, SCREEN_COLOR)
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH / 14, SCREEN_HEIGHT / 40)
    game_screen.blit(text, textRect)


def draw_snake():
    global snake_pos_lst

    for pos_tpl in snake_pos_lst:
        pygame.draw.circle(game_screen, color=SNAKE_COLOR, center=tuple(pos_tpl), radius=SNAKE_SIZE)


def game_action(key: pygame.key):
    global head_pos_x
    global head_pos_y
    global snake_dir
    global snake_pos_lst
    global is_space
    global game_speed
    global score
    tail = snake_pos_lst[0]

    if (key == pygame.K_DOWN) and (snake_dir != 'up'):
        snake_dir = 'down'
    elif (key == pygame.K_UP) and (snake_dir != 'down'):
        snake_dir = 'up'
    if (key == pygame.K_RIGHT) and (snake_dir != 'left'):
        snake_dir = 'right'
    elif (key == pygame.K_LEFT) and (snake_dir != 'right'):
        snake_dir = 'left'
    elif key == pygame.K_s:
        is_space ^= 1
    elif key == pygame.K_n:
        init_game()
    elif key == pygame.K_p:
        snake_dir = ''

    if snake_dir == 'down':
        head_pos_y += STEP_LENGTH
    if snake_dir == 'up':
        head_pos_y -= STEP_LENGTH
    if snake_dir == 'right':
        head_pos_x += STEP_LENGTH
    if snake_dir == 'left':
        head_pos_x -= STEP_LENGTH

    # check if the head hit part of the body or hit the screen edges
    for (pox, poy) in snake_pos_lst:
        if (pox == head_pos_x) and (poy == head_pos_y):
            continue

        if (((pox == head_pos_x) and (poy == head_pos_y)) or
            ((pox >= SCREEN_WIDTH) or (pox <= 0) or (poy >= SCREEN_HEIGHT) or (poy <= 0))):
            finish_game()
            return

    snake_pos_lst.append((head_pos_x, head_pos_y))
    if is_space:
        tail = snake_pos_lst.pop(0)

    if (abs(head_pos_x - pos_food_x) <= SNAKE_SIZE) and (abs(head_pos_y - pos_food_y) <= SNAKE_SIZE):
        print(f'Head: ({head_pos_x}, {head_pos_y})\n')
        draw_food(True)
        snake_pos_lst.insert(0, tail)
        game_speed += 2
        score += 1


def play_game():
    global game_over
    global game_screen
    global head_pos_x
    global head_pos_y
    global game_speed
    draw_food(True)
    key = None

    while not game_over:
        game_screen.fill(SCREEN_COLOR)
        game_action(key)
        draw_snake()
        draw_food()
        draw_score()
        pygame.display.update()
        pygame.time.Clock().tick(game_speed)

        key = None
        for game_event in pygame.event.get():
            if game_event.type == KEYBOARD_PRESSED:
                if game_event.key == pygame.K_ESCAPE:
                    finish_game()
                else:
                    key = game_event.key
            elif game_event.type == pygame.QUIT:
                finish_game()


if __name__ == '__main__':
    try:
        init_game()
        play_game()
    except Exception as e:
        msg = tkinter.Tk()
        msg.title('Snake Cather )-;')
        msg.geometry('300x1')
        tkinter.messagebox.showwarning('Snake Cather )-;', f'Unfortunately, the game has closed ({e})', parent=msg)
