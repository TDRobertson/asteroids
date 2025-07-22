# asteroid.py - Defines the Asteroid class for the game
import pygame  # For graphics and vector math
import random  # For randomizing asteroid splits
from constants import *  # Game constants
from circleshape import CircleShape  # Base class for circular game objects


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        # Initialize asteroid at (x, y) with given radius
        super().__init__(x, y, radius)

    def draw(self, screen):
        # Draw the asteroid as a white circle
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        # Move the asteroid according to its velocity and delta time
        self.position += self.velocity * dt

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
