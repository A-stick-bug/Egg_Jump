"""Dino Game in Python

A game similar to the famous Chrome Dino Game, built using pygame.
Made by intern: @bassemfarid, no one or nothing else.
"""

import sys
import pygame
import time
from random import randint
import random
from collections import namedtuple
from math import ceil


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
    if frame % 300 == 0 and game_state == "playing":
        t = time.time() - start_time
        fps = round(frame / t, 2)
        print(f"Frame: {frame}, Time: {round(t, 2)} , FPS: {fps}")  # ensure 60 fps
        if fps < 55:
            print("LOW FPS WARNING", file=sys.stderr)


def add_score(scores, to_add):
    """add a score to the list of top 10 scores and keep scores sorted"""
    scores.append(to_add)
    scores.sort(reverse=True)  # sort to remove smallest score
    scores.pop()


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


def display_main_menu():
    """Display the main menu with game title, leaderboard, and character selection"""
    display_scores(scores)

    # write the game's title on the screen
    game_name = 'EGG JUMP'
    title_font = pygame.font.Font("font/MainluxLight-DOAJx.otf", 110)
    text_surface = title_font.render(game_name, True, "#FFF6F6")
    text_rect = text_surface.get_rect(center=(307, 80))
    screen.blit(text_surface, text_rect)

    # todo: display playable characters which are resized


def display_player_health(hp, shield):
    """display the current player HP and shield"""
    hp = ceil(hp)
    shield = ceil(shield)
    x, y = 20, 20
    scaling = 2.1
    width, height = 100, 40
    border_width = 2

    width *= scaling

    # draw hp bar and create black border
    bar_width = hp * scaling
    pygame.draw.rect(screen, "green", (x, y, bar_width, height))
    pygame.draw.rect(screen, "black", (x, y, width, height), border_width)

    # write hp as text
    font = pygame.font.SysFont('Comic sans', 19, bold=True)
    hp_text = font.render(f"{hp}/100", True, "black")
    text_rect = hp_text.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(hp_text, text_rect)

    if shield > 0:  # draw shield bar to the left of HP bar
        x += width
        width, height = 25, 40

        width -= border_width  # adjust borders
        width *= scaling

        # draw shield bar and create black border
        bar_width = width - (25 - shield) * scaling
        pygame.draw.rect(screen, "#8FFFF2", (x, y, bar_width, height))
        pygame.draw.rect(screen, "black", (x, y, width, height), border_width)

        # write shield as text
        font = pygame.font.SysFont('Comic sans', 19, bold=True)
        hp_text = font.render(f"{shield}", True, "black")
        text_rect = hp_text.get_rect(center=(x + width / 2, y + height / 2))
        screen.blit(hp_text, text_rect)


def display_player_power_up():
    """Displays the player's current power up and how much time
    there is remaining if you currently have one active"""
    if current_power_up == no_power_up:
        return
    x, y = 560, 20
    width, height = 140, 40
    border_width = 2

    # draw the power up icon, scale it down to fit in the bar
    icon_surf = get_power_up_surf[current_power_up.type]
    icon_surf = pygame.transform.scale(icon_surf, (height, height))
    icon_rect = icon_surf.get_rect(topleft=(x - height, y))
    screen.blit(icon_surf, icon_rect)

    # fill in the bar to represent how much time the power up has left
    max_val = get_max_power_up_val[current_power_up.type]
    power_up_color = get_power_up_color[current_power_up.type]
    bar_width = width * (current_power_up.value / max_val)
    pygame.draw.rect(screen, power_up_color, (x, y, bar_width, height))

    # draw borders
    pygame.draw.rect(screen, "black", (x, y, width, height), border_width)


def handle_egg_objects():
    """Does the following actions on each egg objects:
    1. move towards player and display it
    2. check for collision with player and change player HP if needed"""
    global player_hp, player_shield
    for i in reversed(range(len(eggs))):
        egg = eggs[i]

        # move egg
        egg.rect.x -= get_obstacle_speed(frame)
        if egg.rect.right <= 0:  # replace egg with a new one
            eggs.pop(i)
            eggs.append(get_egg(eggs[-1].rect.right, frame))
            continue

        # display egg
        egg_surf_temp = get_egg_surf[egg.type]
        if not egg.visible:  # this type of eggs gradually turns invisible
            egg_surf_temp.set_alpha(255 * (egg.rect.x - 300) / WIDTH)
        else:
            egg_surf_temp.set_alpha(255)
        screen.blit(egg_surf_temp, egg.rect)

        # handle player-egg collision
        # no collisions or egg has already hit player once
        if not egg.rect.colliderect(player_rect) or egg.destroyed:
            continue
        eggs[i] = Egg(egg.rect, egg.type, True, egg.visible)  # make sure the same egg doesn't deal damage again

        # normal egg: instant kill or break shield
        if egg.type == "normal" or egg.type == "flying" or egg.type == "flying2":
            if player_shield > 0:
                player_shield = 0
            else:
                player_hp = 0
        # fried egg: take 20 damage
        elif egg.type == "fried":
            if player_shield > 0:
                player_shield = max(0, player_shield - 20)
            else:
                player_hp -= 20


