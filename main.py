import pygame
import random

# Inicializa o pygame
pygame.init()

# Criar tela com 800x600 pixels de resolução
screen = pygame.display.set_mode((800, 600))

# Título e Ícone
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('penis.png')
pygame.display.set_icon(icon)

# Jogador
playerImg = pygame.image.load('penis_player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Inimigo
enemyImg = pygame.image.load('vagina.png')
enemyX = random.randint(0,800)
enemyY = random.randint(50,150)
enemyX_change = 0.3
enemyY_change = 0


# Desenhar jogador na tela
def player(x, y):
    screen.blit(playerImg, (x, y))


# Desenhar inimigo na tela
def enemy(x, y):
    screen.blit(enemyImg, (x, y))


# Game Loop
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:  # Verifica se houve alguma teclada
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
        if event.type == pygame.KEYUP:  # Verifica se liberou o dedo da tecla
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Pintar a tela com RGB
    screen.fill((255, 255, 255))

    # Atribuir valor de posição mudado pra coordenada X
    playerX += playerX_change

    # Adicionando limites ao player pra ele não escapar da tela
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:  # 800 - 64, que é o tamanho da sprite da rola
        playerX = 736

    # Iniciar o player com as posições iniciais, função definida lá em cima
    player(playerX, playerY)

    # Iniciar inimigo
    enemy(enemyX, enemyY)

    # Tem que atualizar a tela no loop se não vai ficar a mesma coisa
    pygame.display.update()
