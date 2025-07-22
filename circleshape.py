# circleshape.py - Base class for circular game objects (player, asteroids, shots)
import pygame  # For sprite and vector math
from constants import *

# --- Polygon collision utilities ---
def polygons_collide(poly1, poly2):
    # poly1 and poly2 are lists of (x, y) tuples
    for polygon in [poly1, poly2]:
        for i1, p1 in enumerate(polygon):
            i2 = (i1 + 1) % len(polygon)
            p2 = polygon[i2]
            # Get the edge vector
            edge = (p2[0] - p1[0], p2[1] - p1[1])
            # Get the perpendicular axis
            axis = (-edge[1], edge[0])
            # Project both polygons onto the axis
            min1, max1 = project_polygon(axis, poly1)
            min2, max2 = project_polygon(axis, poly2)
            # Check for overlap
            if max1 < min2 or max2 < min1:
                return False  # Separating axis found
    return True  # No separating axis found, polygons collide

def project_polygon(axis, polygon):
    dots = [axis[0]*p[0] + axis[1]*p[1] for p in polygon]
    return min(dots), max(dots)

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
        # Use polygon collision if both have get_absolute_points, else fallback to circle
        if hasattr(self, 'get_absolute_points') and hasattr(other, 'get_absolute_points'):
            return polygons_collide(self.get_absolute_points(), other.get_absolute_points())
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
