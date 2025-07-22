# player.py - Defines the Player class for the game
import pygame  # For graphics and input
from constants import *  # Game constants
from circleshape import CircleShape  # Base class for circular game objects
from shot import Shot  # Shot (bullet) class


class Player(CircleShape):
    def __init__(self, x, y):
        # Initialize player at (x, y) with a set radius
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0  # Player's facing direction
        self.shot_cooldown = 0  # Time until next shot allowed
        self.velocity = pygame.Vector2(0, 0)  # Ensure velocity is initialized
        self.acceleration = pygame.Vector2(0, 0)  # For acceleration-based movement

    def draw(self, screen):
        # Draw the player as a triangle (spaceship)
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def triangle(self):
        # Calculate the three points of the player's triangle
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def get_absolute_points(self):
        # Return the triangle points for polygon collision
        return [tuple(p) for p in self.triangle()]

    def update(self, dt):
        # Handle player input and update state
        keys = pygame.key.get_pressed()
        self.shot_cooldown -= dt

        # Acceleration logic
        if keys[pygame.K_w]:
            forward = pygame.Vector2(0, 1).rotate(self.rotation)
            self.acceleration = forward * PLAYER_ACCELERATION
        elif keys[pygame.K_s]:
            backward = pygame.Vector2(0, -1).rotate(self.rotation)
            self.acceleration = backward * PLAYER_ACCELERATION
        else:
            self.acceleration = pygame.Vector2(0, 0)

        # Update velocity and apply friction
        self.velocity += self.acceleration * dt
        self.velocity *= PLAYER_FRICTION

        # Update position
        self.position += self.velocity * dt

        # Rotation
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

        # Screen wrapping
        self.wrap_position()

    def shoot(self):
        # Fire a shot if cooldown has elapsed
        if self.shot_cooldown > 0:
            return
        self.shot_cooldown = PLAYER_SHOOT_COOLDOWN
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        # Ensure shot is used so linter does not complain
        return shot

    def rotate(self, dt):
        # Rotate the player
        self.rotation += PLAYER_TURN_SPEED * dt