def handle_power_up_objects():
    """move power up spawns towards player and check if
    the player picked up any"""
    global current_power_up
    for i in reversed(range(len(power_ups))):
        power_up_obj = power_ups[i]
        # move power up towards player
        power_up_obj.rect.x -= get_obstacle_speed(frame)
        if power_up_obj.rect.right <= 0:  # out of map, remove it
            power_ups.pop(i)
            continue

        # display power up
        power_up_surf_temp = get_power_up_surf[power_up_obj.type]
        screen.blit(power_up_surf_temp, power_up_obj.rect)

        # check for collisions and update player's power up if needed
        if power_ups[i].rect.colliderect(player_rect):
            current_power_up = Player_power_up(power_ups[i].type, power_ups[i].value)
            power_ups.pop(i)  # don't pick up power-up twice


def handle_player_state():
    """Handle the player's current action and display it on screen,
    Shrink the character rect if player is currently small"""
    global player_rect
    if player_is_small:
        # player is flying
        if current_power_up.type == "fly":
            scaled_surf = pygame.transform.scale_by(player_surf_fly, 0.6)
            player_rect = scaled_surf.get_rect(topleft=(15, 80))
            screen.blit(scaled_surf, player_rect)
        # player is crawling
        elif keys[pygame.K_DOWN] and player_rect.bottom == GROUND_Y:
            if frame % 20 < 10:  # animate based on frame
                scaled_surf = pygame.transform.scale_by(player_surf_crawl, 0.6)
                player_rect = scaled_surf.get_rect(bottomleft=(15, player_rect.bottom))
                screen.blit(scaled_surf, player_rect)
            else:
                scaled_surf = pygame.transform.scale_by(player_surf_crawl_2, 0.6)
                player_rect = scaled_surf.get_rect(bottomleft=(15, player_rect.bottom))
                screen.blit(scaled_surf, player_rect)
        # player is walking or jumping
        else:
            if player_rect.bottom != GROUND_Y:  # use jump animation
                scaled_surf = pygame.transform.scale_by(player_surf_jump, 0.6)
                player_rect = scaled_surf.get_rect(bottomleft=(25, player_rect.bottom))
                screen.blit(scaled_surf, player_rect)
            else:  # on the ground, determine animation based on frame
                if frame % 20 < 10:
                    scaled_surf = pygame.transform.scale_by(player_surf_walk, 0.6)
                    player_rect = scaled_surf.get_rect(bottomleft=(25, player_rect.bottom))
                    screen.blit(scaled_surf, player_rect)
                else:
                    scaled_surf = pygame.transform.scale_by(player_surf_walk2, 0.6)
                    player_rect = scaled_surf.get_rect(bottomleft=(25, player_rect.bottom))
                    screen.blit(scaled_surf, player_rect)

    else:
        # player is flying
        if current_power_up.type == "fly":
            player_rect = player_surf_fly.get_rect(topleft=(15, 80))
            screen.blit(player_surf_fly, player_rect)
        # player is crawling
        elif keys[pygame.K_DOWN] and player_rect.bottom == GROUND_Y:
            if frame % 20 < 10:  # animate based on frame
                player_rect = player_surf_crawl.get_rect(bottomleft=(15, player_rect.bottom))
                screen.blit(player_surf_crawl, player_rect)
            else:
                player_rect = player_surf_crawl_2.get_rect(bottomleft=(15, player_rect.bottom))
                screen.blit(player_surf_crawl_2, player_rect)
        # player is walking or jumping
        else:
            if player_rect.bottom != GROUND_Y:  # use jump animation
                player_rect = player_surf_jump.get_rect(bottomleft=(25, player_rect.bottom))
                screen.blit(player_surf_jump, player_rect)
            else:  # on the ground, determine animation based on frame
                if frame % 20 < 10:
                    player_rect = player_surf_walk.get_rect(bottomleft=(25, player_rect.bottom))
                    screen.blit(player_surf_walk, player_rect)
                else:
                    player_rect = player_surf_walk2.get_rect(bottomleft=(25, player_rect.bottom))
                    screen.blit(player_surf_walk2, player_rect)


