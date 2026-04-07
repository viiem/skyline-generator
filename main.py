import pygame
from PIL import Image, ImageDraw
import random
import os
from datetime import datetime

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Procedural Skyline Generator")


def random_color(alpha=255):
    return (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        alpha
    )

#random taivaan väri
def generate_sky():
    img = Image.new("RGBA", (SCREEN_WIDTH, SCREEN_HEIGHT), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    sky_color = random_color()
    sky_height = SCREEN_HEIGHT // 2
    draw.rectangle((0, 0, SCREEN_WIDTH, sky_height), fill=sky_color)
    return img, sky_color

#random maan väri
def generate_land():
    img = Image.new("RGBA",(SCREEN_WIDTH, SCREEN_HEIGHT),(0,0,0,0))
    draw = ImageDraw.Draw(img)

    draw.rectangle((0, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT),
                   fill = random_color())
    return img

#randomilla joko vuoret, puut, rakennukset tai meri
def generate_object():
    img = Image.new("RGBA", (SCREEN_WIDTH, SCREEN_HEIGHT), (0,0,0,0))
    draw = ImageDraw.Draw(img)

    choice = random.choice(["mountains", "city", "forest", "hills"])
    sea_or_no = random.choice(["sea", "no_sea"]) #näin kunnes keksin merelle jotain muutakin grafiikkaa
    horizon = SCREEN_HEIGHT//2
    if sea_or_no == "sea":
        sea_color = random_color()
        sea_height = random.randint(10, 200)
        draw.rectangle(
            (0, horizon, SCREEN_WIDTH, horizon + sea_height),
            fill=sea_color
        )

    if choice == "mountains":
        for _ in range (random.randint(5,100)):
            peak_x = random.randint(0, SCREEN_WIDTH)
            peak_y = random.randint(horizon - 150, horizon - 50)

            draw.polygon([
                (peak_x - 100, horizon),
                (peak_x, peak_y),
                (peak_x + 100, horizon)
            ], fill = random_color())
        
    elif choice == "city":
        for _ in range(random.randint(10,100)):
            x = random.randint(0, SCREEN_WIDTH)
            height = random.randint(50,120)

            draw.rectangle(
                (x, horizon - height, x+40, horizon),
                fill = random_color()
            )

    elif choice == "forest":
        #luodaan värit ennen loopia että kaikki saa saman värin
        #todo: erilaisia puita
        leaf_color = random_color()
        trunk_color = random_color()

        for _ in range(random.randint(30,150)):
            x = random.randint(0, SCREEN_WIDTH)
            tree_height = random.randint(40,100)
            #puunrungot
            draw.rectangle(
                (x - 2, horizon - tree_height, x+2, horizon),
                fill = trunk_color
            )
            #puunlatvat
            draw.polygon([
                (x-10, horizon - tree_height + 10),
                (x+10, horizon - tree_height + 10), 
                (x, horizon - tree_height-20)
            ], fill= leaf_color
            )

    elif choice == "hills":
        hill_color = random_color()
        hill_type = random.choice(["big", "small"])

        for _ in range(random.randint(30, 150)):

            if hill_type == "big":
                hill_size = random.randint(100, 400)
            else:
                hill_size = random.randint(10, 100)

            x = random.randint(-50, SCREEN_WIDTH - hill_size//4)
            y = horizon - hill_size // 2

            draw.pieslice(
                (x, y, x + hill_size, y + hill_size),
                start=180,
                end=0,
                fill=hill_color
            )
    return img

#random määrä tähtiä, +kuu, tai ei mitään
def generate_stars(sky_color):
    img = Image.new("RGBA", (SCREEN_WIDTH, SCREEN_HEIGHT), (0,0,0,0))
    draw = ImageDraw.Draw(img)

    shape = random.choice(["none","crescent", "full"])
    sky_height = SCREEN_HEIGHT // 2

    # tähdet
    star_color = random_color()
    for _ in range(random.randint(20,200)):
        x = random.randint(20, SCREEN_WIDTH-20)
        y = random.randint(20, sky_height-20)
        # tähden koko
        star_size = random.randint(1, 3)
        draw.ellipse(
            (x, y, x + star_size, y + star_size),
            fill=star_color
        )

    #täysikuu
    if shape == "full":
        moon_x = random.randint(100, SCREEN_WIDTH - 100)
        moon_y = random.randint(50, sky_height - 50)
        draw.ellipse(
            (moon_x, moon_y, moon_x + 40, moon_y + 40),
            fill=random_color()
        )
    #sirppi
    elif shape == "crescent":
        size = random.randint(30, 50)
        moon_x = random.randint(100, SCREEN_WIDTH - 100 - size)
        moon_y = random.randint(50, sky_height - size)

        #kuu1
        draw.ellipse([moon_x, moon_y, moon_x + size, moon_y + size], fill=random_color())

        #leikkaava kuu
        draw.ellipse([moon_x + size*0.3, moon_y, moon_x + size*1.3, moon_y + size], fill=sky_color)

    return img

#yhdistetään generoidut yhdeksi kuvaksi
def combine_layers():
    base = Image.new("RGBA", (SCREEN_WIDTH, SCREEN_HEIGHT),(0, 0, 0, 255))

    # generate_sky palauttaa tuple (img, sky_color)
    sky_img, sky_color = generate_sky()
    layers = [
        sky_img,
        generate_land(),
        generate_stars(sky_color),  # annetaan sama väri sirpiin
        generate_object()
    ]

    for layer in layers:
        base.alpha_composite(layer)

    return base
# pil-kuva pygameksi
def pil_to_pygame(img):
    mode = img.mode
    size = img.size
    data = img.tobytes()
    return pygame.image.fromstring(data, size, mode)

#render
final = combine_layers()
final.save("scene.png")

#Projektin hakemisto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_DIR = os.path.join(BASE_DIR, "generated_art")
os.makedirs(SAVE_DIR, exist_ok=True)

#ohjelma käyntiin
#ensimmäinen kuva ennen looppia
current_image=pil_to_pygame(combine_layers())

running = True
while running:
    for event in pygame.event.get():
        # lopetetaan heti jos quit
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            current_image = pil_to_pygame(combine_layers())
        # kuvan voi tallentaa itselleen S-näppäimellä
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                #pygame kuva pil-kuvaksi
                import numpy as np
                surface_array = pygame.surfarray.array3d(current_image)
                pil_img = Image.fromarray(np.transpose(surface_array, (1, 0, 2)))

                #nimi timestampilla
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = os.path.join(SAVE_DIR, f"art_{timestamp}.png")
                pil_img.save(filename)
                print(f"Kuva tallennettu: {filename} kansioon generated_art")

    screen.blit(current_image, (0, 0))
    pygame.display.flip()

pygame.quit()