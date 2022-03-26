############################
###      Game    ###########
###########################

#[game]
import pygame
import pygame.locals

pygame.init()
pygame.mixer.init()
pygame.font.init()

#[utils]
import os
import time
import random

############################
#####   REOUSRCES    #######
############################

#[GAME]
FPS = 30

UP_DIRECTION = -1
DOWN_DIRECTION = 1

SPEED = 15
ALIEN_SPEED = 10
BULLET_SPEED = 20 #25

MAX_BULLETS_ON_SCREEN = 2

ALIEN_CHANCE = 1-.7  #probabilty alien will appear
SHOOT_CHANCE =  1 - .071#probabilty alien will shoot

#time taken to make an impression to the user in seonds
IMPRESSION_TIME = 100 / 1000  

#[WINDOW]
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

WINDOW_MARGIN = 50
WINDOW_PADDING = 10
DASHBOARD_HEIGHT = 50

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Shooter")
pygame.display.set_icon(pygame.image.load("./assets/sprites/UFO.jpg"))

#[COLORS]
def getColor(hexValue) -> tuple:
    "Must be in the form: #AAAAAA"
    hexValue = hexValue[1:]
    assert(len(hexValue) == 6)
    return (int(hexValue[:2], 16),
            int(hexValue[2:4], 16),
            int(hexValue[4:], 16)
            )

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

BORDER_COLOR = getColor("#A390FF")
BACKGROUND_COLOR = getColor("#FFFFFF")

RED = getColor("#FF0000")
REDDISH_YELLOW = getColor("#FF8700")
YELLOW = getColor("#FFFF00")
YELLOWISH_GREEN = getColor("#87FF00")
GREEN = getColor("#00FF00")




#[IMAGES]

def rotate(image, angle) -> pygame.Surface:
    image = pygame.transform.rotate(image, angle)
    return image

def scale(image, newSize) -> pygame.Surface:
    #newWidth, newHeight = size
    image = pygame.transform.scale(image, newSize)
    return image

BULLET = rotate(pygame.image.load("./assets/sprites/shot.gif"),180).convert()
BULLET_TANK = scale(pygame.image.load("./assets/sprites/shot.gif"),(10, 20)).convert()
              
BACKGROUND = scale(pygame.image.load(os.path.join(".", "assets", "sprites", "battle.jpg")),
                (WINDOW_WIDTH, WINDOW_HEIGHT)).convert()
TANK  = pygame.image.load("./assets/sprites/player1.gif").convert()
ALIEN_SHIP = pygame.image.load("./assets/sprites/ship_11_animated.gif").convert()
EXPLOSION = pygame.image.load("./assets/sprites/explosion1.gif").convert()

#[SOUNDS]

EXPLODE = pygame.mixer.Sound('./assets/sounds/EXPLOSION Bang 04.wav')
SHOOT = pygame.mixer.Sound('./assets/sounds/WEAPON GUNSHOT Rifle Swish 02.ogg')
SHOOT_2 = pygame.mixer.Sound('./assets/sounds/TECH WEAPON Gun Shot Phaser Down 02.ogg')


#music

pygame.mixer.music.load('./assets/sounds/Tropic Fuse - French Fuse.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(.7)


"🧨🎯🔋✅✔🟢🟢🟠🟠🟡🟡"

print("✔🕙 All resources loaded...")
