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
pygame.display.set_caption("LALA 4 DEAD")

# Load images
MENUBG_IMG = pygame.image.load("img/menu_bg.png")
GAMEOVER_BG = pygame.image.load(os.path.join("img", "gameover_bg.png"))
PLAYAGAIN_IMG = [pygame.image.load(os.path.join("img", "gm_playagain.png")), pygame.image.load(os.path.join("img", "gm_playagain_hover.png"))]
MAINMENU_IMG = [pygame.image.load(os.path.join("img", "gm_mainmenu.png")), pygame.image.load(os.path.join("img", "gm_mainmenu_hover.png"))]
START_IMG = [pygame.image.load(os.path.join("img", "start.png")), pygame.image.load(os.path.join("img", "start_hover.png"))]
ABOUT_IMG = [pygame.image.load(os.path.join("img", "about.png")), pygame.image.load(os.path.join("img", "about_hover.png"))]
ABOUT_BG = pygame.image.load(os.path.join("img", "about_bg.png"))
MAINMENU_BUTTON = [pygame.image.load(os.path.join("img", "mainmenu_button.png")), pygame.image.load(os.path.join("img", "mainmenu_hover.png"))]
BACKGROUND_IMG = pygame.image.load(os.path.join("img", "background.png"))
GAMEWIN_BG = pygame.image.load(os.path.join("img", "youwin_bg.png"))
GAMEBAR_IMG = pygame.image.load(os.path.join("img", "game_bar.png"))
PLAYER_IMG = pygame.image.load(os.path.join("img", "player.png"))
HEALTHBONUS_IMG = [pygame.image.load(os.path.join("img", "healthbonus1.png")), pygame.image.load(os.path.join("img", "healthbonus2.png"))]
BULLET_IMG = pygame.image.load(os.path.join("img", "bullet.png"))
ENEMY_IMG = [pygame.image.load(os.path.join("img", "enemy1.png")), pygame.image.load(os.path.join("img", "enemy2.png")), pygame.image.load(os.path.join("img", "enemy3.png")), pygame.image.load(os.path.join("img", "enemy4.png"))]
SPECIALFIRE_IMG = pygame.image.load(os.path.join("img", "specialfire_img.png"))
SPECIALFIRE_NOT = pygame.image.load(os.path.join("img", "specialfire_notification.png"))
FLAMEBONUS_IMG = pygame.image.load(os.path.join("img", "flame_bonus.png"))

# Appropriate image transformations
BULLET_IMG = pygame.transform.scale(BULLET_IMG, (32, 32))
ENEMY_IMG[0] = pygame.transform.scale(ENEMY_IMG[0], (84, 70))
ENEMY_IMG[1] = pygame.transform.scale(ENEMY_IMG[1], (74, 64))
ENEMY_IMG[2] = pygame.transform.scale(ENEMY_IMG[2], (74, 64))
ENEMY_IMG[3] = pygame.transform.scale(ENEMY_IMG[3], (74, 70))
HEALTHBONUS_IMG[0] = pygame.transform.scale(HEALTHBONUS_IMG[0], (48, 48))
HEALTHBONUS_IMG[1] = pygame.transform.scale(HEALTHBONUS_IMG[1], (32, 48))
BACKGROUND_IMG = pygame.transform.scale(BACKGROUND_IMG, (WIDTH, HEIGHT))

# Add Icon
pygame.display.set_icon(PLAYER_IMG)

# Load Font
GAME_FONT = pygame.font.Font(("8BitMadness.ttf"), 42)
GAMEOVER_FONT = pygame.font.SysFont('8BitMadness.ttf', 90)

# Load Sounds
BG_SOUND = mixer.music.load('sounds/game_song.ogg')
PAUSE_SOUND = mixer.Sound('sounds/pause.ogg')
SPAWN_SOUND = mixer.Sound('sounds/SpawnSound.ogg')
BULLET_SOUND = mixer.Sound('sounds/bullet.ogg')
GAMEOVER_SOUND = mixer.Sound('sounds/GameOver.wav')
GAMEWIN_SOUND = mixer.Sound('sounds/game_win.ogg')
SPECIALFIRE_SOUND = mixer.Sound('sounds/specialfire.ogg')
HEALTHBONUS_SOUND = mixer.Sound('sounds/healthbonus.ogg')
HIT_SOUND = mixer.Sound('sounds/hit.ogg')

