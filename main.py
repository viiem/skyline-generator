import pygame
from PIL import Image, ImageDraw
import random
import os
from datetime import datetime

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800,600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Procedural Skyline Generator")

#random taivaan väri
def generate_sky():
    img = Image.new("RGB",(SCREEN_WIDTH, SCREEN_HEIGHT), (0, 0, 0));
    draw = ImageDraw.Draw(img)
    sky_height = SCREEN_HEIGHT // 2

#random maan väri
def generate_land():

#randomilla joko vuoret, puut, rakennukset tai meri
def generate_object():
    #random määrä tähtiä, kuu, tai ei mitään
def generate_stars():
    img = Image.New("RGB"(SCREEN_WIDTH, SCREEN_HEIGHT), (0,0,0))

#yhdistetään generoidut yhdeksi kuvaksi
def combine_layers():
    base = Image.new("RGBA", (SCREEN_WIDTH, SCREEN_HEIGHT),(10,15,40,255))
    stars = generate_stars()
    land = generate_land()
    obj = generate_object()

    base.alpha_composite(stars)
    base.alpha_composite(land)
    base.alpha_composite(obj)
    
    return base

final = combine_layers()
final.save("scene.png")

# pil-kuva pygameksi
def pil_to_pygame(img):
    mode = img.mode
    size = img.size
    data = img.tobytes()
    return pygame.image.fromstring(data, size, mode)


#ohjelma käyntiin
running = True
while running:
    for event in pygame.event.get():
        # lopetetaan heti jos quit
        if event.type == pygame.QUIT:
            running = False



pygame.quit()