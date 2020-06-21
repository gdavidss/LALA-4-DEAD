import math, random
import sys
import pygame
import os
from pygame import mixer
from pygame.locals import *

# Initialize pygame, sound mixer, screen and font
pygame.init()
#pygame.mixer.init()
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LALA Invaders")

# Load images
BACKGROUND_IMG = pygame.image.load(os.path.join("img", "background.png"))
PLAYER_IMG = pygame.image.load(os.path.join("img", "player.png"))
ENEMY_IMG = pygame.image.load(os.path.join("img", "enemy.png"))
BULLET_IMG = pygame.image.load(os.path.join("img", "flame.gif"))

# Appropriate image transformations
BULLET_IMG = pygame.transform.scale(BULLET_IMG, (32, 32))
BULLET_IMG = pygame.transform.flip(BULLET_IMG, 0, 1)
ENEMY_IMG = pygame.transform.scale(ENEMY_IMG, (74, 64))
BACKGROUND_IMG = pygame.transform.scale(BACKGROUND_IMG, (WIDTH, HEIGHT))

# Load Font
GAME_FONT = pygame.font.SysFont(("8BitMadness.ttf"), 42)
GAMEOVER_FONT = pygame.font.SysFont('8BitMadness.ttf', 90)

# Background and sound
##mixer.music.load('sounds/background.ogg')
##mixer.music.play(-1)

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
                    # pause_sound.play()
                    paused = False
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        SCREEN.blit(GAME_FONT.render("Game Paused", True, (0, 0, 0)), (300, 250))
        SCREEN.blit(GAME_FONT.render("Press P to continue", True, (0, 0, 0)), (250, 300))
        pygame.display.update()
        clock.tick(5)

""""
def gameover_text():
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
"""


class Bullet:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


class Character:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.character_img = None
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.character_img, (self.x, self.y))

    def get_width(self):
        return self.character_img.get_width()

    def get_height(self):
        return self.character_img.get_height()


class Player(Character):
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        super().__init__(x, y)
        self.character_img = PLAYER_IMG
        self.bullet_img = BULLET_IMG
        self.bullets = []
        self.mask = pygame.mask.from_surface(self.character_img)
        self.max_health = health

    def move_bullets(self, vel, enemies):
        self.cooldown(SCREEN)
        for bullet in self.bullets:
            bullet.move(vel)
            if bullet.off_screen(HEIGHT):
                self.bullets.remove(bullet)
            else:
                for enemy in enemies:
                    if bullet.collision(enemy):
                        enemies.remove(enemy)
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)


    def cooldown(self, window):
        """
        Makes sure there's delay before player can shoot again
        """
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            bullet = Bullet(self.x+10, self.y, self.bullet_img)
            self.bullets.append(bullet)
            self.cool_down_counter = 1

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)
        for bullet in self.bullets:
            bullet.draw(window)

    def healthbar(self, window):
        """
        Creates a green and red bar that shows HP under the player
        """
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.character_img.get_height() + 10, self.character_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.character_img.get_height() + 10, self.character_img.get_width() * (self.health / self.max_health), 10))

class Enemy(Character):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.character_img = ENEMY_IMG
        self.mask = pygame.mask.from_surface(self.character_img)

    def move(self, vel):
        self.y += vel

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def game():
    """""-- Variables --"""
    running = True
    FPS = 100
    gameover = False

    level_value = 1
    score_value = 0
    life_value = 3

    # Jogador
    player = Player(370, 480)
    player_vel = 5
    bullet_vel = -5

    enemies = []
    num_of_enemies = 1
    enemy_vel = 2
    enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100))
    enemies.append(enemy)

    # Init Gameover sound state
    ##GameOverSound_state = True

    def redraw_window():
        # Draw background
        SCREEN.blit(BACKGROUND_IMG, (0, 0))

        # Render text
        score_text = GAME_FONT.render(f"Score: {score_value}", 1, (0, 0, 0))
        life_text = GAME_FONT.render(f"Life: {life_value}", 1, (0, 0, 0))
        level_text = GAME_FONT.render(f"Level: {level_value}", 1, (0, 0, 0))

        # Put rendered text onto screen
        SCREEN.blit(score_text, (10, 10))
        SCREEN.blit(life_text, (WIDTH - level_text.get_width() + 10, 10))
        SCREEN.blit(level_text, ((WIDTH - level_text.get_width())//2, 10))

        # Draw enemies
        for enemy in enemies:
            enemy.draw(SCREEN)

        # Draw player
        player.draw(SCREEN)

        if gameover:
            gameover_text = GAMEOVER_FONT.render("GAME OVER", 1, (0, 0, 0))
            SCREEN.blit(gameover_text, (WIDTH/2 - gameover_text.get_width()/2, HEIGHT/2 - gameover_text.get_height()/2))


        # Display changes
        pygame.display.update()


    # Game Loop
    while running:
        clock.tick(FPS)
        redraw_window()

        if life_value <= 0 or player.health <= 0:
            gameover = True
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit()


            # Spawn diego after 10 seconds
            if event.type == USEREVENT:
                ## spawn_sound = mixer.Sound('sounds/SpawnSound.ogg')
                ## spawn_sound.play()
                level_value += 1
                num_of_enemies += 1
                for i in range(num_of_enemies):
                    # Since enemies have the same vel, spawn them off screen to create different Y positions
                    enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100))
                    enemies.append(enemy)


            """"
            # Bonus event
            if event.type == USEREVENT + 1:
                SCREEN.blit(GAME_FONT.render("Press CTRL to bonus", True, (5, 5, 5)), (10, 550))
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LCTRL:
                       pass

                    ##bullet_sound = mixer.Sound('sounds/bullet.ogg')
                    if bullet_state == "ready":
                        bulletX = player.x
                        bullet_state = "fire"
                        fire_bullet(bulletX, bulletY)
                        ##bullet_sound.play()
            """
        # Movement dynamics that allow two keys to be pressed simultaneously
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel > 0:
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH:
            player.x += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()
        if keys[pygame.K_p]:
            pause()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                life_value -= 1
                enemies.remove(enemy)

        player.move_bullets(bullet_vel, enemies)

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