# Appropriate volume transformations
mixer.Sound.set_volume(SPAWN_SOUND, 0.4)
mixer.Sound.set_volume(BULLET_SOUND, 0.4)
mixer.Sound.set_volume(HEALTHBONUS_SOUND, 0.4)
mixer.Sound.set_volume(SPECIALFIRE_SOUND, 0.6)
mixer.Sound.set_volume(GAMEOVER_SOUND, 0.5)
mixer.Sound.set_volume(GAMEWIN_SOUND, 0.5)
mixer.Sound.set_volume(PAUSE_SOUND, 0.5)
mixer.Sound.set_volume(HIT_SOUND, 0.4)

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
        self.img_state = 0
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
        # Bullet animation
        for event in pygame.event.get():
            if event.type == USEREVENT + 1:
                self.img = pygame.transform.flip(self.img, 1, 0)

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
    COOLDOWN = 10

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
        self.firebonus_max = 30
        self.firebonus = 0
        self.specialfire_x = self.x * 3/2
        self.specialfire_y = -self.y + 540
        self.specialfire_state = False
        self.specialfire_image = SPECIALFIRE_IMG
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
                        self.firebonus += 1
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)

    def cooldown(self, window):
        """
        Makes sure there's a delay before player can shoot again
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

    def specialfire_bar(self, window):
        pygame.draw.rect(window, (0, 0, 0), (20, 70, 15, 100))
        pygame.draw.rect(window, (245, 239, 66), (20, 170, 15, -(100 * (self.firebonus/self.firebonus_max))))
        window.blit(FLAMEBONUS_IMG, (20, 175))

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
        self.character_img = random.choice([ENEMY_IMG[0], ENEMY_IMG[1], ENEMY_IMG[2], ENEMY_IMG[3]])
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
        if random.randint(1,10) > 7:
            self.bonus_img = HEALTHBONUS_IMG[1]
            self.health = 100
        else:
            self.bonus_img = HEALTHBONUS_IMG[0]
            self.health = 20

def game():
    # Background Music
    mixer.music.play(-1)
    mixer.music.set_volume(0.2)
    # VARIABLES
    running = True
    FPS = 100
    gameover = False

    wave_value = 0

    player = Player(370, 500)
    player_vel = 6
    bullet_vel = -9

    enemies = []
    num_of_enemies = 0
    enemy_vel = 3

    health_bonuses = []
    hbonus_vel = 4
    spawn_maxheight = -2000

    # timer of 1/10 of second for sprite animation
    pygame.time.set_timer(USEREVENT + 1, 100)

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

        if wave_value == 31:
            mixer.music.stop()
            game_win()

        # Draw specialfire bonus if on
        if player.firebonus >= player.firebonus_max:
            SCREEN.blit(SPECIALFIRE_NOT, (20, 50))
        else:
            player.specialfire_bar(SCREEN)

        # Draw player
        player.draw(SCREEN)

        # Draw Game bar on screen
        SCREEN.blit(GAMEBAR_IMG, (0, 0))

        # Render text
        score_text = GAME_FONT.render(f"Score: {player.score_value}", 1, (0, 0, 0))
        life_text = GAME_FONT.render(f"HP: {player.health}", 1, (0, 0, 0))
        level_text = GAME_FONT.render(f"Wave: {wave_value}/30", 1, (0, 0, 0))

        # Put rendered text on screen
        SCREEN.blit(score_text, (10, 10))
        SCREEN.blit(life_text, (WIDTH - life_text.get_width()-10, 10))
        SCREEN.blit(level_text, ((WIDTH - level_text.get_width()) // 2, 10))

        if gameover:
            mixer.music.stop()
            game_over()

        # Display changes
        pygame.display.update()

    def pause():
        """
        pauses the game
        """
        PAUSE_SOUND.play()
        pygame.mixer.music.pause()
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        PAUSE_SOUND.play()
                        pygame.mixer.music.unpause()
                        paused = False
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            SCREEN.blit(GAME_FONT.render("Game Paused", True, (0, 0, 0)), (300, 250))
            SCREEN.blit(GAME_FONT.render("Press P to continue", True, (0, 0, 0)), (250, 300))
            pygame.display.update()
            clock.tick(5)

    # GAME LOOP
    while running:
        clock.tick(FPS)
        redraw_window()

        if player.health <= 0:
            gameover = True

        # limits value of fire bonus score
        if player.firebonus > player.firebonus_max:
            player.firebonus = player.firebonus_max

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    player.shoot()
                if player.firebonus >= player.firebonus_max:
                    if event.key == K_LCTRL:
                        player.specialfire_state = True
                        pygame.time.set_timer(USEREVENT, 5000)
                        SPECIALFIRE_SOUND.play()
                        player.firebonus = 0

            # Deactivates fire bonus after some time
            if event.type == USEREVENT:
                player.specialfire_state = False

            # Sprite animation for fire bonus
            if event.type == USEREVENT +1:
                if player.specialfire_state:
                    player.specialfire_image = pygame.transform.flip(player.specialfire_image, 1, 0)


        # Movement dynamics that allow two keys to be pressed simultaneously
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel > 0:
            player.character_img = pygame.transform.flip(PLAYER_IMG, 0, 0)
            player.x -= player_vel
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
                enemy = Enemy(random.randrange(100, WIDTH - 100), random.randrange(spawn_maxheight, -50))
                enemies.append(enemy)
            SPAWN_SOUND.play()

            # Spawn random bonus every 3 waves
            if wave_value % 3 == 0:
                bonus = HealthBonus(random.randrange(100, WIDTH - 100), random.randrange(spawn_maxheight, -50))
                health_bonuses.append(bonus)

            # Player and bullet gain velocity every 10 waves
            if wave_value % 10 == 0:
                player_vel += 2
                bullet_vel -= 2
                spawn_maxheight -= 500

        # Health bonus
        for health_bonus in health_bonuses[:]:
            health_bonus.move(hbonus_vel)

            if collide(bonus, player):
                if player.health + bonus.health > 100:
                    player.health = 100
                else:
                    player.health += bonus.health
                HEALTHBONUS_SOUND.play()
                health_bonuses.remove(bonus)

            if bonus.y > HEIGHT:
                health_bonuses.remove(bonus)

        for enemy in enemies[:]:
            enemy.move(enemy_vel)

            # Feels damage if enemy collides with player or get to the bottom
            if collide(enemy, player) or enemy.y + enemy.get_height() > HEIGHT:
                player.health -= 10
                HIT_SOUND.play()
                enemies.remove(enemy)
            # This if below fixes a bug of certain enemies colliding randomly when there special fire wasn't on
            if player.specialfire_state:
                # Prevents game from crashing due to error "list ran out of index" (i have no idea why it happens)
                try:
                    if player.specialfire_collision(enemy):
                        enemies.remove(enemy)
                        player.score_value += 1
                        player.firebonus += 1
                except:
                    pass

        player.move_bullets(bullet_vel, enemies)

def game_over():
    GAMEOVER_SOUND.play()
    while True:
        mx, my = pygame.mouse.get_pos()
        click = False

        # Draw main menu background
        SCREEN.blit(GAMEOVER_BG, (0, 0))

        # Draw buttons on screen
        SCREEN.blit(PLAYAGAIN_IMG[0], (WIDTH / 2 - PLAYAGAIN_IMG[0].get_width() / 2, HEIGHT / 2 - PLAYAGAIN_IMG[0].get_height() / 2+16))
        SCREEN.blit(MAINMENU_IMG[0], (WIDTH / 2 - MAINMENU_IMG[0].get_width() / 2, HEIGHT / 2 + 64))

        # Creating invisble rectangular object on buttons to allow click
        playagain_button = PLAYAGAIN_IMG[0].get_rect(x=WIDTH / 2 - PLAYAGAIN_IMG[0].get_width() / 2, y=HEIGHT / 2 - PLAYAGAIN_IMG[0].get_height() / 2+16)
        mainmenu_button = MAINMENU_IMG[0].get_rect(x=WIDTH / 2 - MAINMENU_IMG[0].get_width() / 2, y=HEIGHT / 2 + 64)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        # Button hover and click dynamics
        if playagain_button.collidepoint((mx, my)):
            SCREEN.blit(PLAYAGAIN_IMG[1],(WIDTH / 2 - PLAYAGAIN_IMG[1].get_width() / 2, HEIGHT / 2 - PLAYAGAIN_IMG[1].get_height() / 2 + 16))
            if click:
                GAMEOVER_SOUND.stop()
                game()
        if mainmenu_button.collidepoint((mx, my)):
            SCREEN.blit(MAINMENU_IMG[1], (WIDTH / 2 - MAINMENU_IMG[1].get_width() / 2, HEIGHT / 2 + 64))
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
        SCREEN.blit(START_IMG[0], (WIDTH / 2 - START_IMG[0].get_width() / 2, HEIGHT / 2 - START_IMG[0].get_height() / 2))
        SCREEN.blit(ABOUT_IMG[0], (WIDTH / 2 - ABOUT_IMG[0].get_width() / 2, HEIGHT / 2 + 48))

        # Creating invisble rectangular object on buttons to allow click
        start_button = START_IMG[0].get_rect(x=WIDTH/2 - START_IMG[0].get_width()/2, y=HEIGHT/2 - START_IMG[0].get_height()/2)
        about_button = ABOUT_IMG[0].get_rect(x=WIDTH/2 - ABOUT_IMG[0].get_width()/2, y=HEIGHT/2 + 48)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        # Button hover and click dynamics
        if start_button.collidepoint((mx, my)):
            SCREEN.blit(START_IMG[1], (WIDTH / 2 - START_IMG[1].get_width() / 2, HEIGHT / 2 - START_IMG[1].get_height() / 2))
            if click:
                game()
        if about_button.collidepoint((mx, my)):
            SCREEN.blit(ABOUT_IMG[1], (WIDTH / 2 - ABOUT_IMG[1].get_width() / 2, HEIGHT / 2 + 48))
            if click:
                about()

        clock.tick(60)
        pygame.display.update()

def game_win():
    GAMEWIN_SOUND.play()
    while True:
        mx, my = pygame.mouse.get_pos()
        click = False

        # Draw main menu background
        SCREEN.blit(GAMEWIN_BG, (0, 0))

        # Draw buttons on screen
        SCREEN.blit(PLAYAGAIN_IMG[0], (WIDTH / 2 - PLAYAGAIN_IMG[0].get_width() / 2, HEIGHT / 2 - PLAYAGAIN_IMG[0].get_height() / 2+16))
        SCREEN.blit(MAINMENU_IMG[0], (WIDTH / 2 - MAINMENU_IMG[0].get_width() / 2, HEIGHT / 2 + 64))

        # Creating invisble rectangular object on buttons to allow click
        playagain_button = PLAYAGAIN_IMG[0].get_rect(x=WIDTH / 2 - PLAYAGAIN_IMG[0].get_width() / 2, y=HEIGHT / 2 - PLAYAGAIN_IMG[0].get_height() / 2+16)
        mainmenu_button = MAINMENU_IMG[0].get_rect(x=WIDTH / 2 - MAINMENU_IMG[0].get_width() / 2, y=HEIGHT / 2 + 64)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        # Button hover and click dynamics
        if playagain_button.collidepoint((mx, my)):
            SCREEN.blit(PLAYAGAIN_IMG[1],(WIDTH / 2 - PLAYAGAIN_IMG[1].get_width() / 2, HEIGHT / 2 - PLAYAGAIN_IMG[1].get_height() / 2 + 16))
            if click:
                GAMEWIN_SOUND.stop()
                game()
        if mainmenu_button.collidepoint((mx, my)):
            SCREEN.blit(MAINMENU_IMG[1], (WIDTH / 2 - MAINMENU_IMG[1].get_width() / 2, HEIGHT / 2 + 64))
            if click:
                GAMEWIN_SOUND.stop()
                main_menu()

        clock.tick(60)
        pygame.display.update()

def about():
    while True:
        mx, my = pygame.mouse.get_pos()
        click = False

        # Draw main menu background
        SCREEN.blit(ABOUT_BG, (0, 0))

        # Draw buttons on screen
        SCREEN.blit(MAINMENU_IMG[0], (WIDTH / 2 - MAINMENU_IMG[0].get_width() / 2, HEIGHT - 100))

        # Creating invisble rectangular object on buttons to allow click
        mainmenu_button = MAINMENU_IMG[0].get_rect(x=WIDTH / 2 - MAINMENU_IMG[0].get_width() / 2, y=HEIGHT - 100)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        # Button hover and click dynamics
        if mainmenu_button.collidepoint((mx, my)):
            SCREEN.blit(MAINMENU_IMG[1], (WIDTH / 2 - MAINMENU_IMG[1].get_width() / 2, HEIGHT - 100))
            if click:
                main_menu()

        clock.tick(60)
        pygame.display.update()

main_menu()
