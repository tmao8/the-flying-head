import pygame
import sys
import random

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flying Head Escape")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

clock = pygame.time.Clock()
FPS = 60

BACKGROUND_IMG = pygame.image.load("images/background.png").convert()
BACKGROUND_IMG = pygame.transform.scale(BACKGROUND_IMG, (WIDTH, HEIGHT))

FLYING_HEAD_IMG = pygame.image.load("images/flying_head.png").convert_alpha()
FLYING_HEAD_IMG = pygame.transform.scale(FLYING_HEAD_IMG, (125, 100))

COAL_TRAP_IMG = pygame.image.load("images/coal.png").convert_alpha()
COAL_TRAP_IMG = pygame.transform.scale(COAL_TRAP_IMG, (100, 75))

OBSTACLE_IMG = pygame.image.load("images/tree.png").convert_alpha()
OBSTACLE_IMG = pygame.transform.scale(OBSTACLE_IMG, (100, 125))

ACORN_IMG = pygame.image.load("images/acorn.png").convert_alpha()
ACORN_IMG = pygame.transform.scale(ACORN_IMG, (50, 50))

flying_head = pygame.Rect(100, HEIGHT // 2, 100, 100)
flying_head_velocity = 0
FLAP_STRENGTH = -8
gravity = 0.5

obstacles = []
coal_traps = []
acorns = []
SPAWN_RATE = 1500
last_spawn_time = pygame.time.get_ticks()

# Score
score = 0
font = pygame.font.Font(None, 36)

def spawn_obstacle():
    y_pos = random.randint(100, HEIGHT - 100)
    obstacle = pygame.Rect(WIDTH, y_pos, 50, 10)
    y_pos = random.randint(100, HEIGHT - 100)
    coal_trap = pygame.Rect(WIDTH + random.randint(100, 200), y_pos + random.randint(-50, 50), 30, 30)
    y_pos = random.randint(100, HEIGHT - 100)
    acorn = pygame.Rect(WIDTH + random.randint(200, 300), y_pos + random.randint(-100, 100), 20, 20)
    obstacles.append(obstacle)
    coal_traps.append(coal_trap)
    acorns.append(acorn)

def draw_text(text, x, y):
    render = font.render(text, True, WHITE)
    screen.blit(render, (x, y))

TITLE_IMG = pygame.Surface((WIDTH, HEIGHT)) 
TITLE_IMG.fill((50, 50, 100))

def draw_text(text, y, center_x=True):
    render = font.render(text, True, WHITE)
    text_rect = render.get_rect()
    if center_x:
        text_rect.center = (WIDTH // 2, y)
    else:
        text_rect.topleft = (10, y)
    screen.blit(render, text_rect)

def show_title_screen():
    """
    Displays the title screen with introductory text.
    """
    while True:
        screen.fill(BLACK)
        screen.blit(TITLE_IMG, (0, 0))
        
        draw_text("Flying Head Escape", HEIGHT // 4)
        draw_text("You are the Flying Head.", HEIGHT // 2 - 100)
        draw_text("After getting tricked into eating burning coal, you are in deep pain.", HEIGHT // 2 - 50)
        draw_text("As you run into the forest, there are obstacles, burning coals, and acorns.", HEIGHT // 2)
        draw_text("Consume acorns to earn points. However, consuming anything else will result in death!", HEIGHT // 2 + 50)
        draw_text("Reach a score of 10 to escape victorious and continue terrorizing the village.", HEIGHT // 2 + 100)
        draw_text("Press SPACE to Begin, and press SPACE to jump", HEIGHT // 2 + 150)
        
        pygame.display.flip()
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

show_title_screen()

# Game Loop
running = True
while running:
    screen.blit(BACKGROUND_IMG, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                flying_head_velocity = FLAP_STRENGTH

    flying_head_velocity += gravity
    flying_head.y += int(flying_head_velocity)

    if flying_head.top < 0 or flying_head.bottom > HEIGHT:
        draw_text("You Lost!", HEIGHT // 2)
        pygame.display.flip()
        pygame.time.delay(2000)
        running = False

    if pygame.time.get_ticks() - last_spawn_time > SPAWN_RATE:
        spawn_obstacle()
        last_spawn_time = pygame.time.get_ticks()

    for obstacle in obstacles[:]:
        obstacle.x -= 5
        if obstacle.x + obstacle.width + 50 < 0:
            obstacles.remove(obstacle)

    for trap in coal_traps[:]:
        trap.x -= 5
        if trap.x + trap.width + 50 < 0:
            coal_traps.remove(trap)

    for acorn in acorns[:]:
        acorn.x -= 5
        if acorn.x + acorn.width + 50 < 0:
            acorns.remove(acorn)

    for obstacle in obstacles:
        if flying_head.colliderect(obstacle):
            draw_text("You Lost!", HEIGHT // 2)
            pygame.display.flip()
            pygame.time.delay(2000)
            running = False

    for trap in coal_traps:
        if flying_head.colliderect(trap):
            draw_text("You Lost!", HEIGHT // 2)
            pygame.display.flip()
            pygame.time.delay(2000)
            running = False

    for acorn in acorns:
        if flying_head.colliderect(acorn):
            acorns.remove(acorn)
            score += 1

    if score >= 10:
        draw_text("You Win!", HEIGHT // 2)
        pygame.display.flip()
        pygame.time.delay(2000)
        running = False

    screen.blit(FLYING_HEAD_IMG, flying_head.topleft)

    for obstacle in obstacles:
        screen.blit(OBSTACLE_IMG, obstacle.topleft)

    for trap in coal_traps:
        screen.blit(COAL_TRAP_IMG, trap.topleft)

    for acorn in acorns:
        screen.blit(ACORN_IMG, acorn.topleft)

    draw_text(f"Score: {score}", 10, 10)

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()
