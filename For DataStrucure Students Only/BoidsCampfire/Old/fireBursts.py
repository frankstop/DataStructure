import pygame
import numpy as np
import random

# Initialize Pygame
pygame.init()

# Screen Dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Campfire with Embers")

# Colors
BLACK = (0, 0, 0)
FIRE_COLOR = (255, 140, 0)  # Fire
EMBER_COLOR = (255, 69, 0)  # Ember
BACKGROUND_COLOR = (30, 30, 30)

# Opacity Parameter
OPACITY = 230  # Max alpha value for embers (0 to 255)

# Boid Class for Embers
class Boid:
    def __init__(self, x, y, vx, vy, lifetime):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.lifetime = lifetime  # Tracks ember fade-out

# Function to generate a burst of embers
def generate_burst(burst_type):
    if burst_type == 'small':
        num = 20
        velocity_range = (-1, 1, -3, -1)
        lifetime_range = (100, 150)
    elif burst_type == 'medium':
        num = 50
        velocity_range = (-2, 2, -4, -2)
        lifetime_range = (150, 200)
    elif burst_type == 'big':
        num = 80
        velocity_range = (-3, 3, -5, -3)
        lifetime_range = (200, 250)
    else:
        return []

    new_embers = []
    for _ in range(num):
        new_embers.append(Boid(
            WIDTH // 2 + random.uniform(-30, 30),  # Start near center
            HEIGHT - 50,  # Near bottom
            random.uniform(velocity_range[0], velocity_range[1]),  # vx
            random.uniform(velocity_range[2], velocity_range[3]),  # vy
            random.uniform(lifetime_range[0], lifetime_range[1])  # lifetime
        ))
    return new_embers

# Initialize embers
NUM_EMBERS = 100
embers = [Boid(
    WIDTH // 2 + random.uniform(-30, 30),  # Start near center
    HEIGHT - 50,  # Near bottom
    random.uniform(-1, 1),  # Random velocity
    random.uniform(-3, -1),
    random.uniform(100, 200)  # Random lifetime
) for _ in range(NUM_EMBERS)]

# Burst Timers (in milliseconds)
small_burst_interval = 3000  # 3 seconds
medium_burst_interval = 7000  # 7 seconds
big_burst_interval = 11000  # 11 seconds

# Initialize last burst times
last_small_burst = pygame.time.get_ticks()
last_medium_burst = pygame.time.get_ticks()
last_big_burst = pygame.time.get_ticks()

# Simulation Loop
clock = pygame.time.Clock()
running = True
while running:
    current_time = pygame.time.get_ticks()
    screen.fill(BACKGROUND_COLOR)

    # Draw static campfire
    pygame.draw.circle(screen, FIRE_COLOR, (WIDTH // 2, HEIGHT - 50), 30)

    # Handle bursts
    # Small burst every 3 seconds
    if current_time - last_small_burst >= small_burst_interval:
        embers.extend(generate_burst('small'))
        last_small_burst = current_time

    # Medium burst every 7 seconds
    if current_time - last_medium_burst >= medium_burst_interval:
        embers.extend(generate_burst('medium'))
        last_medium_burst = current_time

    # Big burst every 11 seconds
    if current_time - last_big_burst >= big_burst_interval:
        embers.extend(generate_burst('big'))
        last_big_burst = current_time

    # Update and draw embers
    for ember in embers[:]:
        # Update position
        ember.x += ember.vx
        ember.y += ember.vy
        ember.lifetime -= 1  # Reduce lifetime

        # Add randomness to simulate flicker
        ember.vx += random.uniform(-0.1, 0.1)
        ember.vy += random.uniform(-0.1, 0.1)

        # Ember color based on lifetime and global opacity
        alpha = max(0, int((ember.lifetime / 250) * OPACITY))  # Adjusted denominator for max lifetime
        ember_color = (EMBER_COLOR[0], EMBER_COLOR[1], EMBER_COLOR[2], alpha)

        # Draw ember as a fading circle
        s = pygame.Surface((6, 6), pygame.SRCALPHA)  # Create a surface for transparency
        pygame.draw.circle(s, ember_color, (3, 3), 3)
        screen.blit(s, (int(ember.x), int(ember.y)))

        # Remove ember if burned out or out of screen bounds
        if ember.lifetime <= 0 or ember.y < 0:
            embers.remove(ember)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()