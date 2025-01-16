# rules: 
# 1. Every turn, a new tile will randomly appear in an empty spot on the board 
# with a value of either 2 or 4.
# 2. Tiles slide as far as possible in the chosen direction until they are stopped 
# by either another tile or the edge of the grid.
# 3. If two tiles of the same number collide while moving, 
# they will merge into a tile with the total value of the two tiles that collided.
# 4. The resulting tile cannot merge with another tile again in the same move.
# 5. If a move causes three consecutive tiles of the same value to slide together, 
# only the two tiles farthest along the direction of motion will combine.
# 6. If all four spaces in a row or column are filled with tiles of the same value,
# a move parallel to that row/column will combine the first two and last two.

import pygame
import random

pygame.init()

window_width = 600
window_height = 600
rows = 4
cols = 4

tile_height = window_height // rows
tile_width = window_width // cols

outline_thickness = 6

font = pygame.font.SysFont("helvetica", 20)
font_color_1 = (77, 77, 77)
font_color_2 = (255, 255, 255)
tile_colors = {
    2: (255, 255, 255),
    4: (255, 255, 224),
    8: (255, 218, 153),
    16: (255, 169, 71),
    32: (255, 118, 59),
    64: (255, 91, 59),
    128: (255, 226, 79),
    256: (240, 228, 65),
    512: (240, 219, 26),
    1024: (240, 233, 17),
    2048: (237, 230, 17)
}
outline_color = (120, 119, 104)
empty_tile_color = (99, 99, 88)

screen = pygame.display.set_mode((window_width, window_height))


def drawGrid(screen):
    pygame.draw.rect(screen, outline_color, (0, 0, window_width, window_height), outline_thickness)

    for row in range(1, rows):
        y = row * tile_height
        pygame.draw.line(screen, outline_color, (0, y), (window_width, y), outline_thickness)

    for col in range(1, cols):
        x = col * tile_width
        pygame.draw.line(screen, outline_color, (x, 0), (x, window_height), outline_thickness)


def main():
    clock = pygame.time.Clock()
    pygame.display.set_caption("2048")

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((254, 255, 242))

        drawGrid(screen)
        pygame.display.flip()
        clock.tick(60)


main()