def get_egg(prev_loc, frame):
    """Returns an Egg object based on current phase and previous egg location
    Makes sure that 2 eggs are not too close together, so it is always possible to win"""
    phase = get_phase(frame)

    # phase 1: only spawn normal eggs
    if phase == 1:
        # ensure eggs aren't too close to each other and have some variation
        left = max(MIN_EGG_DIST + prev_loc + randint(0, 150), randint(800, 1100))
        return Egg(egg_surf.get_rect(bottomleft=(left, GROUND_Y)), "normal", False, True)

    # phase 2: spawn normal and fried eggs with equal probability
    elif phase == 2:
        if randint(0, 1) == 0:  # spawn normal egg
            left = max(MIN_EGG_DIST + prev_loc + randint(0, 150), randint(800, 1100))
            return Egg(egg_surf.get_rect(bottomleft=(left, GROUND_Y)), "normal", False, True)
        else:  # spawn fried egg, these can be closer together
            left = max(MIN_EGG_DIST + prev_loc + randint(-35, 120), randint(800, 950))
            return Egg(egg_surf_fried.get_rect(bottomleft=(left, GROUND_Y)), "fried", False, True)

    # phase 3: spawn eggs with 30/30/20/20 chance respectively
    elif phase == 3:
        type_egg = randint(1, 10)
        if type_egg <= 3:  # spawn normal egg
            left = max(MIN_EGG_DIST + prev_loc + randint(0, 150), randint(800, 1100))
            return Egg(egg_surf.get_rect(bottomleft=(left, GROUND_Y)), "normal", False, True)
        elif type_egg <= 6:  # spawn fried egg, these can be closer together
            left = max(MIN_EGG_DIST + prev_loc + randint(-35, 120), randint(800, 950))
            return Egg(egg_surf_fried.get_rect(bottomleft=(left, GROUND_Y)), "fried", False, True)
        elif type_egg <= 8:  # spawn flying egg, jump or duck
            left = max(MIN_EGG_DIST + prev_loc + randint(30, 150), randint(800, 1000))
            return Egg(egg_surf_flying.get_rect(bottomleft=(left, GROUND_Y - 35)), "flying", False, True)
        else:  # spawn flying egg, must duck
            left = max(MIN_EGG_DIST + prev_loc + randint(30, 150), randint(800, 1000))
            return Egg(egg_surf_flying2.get_rect(bottomleft=(left, GROUND_Y - 35)), "flying2", False, True)

    # phase 4: spawn eggs with 30/30/20/20 chance respectively
    # there is a 50% chance the egg will slowly become invisible (it can still kill you)
    else:
        type_egg = randint(1, 10)
        visible = randint(0, 1)
        if type_egg <= 3:  # spawn normal egg
            left = max(MIN_EGG_DIST + prev_loc + randint(0, 150), randint(800, 1100))
            return Egg(egg_surf.get_rect(bottomleft=(left, GROUND_Y)), "normal", False, visible)
        elif type_egg <= 6:  # spawn fried egg, these can be closer together
            left = max(MIN_EGG_DIST + prev_loc + randint(-55, 120), randint(800, 950))
            return Egg(egg_surf_fried.get_rect(bottomleft=(left, GROUND_Y)), "fried", False, visible)
        elif type_egg <= 8:  # spawn flying egg, jump or duck
            left = max(MIN_EGG_DIST + prev_loc + randint(30, 150), randint(800, 1000))
            return Egg(egg_surf_flying.get_rect(bottomleft=(left, GROUND_Y - 35)), "flying", False, visible)
        else:  # spawn flying egg, must duck
            left = max(MIN_EGG_DIST + prev_loc + randint(30, 150), randint(800, 1000))
            return Egg(egg_surf_flying2.get_rect(bottomleft=(left, GROUND_Y - 35)), "flying2", False, visible)


def get_power_up():
    """Spawns a power up object
    Chances: 25% each
    """
    # make sure it doesn't fully overlap with eggs
    location = 800
    for i in range(len(eggs)):
        egg_l = eggs[i].rect.left
        egg_r = eggs[i].rect.right
        if egg_l <= location <= egg_r or location <= egg_l <= location + 40:
            location = eggs[i].rect.right + 20

    # randomly decide what power up you get
    choices = ["health", "shield", "fly", "small"]
    # don't spawn power ups that are currently useless
    if player_hp > 95:
        choices.remove("health")
    if player_shield > 20:
        choices.remove("shield")
    chosen = random.choice(choices)

    # create Power_up object
    coordinates = (location, GROUND_Y)
    surf = get_power_up_surf[chosen]
    value = get_max_power_up_val[chosen]
    return Power_up(surf.get_rect(bottomleft=coordinates), chosen, value)


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


