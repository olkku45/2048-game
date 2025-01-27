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
import math

pygame.init()

window_width = 600
window_height = 600
rows = 4
cols = 4

tile_height = window_height // rows
tile_width = window_width // cols

outline_thickness = 6
move_vel = 80

font = pygame.font.SysFont("Raleway.ttf", 50)
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
background_color = (254, 255, 242)

screen = pygame.display.set_mode((window_width, window_height))


class Tile:


    def __init__(self, value, row, col):
        self.value = value 
        self.row = row
        self.col = col


    def draw(self, screen):
        color = tile_colors[self.value]
        pygame.draw.rect(screen, color, (self.col * tile_width, self.row * tile_height, tile_width, tile_height))

        if self.value >= 8:
            text = font.render(str(self.value), 1, font_color_2)
        else:
            text = font.render(str(self.value), 1, font_color_1)

        text_x = round(self.col * tile_width + (tile_width / 2 - text.get_width() / 2))
        text_y = round(self.row * tile_height + (tile_height / 2 - text.get_height() / 2))
        
        screen.blit(text, (text_x, text_y))


    ''' def set_pos(self, ceil=False):
        if ceil:
            self.row = math.ceil(self.y / tile_height)
            self.col = math.ceil(self.x / tile_width)
        else:
            self.row = math.floor(self.y / tile_height)
            self.col = math.floor(self.x / tile_width)'''


    '''def move(self, delta):
        self.x += delta[0]
        self.y += delta[1]'''


def draw_grid(screen):
    pygame.draw.rect(screen, outline_color, (0, 0, window_width, window_height), outline_thickness)

    for row in range(1, rows):
        y = row * tile_height
        pygame.draw.line(screen, outline_color, (0, y), (window_width, y), outline_thickness)

    for col in range(1, cols):
        x = col * tile_width
        pygame.draw.line(screen, outline_color, (x, 0), (x, window_height), outline_thickness)


def draw(screen, tiles):
    screen.fill(background_color)

    for tile in tiles.values():
        tile.draw(screen)

    draw_grid(screen)


def get_random_pos(tiles):
    row = None
    col = None
    while True:
        row = random.randrange(0, rows)
        col = random.randrange(0, cols)

        if f"{row}{col}" not in tiles:
            return row, col


def generate_tiles():
    tiles = {}

    row, col = get_random_pos(tiles)
    tiles[f"{row}{col}"] = Tile(2, row, col)

    row, col = get_random_pos(tiles)
    value = random.choices([2,4], weights=[80, 20], k=1)[0]
    tiles[f"{row}{col}"] = Tile(value, row, col)

    return tiles


def move_tiles(tiles, direction): 
        
    if direction == "left":
        dx = -1
        dy = 0
        sorted_tiles = sorted(tiles.values(), key=lambda x: x.col, reverse=False)
    
    elif direction == "right":
        dx = 1
        dy = 0
        sorted_tiles = sorted(tiles.values(), key=lambda x: x.col, reverse=True)
    
    elif direction == "up":
        dx = 0
        dy = -1
        sorted_tiles = sorted(tiles.values(), key=lambda x: x.row, reverse=False)

    elif direction == "down":
        dx = 0
        dy = 1
        sorted_tiles = sorted(tiles.values(), key=lambda x: x.row, reverse=True)

    merged = []

    for tile in sorted_tiles.copy():
        while tile.col + dx in range(4) and tile.row + dy in range(4)  and f"{tile.row + dy}{tile.col + dx}" not in tiles:
            tile.col += dx
            tile.row += dy
            update_tiles(tiles, sorted_tiles)

        next_tile_key = f"{tile.row + dy}{tile.col + dx}"
        
        if dx == 0:
            merge_value = tile.col
        else:
            merge_value = tile.row

        if next_tile_key in tiles and tiles[next_tile_key].value == tile.value and merge_value not in merged:
            print("merge")
            sorted_tiles.remove(tile)
            tiles[next_tile_key].value *= 2
            update_tiles(tiles, sorted_tiles)
            if dx == 0:
                #vertical
                merged.append(tile.col)
            else:
                merged.append(tile.row)
    
    #TODO: tämä lopettaa pelin aina kun ruudut ovat täynnä, mutta voi vielä pystyä siirtämään joskus
    if len(tiles) == 16:
        return "lost"
    else:
        row, col = get_random_pos(tiles)
        tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col)
        return "continue"
    

def update_tiles(tiles, new_tiles):
    tiles.clear()
    for tile in new_tiles:
        tiles[f"{tile.row}{tile.col}"] = tile


def main(screen):
    clock = pygame.time.Clock()
    pygame.display.set_caption("2048")

    tiles = generate_tiles()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_a:
                    move_tiles(tiles, "left")
                elif event.key == pygame.K_d:
                    move_tiles(tiles, "right")
                elif event.key == pygame.K_w:
                    move_tiles(tiles, "up")
                elif event.key == pygame.K_s:
                    move_tiles(tiles, "down")

        draw(screen, tiles)

        pygame.display.flip()
        clock.tick(60)


main(screen)