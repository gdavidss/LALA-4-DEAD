import math, random
import sys
import pygame
import os
from pygame import mixer
from pygame.locals import *

# Initialize pygame, sound mixer, screen and font
pygame.init()
#pygame.mixer.init()
WIDTH = 800
HEIGHT = 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

# Load images
BACKGROUND_IMG = pygame.image.load(os.path.join("img", "background.png"))
PLAYER_IMG = pygame.image.load(os.path.join("img", "player.png"))
ENEMY_IMG = pygame.image.load(os.path.join("img", "enemy.png"))
BULLET_IMG = pygame.image.load(os.path.join("img", "flame.gif"))

# Appropriate image transformations
BULLET_IMG = pygame.transform.scale(BULLET_IMG, (32, 32))
BULLET_IMG = pygame.transform.flip(BULLET_IMG, 0, 1)
ENEMY_IMG = pygame.transform.scale(ENEMY_IMG, (80, 64))
BACKGROUND_IMG = pygame.transform.scale(BACKGROUND_IMG, (WIDTH, HEIGHT))  # resize image to 800x600


# Background and sound
##mixer.music.load('sounds/background.ogg')
##mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("LALA Invaders")
pygame.display.set_icon(PLAYER_IMG)

"""""-- Timers --"""
# Clock helps to limit fps
clock = pygame.time.Clock()

# Set a timer for every 10 sec to spawn enemy
pygame.time.set_timer(USEREVENT, 10000)

# Set a timer for every minute to unlock bonus
pygame.time.set_timer(USEREVENT + 1, 5000)


"""""-- Functions --"""
def pause():
    """
    pauses the game
    """
   ## pause_sound = mixer.Sound('sounds/pause.ogg')
   ## pause_sound.play()
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    # add pause song
                   ## pause_sound.play()
                    paused = False
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        SCREEN.blit(GAME_FONT.render("Game Paused", True, (0, 0, 0)), (300, 250))
        SCREEN.blit(GAME_FONT.render("Press P to continue", True, (0, 0, 0)), (250, 300))
        pygame.display.update()
        clock.tick(5)

def game_over_text():
    pygame.mixer.music.pause()
    gameover = True
    # GameOver text
    over_GAME_FONT = pygame.GAME_FONT.GAME_FONT('8BitMadness.ttf', 90)
    over_text = over_GAME_FONT.render("GAME OVER", True, (0, 0, 0))
    SCREEN.blit(over_text, (200, 250))
    while gameover:
        pygame.display.update()
        clock.tick(5)  # game doesn't need 30 fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

# Draw player on SCREEN
def player(x, y):
    SCREEN.blit(PLAYER_IMG, (x, y))


# Draw enemy on SCREEN
def enemy(x, y, i):
    SCREEN.blit(enemy_body[i], (x, y))


def fire_bullet(x, y):
    #bullet_state = "fire"
    SCREEN.blit(BULLET_IMG, (x + 16, y + 10))  # Bullet stay on the middle


def is_collision(enemyX, enemyY, bulletX, bulletY):
    # Distance between two coordenates
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False