DEVELOPER_MODE = False

# Initialize Pygame and create a window
pygame.init()
WIDTH = 800
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True  # Pygame main loop, kills the pygame when False

# constants
MIN_EGG_DIST = 120  # minimum distance between eggs
GROUND_Y = 300  # The Y-coordinate of the ground level

# load scores from leaderboard
with open("leaderboard.txt", "r") as leaderboard:
    scores = [0] * 10
    for score in leaderboard.readlines():  # add top scores
        add_score(scores, int(score))

# Load level assets
sky_surf = pygame.image.load("graphics/level/sky.png").convert()
ground_surf = pygame.image.load("graphics/level/ground.png").convert()

# Load player assets
player_surf_walk = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_surf_walk2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
player_surf_jump = pygame.image.load("graphics/player/player_jump.png").convert_alpha()
player_surf_crawl = pygame.image.load("graphics/player/player_crawl_1.png").convert_alpha()
player_surf_crawl_2 = pygame.image.load("graphics/player/player_crawl_2.png").convert_alpha()
player_surf_fly = pygame.image.load("graphics/player/player_fly.png").convert_alpha()
player_rect = player_surf_walk.get_rect(bottomleft=(25, GROUND_Y))

# Load egg/obstacle assets
egg_surf = pygame.image.load("graphics/egg/egg_normal.png").convert_alpha()  # normal egg
egg_surf_fried = pygame.image.load("graphics/egg/egg_fried.png").convert_alpha()  # fried egg
egg_surf_flying = pygame.image.load("graphics/egg/egg_flying.png").convert_alpha()  # flying egg
egg_surf_flying2 = pygame.image.load("graphics/egg/egg_flying_2.png").convert_alpha()  # big flying egg
get_egg_surf = {"normal": egg_surf,
                "fried": egg_surf_fried,
                "flying": egg_surf_flying,
                "flying2": egg_surf_flying2}
Egg = namedtuple("Egg", ["rect", "type", "destroyed", "visible"])

# load power up assets
health_surf = pygame.image.load("graphics/power_ups/health.png").convert_alpha()
shield_surf = pygame.image.load("graphics/power_ups/shield.png").convert_alpha()
fly_surf = pygame.image.load("graphics/power_ups/fly.png").convert_alpha()
small_surf = pygame.image.load("graphics/power_ups/small.png").convert_alpha()
get_power_up_surf = {"health": health_surf,
                     "shield": shield_surf,
                     "fly": fly_surf,
                     "small": small_surf}
get_max_power_up_val = {"health": 100,  # heal 20 HP
                        "shield": 75,  # gain 15 shield
                        "fly": 7 * 60,  # fly for 7 seconds
                        "small": 7 * 60}  # become small for 7 seconds
get_power_up_color = {"health": "#FF0213",
                      "shield": "#5CE4FF",
                      "fly": "#FFD4FF",
                      "small": "#CCFFFF"}

# Power up objects that spawn on the map
Power_up = namedtuple("Power_up", ["rect", "type", "value"])

# Power up that the player currently has
Player_power_up = namedtuple("Player_power_up", ["type", "value"])
no_power_up = Player_power_up("", 0)

# default game state variables
game_state = "menu"  # determines the current state of the game (menu/died/playing)
jump_start_speed = -17  # The speed at which the player jumps
players_fall_speed = 0  # The current speed at which the player falls
gravity = 1  # acceleration from gravity

frame = 0  # used to keep track of score
screen.fill("black")
start_time = time.time()
player_hp = 100
player_shield = 25
player_is_small = False
eggs = []
power_ups = []
current_power_up = no_power_up

