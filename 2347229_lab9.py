import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 1000
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jet Plane Bombing Game")

# Load images (resized)
background_image = pygame.transform.scale(pygame.image.load("backgroundimage.jpg"), (screen_width, screen_height))  # Load background image
rocket_image = pygame.transform.scale(pygame.image.load("rocket3.png"), (200, 200))  # Adjusted orientation
bomb_image = pygame.transform.scale(pygame.image.load("bomb.png"), (30, 30))
house_image = pygame.transform.scale(pygame.image.load("house.png"), (100, 100))
explosion_image = pygame.transform.scale(pygame.image.load("blast.png"), (100, 100))

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Define constants
JET_SPEED = 5
BOMB_SPEED = 8
BOMB_DROP_FREQUENCY = 0.02  # Adjust this value to control bomb drop frequency

# Define classes
class Jet:
    def __init__(self):
        self.x = screen_width // 2 - 25  # Adjusted the position
        self.y = 0

    def move(self, direction):
        if direction == "left":
            self.x -= JET_SPEED
        elif direction == "right":
            self.x += JET_SPEED

        # Restrict jet movement within the screen boundaries
        self.x = max(0, min(self.x, screen_width - 50))

    def draw(self):
        screen.blit(rocket_image, (self.x, self.y))

class Bomb:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hit_house = False  # Flag to track whether the bomb hit the house

    def move(self):
        self.y += BOMB_SPEED  # Adjusted the bomb's movement direction

    def draw(self):
        if not self.hit_house:
            screen.blit(bomb_image, (self.x, self.y))

    def check_collision(self, house):
        if (self.y >= house.y) and (house.x < self.x < house.x + 100):
            self.hit_house = True

class House:
    def __init__(self):
        self.x = screen_width // 2 - 50
        self.y = screen_height - 100  # Adjusted the position to the bottom of the screen

    def draw(self):
        screen.blit(house_image, (self.x, self.y))

def draw_buttons():
    # Start button
    pygame.draw.rect(screen, GREEN, (50, 50, 100, 50))
    start_font = pygame.font.SysFont(None, 30)
    start_text = start_font.render("Start", True, BLACK)
    screen.blit(start_text, (80, 65))

    # Stop button
    pygame.draw.rect(screen, RED, (200, 50, 100, 50))
    stop_font = pygame.font.SysFont(None, 30)
    stop_text = stop_font.render("Stop", True, BLACK)
    screen.blit(stop_text, (240, 65))

def draw_game_over():
    font = pygame.font.SysFont(None, 100)
    text = font.render("Game Over", True, RED)
    screen.blit(text, (screen_width // 2 - 200, screen_height // 2 - 50))

def draw_score(score):
    font = pygame.font.SysFont(None, 40)
    score_text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(score_text, (50, 20))

# Create game objects
jet = Jet()
house = House()
bombs = []
score = 0
running = False
game_over = False

# Game loop
clock = pygame.time.Clock()

while not game_over:
    screen.blit(background_image, (0, 0))  # Blit the background image

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                jet.move("left")
            elif event.key == pygame.K_RIGHT:
                jet.move("right")
            elif event.key == pygame.K_SPACE:
                if running:
                    bombs.append(Bomb(jet.x + 20, jet.y))  # Adjust the position to match jet's center
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if not running:
                if 50 <= mouse_pos[0] <= 150 and 50 <= mouse_pos[1] <= 100:
                    running = True
            else:
                if 200 <= mouse_pos[0] <= 300 and 50 <= mouse_pos[1] <= 100:
                    running = False

    if running:
        # Drop bombs randomly
        if random.random() < BOMB_DROP_FREQUENCY:
            bombs.append(Bomb(random.randint(0, screen_width - 20), 0))

        # Move and draw bombs
        for bomb in bombs:
            bomb.move()
            bomb.draw()
            bomb.check_collision(house)

            # Increment score if bomb doesn't hit the house
            if not bomb.hit_house and bomb.y >= screen_height:
                score += 1

        # Draw the house
        house.draw()

        # Draw the jet
        jet.draw()

    draw_buttons()
    draw_score(score)
    if any(bomb.hit_house for bomb in bombs):  # Check if any bomb hit the house
        screen.blit(explosion_image, (house.x, house.y))
        draw_game_over()
        pygame.display.flip()
        pygame.time.wait(2000)  # Wait for 2 seconds after game over before closing the window
        game_over = True

    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
