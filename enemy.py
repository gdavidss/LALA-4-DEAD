import pygame
import random

# Inimigo
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 1

for i in range(num_of_enemies):
    enemyImg.append(pygame.transform.scale(pygame.image.load('img/enemy.png'), (80, 64)))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(random.randint(1,4)) # velocidade de mudança horizontal
    enemyY_change.append(40)