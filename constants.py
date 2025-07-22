# constants.py - Game configuration constants

# Display stats
SCREEN_WIDTH = 1280  # Width of the game window
SCREEN_HEIGHT = 720  # Height of the game window

# Asteroid stats
ASTEROID_MIN_RADIUS = 20  # Minimum asteroid size
ASTEROID_KINDS = 3  # Number of asteroid size types
ASTEROID_SPAWN_RATE = 0.8  # seconds between asteroid spawns
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS  # Largest asteroid size

# Player stats
PLAYER_RADIUS = 20  # Player ship size
PLAYER_TURN_SPEED = 300  # Degrees per second
PLAYER_SPEED = 200  # Movement speed
PLAYER_SHOOT_SPEED = 500  # Shot speed
PLAYER_SHOOT_COOLDOWN = 0.4  # seconds between shots

# Shot stats
SHOT_RADIUS = 5  # Size of each shot