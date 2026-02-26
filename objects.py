import pygame
from settings import WORLD_WIDTH,WORLD_HEIGHT,SCREEN_WIDTH,SCREEN_HEIGHT
from assets import textures

wall_group = pygame.sprite.Group()











class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, textures, tile_size=100):
        super().__init__()
        #gets the dimensions and pos of the walls
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        #tiles are based on the width and height of the image tileset
        tiles_x = width // tile_size
        tiles_y = height // tile_size

        #does the vertical and horizontal of the texures
        for i in range(tiles_x):
            for j in range(tiles_y):
                tex = textures["wall_texture"]
                self.image.blit(tex, (i * tile_size, j * tile_size))

        self.rect = self.image.get_rect(topleft=(x, y))



wall_thickness = 1000  # Keep thickness large enough



# Top wall — cuts 1080px into the world
top_wall = Wall(
    x=0,
    y=0,  # starts at very top
    width=WORLD_WIDTH,
    height=wall_thickness,  # extends into world
    textures=textures
)
wall_group.add(top_wall)


# Bottom wall — cuts 1080px upward into the world
bottom_wall = Wall(
    x=0,
    y=WORLD_HEIGHT - wall_thickness,  # starts inside world
    width=WORLD_WIDTH,
    height=wall_thickness,  # extends downward
    textures=textures
)
wall_group.add(bottom_wall)



# Left wall — flush on the left
left_wall = Wall(
    x=0,
    y=0,
    width=wall_thickness,
    height=WORLD_HEIGHT,
    textures=textures
)
wall_group.add(left_wall)

# Right wall — flush on the right
right_wall = Wall(
    x=WORLD_WIDTH - wall_thickness,
    y=0,
    width=wall_thickness,
    height=WORLD_HEIGHT,
    textures=textures
)
wall_group.add(right_wall)


#this is the texture of the floor blit its like a pattern based on the width and height of the scaled image
texture_width,texture_height = 100,100
floor_surface = pygame.Surface((SCREEN_WIDTH + texture_width, SCREEN_HEIGHT + texture_height))
for x in range(0, floor_surface.get_width(), texture_width):
    for y in range(0, floor_surface.get_height(), texture_height):
        floor_surface.blit(textures["floor_texture"], (x, y))





