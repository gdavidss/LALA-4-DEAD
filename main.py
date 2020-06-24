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
MENUBG_IMG = pygame.image.load(os.path.join("img", "menu_bg.png"))
GAMEOVER_BG = pygame.image.load(os.path.join("img", "gameover_bg.png"))
PLAYAGAIN_IMG = pygame.image.load(os.path.join("img", "gm_playagain.png"))
PLAYAGAIN_HOVER = pygame.image.load(os.path.join("img", "gm_playagain_hover.png"))
MAINMENU_IMG = pygame.image.load(os.path.join("img", "gm_mainmenu.png"))
MAINMENU_HOVER = pygame.image.load(os.path.join("img", "gm_mainmenu_hover.png"))
START_IMG = pygame.image.load(os.path.join("img", "start.png"))
START_HOVER = pygame.image.load(os.path.join("img", "start_hover.png"))
ABOUT_IMG = pygame.image.load(os.path.join("img", "about.png"))
ABOUT_HOVER = pygame.image.load(os.path.join("img", "about_hover.png"))
BACKGROUND_IMG = pygame.image.load(os.path.join("img", "background.png"))
GAMEBAR_IMG = pygame.image.load(os.path.join("img", "game_bar.png"))
PLAYER_IMG = pygame.image.load(os.path.join("img", "player.png"))
BULLET_IMG = pygame.image.load(os.path.join("img", "flame.gif"))
ENEMY1_IMG = pygame.image.load(os.path.join("img", "enemy.png"))
ENEMY2_IMG = pygame.image.load(os.path.join("img", "enemy2.png"))
ENEMY3_IMG = pygame.image.load(os.path.join("img", "enemy3.png"))
ENEMY4_IMG = pygame.image.load(os.path.join("img", "enemy4.png"))

# Appropriate image transformations
BULLET_IMG = pygame.transform.scale(BULLET_IMG, (32, 32))
BULLET_IMG = pygame.transform.flip(BULLET_IMG, 0, 1)
ENEMY1_IMG = pygame.transform.scale(ENEMY1_IMG, (74, 64))
ENEMY2_IMG = pygame.transform.scale(ENEMY2_IMG, (74, 64))
ENEMY3_IMG = pygame.transform.scale(ENEMY3_IMG, (74, 64))
ENEMY4_IMG = pygame.transform.scale(ENEMY4_IMG, (74, 64))
BACKGROUND_IMG = pygame.transform.scale(BACKGROUND_IMG, (WIDTH, HEIGHT))

# Load Font
GAME_FONT = pygame.font.Font(("8BitMadness.ttf"), 42)
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

"""-- Collide Function --"""
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

        # Special fire bonus
        self.specialfire_x = self.x + 10
        self.specialfire_y = -self.y + 400
        self.specialfire_state = False
        self.specialfire_image = pygame.transform.scale(PLAYER_IMG, (32, HEIGHT))
        self.specialfire_mask = pygame.mask.from_surface(self.specialfire_image)

    def move_bullets(self, vel, enemies):
        """
        Moves every bullet and checks collision with enemy
        """
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
        if self.cool_down_counter == 0 and self.specialfire_state == False:
            BULLET_SOUND.play()
            bullet = Bullet(self.x+10, self.y, self.bullet_img)
            self.bullets.append(bullet)
            self.cool_down_counter = 1

    def draw(self, window):
        """
        Draw player (via super), health bar and bullets that are being shot
        """
        super().draw(window)
        self.health_bar(window)
        for bullet in self.bullets:
            bullet.draw(window)

    def health_bar(self, window):
        """
        Creates a green and red bar that shows HP under the player
        """
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.character_img.get_height() + 10, self.character_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.character_img.get_height() + 10, self.character_img.get_width() * (self.health / self.max_health), 10))

    def specialfire_draw(self, window):
        """
        Makes special fire follow the player and draws it on screen
        """
        self.specialfire_x = self.x + 10
        window.blit(self.specialfire_image, (self.specialfire_x, self.specialfire_y))

    def specialfire_collision(self, enemy):
        """
        Return if a collision between special fire and enemy has happened
        """
        offset_x = enemy.x - self.specialfire_x
        offset_y = enemy.y - self.specialfire_y
        return self.specialfire_mask.overlap(enemy.mask, (offset_x, offset_y)) != None


