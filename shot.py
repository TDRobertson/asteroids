# shot.py - Defines the Shot (bullet) class for the game
import pygame  # For graphics and vector math
from constants import *  # Game constants
from circleshape import CircleShape  # Base class for circular game objects


class Shot(CircleShape):
    def __init__(self, x, y):
        # Initialize shot at (x, y) with a set radius
        super().__init__(x, y, SHOT_RADIUS)

    def draw(self, screen):
        # Draw the shot as a white circle
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        # Move the shot according to its velocity and delta time
        self.position += self.velocity * dt
        # Remove the shot if it leaves the screen
        if (self.position.x < -self.radius or self.position.x > SCREEN_WIDTH + self.radius or
            self.position.y < -self.radius or self.position.y > SCREEN_HEIGHT + self.radius):
            self.kill()
