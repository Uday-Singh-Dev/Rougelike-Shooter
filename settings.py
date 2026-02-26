import pygame
from camera import *
#settings


#FPS
FPS = 80
clock = pygame.time.Clock()

#constants
SCREEN_WIDTH, SCREEN_HEIGHT =1920,1080
WORLD_WIDTH, WORLD_HEIGHT = 6000,6000
camera = Camera((SCREEN_WIDTH,SCREEN_HEIGHT),(WORLD_WIDTH,WORLD_HEIGHT))


#simple func to create the window
def window(width,height,name):
    screen = pygame.display.set_mode()
    pygame.display.set_caption(name)
    return screen
    
    


#initialise
pygame.init()
pygame.mixer.init()
#sets volume channels 
pygame.mixer.set_num_channels(32) 

#uses the window func
screen = window(SCREEN_WIDTH,SCREEN_HEIGHT,"shooter")

#set mouse to invisible and toggle when needed
pygame.mouse.set_visible(False)
