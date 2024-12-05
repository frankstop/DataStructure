import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from boids_simulation import BoidSimulation

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
boid_points, = ax.plot([], [], 'bo', markersize=4)

def update(frame):
    simulation.update()
    x_coords = [boid.x for boid in simulation.boids]
    y_coords = [boid.y for boid in simulation.boids]
    boid_points.set_data(x_coords, y_coords)
    return boid_points,

ani = FuncAnimation(fig, update, frames=200, interval=50, blit=True)
plt.show()