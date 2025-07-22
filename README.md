# Asteroids Game (Python, Pygame)

This is a simple Asteroids-style arcade game implemented in Python using the Pygame library.

## Features
- **Player-controlled spaceship** with acceleration-based movement and inertia (classic Asteroids feel)
- **Screen wrapping** for player and asteroids: objects reappear on the opposite edge
- **Multiple lives and respawning**: player respawns at the center with a brief invincibility period (flashing effect)
- **Scoring system**: earn points for destroying asteroids (more for smaller ones)
- **Asteroid splitting**: large asteroids split into smaller ones when shot
- **Asteroid spawn cap**: the number of asteroids on screen is limited and increases over time for progressive difficulty
- **Shots disappear at screen edge**: shots are removed when they leave the play area (no wrapping)
- **Continuous asteroid spawning** from the edges
- **Collision detection** between player, asteroids, and shots
- **Lumpy asteroids**: asteroids are drawn as irregular polygons for a more classic, jagged look
- **Score display**: shooting asteroids gives points, larger asteroids are worth more
- **Fully commented code** for clarity and learning

## Project Structure
- `main.py` - Main entry point; sets up the game loop and handles all game logic
- `player.py` - Defines the Player class (spaceship)
- `asteroid.py` - Defines the Asteroid class and splitting logic
- `asteroidfield.py` - Manages asteroid spawning, spawn cap, and updates
- `shot.py` - Defines the Shot (bullet) class
- `circleshape.py` - Base class for all circular game objects (player, asteroids, shots)
- `constants.py` - All game configuration constants

## Requirements
- Python 3.10+ installed 
- [uv project and package manager](https://github.com/astral-sh/uv) (for dependency management and running scripts)
- Access to a unix-like shell (e.g. zsh or bash)

## How to Run
1. Install uv:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
2. Initialize uv in your project (if not already done):
   ```bash
   uv init
   ```
3. Create a new virtual environment:
   ```bash
   uv venv
   ```
4. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```
5. Add dependencies:
   ```bash
   uv add -r requirements.txt
   ```
6. Run the game using uv:
   ```bash
   uv run main.py
   ```

## Controls
- `W`/`S`: Accelerate forward/backward (with inertia)
- `A`/`D`: Rotate left/right
- `Space`: Shoot
- Close the window or press the close button to exit

## Gameplay Notes
- **Lives:** You start with multiple lives. On collision with an asteroid, you lose a life and respawn at the center, invincible for a short time (flashing).
- **Score:** Destroy asteroids for points. Smaller asteroids are worth more.
- **Asteroid Cap:** The number of asteroids on screen is limited (starts at 10 by default) and increases every 10 seconds.
- **Screen Wrapping:** Player and asteroids wrap around the screen edges. Shots do not wrap and are removed when leaving the screen.
- **Lumpy Asteroids:** Asteroids are drawn as irregular polygons for a more classic, jagged look.
- **Difficulty:** The game gets harder as more asteroids are allowed on screen over time.

## Notes
- This project is intended for educational purposes and as a starting point for further development.
