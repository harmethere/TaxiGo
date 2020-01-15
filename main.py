import pygame
import random

pygame.init()


# load files

car_img = pygame.image.load('pics/taxicar2.png')
uber_img = pygame.image.load('pics/ubercar2.png')
bg = pygame.image.load("pics/bg.png")
bg2 = pygame.image.load("pics/bg2.png")
crash_sound = pygame.mixer.Sound("sound/crash3.wav")
pygame.mixer.music.load('sound/jazz.wav')


# define constants

display_width = 800
display_height = 600

black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
green = (0, 200, 0)
blue = (0, 0, 200)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)

car_wid = car_img.get_width() -15#collisionfix
car_hei = car_img.get_height() -20#collisionfix

uber_wid = uber_img.get_width() -15#collisionfix
uber_hei = uber_img.get_height() -10#collisionfix

road_lanes = [195, 300, 420, 527]


# prepare board

screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Taxi vs Uber 2')
clock = pygame.time.Clock()

pause = False


# functions

def things_defeated(count):
    font = pygame.font.SysFont("comicsansms", 25)
    text = font.render("Defeated: " + str(count), True, white)
    screen.blit(text, (0, 0))


def text_objects(text, font):
    text_surface = font.render(text, True, white)
    return text_surface, text_surface.get_rect()


def crash():
    pygame.mixer.Sound.play(crash_sound)
    pygame.mixer.music.stop()

    large_text = pygame.font.SysFont("comicsansms", 115)
    text_surf, text_rect = text_objects("You Crashed", large_text)
    text_rect.center = ((display_width / 2), (display_height / 2))
    screen.blit(text_surf, text_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        button("Play Again", 150, 450, 100, 50, green, bright_green, game_loop)
        button("Quit", 550, 450, 100, 50, red, bright_red, quit_game)

        pygame.display.update()
        clock.tick(15)


def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))
    small_text = pygame.font.SysFont("comicsansms", 20)
    text_surf, text_rect = text_objects(msg, small_text)
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(text_surf, text_rect)


def quit_game():
    pygame.quit()
    quit()


def unpause():
    global pause
    pygame.mixer.music.unpause()
    pause = False


def paused():
    pygame.mixer.music.pause()

    large_text = pygame.font.SysFont("comicsansms", 115)
    text_surf, text_rect = text_objects("Paused", large_text)
    text_rect.center = ((display_width / 2), (display_height / 2))
    screen.blit(text_surf, text_rect)

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        button("Continue", 150, 450, 100, 50, green, bright_green, unpause)
        button("Exit", 550, 450, 100, 50, red, bright_red, quit_game)

        pygame.display.update()
        clock.tick(15)


def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        screen.blit(bg, (0, 0))
        large_text = pygame.font.SysFont("comicsansms", 115)
        text_surf, text_rect = text_objects("Taxi vs Uber 2", large_text)
        text_rect.center = ((display_width / 2), (display_height / 2))
        screen.blit(text_surf, text_rect)

        button("Go!", 150, 450, 100, 50, green, bright_green, game_loop)
        button("Exit", 550, 450, 100, 50, red, bright_red, quit_game)

        pygame.display.update()
        clock.tick(15)


def game_loop():
    global pause

    pygame.mixer.music.play(-1)

    # put car
    x = display_width * 0.45
    y = display_height * 0.74
    x_change = 0
    speed = 8
    defeated = 0

    # put uber & uber2
    uber_x = random.choice(road_lanes)
    uber_y = -600
    uber2_x = random.choice(road_lanes)
    uber2_y = -1000
    uber_speed = 2

    # put background
    bg_y = 0
    bg2_y = -bg.get_height()

    while 1:

        # events control
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -10
                if event.key == pygame.K_RIGHT:
                    x_change = 10
                if event.key == pygame.K_p:
                    pause = True
                    paused()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0


        # move background

        bg_y += speed
        bg2_y += speed

        if bg_y > bg.get_height():
            bg_y = -bg.get_height()

        if bg2_y > bg.get_height():
            bg2_y = -bg.get_height()

        screen.blit(bg, (0, bg_y))
        screen.blit(bg2, (0, bg2_y))


        # move uber & uber2

        uber_y += uber_speed
        if uber_y > display_height:  # uber hidden at bottom
            uber_y = 0 - uber_hei
            uber_x = random.choice(road_lanes)
            defeated += 1
            uber_speed += 0.5
            speed += 0.8

        screen.blit(uber_img, [uber_x, uber_y, uber_wid, uber_hei])
        #pygame.draw.rect(screen, red, [uber_x, uber_y, uber_wid, uber_hei], 1)

        uber2_y += uber_speed
        if uber2_y > display_height:  # uber2 hidden at bottom
            uber2_y = random.choice([0 - uber_hei, 0 - uber_hei*2 - display_height])
            uber2_x = random.choice(road_lanes)
            defeated += 1

        screen.blit(uber_img, [uber2_x, uber2_y, uber_wid, uber_hei])
        #pygame.draw.rect(screen, blue, [uber2_x, uber2_y, uber_wid, uber_hei], 1)


        # move car

        x += x_change
        # can't cross the barriers
        x = min(x, display_width - 202)
        x = max(x, 125)

        screen.blit(car_img, (x, y))
        #pygame.draw.rect(screen, green, [x, y, car_wid, car_hei], 1)


        # crash with uber
        if y < uber_y+uber_hei and y+car_hei > uber_y:
            if x > uber_x and x < uber_x+uber_wid or x+car_wid > uber_x and x+car_wid < uber_x+uber_wid:
                crash()

        # crash with uber2
        if y < uber2_y+uber_hei and y+car_hei > uber2_y:
            if x > uber2_x and x < uber2_x+uber_wid or x+car_wid > uber2_x and x+car_wid < uber2_x+uber_wid:
                crash()


        things_defeated(defeated)
        pygame.display.update()
        clock.tick(100)


# main

game_intro()
game_loop()
quit_game()