import math, random
import sys
import pygame
import os
from pygame import mixer
from pygame.locals import *

# Initialize pygame, sound mixer, screen and font
pygame.init()
pygame.mixer.init()
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

# Load Sounds
BG_SOUND = mixer.music.load('sounds/background.ogg')
PAUSE_SOUND = mixer.Sound('sounds/pause.ogg')
SPAWN_SOUND = mixer.Sound('sounds/SpawnSound.ogg')
BULLET_SOUND = mixer.Sound('sounds/bullet.ogg')
GAMEOVER_SOUND = mixer.Sound('sounds/GameOver.wav')

# Background and sound
##mixer.music.play(-1)

"""""-- Timers --"""
# Clock helps to limit fps
clock = pygame.time.Clock()

"""-- Collision Function --"""
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

"""""-- Classes --"""

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

    def bullet_collision(self, obj):
        return collide(self, obj)


class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.character_img = None
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.character_img, (self.x, self.y))

    def get_width(self):
        return self.character_img.get_width()

    def get_height(self):
        return self.character_img.get_height()


class Player(Character):
    COOLDOWN = 20

    def __init__(self, x, y, health=100):
        super().__init__(x, y)
        self.character_img = PLAYER_IMG
        self.health = health
        self.bullet_img = BULLET_IMG
        self.bullets = []
        self.score_value = 0
        self.mask = pygame.mask.from_surface(self.character_img)
        self.max_health = health
        self.fire_x = self.x + 32
        self.fire_y = -self.y + 400

        # Fire bonus
        self.fire_state = False
        self.fire_image = pygame.transform.scale(PLAYER_IMG, (32, HEIGHT))
        self.fire_mask = pygame.mask.from_surface(self.fire_image)

    def move_bullets(self, vel, enemies):
        self.cooldown(SCREEN)
        for bullet in self.bullets:
            bullet.move(vel)
            if bullet.off_screen(HEIGHT):
                self.bullets.remove(bullet)
            else:
                for enemy in enemies:
                    if bullet.bullet_collision(enemy):
                        enemies.remove(enemy)
                        self.score_value += 1
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
        """
        Checks if cooldown is zero to allow bullet to be shot
        """
        if self.cool_down_counter == 0 and self.fire_state == False:
            BULLET_SOUND.play()
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

    def fire_special_draw(self, window):
        self.fire_x = self.x + 10
        window.blit(self.fire_image, (self.fire_x, self.fire_y))


    def firecollide(self, enemy):
        #fire_image_rect = self.fire_image.get_rect()
        offset_x = enemy.x - self.fire_x
        offset_y = enemy.y - self.fire_y
        return self.fire_mask.overlap(enemy.mask, (offset_x, offset_y)) != None


class Enemy(Character):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.character_img = ENEMY_IMG
        self.mask = pygame.mask.from_surface(self.character_img)

    def move(self, vel):
        self.y += vel

class HealthBonus():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bonustype()
        self.mask = pygame.mask.from_surface(self.bonus_img)

    def draw(self, window):
        window.blit(self.bonus_img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def bonustype(self):
        if random.randint(1,10) > 8:
            self.bonus_img = BULLET_IMG
            self.health = 100
        else:
            self.bonus_img = PLAYER_IMG
            self.health = 20

def game():
    """""-- Variables --"""
    running = True
    FPS = 60
    gameover = False

    wave_value = 0

    player = Player(370, 480)
    player_vel = 8
    bullet_vel = -9

    enemies = []
    num_of_enemies = 0
    enemy_vel = 2

    bonuses = []
    bonus_vel = 3

    def redraw_window():
        # Draw background
        SCREEN.blit(BACKGROUND_IMG, (0, 0))

        # Draw enemies
        for enemy in enemies:
            enemy.draw(SCREEN)

        # Draw Bonus
        for bonus in bonuses:
            bonus.draw(SCREEN)

        # Draw Fire bonus
        if player.fire_state:
            player.fire_special_draw(SCREEN)

        # Draw player
        player.draw(SCREEN)

        # Render text
        score_text = GAME_FONT.render(f"Score: {player.score_value}", 1, (0, 0, 0))
        life_text = GAME_FONT.render(f"HP: {player.health}", 1, (0, 0, 0))
        level_text = GAME_FONT.render(f"Wave: {wave_value}", 1, (0, 0, 0))

        # Put rendered text on screen
        SCREEN.blit(score_text, (10, 10))
        SCREEN.blit(life_text, (WIDTH - level_text.get_width(), 10))
        SCREEN.blit(level_text, ((WIDTH - level_text.get_width()) // 2, 10))

        if gameover:
            GAMEOVER_SOUND.play()
            gameover_text = GAMEOVER_FONT.render("GAME OVER", 1, (0, 0, 0))
            SCREEN.blit(gameover_text, (WIDTH/2 - gameover_text.get_width()/2, HEIGHT/2 - gameover_text.get_height()/2))

        # Display changes
        pygame.display.update()

    def pause():
        """
        pauses the game
        """
        PAUSE_SOUND.play()
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        PAUSE_SOUND.play()
                        paused = False
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            SCREEN.blit(GAME_FONT.render("Game Paused", True, (0, 0, 0)), (300, 250))
            SCREEN.blit(GAME_FONT.render("Press P to continue", True, (0, 0, 0)), (250, 300))
            pygame.display.update()
            clock.tick(5)

    # Timer that unlocks fire ray every minute
    pygame.time.set_timer(USEREVENT, 5000)

    # Game Loop
    while running:
        clock.tick(FPS)
        redraw_window()

        if player.health <= 0:
            gameover = True
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    player.shoot()
            # Unlocks fire after one minute
            if event.type == USEREVENT:
                player.fire_state = True
                pygame.time.set_timer(USEREVENT + 1, 4000)
            if event.type == USEREVENT+1:
                player.fire_state = False

        # Movement dynamics that allow two keys to be pressed simultaneously
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel > 0:
            player.x -= player_vel
            player.character_img = pygame.transform.flip(PLAYER_IMG, 0, 0)
            if player.fire_state:
                player.fire_x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH:
            player.character_img = pygame.transform.flip(PLAYER_IMG, 1, 0)
            player.x += player_vel
            if player.fire_state:
                player.fire_x += player_vel
        if keys[pygame.K_p]:
            pause()

        # Spawn enemies after all others have been eliminated
        if len(enemies) == 0:
            wave_value += 1
            num_of_enemies += 1
            for i in range(num_of_enemies):
                # Since enemies have the same vel, spawn them off screen to create different Y positions
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100))
                enemies.append(enemy)
            SPAWN_SOUND.play()
            # Spawn random bonus every 4 levels
            if wave_value % 3 == 0:
                bonus = HealthBonus(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100))
                bonuses.append(bonus)

        for bonus in bonuses[:]:
            bonus.move(bonus_vel)

            if collide(bonus, player):
                if player.health + bonus.health > 100:
                    player.health = 100
                else:
                    player.health += bonus.health
                bonuses.remove(bonus)

            if bonus.y > HEIGHT:
                bonuses.remove(bonus)
                print("deletado")


        for enemy in enemies[:]:
            enemy.move(enemy_vel)

            # Feels damage if enemy collides with player or get to the bottom
            if collide(enemy, player) or enemy.y + enemy.get_height() > HEIGHT:
                player.health -= 10
                enemies.remove(enemy)

            if player.firecollide(enemy):
                    enemies.remove(enemy)
                    player.score_value += 1

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

game()
"""-- Game Loop --"""