class Enemy(Character):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.character_img = random.choice([ENEMY1_IMG, ENEMY2_IMG, ENEMY3_IMG, ENEMY4_IMG])
        self.mask = pygame.mask.from_surface(self.character_img)

    def move(self, vel):
        self.y += vel

class HealthBonus():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bonus_type()
        self.mask = pygame.mask.from_surface(self.bonus_img)

    def draw(self, window):
        window.blit(self.bonus_img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def bonus_type(self):
        # 30% chances of getting Llama (100HP) and 70% of 20HP
        if random.randint(1,10) >= 7:
            self.bonus_img = BULLET_IMG
            self.health = 100
        else:
            self.bonus_img = PLAYER_IMG
            self.health = 20

def game():
    # VARIABLES
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

    health_bonuses = []
    hbonus_vel = 3


    # REDRAW WINDOW
    def redraw_window():
        # Draw background
        SCREEN.blit(BACKGROUND_IMG, (0, 0))

        # Draw enemies
        for enemy in enemies:
            enemy.draw(SCREEN)

        # Draw Bonus
        for bonus in health_bonuses:
            bonus.draw(SCREEN)

        # Draw specialfire bonus if on
        if player.specialfire_state:
            player.specialfire_draw(SCREEN)

        # Draw player
        player.draw(SCREEN)

        SCREEN.blit(GAMEBAR_IMG, (0, 0))

        # Render text
        score_text = GAME_FONT.render(f"Score: {player.score_value}", 1, (0, 0, 0))
        life_text = GAME_FONT.render(f"HP: {player.health}", 1, (0, 0, 0))
        level_text = GAME_FONT.render(f"Wave: {wave_value}", 1, (0, 0, 0))

        # Put rendered text on screen
        SCREEN.blit(score_text, (10, 10))
        SCREEN.blit(life_text, (WIDTH - level_text.get_width(), 10))
        SCREEN.blit(level_text, ((WIDTH - level_text.get_width()) // 2, 10))

        if gameover:
            game_over()

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

    # Timer that unlocks special fire every minute
    pygame.time.set_timer(USEREVENT, 60000)

    # GAME LOOP
    while running:
        clock.tick(FPS)
        redraw_window()

        if player.health <= 0:
            gameover = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    player.shoot()
            # Unlocks specialfire after one minute
            if event.type == USEREVENT:
                player.specialfire_state = True
                pygame.time.set_timer(USEREVENT + 1, 4000)
            if event.type == USEREVENT+1:
                player.specialfire_state = False

        # Movement dynamics that allow two keys to be pressed simultaneously
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel > 0:
            player.x -= player_vel
            player.character_img = pygame.transform.flip(PLAYER_IMG, 0, 0)
            if player.specialfire_state:
                player.specialfire_x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH:
            player.character_img = pygame.transform.flip(PLAYER_IMG, 1, 0)
            player.x += player_vel
            if player.specialfire_state:
                player.specialfire_x += player_vel
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
                health_bonuses.append(bonus)

        # Health bonus
        for health_bonus in health_bonuses[:]:
            health_bonus.move(hbonus_vel)

            if collide(bonus, player):
                if player.health + bonus.health > 100:
                    player.health = 100
                else:
                    player.health += bonus.health
                health_bonuses.remove(bonus)

            if bonus.y > HEIGHT:
                health_bonuses.remove(bonus)

        for enemy in enemies[:]:
            enemy.move(enemy_vel)

            # Feels damage if enemy collides with player or get to the bottom
            if collide(enemy, player) or enemy.y + enemy.get_height() > HEIGHT:
                player.health -= 10
                enemies.remove(enemy)

            if player.specialfire_collision(enemy):
                enemies.remove(enemy)
                player.score_value += 1

        player.move_bullets(bullet_vel, enemies)

def game_over():
    GAMEOVER_SOUND.play()
    while True:
        mx, my = pygame.mouse.get_pos()
        click = False

        # Draw main menu background
        SCREEN.blit(GAMEOVER_BG, (0, 0))

        # Draw buttons on screen
        SCREEN.blit(PLAYAGAIN_IMG, (WIDTH / 2 - PLAYAGAIN_IMG.get_width() / 2, HEIGHT / 2 - START_IMG.get_height() / 2+16))
        SCREEN.blit(MAINMENU_IMG, (WIDTH / 2 - MAINMENU_IMG.get_width() / 2, HEIGHT / 2 + 64))

        # Creating invisble rectangular object on buttons to allow click
        playagain_button = START_IMG.get_rect(x=WIDTH / 2 - START_IMG.get_width() / 2, y=HEIGHT / 2 - START_IMG.get_height() / 2+16)
        mainmenu_button = ABOUT_IMG.get_rect(x=WIDTH / 2 - ABOUT_IMG.get_width() / 2, y=HEIGHT / 2 + 64)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        # Button hover and click dynamics
        if playagain_button.collidepoint((mx, my)):
            SCREEN.blit(PLAYAGAIN_HOVER,(WIDTH / 2 - PLAYAGAIN_HOVER.get_width() / 2, HEIGHT / 2 - PLAYAGAIN_HOVER.get_height() / 2+16))
            if click:
                GAMEOVER_SOUND.stop()
                game()
        if mainmenu_button.collidepoint((mx, my)):
            SCREEN.blit(MAINMENU_HOVER, (WIDTH / 2 - MAINMENU_HOVER.get_width() / 2, HEIGHT / 2 + 64))
            if click:
                GAMEOVER_SOUND.stop()
                main_menu()

        clock.tick(60)
        pygame.display.update()

def main_menu():
    while True:
        mx, my = pygame.mouse.get_pos()
        click = False

        # Draw main menu background
        SCREEN.blit(MENUBG_IMG, (0, 0))

        # Draw buttons on screen
        SCREEN.blit(START_IMG, (WIDTH / 2 - START_IMG.get_width() / 2, HEIGHT / 2 - START_IMG.get_height() / 2))
        SCREEN.blit(ABOUT_IMG, (WIDTH / 2 - ABOUT_IMG.get_width() / 2, HEIGHT / 2 + 48))

        # Creating invisble rectangular object on buttons to allow click
        start_button = START_IMG.get_rect(x=WIDTH/2 - START_IMG.get_width()/2, y=HEIGHT/2 - START_IMG.get_height()/2)
        about_button = ABOUT_IMG.get_rect(x=WIDTH/2 - ABOUT_IMG.get_width()/2, y=HEIGHT/2 + 48)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        # Button hover and click dynamics
        if start_button.collidepoint((mx, my)):
            SCREEN.blit(START_HOVER, (WIDTH / 2 - START_HOVER.get_width() / 2, HEIGHT / 2 - START_HOVER.get_height() / 2))
            if click:
                game()
        if about_button.collidepoint((mx, my)):
            SCREEN.blit(ABOUT_HOVER, (WIDTH / 2 - ABOUT_HOVER.get_width() / 2, HEIGHT/2 + 48))
            if click:
                about()

        clock.tick(60)
        pygame.display.update()

def about():
    while True:
        mx, my = pygame.mouse.get_pos()
        click = False

        # Draw main menu background
        SCREEN.blit(MENUBG_IMG, (0, 0))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        # Button hover and click dynamics

        clock.tick(60)
        pygame.display.update()


main_menu()
"""-- Game Loop --"""