import pygame
import time
import random
import sys

# Initializing pygame
pygame.init()

# Window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("CAR RACING")

# Loading all images
c1_img = pygame.image.load("car1.jpg")
clock = pygame.time.Clock()
grass = pygame.image.load("grass.jpg")
y_strip = pygame.image.load("y_strip.jpg")
strip = pygame.image.load("strip.jpg")
start = pygame.image.load("start.jpg")


# Function for getting all images
def background():
    screen.blit(grass, (0, 0))
    screen.blit(grass, (700, 0))
    screen.blit(y_strip, (400, 0))
    screen.blit(y_strip, (400, 100))
    screen.blit(y_strip, (400, 200))
    screen.blit(y_strip, (400, 300))
    screen.blit(y_strip, (400, 400))
    screen.blit(y_strip, (400, 500))
    screen.blit(y_strip, (400, 600))
    screen.blit(strip, (120, 0))
    screen.blit(strip, (680, 0))


# Getting the car on screen
def car(x, y):
    screen.blit(c1_img, (x, y))


x_change = 0
x = 400
y = 470
car_width = 56
op_speed = 10
obs = 0
y_change = 0
obs_x = random.randrange(200, 650)
obs_y = -750
op_width = 56
op_height = 125
car_passed = 0
score = 0
level = 0


# Function for enemy cars
def obstacle(obs_x, obs_y, obs):
    if obs == 0:
        obs_img = pygame.image.load("car2.jpg")
    elif obs == 1:
        obs_img = pygame.image.load("car3.jpg")
    elif obs == 2:
        obs_img = pygame.image.load("car4.jpg")
    elif obs == 3:
        obs_img = pygame.image.load("car5.jpg")
    elif obs == 4:
        obs_img = pygame.image.load("car6.jpg")
    elif obs == 5:
        obs_img = pygame.image.load("car7.jpg")
    screen.blit(obs_img, (obs_x, obs_y))


# message to display
font = pygame.font.SysFont("None", 150)
render = font.render("CAR CRASHED", True, (0, 0, 0))


# Function to display score
def sc(car_passed, score):
    s_font = pygame.font.SysFont(None, 35)
    passed = s_font.render("Passed:" + str(car_passed), True, (0, 0, 0))
    score = s_font.render("Score:" + str(score), True, (0, 0, 0))
    screen.blit(passed, (0, 30))
    screen.blit(score, (0, 70))


# Text on Buttons
def text(text, font):
    texts = font.render(text, True, (255, 255, 255))
    return texts, texts.get_rect()


# Game loop
def game_loop():
    global op_speed, x, car_passed, level, x_change, y_change, y, obs_y, obs_x, obs, score, font
    running = True
    while running:

        # For checking events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # QUIT event
                running = False
            if event.type == pygame.KEYDOWN:  # KEYDOWN event
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_s:  # Increase speed
                    op_speed += 2
                if event.key == pygame.K_b:  # Decrease speed
                    op_speed -= 2
            if event.type == pygame.KEYUP:  # KEYUP event
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change
        screen.fill((119, 119, 119))
        background()
        obs_y -= (op_speed / 4)
        obstacle(obs_x, obs_y, obs)
        obs_y += op_speed
        car(x, y)
        sc(car_passed, score)

        # Restricting the movement
        if x > 680 - car_width or x < 120:
            x_change = 0

        # Logic for car passing
        if obs_y > 600:
            obs_y = 0 - op_height
            obs_x = random.randrange(200, 650)
            obs = random.randrange(0, 6)
            car_passed += 1
            score = car_passed * 10

            # Level Up every 10 passed cars
            if int(car_passed) % 10 == 0:
                level += 1
                op_speed += 2
                font = pygame.font.SysFont(None, 50)
                level_text = font.render("Level " + str(level), True, (0, 0, 0))
                screen.blit(level_text, (0, 100))
                pygame.display.flip()

        # Car crash logic
        if y < obs_y + op_height:
            if x > obs_x and x < obs_x + op_width or x + car_width > obs_x and x + car_width < obs_x + op_width:
                crash()

        pygame.display.update()
        clock.tick(60)


def crash():
    # Displaying crash message
    font_crash = pygame.font.SysFont(None, 100)
    screen.blit(render, (100, 200))
    pygame.display.update()
    time.sleep(2)

    # Restart the game after a crash
    game_loop()


def intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((255, 255, 255))
        font_intro = pygame.font.SysFont(None, 100)
        text_intro = font_intro.render("CAR RACING", True, (0, 0, 0))
        screen.blit(start, (80, 540))
        screen.blit(start, (580, 540))
        screen.blit(text_intro, (180, 200))
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # Check if Start or Quit button clicked
        if 80 + 150 > mouse[0] > 80 and 540 + 50 > mouse[1] > 540:
            pygame.draw.rect(screen, (255, 0, 0), (80, 540, 150, 50))
            if click == (1, 0, 0):
                game_loop()
        if 580 + 150 > mouse[0] > 580 and 540 + 50 > mouse[1] > 540:
            pygame.draw.rect(screen, (255, 0, 0), (580, 540, 150, 50))
            if click == (1, 0, 0):
                pygame.quit()

        t = pygame.font.SysFont("arial", 30, "bold")
        texts, textr = text("START", t)
        textr.center = (80 + (150 / 2), 540 + (50 / 2))
        screen.blit(texts, textr)
        texts, textr = text("QUIT", t)
        textr.center = (580 + (150 / 2), 540 + (50 / 2))
        screen.blit(texts, textr)
        pygame.display.update()


intro()  # Calling the intro function
pygame.quit()
