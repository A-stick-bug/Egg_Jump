"""Dino Game in Python

A game similar to the famous Chrome Dino Game, built using pygame.
Made by intern: @bassemfarid, no one or nothing else.

Each egg is consisted of the following information:
(rect, type, destroyed, visible)
"""

import pygame
import time
from random import randint


def dev_grid():
    """
    --PLEASE REMOVE BEFORE SUBMITTING--
    Pygame debugger (by Ivan Li)
    - todo: Right click to get mouse coordinates
    """
    # 1. Draw grid
    grid_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for i in range(0, WIDTH, 100):  # big vertical lines
        line = pygame.Rect(i, 0, 2, HEIGHT)
        pygame.draw.rect(grid_surface, "red", line)
    for i in range(0, HEIGHT, 100):  # big horizontal lines
        line = pygame.Rect(0, i, WIDTH, 2)
        pygame.draw.rect(grid_surface, "red", line)
    for i in range(0, WIDTH, 20):  # small vertical lines
        line = pygame.Rect(i, 0, 1, HEIGHT)
        pygame.draw.rect(grid_surface, "grey", line)
    for i in range(0, HEIGHT, 20):  # small horizontal lines
        line = pygame.Rect(0, i, WIDTH, 1)
        pygame.draw.rect(grid_surface, "grey", line)
    screen.blit(grid_surface, (0, 0))  # display grid line on main screen

    # 2: Check FPS every 5 seconds
    if frame % 300 == 0 and is_playing:
        t = time.time() - start_time
        fps = round(frame / t, 2)
        print(f"Frame: {frame}, Time: {round(t, 2)} , FPS: {fps}")  # ensure 60 fps

    # # 3: Mouse position debug (with right click)
    # for event in pygame.event.get():
    #     if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
    #         print(f"MOUSE POSITION: {event.pos}")


def display_scores():
    """Displays the top 10 scores on the game menu"""
    x_pos = 620  # top-left corner of scores display
    y_pos = 20
    spacing = 32

    # display leaderboard title
    font = pygame.font.SysFont('Comic sans', 24, bold=True)
    title_text = font.render("Top 10 Scores", True, "white")
    screen.blit(title_text, (x_pos, y_pos))

    # display top 10 scores
    font = pygame.font.SysFont('Comic sans', 24)
    for index, score in enumerate(scores):
        y_pos += spacing  # space out scores evenly
        score_text = font.render(f"{index + 1}. {score}", True, "white")
        screen.blit(score_text, (x_pos, y_pos))


def display_playing_menu():
    """Displays the menu about the current running game such as HP, shield, and power ups"""


def spawn_egg(prev_loc):
    """Spawn eggs based on current phase and previous egg location"""
    phase = get_phase()
    if phase == 1:  # phase 1: only spawn normal eggs
        # ensure eggs aren't too close to each other and have some variation
        left = max(MIN_EGG_DIST + prev_loc + randint(0, 150), randint(800, 1100))
        return egg_surf.get_rect(bottomleft=(left, GROUND_Y)), "normal", False, True

    elif phase == 2:  # phase 2: spawn normal and fried eggs with equal probability
        if randint(0, 1) == 0:  # spawn normal egg
            left = max(MIN_EGG_DIST + prev_loc + randint(0, 150), randint(800, 1100))
            return egg_surf.get_rect(bottomleft=(left, GROUND_Y)), "normal", False, True
        else:  # spawn fried egg, these can be closer together
            left = max(MIN_EGG_DIST + prev_loc + randint(-80, 120), randint(800, 950))
            return egg_surf_fried.get_rect(bottomleft=(left, GROUND_Y)), "fried", False, True

    else:
        raise NotImplementedError


def get_phase():
    """Gets the current game phase based on the current frame"""
    if frame < 900:
        return 2
    elif frame < 1800:
        return 2
    elif frame < 2700:
        return 3
    else:
        return 4


def get_obstacle_speed():
    """get the speed at which obstacles move left, depending on the phase"""
    phase = get_phase()
    if phase == 1:
        return 5
    elif phase == 2:
        return 6
    elif phase == 3:
        return 7
    else:
        return 8


DEVELOPER_MODE = True

# Initialize Pygame and create a window
pygame.init()
WIDTH = 800
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True  # Pygame main loop, kills the pygame when False

# Egg constants
MIN_EGG_DIST = 120  # minimum distance between eggs

# Game state variables
is_playing = False  # Whether the game is currently being played
GROUND_Y = 300  # The Y-coordinate of the ground level
JUMP_GRAVITY_START_SPEED = -17  # The speed at which the player jumps
players_gravity = 0  # The current speed at which the player falls

# Load level assets
sky_surf = pygame.image.load("graphics/level/sky.png").convert()
ground_surf = pygame.image.load("graphics/level/ground.png").convert()
game_font = pygame.font.Font("font/Pixeltype.ttf", 50)

