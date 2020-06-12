import pygame
# Jogador
playerImg = pygame.image.load('img/penis_player.png')
playerImg = pygame.transform.flip(playerImg, 0, 1)  #virar imagem
playerX = 370
playerY = 480
playerX_change = 0