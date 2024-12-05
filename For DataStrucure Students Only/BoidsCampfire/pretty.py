import pygame
import random
import sys
import math  # For potential future enhancements like smooth movements

# Initialize Pygame
pygame.init()

# Configuration Class
class Config:
    # Screen Settings
    WIDTH = 1600
    HEIGHT = 1200
    BACKGROUND_COLOR = (30, 30, 30)
    FPS = 60

    # Campfire Settings
    CAMPFIRE_IMAGE_PATH = 'myFire.png'  # Path to your campfire image
    CAMPFIRE_SCALE = (400, 300)         # Scale of the campfire image
    CAMPFIRE_OFFSET_Y = 100              # Distance from the bottom

    # Ember Settings
    EMBER_IMAGE_PATH = 'Ember.png'      # Path to your ember image
    EMBER_SCALE = (50, 50)              # Scale of the ember image
    MAX_OPACITY = 230                   # Maximum alpha value for embers (0 to 255)
    MAX_LIFETIME = 250                  # Maximum lifetime for embers

    # Burst Settings
    BURST_TYPES = {
        'small': {'num': 20, 'velocity_range': (-1, 1, -3, -1), 'lifetime_range': (100, 150)},
        'medium': {'num': 50, 'velocity_range': (-2, 2, -4, -2), 'lifetime_range': (150, 200)},
        'big': {'num': 80, 'velocity_range': (-3, 3, -5, -3), 'lifetime_range': (200, 250)},
    }
    BURST_INTERVALS = {
        'small': 3000,   # milliseconds
        'medium': 7000,
        'big': 11000,
    }

    # Ember Generation Settings
    NUM_CONTINUOUS_EMBERS = 100
    CONTINUOUS_EMBER_VX_RANGE = (-1, 1)
    CONTINUOUS_EMBER_VY_RANGE = (-3, -1)
    CONTINUOUS_EMBER_LIFETIME_RANGE = (100, 200)
    CONTINUOUS_EMBER_OFFSET_X = 30
    CONTINUOUS_EMBER_OFFSET_Y = 50

    # Movement Scalars
    HEIGHT_SCALAR = 1.0    # Controls vertical movement
    ALIGNMENT_SCALAR = 1.0 # Controls horizontal spread

    # Maximum Number of Embers
    MAX_BOIDS = 500        # Prevents unlimited growth of embers

# Initialize Screen
screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
pygame.display.set_caption("Campfire with Embers and Bursts")

# Load and Scale Images
def load_and_scale_image(path, scale):
    try:
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, scale)
    except pygame.error as e:
        print(f"Unable to load image '{path}': {e}")
        pygame.quit()
        sys.exit()

fire_image = load_and_scale_image(Config.CAMPFIRE_IMAGE_PATH, Config.CAMPFIRE_SCALE)
particle_image = load_and_scale_image(Config.EMBER_IMAGE_PATH, Config.EMBER_SCALE)

# Define Fire Position
fire_x = Config.WIDTH // 2
fire_y = Config.HEIGHT - Config.CAMPFIRE_OFFSET_Y
fire_rect = fire_image.get_rect(center=(fire_x, fire_y))

# Boid Class for Embers
class Boid:
    def __init__(self, x, y, vx, vy, lifetime):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.lifetime = lifetime  # Tracks ember fade-out

# Function to generate a burst of embers
def generate_burst(burst_type, origin_x, origin_y, embers):
    burst_config = Config.BURST_TYPES.get(burst_type)
    if not burst_config:
        return []

    num = burst_config['num']
    vx_min, vx_max, vy_min, vy_max = burst_config['velocity_range']
    lifetime_min, lifetime_max = burst_config['lifetime_range']

    new_embers = []
    for _ in range(num):
        # Check if adding a new ember exceeds MAX_BOIDS
        if len(embers) + len(new_embers) >= Config.MAX_BOIDS:
            break
        new_embers.append(Boid(
            origin_x + random.uniform(-Config.CONTINUOUS_EMBER_OFFSET_X, Config.CONTINUOUS_EMBER_OFFSET_X),
            origin_y - Config.CONTINUOUS_EMBER_OFFSET_Y,
            random.uniform(vx_min, vx_max) * Config.ALIGNMENT_SCALAR,
            random.uniform(vy_min, vy_max) * Config.HEIGHT_SCALAR,
            random.uniform(lifetime_min, lifetime_max)
        ))
    return new_embers