class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def game():
    """""-- Variables --"""
    # GLOBAL VARIABLES
    global enemy_body
    global bullet_state
    global level_value
    global score_value
    global life_value
    global GAME_FONT

    GAME_FONT = pygame.font.SysFont(("8BitMadness.ttf"), 42)

    # Bullet
    bulletX = 0
    bulletY = 480
    bulletX_change = 0
    bulletY_change = 7
    bullet_state = "ready"

    # Score and levelscore_value
    level_value = 1
    score_value = 0

    # Jogador
    life_value = 3
    playerX = 370
    playerY = 480
    playerX_change = 0

    # Inimigo
    enemy_body = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []
    num_of_enemies = 1

    for i in range(num_of_enemies):
        enemy_body.append(ENEMY_IMG)
        enemyX.append(random.randint(0, 735))
        enemyY.append(random.randint(50, 150))
        # Attributes a random horizontal velocity to enemy
        enemyX_change.append(random.randint(1, 4))
        enemyY_change.append(40)

    # Init Gameover sound state
    ##GameOverSound_state = True

    # Game Loop
    running = True
    FPS = 100

    def redraw_window():
        #SCREEN.blit(BACKGROUND_IMG, (0, 0))
        score_text = GAME_FONT.render(f"Score: {score_value}", 1, (0, 0, 0))
        life_text = GAME_FONT.render(f"Life: {life_value}", 1, (0, 0, 0))
        level_text = GAME_FONT.render(f"Level: {level_value}", 1, (0, 0, 0))
        SCREEN.blit(score_text, (10, 10))
        SCREEN.blit(life_text, (WIDTH - level_text.get_width() + 10, 10))
        SCREEN.blit(level_text, ((WIDTH - level_text.get_width())//2, 10))
        pygame.display.update()


    while running:
        clock.tick(FPS)
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit()

            # Spawn diego after 10 seconds
            if event.type == USEREVENT:
                level_value += 1
                num_of_enemies += 1
                for i in range(num_of_enemies):
                    enemy_body.append(ENEMY_IMG)
                    enemyX.append(random.randint(0, 735))
                    enemyY.append(random.randint(50, 150))
                    enemyX_change.append(random.randint(1, 4))
                    enemyY_change.append(40)
               ## spawn_sound = mixer.Sound('sounds/SpawnSound.ogg')
               ## spawn_sound.play()
            # Bonus event
            if event.type == USEREVENT + 1:
                SCREEN.blit(GAME_FONT.render("Press CTRL to bonus", True, (5, 5, 5)), (10, 550))
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LCTRL:
                        SCREEN.blit(BACKGROUND_IMG, (0, 0))

            if event.type == pygame.KEYDOWN:  # Verifies if key has been pressed
                if event.key == pygame.K_LEFT:
                    playerX_change = -4.5
                if event.key == pygame.K_RIGHT:
                    playerX_change = 4.5
                if event.key == pygame.K_SPACE:
                    ##bullet_sound = mixer.Sound('sounds/bullet.ogg')
                    if bullet_state == "ready":
                        bulletX = playerX
                        bullet_state = "fire"
                        fire_bullet(bulletX, bulletY)
                        ##bullet_sound.play()
                if event.key == pygame.K_p:
                    pause()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    playerX_change = 0
                if event.key == pygame.K_RIGHT:
                    playerX_change = 0

        # Imagem do background
        SCREEN.blit(BACKGROUND_IMG, (0, 0))

        # Atribuir valor de posição mudado pra coordenada X
        playerX += playerX_change

        # Makes player not escape SCREEN
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
                    ##lifelost_sound = mixer.Sound('sounds/LifeLost.wav')
                    ##lifelost_sound.play()
                    pass
                if life <= 0:
                    ##gameover_sound = mixer.Sound('sounds/GameOver.wav')
                    if GameOverSound_state:
                        ##gameover_sound.play()
                        pass
                    GameOverSound_state = False
                    for j in range(num_of_enemies):
                        enemyY[j] = 2000  # Enemies get out of SCREEN
                    game_over_text()
                    life = 0
                    break
                else:
                    # reset all enemies position
                    for x in range(num_of_enemies):
                        enemyX[x] = random.randint(0, 735)
                        enemyY[x] = random.randint(50, 150)
                        enemyX_change[x] = random.randint(1, 4)  # velocidade de mudança horizontal
                        enemyY_change[x] = 40

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = random.randint(1, 3)
                enemyY[i] += enemyY_change[i]  # adiciona pixels toda vez q colide
            elif enemyX[i] >= 736:  # 800 - 64, that refers to the sprite size
                enemyX_change[i] = -random.randint(1, 3)
                enemyY[i] += enemyY_change[i]  # adiciona pixels toda vez q colide

                # Colisão
            collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                # Selects a random audio file from three choices and play it when collision happens
                reaction_random = "sounds/Reaction" + str(random.randint(1, 5)) + ".wav"
              ##  reaction_sound = mixer.Sound(reaction_random)
              ##  reaction_sound.play()
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

def main_menu():
    while True:
        SCREEN.blit(BACKGROUND_IMG, (0, 0))
        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(250, 250, 200, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                game()
        pygame.draw.rect(SCREEN, (255, 255, 255), button_1)
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        clock.tick(60)
        pygame.display.update()

main_menu()
"""-- Game Loop --"""