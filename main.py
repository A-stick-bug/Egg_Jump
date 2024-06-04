"""Dino Game in Python

A game similar to the famous Chrome Dino Game, built using pygame.
Made by intern: @bassemfarid, no one or nothing else.

Each egg is consisted of the following information:
(rect, type, destroyed, visible)
"""

import sys
import pygame
import time
from random import randint


def dev_grid():
    """
    Create coordinate grid for easy drawing and check frame rate
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
        if fps < 55:
            print("LOW FPS WARNING", file=sys.stderr)


def display_scores(scores):
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


def display_playing_menu(hp, shield):
    """Displays the menu about the current running game such as HP, shield, and power ups"""
    x, y = 20, 20
    scaling = 2
    width, height = 100, 40
    border_size = 2

    width *= scaling

    # draw hp bar and create black border
    bar_size = width - (100 * scaling - scaling * hp)
    pygame.draw.rect(screen, "green", (x, y, bar_size, height))
    pygame.draw.rect(screen, "black", (x, y, width, height), border_size)

    # write hp as text
    font = pygame.font.SysFont('Comic sans', 19, bold=True)
    hp_text = font.render(f"{hp}/100", True, "black")
    text_rect = hp_text.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(hp_text, text_rect)

    if shield > 0:  # draw shield bar to the left of HP bar
        x += width
        width, height = 25, 40

        width -= border_size  # adjust borders
        width *= scaling

        # draw shield bar and create black border
        bar_size = width - (25 * scaling - scaling * shield)
        pygame.draw.rect(screen, "#8FFFF2", (x, y, bar_size, height))
        pygame.draw.rect(screen, "black", (x, y, width, height), border_size)

        # write shield as text
        font = pygame.font.SysFont('Comic sans', 19, bold=True)
        hp_text = font.render(f"{shield}", True, "black")
        text_rect = hp_text.get_rect(center=(x + width // 2, y + height // 2))
        screen.blit(hp_text, text_rect)


def spawn_egg(prev_loc, frame):
    """Spawn eggs based on current phase and previous egg location
    Makes sure that 2 eggs are not too close together, so it is always possible to win
    :returns egg tuple: (egg_rect: Surface, egg_type: str, is_destroyed: bool, stays_visible: bool)"""
    phase = get_phase(frame)

    # phase 1: only spawn normal eggs
    if phase == 1:
        # ensure eggs aren't too close to each other and have some variation
        left = max(MIN_EGG_DIST + prev_loc + randint(0, 150), randint(800, 1100))
        return egg_surf.get_rect(bottomleft=(left, GROUND_Y)), "normal", False, True

    # phase 2: spawn normal and fried eggs with equal probability
    elif phase == 2:
        if randint(0, 1) == 0:  # spawn normal egg
            left = max(MIN_EGG_DIST + prev_loc + randint(0, 150), randint(800, 1100))
            return egg_surf.get_rect(bottomleft=(left, GROUND_Y)), "normal", False, True
        else:  # spawn fried egg, these can be closer together
            left = max(MIN_EGG_DIST + prev_loc + randint(-35, 120), randint(800, 950))
            return egg_surf_fried.get_rect(bottomleft=(left, GROUND_Y)), "fried", False, True

    # phase 3: spawn eggs with 30/30/20/20 chance respectively
    elif phase == 3:
        type_egg = randint(1, 10)
        if type_egg <= 3:  # spawn normal egg
            left = max(MIN_EGG_DIST + prev_loc + randint(0, 150), randint(800, 1100))
            return egg_surf.get_rect(bottomleft=(left, GROUND_Y)), "normal", False, True
        elif type_egg <= 6:  # spawn fried egg, these can be closer together
            left = max(MIN_EGG_DIST + prev_loc + randint(-35, 120), randint(800, 950))
            return egg_surf_fried.get_rect(bottomleft=(left, GROUND_Y)), "fried", False, True
        elif type_egg <= 8:  # spawn flying egg, jump or duck
            left = max(MIN_EGG_DIST + prev_loc + randint(30, 150), randint(800, 1000))
            return egg_surf_flying.get_rect(bottomleft=(left, GROUND_Y - 35)), "flying", False, True
        else:  # spawn flying egg, must duck
            left = max(MIN_EGG_DIST + prev_loc + randint(30, 150), randint(800, 1000))
            return egg_surf_flying2.get_rect(bottomleft=(left, GROUND_Y - 35)), "flying2", False, True

    # phase 4: spawn eggs with 30/30/20/20 chance respectively
    # there is a 50% chance the egg will slowly become invisible (it can still kill you)
    elif phase == 4:
        type_egg = randint(0, 3)
        visible = randint(0, 1)
        if type_egg == 0:  # spawn normal egg
            left = max(MIN_EGG_DIST + prev_loc + randint(0, 150), randint(800, 1100))
            return egg_surf.get_rect(bottomleft=(left, GROUND_Y)), "normal", False, visible
        elif type_egg == 1:  # spawn fried egg, these can be closer together
            left = max(MIN_EGG_DIST + prev_loc + randint(-35, 120), randint(800, 950))
            return egg_surf_fried.get_rect(bottomleft=(left, GROUND_Y)), "fried", False, visible
        elif type_egg == 2:  # spawn flying egg, jump or duck
            left = max(MIN_EGG_DIST + prev_loc + randint(30, 150), randint(800, 1000))
            return egg_surf_flying.get_rect(bottomleft=(left, GROUND_Y - 35)), "flying", False, visible
        else:  # spawn flying egg, must duck
            left = max(MIN_EGG_DIST + prev_loc + randint(30, 150), randint(800, 1000))
            return egg_surf_flying2.get_rect(bottomleft=(left, GROUND_Y - 35)), "flying2", False, visible
    else:
        raise NotImplementedError


def get_phase(frame):
    """Gets the current game phase based on the current frame"""
    if frame < 900:
        return 1
    elif frame < 1800:
        return 2
    elif frame < 2700:
        return 3
    else:
        return 4


def get_obstacle_speed(frame):
    """Get the speed at which obstacles move left, depending on the frame
    Fastest speed is reached in 4th phase"""
    slowest = 5.5
    fastest = 8
    if frame < 2700:
        return frame * (fastest - slowest) / 2700 + slowest
    else:
        return fastest


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
player_surf_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
player_surf_jump = pygame.image.load("graphics/player/player_jump.png").convert_alpha()
player_surf_crawl = pygame.image.load("graphics/player/player_crawl_1.png").convert_alpha()
player_surf_crawl_2 = pygame.image.load("graphics/player/player_crawl_2.png").convert_alpha()
player_rect = player_surf.get_rect(bottomleft=(25, GROUND_Y))

# Load egg/obstacle assets
egg_surf = pygame.image.load("graphics/egg/egg_normal.png").convert_alpha()  # normal egg
egg_surf_fried = pygame.image.load("graphics/egg/egg_fried.png").convert_alpha()  # fried egg
egg_surf_flying = pygame.image.load("graphics/egg/egg_flying.png").convert_alpha()  # flying egg
egg_surf_flying2 = pygame.image.load("graphics/egg/egg_flying_2.png").convert_alpha()  # big flying egg
get_surf = {"normal": egg_surf,
            "fried": egg_surf_fried,
            "flying": egg_surf_flying,
            "flying2": egg_surf_flying2}

frame = 0
screen.fill("black")
start_time = time.time()
player_hp = 100
player_shield = 25
player_state = "walking"
eggs = []
flying_timer = 0

while running:
    # Poll for events
    for event in pygame.event.get():
        # pygame.QUIT --> user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False

        # When player wants to play again by pressing SPACE
        if not is_playing and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            is_playing = True

    keys = pygame.key.get_pressed()  # check for held down keys
    if is_playing:
        # check if player is crawling, walking, or flying
        if keys[pygame.K_DOWN] and player_rect.bottom == GROUND_Y:
            player_state = "crawling"
        elif flying_timer > 0:
            player_state = "flying"
        else:
            player_state = "walking"

        # player does an action
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

        # draw score counter
        cur_score = frame // 4
        score_surf = game_font.render(f"SCORE: {cur_score}", False, "Black")
        score_rect = score_surf.get_rect(center=(400, 40))
        pygame.draw.rect(screen, "#c0e8ec", score_rect)
        pygame.draw.rect(screen, "#c0e8ec", score_rect, 10)
        screen.blit(score_surf, score_rect)

        # Move and display all eggs
        for i in reversed(range(len(eggs))):
            egg_rect, egg_type, destroyed, visible = eggs[i]
            egg_rect.x -= get_obstacle_speed(frame)
            if egg_rect.right <= 0:  # replace egg with a new one
                eggs.pop(i)
                eggs.append(spawn_egg(eggs[-1][0].right, frame))
            egg_surf_temp = get_surf[egg_type]
            if not visible:  # this type of eggs gradually turns invisible
                egg_surf_temp.set_alpha(255 * (egg_rect.x - 200) / WIDTH)
            else:
                egg_surf_temp.set_alpha(255)
            screen.blit(egg_surf_temp, egg_rect)

        # Adjust player's vertical location then blit it
        players_gravity += 1
        player_rect.y += players_gravity
        player_rect.bottom = min(GROUND_Y, player_rect.bottom)  # don't go below ground

        if player_state == "walking":
            if player_rect.bottom != GROUND_Y:  # use jump animation
                player_rect = player_surf_jump.get_rect(bottomleft=(25, player_rect.bottom))
                screen.blit(player_surf_jump, player_rect)
            else:  # on the ground, check if ducking or determine animation based on frame
                if frame % 20 < 10:
                    player_rect = player_surf_2.get_rect(bottomleft=(25, player_rect.bottom))
                    screen.blit(player_surf_2, player_rect)
                else:
                    player_rect = player_surf.get_rect(bottomleft=(25, player_rect.bottom))
                    screen.blit(player_surf, player_rect)
        elif player_state == "crawling":
            if frame % 20 < 10:  # animate based on frame
                player_rect = player_surf_crawl.get_rect(bottomleft=(15, player_rect.bottom))
                screen.blit(player_surf_crawl, player_rect)
            else:
                player_rect = player_surf_crawl_2.get_rect(bottomleft=(15, player_rect.bottom))
                screen.blit(player_surf_crawl_2, player_rect)

        # display health and shield bars
        display_playing_menu(player_hp, player_shield)

        # handle player collision
        for i in range(len(eggs)):
            egg_rect, egg_type, destroyed, visible = eggs[i]
            # no collisions or egg has already hit player once
            if not egg_rect.colliderect(player_rect) or destroyed:
                continue
            eggs[i] = (egg_rect, egg_type, True, visible)  # make sure the same egg doesn't deal damage again

            # normal egg: instant kill or break shield
            if egg_type == "normal" or egg_type == "flying" or egg_type == "flying2":
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
        player_state = "walking"
        flying_timer = 0

        # spawn phase 1 eggs
        eggs = [spawn_egg(800, frame)]
        eggs.append(spawn_egg(eggs[-1][0].right, frame))
        eggs.append(spawn_egg(eggs[-1][0].right, frame))
        eggs.append(spawn_egg(eggs[-1][0].right, frame))

        # load menu
        display_scores(scores)

    if DEVELOPER_MODE:  # DEBUG FEATURES
        dev_grid()

    # flip() the display to put your work on screen
    pygame.display.flip()
    frame += 1
    clock.tick(60)  # limits FPS to 60

pygame.quit()
