import math
from pygame import mixer
from pygame.locals import *

# Modules import
from enemy import *
from player import *

# Init pygame and sound mixer
pygame.init()
mixer.init()

# Init Gameover sound state
GameOverSound_state = True

# Create screen with 800x600 pixel resolution
screen = pygame.display.set_mode((800, 600))

# Background image and sound
background = pygame.image.load('img/background.png')
background = pygame.transform.scale(background, (800, 600)) # resize image to 800x600
#mixer.music.load('sounds/background.mp3')
#mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Diego Invaders")
icon = pygame.image.load('img/player.png')
pygame.display.set_icon(icon)

# Bullet
# ready - você não pode ver a bala na tela
# fire - a bala está se movendo
bulletImg = pygame.transform.scale(pygame.image.load('img/flame.gif'), (32, 32))
bulletImg = pygame.transform.flip(bulletImg, 0, 1)  #virar imagem
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 7
bullet_state = "ready"

# Score and level
level = 1
score_value = 0
font = pygame.font.Font('8BitMadness.ttf', 42)

# GameOver text
over_font = pygame.font.Font('8BitMadness.ttf', 90)

"""""-- Functions --"""
def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (0,0,0))
    screen.blit(score, (x, y))

def show_life(x,y):
    life_show = font.render("Life: " + str(life), True, (0,0,0))
    screen.blit(life_show, (x, y))

def show_level(x,y):
    level_show = font.render("Level: " + str(level), True, (0,0,0))
    screen.blit(level_show, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (0,0,0))
    screen.blit(over_text, (200, 250))

# Draw player on screen
def player(x, y):
    screen.blit(playerImg, (x, y))

# Draw enemy on screen
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16, y+10)) # Bullet stay on the middle

def isCollision(enemyX, enemyY, bulletX, bulletY):
    # Distance between two coordenates
    distance = math.sqrt(math.pow(enemyX-bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False

"""""-- Timers --"""
# Clock helps to limit fps
clock = pygame.time.Clock()

# Set a timer for every 10 sec
pygame.time.set_timer(USEREVENT, 10000)

"""""-- Game loop --"""
running = True
while running:
    clock.tick(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Spawn diego after 10 seconds
        if event.type == USEREVENT:
            level += 1
            num_of_enemies += 1
            for i in range(num_of_enemies):
                enemyImg.append(pygame.transform.scale(pygame.image.load('img/enemy.png'), (80, 64)))
                enemyX.append(random.randint(0, 735))
                enemyY.append(random.randint(50, 150))
                enemyX_change.append(random.randint(1,4))  # Horizontal velocity change
                enemyY_change.append(40)

        if event.type == pygame.KEYDOWN:  # Verifies if key has been pressed
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                bullet_sound = mixer.Sound('sounds/bullet.ogg')
                if bullet_state is "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    bullet_sound.play()
        if event.type == pygame.KEYUP: # Verifies if key has been released
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Pintar a tela com RGB
    screen.fill((255, 255, 255))

    # Imagem do background
    screen.blit(background, (0, 0))

    # Atribuir valor de posição mudado pra coordenada X
    playerX += playerX_change

    # Makes player not escape screen
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:  # 800 - 64, that refers to the sprite size
        playerX = 736

    # Movimento do inimigo com bate e volta nas laterais
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            life -= 1
            # add live lost sound here
            if life > 0:
                lifelost_sound = mixer.Sound('sounds/LifeLost.wav')
                lifelost_sound.play()
            if life <= 0:
                gameover_sound = mixer.Sound('sounds/GameOver.wav')
                if GameOverSound_state:
                    gameover_sound.play()
                GameOverSound_state = False
                for j in range(num_of_enemies):
                    enemyY[j] = 2000 # Enemies get out of screen
                game_over_text()
                life = 0
                break
            else:
                # reset all enemies position
                for x in range(num_of_enemies):
                    enemyX[x] = random.randint(0, 735)
                    enemyY[x] = random.randint(50, 150)
                    enemyX_change[x] = random.randint(1,4)  # velocidade de mudança horizontal
                    enemyY_change[x] = 40


        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = random.randint(1,4)
            enemyY[i] += enemyY_change[i] # adiciona pixels toda vez q colide
        elif enemyX[i] >= 736:  # 800 - 64, that refers to the sprite size
            enemyX_change[i] = -random.randint(1,4)
            enemyY[i] += enemyY_change[i] # adiciona pixels toda vez q colide

            # Colisão
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            # Selects a random audio file from three choices and play it when collision happens
            reaction_random = "sounds/Reaction" + str(random.randint(1,11)) + ".wav"
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

    # Show score, life and level functions
    show_score(10, 10)
    show_life(670, 10)
    show_level(335, 10)

    # Tem que atualizar a tela no loop se não vai ficar a mesma coisa
    pygame.display.update()
