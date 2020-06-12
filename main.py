import math
from pygame import mixer

# Modules import
from enemy import *
from player import *



# Inicializa o pygame e o mixer
pygame.init()
mixer.init()

# Create screen with 800x600 pixel resolution
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('img/background.png')
background = pygame.transform.scale(background, (800, 600)) # resize image to 800x600

# Background Sound
mixer.music.load('sounds/background.mp3')
mixer.music.play(-1)

# Título e Ícone
pygame.display.set_caption("Bota Invaders")
icon = pygame.image.load('img/penis.png')
pygame.display.set_icon(icon)

# Bullet
# ready - você não pode ver a bala na tela
# fire - a bala está se movendo
bulletImg = pygame.image.load('img/bullet.png')
bulletImg = pygame.transform.flip(bulletImg, 0, 1)  #virar imagem
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 8
bullet_state = "ready"

# Pontuação
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Texto de Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x,y):
    score = font.render("Botadas: " + str(score_value), True, (0,0,0))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("NÃO BOTASTE", True, (0,0,0))
    screen.blit(over_text, (200, 250))

# Desenhar jogador na tela
def player(x, y):
    screen.blit(playerImg, (x, y))

# Desenhar inimigo na tela
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16, y+10)) # Bullet stay on the middle

def isCollision(enemyX, enemyY, bulletX, bulletY):
    # Distância entre duas coordenadas abaixo
    distance = math.sqrt(math.pow(enemyX-bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False

# Game Loop
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:  # Verifica se houve alguma teclada
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                bullet_sound = mixer.Sound('sounds/bullet.wav')
                bullet_sound.play()
                if bullet_state is "ready":
                    # Pega a coordenada X atual da rola
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:  # Verifica se liberou o dedo da tecla
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Pintar a tela com RGB
    screen.fill((255, 255, 255))

    # Imagem do background
    screen.blit(background, (0, 0))

    # Atribuir valor de posição mudado pra coordenada X
    playerX += playerX_change

    # Movimento do inimigo com bate e volta nas laterais
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            life -= 1
            print(life)
            if life <= 0:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000 # inimigos somem da tela
                game_over_text()
                break
            else:
                for x in range(num_of_enemies):
                    enemyX[x] = random.randint(0, 735)
                    enemyY[x] = random.randint(50, 150)
                    enemyX_change[x] = 2  # velocidade de mudança horizontal
                    enemyY_change[x] = 40


        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i] # adiciona pixels toda vez q colide
            enemyY_change[i] += random.randint(5,12) # creates random Y velocity to improve fun!
        elif enemyX[i] >= 736:  # 800 - 64, that refers to the sprite size
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i] # adiciona pixels toda vez q colide
            enemyY_change[i] += random.randint(5,12)

            # Colisão
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            # Selects a random audio file from three choices and play it when collision happens
            reaction_random = "sounds/Reaction" + str(random.randint(1,3)) + ".wav"
            reaction_sound = mixer.Sound(reaction_random)
            reaction_sound.play()
            # reset bullet and enemy
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        # Iniciar inimigo
        enemy(enemyX[i], enemyY[i], i)

    # Movimento da bala
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Iniciar o player com as posições iniciais, função definida lá em cima
    player(playerX, playerY)

    # mostrar pontuação na tela
    show_score(textX, textY)

    # Tem que atualizar a tela no loop se não vai ficar a mesma coisa
    pygame.display.update()
