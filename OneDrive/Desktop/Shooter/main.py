import pygame
import math
import random
from pygame import mixer

# Initialize pygame
pygame.init()

# Creation of screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('backgroond.jpg')

# Background Music
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Shooter")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('rocket.png')
playerX = 370
playerY = 480
playerX_movement = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_movement = []
enemyY_movement = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien1.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_movement.append(0.7)
    enemyY_movement.append(30)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_movement = 0
bulletY_movement = 4
bullet_state = "Ready"    # So you can't see the bullet

# Score
score_value = 0
font = pygame.font.Font('04b_30__.ttf', 32)
textX = 10
textY = 10

# Game Over Text
over_font = pygame.font.Font('04b_30__.ttf', 64)

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (190, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "Fire"
    screen.blit(bulletImg, (x + 16, y + 10))
   # (x - 10, y + 10)) for double bullets
   # (x + 45, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# Game loop
running = True
while running:
    # RGB
    screen.fill([60, 61, 111])

    # Background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check if right or left key is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_movement = -2
            if event.key == pygame.K_RIGHT:
                playerX_movement = 2
            if event.key == pygame.K_SPACE:
                if bullet_state is "Ready":
                    pewPew =  mixer.Sound('laser.wav')
                    pewPew.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_movement = 0

    # For player boundaries
    playerX += playerX_movement
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # For enemy boundaries and movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_movement[i]
        if enemyX[i] <= 0:
            enemyX_movement[i] = 1
            enemyY[i] += enemyY_movement[i]
        elif enemyX[i] >= 736:
            enemyX_movement[i] = -1
            enemyY[i] += enemyY_movement[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            boom = mixer.Sound('explosion.wav')
            boom.play()
            bulletY = 480
            bullet_state = "Ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Shoot
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "Ready"
    if bullet_state is "Fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_movement

    player(playerX, playerY)
    show_score(textX, textY)

    pygame.display.update()
