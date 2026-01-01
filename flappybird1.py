import pygame
from sys import exit
import random

pygame.init()

GAME_WIDTH = 360
GAME_HEIGHT = 640

window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

def load_font(size):
    try:
        return pygame.font.Font("font/PressStart2P.ttf", size)
    except:
        return pygame.font.SysFont("arial", size, bold=True)

background_image = pygame.image.load("flappybirdbg.png")

bird_width, bird_height = 34, 24
bird_image = pygame.image.load("flappybird.png")
bird_image = pygame.transform.scale(bird_image, (bird_width, bird_height))

pipe_width, pipe_height = 64, 512

top_pipe_image = pygame.transform.scale(
    pygame.image.load("toppipe.png"),
    (pipe_width, pipe_height)
)

bottom_pipe_image = pygame.transform.scale(
    pygame.image.load("bottompipe.png"),
    (pipe_width, pipe_height)
)

bird_x = GAME_WIDTH // 8
bird_y = GAME_HEIGHT // 2

class Bird(pygame.Rect):
    def __init__(self):
        super().__init__(bird_x, bird_y, bird_width, bird_height)
        self.img = bird_image

class Pipe(pygame.Rect):
    def __init__(self, img):
        super().__init__(GAME_WIDTH, 0, pipe_width, pipe_height)
        self.img = img
        self.passed = False

bird = Bird()
pipes = []

velocity_y = 0
gravity = 0.4
velocity_x = -2
score = 0
game_state = "start"

def draw_panel(x, y, w, h):
    panel = pygame.Surface((w, h))
    panel.set_alpha(180)
    panel.fill((0, 0, 0))
    window.blit(panel, (x, y))
    pygame.draw.rect(window, (255, 255, 255), (x, y, w, h), 2)

def draw():
    window.blit(background_image, (0, 0))

    for pipe in pipes:
        window.blit(pipe.img, pipe)

    window.blit(bird.img, bird)

    score_font = load_font(14)
    score_text = score_font.render(str(int(score)), True, (255, 255, 255))
    window.blit(score_text, (10, 10))

def draw_start_screen():
    window.blit(background_image, (0, 0))
    window.blit(bird.img, bird)

    draw_panel(40, 160, GAME_WIDTH - 80, 260)

    title_font = load_font(22)
    title = title_font.render("FLAPPY BIRD", True, (255, 255, 0))
    window.blit(title, title.get_rect(center=(GAME_WIDTH // 2, 210)))

    info_font = load_font(11)
    info = info_font.render("PRESS SPACE TO START", True, (255, 255, 255))
    window.blit(info, info.get_rect(center=(GAME_WIDTH // 2, 270)))

    control_font = load_font(8)
    control = control_font.render("SPACE / X / UP : FLY", True, (200, 200, 200))
    window.blit(control, control.get_rect(center=(GAME_WIDTH // 2, 310)))

def draw_game_over_screen():
    window.blit(background_image, (0, 0))

    for pipe in pipes:
        window.blit(pipe.img, pipe)

    window.blit(bird.img, bird)

    draw_panel(40, 170, GAME_WIDTH - 80, 280)

    over_font = load_font(20)
    over = over_font.render("GAME OVER", True, (255, 80, 80))
    window.blit(over, over.get_rect(center=(GAME_WIDTH // 2, 210)))

    score_font = load_font(14)
    score_text = score_font.render(f"SCORE : {int(score)}", True, (255, 255, 255))
    window.blit(score_text, score_text.get_rect(center=(GAME_WIDTH // 2, 260)))

    restart_font = load_font(9)
    restart = restart_font.render("PRESS SPACE TO RESTART", True, (200, 200, 200))
    window.blit(restart, restart.get_rect(center=(GAME_WIDTH // 2, 320)))

def move():
    global velocity_y, score, game_state

    velocity_y += gravity
    bird.y += velocity_y
    bird.y = max(bird.y, 0)

    if bird.y > GAME_HEIGHT:
        game_state = "game_over"

    for pipe in pipes:
        pipe.x += velocity_x

        if not pipe.passed and bird.x > pipe.x + pipe.width:
            score += 0.5
            pipe.passed = True

        if bird.colliderect(pipe):
            game_state = "game_over"

    while pipes and pipes[0].x < -pipe_width:
        pipes.pop(0)

def create_pipes():
    gap = GAME_HEIGHT // 4
    top_y = -pipe_height // 2 - random.randint(0, pipe_height // 2)

    top_pipe = Pipe(top_pipe_image)
    top_pipe.y = top_y

    bottom_pipe = Pipe(bottom_pipe_image)
    bottom_pipe.y = top_pipe.y + pipe_height + gap

    pipes.extend([top_pipe, bottom_pipe])

PIPE_EVENT = pygame.USEREVENT
pygame.time.set_timer(PIPE_EVENT, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == PIPE_EVENT and game_state == "playing":
            create_pipes()

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_x, pygame.K_UP):
                if game_state == "start":
                    game_state = "playing"
                    velocity_y = -6
                elif game_state == "playing":
                    velocity_y = -6
                elif game_state == "game_over":
                    bird.y = bird_y
                    velocity_y = 0
                    pipes.clear()
                    score = 0
                    game_state = "start"

    if game_state == "start":
        draw_start_screen()
    elif game_state == "playing":
        move()
        draw()
    elif game_state == "game_over":
        draw_game_over_screen()

    pygame.display.update()
    clock.tick(60)
