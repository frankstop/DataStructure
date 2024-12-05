import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from boids_simulation import BoidSimulation
import numpy as np

# Parameters for the simulation
params = {
    "visual_range": 75,
    "protected_range": 20,
    "centering_factor": 0.005,
    "avoid_factor": 0.05,
    "matching_factor": 0.05,
    "max_speed": 10,
    "min_speed": 2
}

# Simulation dimensions and number of boids
width, height = 800, 600
num_boids = 50

# Create the simulation
simulation = BoidSimulation(num_boids, width, height, params)

# Visualization setup
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(0, width)
ax.set_ylim(0, height)
ax.axis('off')  # Hide axes for a cleaner look

# Initialize scatter plot for boids
boid_scatter = ax.scatter([], [], s=50, c="blue", marker="o")

def init():
    """Initialize the animation."""
    # Provide an empty 2D array for set_offsets() during initialization
    boid_scatter.set_offsets(np.empty((0, 2)))
    return (boid_scatter,)

def update(frame):
    """Update boid positions and animation frame."""
    simulation.update()
    
    # Wrap boids around the screen (torus wrapping)
    for boid in simulation.boids:
        boid.x %= width
        boid.y %= height

    # Update scatter plot with new boid positions
    positions = np.array([(boid.x, boid.y) for boid in simulation.boids])
    boid_scatter.set_offsets(positions)
    return (boid_scatter,)

# Create animation
ani = FuncAnimation(
    fig, update, init_func=init, frames=200, interval=50, blit=True
)

plt.show()