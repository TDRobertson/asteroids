# main.py - Main entry point for the Asteroids game
# Imports
import sys  # For system exit
import pygame  # For game graphics and input
from constants import *  # Game constants
from player import Player  # Player class
from asteroid import Asteroid  # Asteroid class
from asteroidfield import AsteroidField  # Asteroid field manager
from shot import Shot  # Shot (bullet) class

INVINCIBILITY_DURATION = 2.0  # seconds


def main():

    pygame.mixer.pre_init(44100, -16, 2, 2048)
    # Initialize pygame and set up the display
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Set the window caption
    pygame.display.set_caption("Asteroids")

    # Set the window icon
    #icon = pygame.image.load("assets/icon.png")
    #pygame.display.set_icon(icon)

    # Music
    pygame.mixer.music.load("assets/Space_Fighter_Loop.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    # Sound effects
    explosion_sound = pygame.mixer.Sound("assets/150210__pumodi__explosion-3.mp3")  # Explosion 3 by pumodi
    blaster_sound = pygame.mixer.Sound("assets/retro-blaster-fire.wav")  # Retro Blaster Fire by astrand
    player_explosion_sound = pygame.mixer.Sound("assets/SFX_Explosion_17.wav")  # Player explosion by jalastram
    blaster_sound.set_volume(0.5)
    explosion_sound.set_volume(0.5)
    player_explosion_sound.set_volume(0.5)

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
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, blaster_sound=blaster_sound)

    dt = 0  # Delta time for frame updates
    score = 0  # Initialize score
    lives = 3  # Number of lives
    invincible = False  # Is the player currently invincible?
    invincibility_timer = 0.0  # Time left for invincibility
    player_dead = False  # Is the player currently dead (waiting to respawn)?
    player_respawn_timer = 0.0  # Time left until player respawn

    # Asteroid limit logic
    max_asteroids = 10  # Starting limit
    asteroid_increase_timer = 0.0
    ASTEROID_INCREASE_INTERVAL = 10.0  # seconds between increases

    # Set up font for score and lives display
    pygame.font.init()
    font = pygame.font.SysFont(None, 36)

    # Main game loop
    while True:
        # Handle events (e.g., window close)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Update all updatable sprites
        updatable.update(dt)

        # Handle invincibility timer
        if invincible:
            invincibility_timer -= dt
            if invincibility_timer <= 0:
                invincible = False

        # Handle player respawn timer
        if player_dead:
            player_respawn_timer -= dt
            if player_respawn_timer <= 0:
                # Respawn player at center and reset velocity/rotation
                player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                player.velocity = pygame.Vector2(0, 0)
                player.rotation = 0
                invincible = True
                invincibility_timer = INVINCIBILITY_DURATION
                player_dead = False

        # Increase max asteroids over time
        asteroid_increase_timer += dt
        if asteroid_increase_timer > ASTEROID_INCREASE_INTERVAL:
            asteroid_increase_timer = 0
            max_asteroids += 1

        # Pass max_asteroids to AsteroidField
        asteroid_field.max_asteroids = max_asteroids
        asteroid_field.asteroids_group = asteroids

        # Check for collisions between asteroids and player/shots
        for asteroid in asteroids:
            if not invincible and not player_dead and asteroid.collides_with(player):
                lives -= 1
                if lives <= 0:
                    print(f"Game over! Final score: {score}")
                    sys.exit()
                else:
                    # Play player explosion sound and start respawn timer
                    player_explosion_sound.play()
                    player_dead = True
                    player_respawn_timer = player_explosion_sound.get_length()
            for shot in shots:
                if asteroid.collides_with(shot):
                    shot.kill()  # Remove shot
                    # Award points based on asteroid size
                    if asteroid.radius <= ASTEROID_MIN_RADIUS:
                        score += 100  # Smallest asteroid
                    else:
                        score += 50   # Larger asteroid
                    explosion_sound.play()  # Play explosion sound
                    asteroid.split()  # Split asteroid or destroy

        # Clear the screen
        screen.fill("black")

        # Draw all drawable sprites
        for obj in drawable:
            # Make the player flash while invincible, and hide if dead
            if obj is player:
                if not player_dead:
                    if invincible:
                        if int(invincibility_timer * 10) % 2 == 0:
                            obj.draw(screen)
                    else:
                        obj.draw(screen)
            else:
                obj.draw(screen)

        # Render and display the score
        score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_surface, (10, 10))
        # Render and display the lives
        lives_surface = font.render(f"Lives: {lives}", True, (255, 255, 255))
        screen.blit(lives_surface, (10, 50))

        pygame.display.flip()  # Update the display

        # Limit the framerate to 60 FPS and calculate delta time
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
