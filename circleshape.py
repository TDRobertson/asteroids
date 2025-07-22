# circleshape.py - Base class for circular game objects (player, asteroids, shots)
import pygame  # For sprite and vector math
from constants import *

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # Add to containers if defined, else just initialize as a sprite
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.position = pygame.Vector2(x, y)  # Position in the game world
        self.velocity = pygame.Vector2(0, 0)  # Velocity vector
        self.radius = radius  # Collision/drawing radius

    def draw(self, screen):
        # Must be overridden by subclasses to draw the object
        pass

    def update(self, dt):
        # Must be overridden by subclasses to update the object
        pass

    def collides_with(self, other):
        # Check collision with another circular object
        return self.position.distance_to(other.position) <= self.radius + other.radius

    def wrap_position(self):
        # Wrap the object around the screen if its center is completely outside (using radius)
        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius
        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius
