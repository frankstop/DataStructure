import numpy as np

class Boid:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

class BoidSimulation:
    def __init__(self, num_boids, width, height, params):
        self.boids = [Boid(
            np.random.uniform(0, width),
            np.random.uniform(0, height),
            np.random.uniform(-1, 1),
            np.random.uniform(-1, 1)
        ) for _ in range(num_boids)]
        
        self.width = width
        self.height = height
        self.params = params

    def update(self):
        for boid in self.boids:
            xpos_avg, ypos_avg, xvel_avg, yvel_avg = 0, 0, 0, 0
            close_dx, close_dy = 0, 0
            neighboring_boids = 0

            for other in self.boids:
                if boid == other:
                    continue

                dx = boid.x - other.x
                dy = boid.y - other.y
                distance_squared = dx**2 + dy**2

                if distance_squared < self.params['visual_range']**2:
                    if distance_squared < self.params['protected_range']**2:
                        close_dx += dx
                        close_dy += dy
                    else:
                        xpos_avg += other.x
                        ypos_avg += other.y
                        xvel_avg += other.vx
                        yvel_avg += other.vy
                        neighboring_boids += 1
            
            if neighboring_boids > 0:
                xpos_avg /= neighboring_boids
                ypos_avg /= neighboring_boids
                xvel_avg /= neighboring_boids
                yvel_avg /= neighboring_boids

                boid.vx += (xpos_avg - boid.x) * self.params['centering_factor']
                boid.vy += (ypos_avg - boid.y) * self.params['centering_factor']
                boid.vx += (xvel_avg - boid.vx) * self.params['matching_factor']
                boid.vy += (yvel_avg - boid.vy) * self.params['matching_factor']

            boid.vx += close_dx * self.params['avoid_factor']
            boid.vy += close_dy * self.params['avoid_factor']

            if boid.x < 0 or boid.x > self.width:
                boid.vx *= -1
            if boid.y < 0 or boid.y > self.height:
                boid.vy *= -1

            speed = np.sqrt(boid.vx**2 + boid.vy**2)
            if speed > self.params['max_speed']:
                boid.vx = (boid.vx / speed) * self.params['max_speed']
                boid.vy = (boid.vy / speed) * self.params['max_speed']

            if speed < self.params['min_speed']:
                boid.vx = (boid.vx / speed) * self.params['min_speed']
                boid.vy = (boid.vy / speed) * self.params['min_speed']

            boid.x += boid.vx
            boid.y += boid.vy