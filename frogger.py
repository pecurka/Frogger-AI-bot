import pygame
import random
import time

pygame.init()
screen_width = 350
screen_height = 400
white = (255, 255, 255)

finish = False   # Check if application is running
fps = 20  # Simulation speed, can be changed if needed
frogNum = 100  # Number of frogs in each generation, can be changed if needed

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Frogger-AI-bot')
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
backgroundImage = pygame.image.load('images/background.gif')

turtles = pygame.sprite.Group()
frogs = pygame.sprite.Group()

frog = pygame.image.load('images/frog10.gif')
frogDead = pygame.image.load('images/frog11.png')

yellowCar = pygame.image.load('images/yellowCar.gif')  # row 2
dozer = pygame.image.load('images/dozer.gif')  # row 3
purpleCar = pygame.image.load('images/purpleCar.gif')  # row 4
greenCar = pygame.image.load('images/greenCar.gif')  # row 5
truck = pygame.image.load('images/truck.gif')  # row 6

logShort = pygame.image.load('images/logShort.gif')
logMedium = pygame.image.load('images/logMedium.gif')
logLong = pygame.image.load('images/logLong.gif')

twoTurtles = pygame.image.load('images/turtletwo.gif')
twoTurtlesDive = pygame.image.load('images/turtletwodown.gif')
threeTurtles = pygame.image.load('images/turtlethree.gif')
threeTurtlesDive = pygame.image.load('images/turtlethreedown.gif')

turtleCounter = 0  # Timer for turtle state

class Turtle(pygame.sprite.Sprite):
    def __init__(self, canDive, size, startX, startY, width, height, speed):
        pygame.sprite.Sprite.__init__(self)
        self.canDive = canDive  # 1 - does not dive, 2 - dives
        self.size = size
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.x = startX
        self.rect.y = startY
        self.width = width
        self.height = height
        self.speed = speed
        self.state = 0  # 0 - not diving, 1 - diving

        if (self.size == 2):
            self.image = twoTurtles
        elif (self.size == 3):
            self.image = threeTurtles

    # Updates location of turtle
    def update(self):
        self.rect.x += self.speed

        if (self.size == 2):
            if (self.rect.x + 50 < 0):
                self.rect.x = screen_width + 50
        elif (self.size == 3):
            if (self.rect.x + 75 < 0):
                self.rect.x = screen_width + 75

        self.collision()

    # Checks to see if frog is on turtle, if turtles have dived frog needs to die
    def collision(self):
        for f in frogs:
            if f.rect.colliderect(self) and f.dead == False:
                if self.state == 1:
                    f.die()
                else:
                    f.rect.x += self.speed

class Log(pygame.sprite.Sprite):
    def __init__(self, startX, startY, size, width, height, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.x = startX
        self.rect.y = startY
        self.size = size
        self.width = width
        self.height = height
        self.speed = speed

        if (self.size == 'short'):
            self.image = logShort
        elif (self.size == 'medium'):
            self.image = logMedium
        elif (self.size == 'long'):
            self.image = logLong

    # Updating log position
    def update(self):
        self.rect.x += self.speed

        if (self.size == 'short' or self.size == 'medium'):
            if (self.rect.x - 100 > screen_width):
                self.rect.x = -100
        else:
            if (self.rect.x - 200 > screen_width):
                self.rect.x = -200

        self.collision()

    # Checking for collision with frogs
    def collision(self):
        for f in frogs:
            if f.rect.colliderect(self) and f.dead == False:
                f.rect.x += self.speed

# Car Object
class Car(pygame.sprite.Sprite):
    def __init__(self, startX, startY, img, speed, direction, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.x = startX
        self.rect.y = startY
        self.img = img
        self.speed = speed
        self.direction = direction  # -1 - left, 1 - right
        self.width = width
        self.height = height

        if (self.img == 'yellow'):
            self.image = yellowCar
        elif (self.img == 'green'):
            self.image = greenCar
        elif (self.img == 'truck'):
            self.image = truck
        elif (self.img == 'dozer'):
            self.image = dozer
        elif (self.img == 'purple'):
            self.image = purpleCar

    # Update car position
    def update(self):
        if (self.direction == -1):
            self.rect.x += self.speed
        elif (self.direction == 1):
            self.rect.x -= self.speed

        if (self.direction == -1 and self.rect.x - 75 > screen_width):
            self.rect.x = -75
        elif (self.direction == 1 and self.rect.x + 75 < 0):
            self.rect.x = screen_width + 75
        self.collision()

    # Checks car collision with frogs
    def collision(self):
        for f in frogs:
            if (self.rect.colliderect(f) and f.dead == False):
                f.die()

# Sets and resets the game screen
def set():
    for t in turtles:
        t.kill()
    for a in all_sprites:
        a.kill()

    turtleCounter = 0

    # Creation of objects
    # (canDive, size, startX, startY, width, height, speed)
    for i in range(0, 8):
        if i < 4:
            if i % 2 == 0: #every second turtle should be able to dive
                turtles.add(Turtle(2, 3, 100 * (4 - i), 175, 75, 25, -2))
            else:
                turtles.add(Turtle(1, 3, 100 * (4 - i), 175, 75, 25, -2))
        else:
            if i % 2 == 0:
                turtles.add(Turtle(2, 2, 87.5 * (8 - i), 100, 50, 25, -2))
            else:
                turtles.add(Turtle(1, 2, 87.5 * (8 - i), 100, 50, 25, -2))
    # (x, y, img, speed, direction, width, height)
    for i in range(0, 9):
        if i < 3:
            all_sprites.add(Log(-100 + 150 * (3 - i), 150, 'short', 62.5, 25, 3))
        elif i < 6:
            all_sprites.add(Log(-150 + 200 * (6 - i), 125, 'long', 150, 25, 4))
        else:
            all_sprites.add(Log(-200 + 150 * (9 - i), 75, 'medium', 87.5, 25, 6))
    for i in range(0, 12):
        if i < 3:
            all_sprites.add(Car(100 + 75 * (3 - i), 325, 'yellow', 6, 1, 25, 25))
        elif i < 6:
            all_sprites.add(Car(-150 + 75 * (6 - i), 300, 'dozer', 2, -1, 25, 25))
        elif i < 9:
            all_sprites.add(Car(50 + 75 * (9 - i), 275, 'purple', 4, 1, 25, 25))
        elif i < 10:
            all_sprites.add(Car(25 + 75 * (10 - i), 250, 'green', 10, -1, 25, 25))
        else:
            all_sprites.add(Car(50 + 150 * (12 - i), 225, 'truck', 3, 1, 50, 25))

set()

# The main game loop
while not finish:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True

    screen.blit(backgroundImage, (0, 0))

    all_sprites.update()
    all_sprites.draw(screen)
    turtles.update()
    turtles.draw(screen)
    frogs.update()
    frogs.draw(screen)

    pygame.display.update()
    clock.tick(fps)

    # Handling diving of turtles
    turtleCounter += 1
    if turtleCounter == 50:
        turtleCounter = 0
        for t in turtles:
            if t.canDive == 2:
                if t.state == 0:
                    t.state = 1
                    if t.size == 2:
                        t.image = twoTurtlesDive
                    else:
                        t.image = threeTurtlesDive
                else:
                    t.state = 0
                    if t.size == 2:
                        t.image = twoTurtles
                    else:
                        t.image = threeTurtles

pygame.quit()
quit()
