import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
from boids_simulation import BoidSimulation
import numpy as np

# PARAMETERS (Set all adjustable options here)
params = {
    # Boid Behavior
    "visual_range": 75,          # How far a boid can see other boids
    "protected_range": 20,       # How close is "too close" (avoidance range)
    "centering_factor": 0.005,   # How strongly boids move to the center of their neighbors
    "avoid_factor": 0.05,        # How strongly boids avoid close neighbors
    "matching_factor": 0.05,     # How strongly boids match velocities with neighbors

    # Speed Limits
    "max_speed": 10,             # Maximum speed a boid can reach
    "min_speed": 2,              # Minimum speed to prevent boids from stopping

    # World Settings
    "width": 400,                # Width of the simulation area
    "height": 300,               # Height of the simulation area
    "num_boids": 150              # Number of boids in the simulation
}

# Create the simulation
simulation = BoidSimulation(params["num_boids"], params["width"], params["height"], params)

# Visualization setup
plt.rcParams['toolbar'] = 'none'  # Disable toolbar
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(0, params["width"])
ax.set_ylim(0, params["height"])
ax.axis('off')  # Hide axes for a cleaner look

# Initialize scatter plot for boids
boid_scatter = ax.scatter([], [], s=50, c="blue", marker="o")
mouse_marker, = ax.plot([], [], 'ro', markersize=10, label="Mouse Boid")  # Red marker for the mouse boid

# Initialize mouse position and state
mouse_position = None  # None means mouse is outside the screen

# Add slider for speed control
slider_ax = plt.axes([0.2, 0.02, 0.6, 0.03])  # Position: [left, bottom, width, height]
speed_slider = Slider(slider_ax, "Speed", 0.1, 2.0, valinit=1.0)

def on_mouse_move(event):
    """Update mouse position when inside the plot."""
    global mouse_position
    if event.inaxes == ax:
        mouse_position = np.array([event.xdata, event.ydata])
    else:
        mouse_position = None  # Mouse is outside the plot area

# Connect mouse motion event to the figure
fig.canvas.mpl_connect('motion_notify_event', on_mouse_move)

def init():
    """Initialize the animation."""
    boid_scatter.set_offsets(np.empty((0, 2)))
    mouse_marker.set_data([], [])  # Start with no mouse marker
    return boid_scatter, mouse_marker

def update(frame):
    """Update boid positions and animation frame."""
    simulation.update()
    
    # Incorporate the mouse boid into the simulation if it's on the screen
    if mouse_position is not None:
        for boid in simulation.boids:
            dx = mouse_position[0] - boid.x
            dy = mouse_position[1] - boid.y
            distance_squared = dx**2 + dy**2

            if distance_squared < params['visual_range']**2:
                if distance_squared < params['protected_range']**2:
                    boid.vx -= dx * params['avoid_factor']
                    boid.vy -= dy * params['avoid_factor']
                else:
                    boid.vx += (mouse_position[0] - boid.x) * params['centering_factor']
                    boid.vy += (mouse_position[1] - boid.y) * params['centering_factor']

    # Wrap boids around the screen (torus wrapping)
    for boid in simulation.boids:
        boid.x %= params["width"]
        boid.y %= params["height"]

    # Scale boid velocities based on the slider
    speed_factor = speed_slider.val
    for boid in simulation.boids:
        boid.vx *= speed_factor
        boid.vy *= speed_factor

    # Update scatter plot with new boid positions
    positions = np.array([(boid.x, boid.y) for boid in simulation.boids])
    boid_scatter.set_offsets(positions)

    # Update mouse marker if the mouse is on the screen
    if mouse_position is not None:
        mouse_marker.set_data([mouse_position[0]], [mouse_position[1]])
    else:
        mouse_marker.set_data([], [])

    return boid_scatter, mouse_marker

# Create animation
ani = FuncAnimation(
    fig, update, init_func=init, frames=200, interval=16, blit=True  # Smooth animation
)

plt.show()