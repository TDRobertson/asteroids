# asteroid.py - Defines the Asteroid class for the game
import pygame  # For graphics and vector math
import random  # For randomizing asteroid splits
import math  # For trigonometric functions
from constants import *  # Game constants
from circleshape import CircleShape  # Base class for circular game objects


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        # Initialize asteroid at (x, y) with given radius
        super().__init__(x, y, radius)
        self.lumpy_points = self.generate_lumpy_shape()

    def generate_lumpy_shape(self, num_points=12, lumpiness=0.4):
        # Generate a list of points for a lumpy asteroid polygon
        points = []
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            rand_radius = self.radius * (1 + random.uniform(-lumpiness, lumpiness))
            x = math.cos(angle) * rand_radius
            y = math.sin(angle) * rand_radius
            points.append((x, y))
        return points

    def get_absolute_points(self):
        px = float(getattr(self.position, 'x', 0.0))
        py = float(getattr(self.position, 'y', 0.0))
        return [(px + x, py + y) for (x, y) in self.lumpy_points]

    def draw(self, screen):
        # Calculate the absolute positions of the lumpy points
        abs_points = self.get_absolute_points()
        pygame.draw.polygon(screen, "white", abs_points, 2)

    def update(self, dt):
        # Move the asteroid according to its velocity and delta time
        self.position += self.velocity * dt
        self.wrap_position()

    def split(self):
        # Remove this asteroid from all groups
        self.kill()

        # If the asteroid is too small, do not split further
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        # Randomize the angle of the split for variety
        random_angle = random.uniform(20, 50)

        a = self.velocity.rotate(random_angle)
        b = self.velocity.rotate(-random_angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS
        # Ensure containers are set for new asteroids
        Asteroid.containers = getattr(self, 'containers', ())
        x = getattr(self.position, 'x', 0.0)
        y = getattr(self.position, 'y', 0.0)
        asteroid1 = Asteroid(x, y, new_radius)
        asteroid1.velocity = a * 1.2
        asteroid2 = Asteroid(x, y, new_radius)
        asteroid2.velocity = b * 1.2
