import random
import math
import pygame

# Initialize the pygame
pygame.init()

# Create the screen of the game
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
distance_screen_bar = 20
bar_height = 140
bar_width = 20
ball_height_width = 24
speed = 4

# Title, Icon and Background
pygame.display.set_caption("Pong")
icon = pygame.image.load('pong.png')
background = pygame.image.load('Pong background.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('pong bar.png')
playerX = screen_width - distance_screen_bar - bar_width
playerY = screen_height/2 - bar_height/2
playerY_change = 0


def player(x, y):
    screen.blit(playerImg, (x, y))

# Opponent
opponentImg = pygame.image.load('pong bar opponent.png')
opponentX = distance_screen_bar
opponentY = screen_height/2 - bar_height/2
opponentY_change = 0

def opponent(x, y):
    screen.blit(opponentImg, (x, y))

# Ball
ballImg = pygame.image.load('ball.png')
ballX = screen_width/2 - ball_height_width
ballY = screen_height/2 - ball_height_width
ballX_change = random.choice([1, -1]) * speed
ballY_change = random.choice([1, 0, -1]) * speed

def ball(x, y):
    screen.blit(ballImg, (ballX, ballY))

#Score
score_Player = 0
score_Opponent = 0
font = pygame.font.Font('freesansbold.ttf', 32)
score_Player_textX = screen_width/2 + 10
score_Player_textY = 10
score_Opponent_textX = screen_width/2 - 32
score_Opponent_textY = 10

def show_score(x,y, points):
    score = font.render(str(points), True, (255, 255, 255))
    screen.blit(score, (x,y))

# Collision
def isCollision_Opponent(barX, barY, ballX, ballY):
    bar = barY + bar_height
    if ballY + ball_height_width >= barY and ballY <= bar:
        if ballX <= barX + bar_width:
            return True
    else:
        return False

def isCollision_Player(barX, barY, ballX, ballY):
    bar = barY + bar_height
    if ballY + ball_height_width >= barY and ballY <= bar:
        if ballX >= barX - bar_width:
            return True
    else:
        return False


# Game Loop
running = True
a = 0
b = 0
c = 0
while running:
# Screen background
    screen.blit(background, (0, 0))
    pygame.draw.aaline(screen, (255,255,255), (screen_width/2,0), (screen_width/2, screen_height))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Movement keys events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                playerY_change = -speed
            if event.key == pygame.K_DOWN:
                playerY_change = speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0


# Move ball for ballX/Y_change value
    ballX += ballX_change
    ballY += ballY_change

# Move opponent for opponentY_change value
    opponentY += opponentY_change

# Move player for playerY value
    playerY += playerY_change

# Opponent moving up when ball is going up, same with down
    if ballY + ball_height_width > opponentY+bar_height and ballY_change >= 0:
        opponentY_change = speed - 1
    if ballY < opponentY and ballY_change <= 0:
        opponentY_change = -speed + 1

# Player moving up when ball is going up, same with down
#    if ballY + ball_height_width > playerY + bar_height and ballY_change >= 0:
#        playerY_change = speed
#    if ballY < playerY and ballY_change <= 0:
#        playerY_change = -speed

# Collision Opponent
    collision_opponent = isCollision_Opponent(opponentX, opponentY, ballX, ballY)
    if collision_opponent:
        ballX_change *= -1.1
        if ballY_change == 0:
            ballY_change = random.choice([1, -1]) * speed
        if opponentY_change > 0:
            ballY_change = speed
        if opponentY_change < 0:
            ballY_change *= 1

# Collision Player
    collision_player = isCollision_Player(playerX, playerY, ballX, ballY)
    if collision_player:
        ballX_change *= -1.1
        screen.fill((a, b, c))
        if ballY_change == 0:
            ballY_change = random.choice([1, -1]) * speed
        if playerY_change > 0:
            ballY_change = speed
        if playerY_change < 0:
            ballY_change *= 1

# Opponent screen boundaries
    if opponentY <= 0:
        opponentY = 0
    elif opponentY >= screen_height - bar_height:
        opponentY = screen_height - bar_height

# Ball screen boundaries, restart after score, save scores
    if ballY <= 0:
        ballY_change = speed
    elif ballY >= screen_height - ball_height_width:
        ballY_change = -speed
    if ballX <= -ball_height_width or ballX >= screen_width:
        ballX_change = 0
        ballY_change = 0
        if ballX <= -ball_height_width:
            score_Player += 1
            ballX_change = speed
            ballY_change = random.choice([1, 0, -1]) * speed
        if ballX >= screen_width:
            score_Opponent += 1
            ballX_change = -speed
            ballY_change = random.choice([1, 0, -1]) * speed
        ballX = screen_width/2 - ball_height_width
        ballY = screen_height/2 - ball_height_width
        print("Score Opponent: ", score_Opponent, " Score Player: ", score_Player)


# Player screen boundaries
    if playerY <= 0:
        playerY = 0
    elif playerY >= screen_height - bar_height:
        playerY = screen_height - bar_height

# Loading model positions
    player(playerX, playerY)
    opponent(opponentX, opponentY)
    ball(ballX, ballY)
    if score_Opponent > 9:
        score_Opponent_textX = screen_width/2 - 45
    show_score(score_Opponent_textX, score_Opponent_textY, score_Opponent)
    show_score(score_Player_textX, score_Player_textY, score_Player)
    pygame.display.update()
