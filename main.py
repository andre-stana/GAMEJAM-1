import pygame
from pygame import mixer
import os
import random

SCREEN_HEIGHT = 480
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("assets/emeu/run", "run1.png")),
           pygame.image.load(os.path.join("assets/emeu/run", "run2.png")),
           pygame.image.load(os.path.join("assets/emeu/run", "run3.png")),
           pygame.image.load(os.path.join("assets/emeu/run", "run4.png"))]

JUMPING = pygame.image.load(os.path.join("assets/emeu/run", "run1.png"))

DUCKING = [pygame.image.load(os.path.join("assets/emeu/down", "down1.png")),
           pygame.image.load(os.path.join("assets/emeu/down", "down2.png")),
           pygame.image.load(os.path.join("assets/emeu/down", "down3.png")),
           pygame.image.load(os.path.join("assets/emeu/down", "down4.png"))]

SMALL_ENEMY = [pygame.image.load(os.path.join("assets/cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("assets/cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("assets/cactus", "SmallCactus3.png"))]

LARGE_ENEMY = [pygame.image.load(os.path.join("assets/cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("assets/cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("assets/cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("assets/bird", "bird1.png")),
        pygame.image.load(os.path.join("assets/bird", "bird2.png"))]

ROCK = [pygame.image.load(os.path.join("assets/rock", "rock1.png")),
        pygame.image.load(os.path.join("assets/rock", "rock2.png")),
        pygame.image.load(os.path.join("assets/rock", "rock3.png")),
        pygame.image.load(os.path.join("assets/rock", "rock4.png"))]

BG = pygame.image.load(os.path.join("assets/other", "background.png"))

EPITECH_BG = pygame.image.load(os.path.join("assets/other", "epitech_background.png"))

EPITECH_BG = pygame.transform.scale(EPITECH_BG, (SCREEN_WIDTH, SCREEN_HEIGHT))

VICTOR_BG = pygame.image.load(os.path.join("assets/other", "vic2.png"))

VICTOR_BG = pygame.transform.scale(VICTOR_BG, (SCREEN_WIDTH, SCREEN_HEIGHT))

mixer.init()
mixer.pre_init(44100, -16, 1, 512)

DICTATOR_SONG = mixer.Sound(os.path.join("assets/sound", "victor.mp3"))
DICTATOR_SONG.set_volume(0.2)

CHRISTMAS_SONG = mixer.Sound(os.path.join("assets/sound", "christmas.mp3"))
CHRISTMAS_SONG.set_volume(0.2)

class Player:
    X_POS = 80
    Y_POS = 340
    Y_POS_DUCK = 350
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.player_duck = False
        self.player_run = True
        self.player_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.player_rect = self.image.get_rect()
        self.player_rect.x = self.X_POS
        self.player_rect.y = self.Y_POS

        self.rock_step_index = 0
        self.rock = ROCK
        self.rock_img = self.rock[0]
        self.rock_rect = self.rock_img.get_rect()
        self.rock_rect.x = self.X_POS - 125
        self.rock_rect.y = self.Y_POS - 50

    def update(self, userInput):

        self.rock_img = self.rock[self.rock_step_index // 5]

        if self.player_duck:
            self.duck()
        if self.player_run:
            self.run()
        if self.player_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if self.rock_step_index >= 10:
            self.rock_step_index = 0

        if userInput[pygame.K_UP] and not self.player_jump:
            self.player_duck = False
            self.player_run = False
            self.player_jump = True
        elif userInput[pygame.K_DOWN] and not self.player_jump:
            self.player_duck = True
            self.player_run = False
            self.player_jump = False
        elif not (self.player_jump or userInput[pygame.K_DOWN]):
            self.player_duck = False
            self.player_run = True
            self.player_jump = False

        self.rock_step_index += 1

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.player_rect = self.image.get_rect()
        self.player_rect.x = self.X_POS
        self.player_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.player_rect = self.image.get_rect()
        self.player_rect.x = self.X_POS
        self.player_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.player_jump:
            self.player_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.player_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.rock_img, (self.rock_rect.x, self.rock_rect.y))
        if (self.player_duck):
            SCREEN.blit(self.image, (self.player_rect.x, self.player_rect.y - 10))
        else:
            SCREEN.blit(self.image, (self.player_rect.x, self.player_rect.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallEnemy(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class LargeEnemy(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, BG
    run = True
    clock = pygame.time.Clock()
    player = Player()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0

    sound_play = False

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():
        index = 0
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, -10))
        SCREEN.blit(BG, (image_width + x_pos_bg, -10))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, -10))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    def check_multiple_keys(keys):
        for key in keys:
            if not pygame.key.get_pressed()[key]:
                return False
        return True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        keys = [pygame.K_v, pygame.K_i, pygame.K_c, pygame.K_t, pygame.K_o, pygame.K_r]
        if (check_multiple_keys(keys)):
            BG = VICTOR_BG
            if not sound_play:
                sound_play = True
                DICTATOR_SONG.play()

        keys = [pygame.K_e, pygame.K_p, pygame.K_i, pygame.K_t, pygame.K_e, pygame.K_c, pygame.K_h]
        if (check_multiple_keys(keys)):
            BG = EPITECH_BG
            if not sound_play:
                sound_play = True
                CHRISTMAS_SONG.play()

        background()

        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallEnemy(SMALL_ENEMY))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeEnemy(LARGE_ENEMY))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.player_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)

        player.draw(SCREEN)

        score()

        clock.tick(30)
        pygame.display.update()


def menu(death_count):
    global points
    run = True
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)
        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0, 0, 0))
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                main()


pygame.init()
pygame.display.set_caption("EmeuJam")

menu(death_count=0)
