import pygame
import random
import math
from PIL import Image, ImageDraw, ImageFont

# Initialize pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 1200
NUM_EMOJIS = 50
EMOJI_SIZE = 40

# Colors
BACKGROUND_COLOR = (30, 30, 30)

# Emojis to render
EMOJIS = ["😀", "🎉", "🌟", "🔥", "🍕", "🐱", "🚀", "🌍"]

# Initialize screen
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("BSP Tree Emoji Renderer")

# Generate random positions for emojis
emoji_data = [
    {
        "emoji": random.choice(EMOJIS),
        "position": (random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)),
    }
    for _ in range(NUM_EMOJIS)
]

def create_emoji_surface(emoji, size):
    font_path = "/System/Library/Fonts/Apple Color Emoji.ttc"  # Path to .ttc file
    font = ImageFont.truetype(font_path, size, index=0)  # Use font face index 0
    img = Image.new("RGBA", (size, size), (255, 255, 255, 0))  # Transparent background
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), emoji, font=font, fill=(255, 255, 255, 255))  # Draw emoji
    return pygame.image.fromstring(img.tobytes(), img.size, img.mode)

# Create surfaces for emojis
emoji_surfaces = [
    {
        "surface": create_emoji_surface(data["emoji"], EMOJI_SIZE),
        "position": data["position"],
    }
    for data in emoji_data
]

# BSP Node class
class BSPNode:
    def __init__(self, x, y, surface, left=None, right=None):
        self.x = x
        self.y = y
        self.surface = surface
        self.left = left
        self.right = right

    def insert(self, obj_x, obj_y, obj_surface):
        if obj_x < self.x:
            if self.left is None:
                self.left = BSPNode(obj_x, obj_y, obj_surface)
            else:
                self.left.insert(obj_x, obj_y, obj_surface)
        else:
            if self.right is None:
                self.right = BSPNode(obj_x, obj_y, obj_surface)
            else:
                self.right.insert(obj_x, obj_y, obj_surface)

    def is_visible(self, viewer_x, viewer_y):
        distance = math.sqrt((self.x - viewer_x) ** 2 + (self.y - viewer_y) ** 2)
        return max(0, 1 - distance / max(WINDOW_WIDTH, WINDOW_HEIGHT))  # Opacity based on distance

# Build a BSP tree
def build_bsp_tree(objects):
    if not objects:
        return None
    median = len(objects) // 2
    x, y, surface = objects[median]
    node = BSPNode(x, y, surface)
    node.left = build_bsp_tree(objects[:median])
    node.right = build_bsp_tree(objects[median + 1 :])
    return node

# Prepare emoji data and build BSP tree
sorted_positions = sorted(
    [(e["position"][0], e["position"][1], e["surface"]) for e in emoji_surfaces], key=lambda p: p[0]
)
bsp_tree = build_bsp_tree(sorted_positions)

# Render emojis based on visibility
def render_emojis(tree, viewer_x, viewer_y):
    if tree is None:
        return
    opacity = tree.is_visible(viewer_x, viewer_y)
    x, y = tree.x, tree.y
    if opacity > 0:
        surface = tree.surface.copy()
        surface.set_alpha(int(opacity * 255))
        screen.blit(surface, (x, y))
    render_emojis(tree.left, viewer_x, viewer_y)
    render_emojis(tree.right, viewer_x, viewer_y)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get mouse position as viewer position
    viewer_x, viewer_y = pygame.mouse.get_pos()

    # Clear screen
    screen.fill(BACKGROUND_COLOR)

    # Render emojis based on viewer position
    render_emojis(bsp_tree, viewer_x, viewer_y)

    pygame.display.flip()

pygame.quit()