# Function to generate a single continuous ember
def generate_continuous_ember(origin_x, origin_y, embers):
    if len(embers) >= Config.MAX_BOIDS:
        return None  # Do not create more embers if at max

    return Boid(
        origin_x + random.uniform(-Config.CONTINUOUS_EMBER_OFFSET_X, Config.CONTINUOUS_EMBER_OFFSET_X),
        origin_y - Config.CONTINUOUS_EMBER_OFFSET_Y,
        random.uniform(*Config.CONTINUOUS_EMBER_VX_RANGE) * Config.ALIGNMENT_SCALAR,
        random.uniform(*Config.CONTINUOUS_EMBER_VY_RANGE) * Config.HEIGHT_SCALAR,
        random.uniform(*Config.CONTINUOUS_EMBER_LIFETIME_RANGE)
    )

# Initialize continuous embers
embers = []
for _ in range(Config.NUM_CONTINUOUS_EMBERS):
    ember = generate_continuous_ember(fire_x, fire_y, embers)
    if ember:
        embers.append(ember)

# Burst Timers
last_burst_times = {
    'small': pygame.time.get_ticks(),
    'medium': pygame.time.get_ticks(),
    'big': pygame.time.get_ticks(),
}

# Simulation Loop
clock = pygame.time.Clock()
running = True

while running:
    current_time = pygame.time.get_ticks()

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Add event handling for moving the campfire here if needed

    # Example: Move the campfire up and down with arrow keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        fire_y -= 5  # Move up
        # Ensure the campfire doesn't move off the screen
        fire_y = max(fire_y, Config.CAMPFIRE_OFFSET_Y)
    if keys[pygame.K_DOWN]:
        fire_y += 5  # Move down
        fire_y = min(fire_y, Config.HEIGHT - Config.CAMPFIRE_OFFSET_Y)
    # Update fire_rect position
    fire_rect.center = (fire_x, fire_y)

    # Fill Background
    screen.fill(Config.BACKGROUND_COLOR)

    # Draw static campfire image
    screen.blit(fire_image, fire_rect)

    # Handle bursts
    for burst_type, interval in Config.BURST_INTERVALS.items():
        if current_time - last_burst_times[burst_type] >= interval:
            new_bursts = generate_burst(burst_type, fire_x, fire_y, embers)
            embers.extend(new_bursts)
            last_burst_times[burst_type] = current_time

    # Update and draw embers
    for ember in embers[:]:
        # Update position
        ember.x += ember.vx
        ember.y += ember.vy
        ember.lifetime -= 1  # Reduce lifetime

        # Add randomness to simulate flicker
        ember.vx += random.uniform(-0.05, 0.05)
        ember.vy += random.uniform(-0.05, 0.05)

        # Calculate alpha based on lifetime and global opacity
        alpha = max(0, min(Config.MAX_OPACITY, int((ember.lifetime / Config.MAX_LIFETIME) * Config.MAX_OPACITY)))
        ember_image = particle_image.copy()
        ember_image.set_alpha(alpha)

        # Draw the ember
        screen.blit(ember_image, (int(ember.x), int(ember.y)))

        # Remove ember if lifetime is over or out of screen bounds
        if (ember.lifetime <= 0 or
            ember.y < 0 or ember.x < 0 or ember.x > Config.WIDTH):
            embers.remove(ember)
            # Replenish with a new continuous ember
            new_continuous = generate_continuous_ember(fire_x, fire_y, embers)
            if new_continuous:
                embers.append(new_continuous)

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(Config.FPS)

# Clean up
pygame.quit()
sys.exit()