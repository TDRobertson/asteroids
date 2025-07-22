# main.py - Main entry point for the Asteroids game
# Imports
import sys  # For system exit
import pygame  # For game graphics and input
from constants import *  # Game constants
from player import Player  # Player class
from asteroid import Asteroid  # Asteroid class
from asteroidfield import AsteroidField  # Asteroid field manager
from shot import Shot  # Shot (bullet) class


def main():
    # Initialize pygame and set up the display
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Sprite groups for update/draw logic
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # Assign containers for each sprite type
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()  # Manages asteroid spawning

    Player.containers = (updatable, drawable)

    # Create the player at the center of the screen
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    dt = 0  # Delta time for frame updates

    # Main game loop
    while True:
        # Handle events (e.g., window close)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Update all updatable sprites
        updatable.update(dt)

        # Check for collisions between asteroids and player/shots
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                print("Game over!")
                sys.exit()
            for shot in shots:
                if asteroid.collides_with(shot):
                    shot.kill()  # Remove shot
                    asteroid.split()  # Split asteroid or destroy

        # Clear the screen
        screen.fill("black")

        # Draw all drawable sprites
        for obj in drawable:
            obj.draw(screen)

        pygame.display.flip()  # Update the display

        # Limit the framerate to 60 FPS and calculate delta time
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