while running:
    frame_events = pygame.event.get()
    # check if user pressed X and want to exit game
    for event in frame_events:
        if event.type == pygame.QUIT:
            running = False

    if game_state == "playing":
        screen.fill("purple")  # wipe the screen
        # display the game's background
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, GROUND_Y))

        # display health and shield bars
        display_player_health(player_hp, player_shield)

        # display score counter
        cur_score = frame // 4
        game_font = pygame.font.Font("font/Pixeltype.ttf", 50)
        score_surf = game_font.render(f"SCORE: {cur_score}", False, "Black")
        score_rect = score_surf.get_rect(center=(400, 43))
        pygame.draw.rect(screen, "#c0e8ec", score_rect)
        pygame.draw.rect(screen, "#c0e8ec", score_rect, 10)
        screen.blit(score_surf, score_rect)

        # handle player actions
        keys = pygame.key.get_pressed()
        # [space] or [up_arrow] to jump, you can hold down keys
        if ((keys[pygame.K_SPACE] or keys[pygame.K_UP])
                and player_rect.bottom >= GROUND_Y):
            players_fall_speed = jump_start_speed
        # [down_arrow] to drop down from a jump or flying
        elif (any(event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN for event in frame_events)
              and player_rect.bottom < GROUND_Y):
            players_fall_speed = max(players_fall_speed, -jump_start_speed * 0.75)
            if current_power_up.type == "fly":  # stop flying
                players_fall_speed = -jump_start_speed * 0.75
                current_power_up = no_power_up

        # reset power up dependent variables
        jump_start_speed = -17
        player_is_small = False

        # handle player's current power up and update if needed
        display_player_power_up()
        if current_power_up.type == "health":
            player_hp = min(100, player_hp + 0.2)
        elif current_power_up.type == "shield":
            player_shield = min(25, player_shield + 0.2)
        elif current_power_up.type == "fly":
            if current_power_up.value == 1:  # start falling after finished flying
                player_rect.y = 80
                players_fall_speed = 0
        elif current_power_up.type == "small":
            # make player smaller (30px high) so you don't need to crawl, also jump higher
            jump_start_speed = -20
            player_is_small = True

        # reduce time remaining for power up
        if current_power_up != no_power_up:
            current_power_up = Player_power_up(current_power_up.type, current_power_up.value - 1)
            if current_power_up.value <= 0:
                current_power_up = no_power_up

        # adjust player's vertical location then blit it
        players_fall_speed += gravity
        player_rect.y += players_fall_speed
        player_rect.bottom = min(GROUND_Y, player_rect.bottom)  # don't go below ground

        # check for player actions like jumping
        handle_player_state()

        # update the states of egg objects
        handle_egg_objects()

        # spawn power-ups around every 500 frames
        if randint(0, 500) == 0:
            power_ups.append(get_power_up())
        handle_power_up_objects()

        # lost game, show death message
        # also make all eggs visible so player can see what killed them
        if player_hp <= 0:
            # make eggs visible
            for egg in eggs:
                egg_surf_temp = get_egg_surf[egg.type]
                egg_surf_temp.set_alpha(255)
                screen.blit(egg_surf_temp, egg.rect)
            # death message
            game_state = "dead"
            death_font = pygame.font.Font("font/Pixeltype.ttf", 80)
            death_message = death_font.render("You Died", True, "red")
            message_rect = death_message.get_rect(center=(WIDTH / 2, 120))
            screen.blit(death_message, message_rect)
            death_font = pygame.font.Font("font/Pixeltype.ttf", 60)
            death_message = death_font.render("Press [SPACE] to restart", True, "red")
            message_rect = death_message.get_rect(center=(WIDTH / 2, 200))
            screen.blit(death_message, message_rect)

        # update frame which is used to keep track of current score
        frame += 1

    # player just died and is in death screen, waiting to go to menu
    elif game_state == "dead":
        # player wants to enter main menu by pressing SPACE
        for event in frame_events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = "menu"

    # player is in main menu, waiting to start a game
    else:
        add_score(scores, frame // 4)  # add current score

        # reset game
        screen.fill("black")
        start_time = time.time()
        frame = 0  # reset score counter
        player_hp = 100
        player_shield = 25
        player_is_small = False
        power_ups = []
        current_power_up = no_power_up

        # spawn phase 1 eggs and space them out
        eggs = [get_egg(800, frame)]
        eggs.append(get_egg(eggs[-1].rect.right, frame))
        eggs.append(get_egg(eggs[-1].rect.right, frame))
        eggs.append(get_egg(eggs[-1].rect.right, frame))

        # load menu
        display_main_menu()

        # check if player selected a character and wants to start a new game
        for event in frame_events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = "playing"

    if DEVELOPER_MODE:  # DEBUG FEATURES
        dev_grid()

    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60

# save score as strings on each line before exiting code
with open("leaderboard.txt", "w") as leaderboard:
    add_score(scores, frame // 4)  # save player's score before they exited
    leaderboard.write("\n".join(map(str, scores)))

pygame.quit()
