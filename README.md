# Asteroids Game (Python, Pygame)

This is a simple Asteroids-style arcade game implemented in Python using the Pygame library.

## Features
- Player-controlled spaceship that can rotate, move, and shoot
- Asteroids that split into smaller pieces when shot
- Continuous asteroid spawning from the edges
- Collision detection between player, asteroids, and shots
- Fully commented code for clarity and learning

## Project Structure
- `main.py` - Main entry point; sets up the game loop and handles all game logic
- `player.py` - Defines the Player class (spaceship)
- `asteroid.py` - Defines the Asteroid class and splitting logic
- `asteroidfield.py` - Manages asteroid spawning and updates
- `shot.py` - Defines the Shot (bullet) class
- `circleshape.py` - Base class for all circular game objects (player, asteroids, shots)
- `constants.py` - All game configuration constants

## Requirements
- Python 3.7+
- [Pygame](https://www.pygame.org/) (install with `pip install pygame`)

## How to Run
1. Install dependencies:
   ```bash
   pip install pygame
   ```
2. Run the game:
   ```bash
   python main.py
   ```

## Controls
- `W`/`S`: Move forward/backward
- `A`/`D`: Rotate left/right
- `Space`: Shoot
- Close the window or press the close button to exit

## Notes
- All code is now fully commented for clarity and maintainability.
- This project is intended for educational purposes and as a starting point for further development.