# Load player assets
player_surf = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_surf2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
player_surf_jump = pygame.image.load("graphics/player/player_jump.png").convert_alpha()
player_rect = player_surf.get_rect(bottomleft=(25, GROUND_Y))

# Load egg/obstacle assets
egg_surf = pygame.image.load("graphics/egg/egg_normal.png").convert_alpha()  # normal egg
egg_surf_fried = pygame.image.load("graphics/egg/egg_fried.png").convert_alpha()  # fried egg
get_surf = {"normal": egg_surf, "fried": egg_surf_fried}

frame = 0

while running:
    # Poll for events
    for event in pygame.event.get():
        # pygame.QUIT --> user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False

        # When player wants to play again by pressing SPACE
        if not is_playing and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            is_playing = True
            # spawn phase 1 eggs
            eggs = [spawn_egg(800)]
            eggs.append(spawn_egg(eggs[-1][0].right))
            eggs.append(spawn_egg(eggs[-1][0].right))
            eggs.append(spawn_egg(eggs[-1][0].right))

    keys = pygame.key.get_pressed()  # check for held down keys
    if is_playing:
        # When player wants to jump/duck
        if ((keys[pygame.K_SPACE] or keys[pygame.K_UP])  # jump
                and player_rect.bottom >= GROUND_Y):
            players_gravity = JUMP_GRAVITY_START_SPEED
        elif keys[pygame.K_DOWN] and player_rect.bottom < GROUND_Y:  # drop down from the air
            players_gravity = max(players_gravity, 10)

    if is_playing:
        screen.fill("purple")  # Wipe the screen

        # Blit the level assets
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, GROUND_Y))

        cur_score = frame // 4
        score_surf = game_font.render(f"SCORE: {cur_score}", False, "Black")
        score_rect = score_surf.get_rect(center=(400, 40))
        pygame.draw.rect(screen, "#c0e8ec", score_rect)
        pygame.draw.rect(screen, "#c0e8ec", score_rect, 10)
        screen.blit(score_surf, score_rect)

        # Move and display all eggs
        for i in reversed(range(len(eggs))):
            egg_rect, egg_type, destroyed, visible = eggs[i]
            egg_rect.x -= get_obstacle_speed()
            if egg_rect.right <= 0:  # replace egg with a new one
                eggs.pop(i)
                eggs.append(spawn_egg(eggs[-1][0].right))
            screen.blit(get_surf[egg_type], egg_rect)

        # Adjust player's vertical location then blit it
        players_gravity += 1
        player_rect.y += players_gravity
        player_rect.bottom = min(GROUND_Y, player_rect.bottom)  # don't go below ground

        if player_rect.bottom != GROUND_Y:  # use jump animation
            player_rect = player_surf_jump.get_rect(bottomleft=(25, player_rect.bottom))
            screen.blit(player_surf_jump, player_rect)
        else:  # on the ground, check if ducking or determine animation based on frame
            if frame % 20 < 10:
                player_rect = player_surf2.get_rect(bottomleft=(25, player_rect.bottom))
                screen.blit(player_surf2, player_rect)
            else:
                player_rect = player_surf.get_rect(bottomleft=(25, player_rect.bottom))
                screen.blit(player_surf, player_rect)

        print(player_hp, player_shield)
        # handle player collision
        for i in range(len(eggs)):
            egg_rect, egg_type, destroyed, visible = eggs[i]
            # no collisions or egg has already hit player once
            if not egg_rect.colliderect(player_rect) or destroyed:
                continue
            eggs[i] = (egg_rect, egg_type, True, visible)  # make sure the same egg doesn't deal damage again

            # normal egg: instant kill or break shield
            if egg_type == "normal":
                print("COLLIDE")
                if player_shield > 0:
                    player_shield = 0
                else:
                    player_hp = 0
            # fried egg: take 20 damage
            elif egg_type == "fried":
                if player_shield > 0:
                    player_shield = max(0, player_shield - 20)
                else:
                    player_hp -= 20

            if player_hp <= 0:  # lost game
                is_playing = False

        # display health and shield bars


    # When game is over, save score and display menu
    else:
        with open("leaderboard.txt", "r") as leaderboard:  # save score to leaderboard
            scores = [0] * 10
            scores.extend([int(x) for x in leaderboard.readlines()])  # read top 10 scores
            scores.append(frame // 4)  # add current score
            scores.sort(reverse=True)  # sort scores high to low
            while len(scores) > 10:
                scores.pop()  # remove smallest score
        with open("leaderboard.txt", "w") as leaderboard:  # save score
            leaderboard.write("\n".join(map(str, scores)))  # store as string

        # reset game
        screen.fill("black")
        start_time = time.time()
        frame = 0  # reset score counter
        player_hp = 100
        player_shield = 25

        # load menu
        display_scores()

    if DEVELOPER_MODE:  # DEBUG FEATURES
        dev_grid()

    # flip() the display to put your work on screen
    pygame.display.flip()
    frame += 1
    clock.tick(60)  # limits FPS to 60

pygame.quit()
