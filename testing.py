# import pygame
# import sys
# from random import randint
#
# pygame.init()
# WIDTH = 800
# HEIGHT = 400
# surface = pygame.display.set_mode((WIDTH, HEIGHT))
# surface.fill((255, 255, 255))
# clock = pygame.time.Clock()
#
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#
#     obstacle = pygame.Rect(randint(0, WIDTH),
#                            randint(0, 100),
#                            1,
#                            randint(0, HEIGHT))
#     # make a surface that will contain the line
#     pygame.draw.rect(surface, "blue", obstacle)
#
#     pygame.display.update()
#     clock.tick(60)
