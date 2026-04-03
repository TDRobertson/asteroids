# Asteroids

> Classic arcade game rebuilt in Python — expanded well beyond the course assignment that started it.

This project began as a structured assignment in Boot.dev's Python course: build a functional Asteroids clone. The course covered the basics — player movement, rotation, shooting, and asteroid spawning and splitting. I kept going. The shipped version adds acceleration-based physics with friction and inertia, SAT polygon collision detection for precise shape-vs-shape hit testing, a full audio system with background music and three independently controlled sound effects, a progressive difficulty system with a dynamic spawn cap, multiple lives with respawn invincibility, and a CI/CD pipeline that builds and releases cross-platform executables for Windows, Linux, and macOS on every version tag push.

---

## At a Glance

| | |
|---|---|
| **Language** | Python 3.12 |
| **Framework** | Pygame 2.6.1 |
| **Package Manager** | uv |
| **Build Tool** | PyInstaller |
| **CI/CD** | GitHub Actions (matrix builds: Windows, Linux, macOS) |
| **Platforms** | Windows · Linux · macOS |
| **Repository** | [github.com/TDRobertson/asteroids](https://github.com/TDRobertson/asteroids) |

---

## Features

### Core Gameplay
- **Acceleration-based movement** — thrust with `W`/`S`, rotate with `A`/`D`; velocity builds and decays with friction (no instant start/stop)
- **Screen wrapping** — player and all asteroids reappear on the opposite edge
- **Asteroid splitting** — large asteroids break into two smaller ones when destroyed; smallest tier is eliminated outright
- **Multiple lives** — start with 3 lives; respawn at screen center on collision
- **Invincibility window** — 2-second grace period after respawn with a visual flashing indicator

### Progression System
- **Scoring** — 50 points for large asteroids, 100 for small
- **Progressive difficulty** — asteroid spawn cap starts at 10 and increases by 1 every 10 seconds
- **Continuous spawning** — new asteroids spawn from all four screen edges throughout the session

### Physics & Collision
- **Delta-time physics** — all movement calculations use frame delta time, keeping behavior consistent at any frame rate
- **Friction simulation** — velocity multiplied by factor (0.99) each frame for authentic arcade inertia
- **SAT collision detection** — Separating Axis Theorem polygon collision for accurate player triangle vs. asteroid shape testing
- **Shots disappear at edge** — bullets removed when leaving the play area; no wrapping

### Audio
- **Background music** — looped space soundtrack at 30% volume
- **Blaster SFX** — fires on every shot
- **Asteroid explosion SFX** — plays on asteroid destruction
- **Player death SFX** — plays on collision; respawn timer is tied to the clip length

### Build & Distribution
- **Cross-platform CI/CD** — GitHub Actions matrix builds for Windows, Linux, and macOS triggered on version tag push
- **Bundled executables** — PyInstaller packages game and audio assets into a distributable directory archive
- **PyInstaller-compatible asset loading** — `resource_path()` abstraction resolves correct paths in both dev and bundled runtimes

---

## Technical Architecture

### Class Hierarchy

```
CircleShape      (circleshape.py)    ← base class: SAT collision, screen wrap
├── Player       (player.py)         ← input handling, thrust, shooting
├── Asteroid     (asteroid.py)       ← lumpy polygon rendering, splitting logic
└── Shot         (shot.py)           ← bullet behavior, edge removal

AsteroidField    (asteroidfield.py)  ← spawn manager, cap enforcement
```

### Design Patterns

**Container-based sprite groups** — Pygame sprite groups handle all update and draw logic. Each class declares its `containers` before instantiation so new sprites automatically register with the correct groups:

```python
Asteroid.containers = (asteroids, updatable, drawable)
Shot.containers = (shots, updatable, drawable)
AsteroidField.containers = updatable
Player.containers = (updatable, drawable)
```

**Delta-time movement** — all velocity and position updates multiply by `dt` (frame delta in seconds), decoupling game speed from frame rate.

**Resource path abstraction** — `resource_path()` resolves asset paths correctly in both development and PyInstaller bundled runtimes:

```python
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS      # PyInstaller temp folder
    except AttributeError:
        base_path = os.path.abspath(".")  # development
    return os.path.join(base_path, relative_path)
```

**Lumpy asteroid generation** — asteroids are rendered as irregular 12-point polygons with a 0.4 lumpiness factor, producing the classic jagged look rather than smooth circles.

**SAT collision detection** — `polygons_collide()` tests each edge axis from both polygons, projects both shapes onto the axis, and returns `False` immediately if a separating axis is found. Enables accurate player triangle vs. irregular asteroid polygon collision without approximation.

### Game Loop

```
1.  Handle events (QUIT, keyboard input)
2.  Update all sprites  →  updatable.update(dt)
3.  Tick invincibility timer and respawn timer
4.  Tick difficulty timer  →  increment max_asteroids every 10s
5.  Pass updated cap to AsteroidField
6.  Collision detection: asteroids × player, asteroids × shots
7.  Clear screen to black
8.  Draw all sprites  →  apply player flash logic during invincibility
9.  Render HUD  →  score and lives
10. pygame.display.flip()
11. clock.tick(60)  →  dt = elapsed ms / 1000
```

---

## Configuration Reference

All tunable constants live in `constants.py`:

| Constant | Value | Unit | Description |
|---|---|---|---|
| `SCREEN_WIDTH` | 1280 | px | Game window width |
| `SCREEN_HEIGHT` | 720 | px | Game window height |
| `ASTEROID_MIN_RADIUS` | 20 | px | Smallest asteroid radius |
| `ASTEROID_MAX_RADIUS` | 60 | px | Largest asteroid radius (`min × kinds`) |
| `ASTEROID_KINDS` | 3 | — | Number of asteroid size tiers |
| `ASTEROID_SPAWN_RATE` | 0.8 | sec | Time between new asteroid spawns |
| `PLAYER_RADIUS` | 20 | px | Player collision radius |
| `PLAYER_TURN_SPEED` | 300 | °/sec | Rotation speed |
| `PLAYER_SPEED` | 200 | px/sec | Base movement speed |
| `PLAYER_ACCELERATION` | 400 | px/sec² | Thrust acceleration |
| `PLAYER_FRICTION` | 0.99 | factor | Velocity multiplier per frame |
| `PLAYER_SHOOT_SPEED` | 500 | px/sec | Shot velocity |
| `PLAYER_SHOOT_COOLDOWN` | 0.4 | sec | Minimum time between shots |
| `INVINCIBILITY_DURATION` | 2.0 | sec | Post-respawn invincibility window |
| `SHOT_RADIUS` | 5 | px | Bullet collision radius |

---

## Project Structure

```
asteroids/
├── main.py               # Game loop, collision detection, HUD, audio init
├── player.py             # Player class: input, thrust, rotation, shooting
├── asteroid.py           # Asteroid class: rendering, splitting logic
├── asteroidfield.py      # Spawn manager: edge spawning, cap enforcement
├── shot.py               # Shot class: velocity, edge removal
├── circleshape.py        # Base class: SAT collision detection, screen wrap
├── constants.py          # All game configuration constants
├── pyproject.toml        # uv project configuration
├── requirements.txt      # Pinned dependencies
├── .python-version       # Python version lock (3.12)
├── uv.lock               # uv dependency lock file
├── .github/
│   └── workflows/
│       └── build.yml     # CI/CD: matrix builds for Windows, Linux, macOS
└── assets/
    ├── Space_Fighter_Loop.mp3          # Background music (looped)
    ├── retro-blaster-fire.wav          # Shot SFX
    ├── SFX_Explosion_17.wav            # Player death SFX
    └── 150210__pumodi__explosion-3.mp3 # Asteroid explosion SFX
```

---

## Getting Started

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager

### Option 1: Download Pre-built Executable (Recommended)

No Python installation required.

1. Go to the [Releases](https://github.com/TDRobertson/asteroids/releases) page
2. Download the archive for your platform (`asteroids-windows.zip` or `asteroids-unix.zip`)
3. Extract and run the executable

### Option 2: Run from Source

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv

# Activate
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate           # Windows

# Install dependencies
uv add -r requirements.txt

# Run
uv run main.py
```

---

## Platform Notes

### Windows
On first run, Windows Defender or SmartScreen may flag the executable as unrecognized. Click **More info → Run anyway**. This is expected behavior for unsigned PyInstaller executables and does not indicate malware.

### macOS
The macOS build targets Intel (x86_64). Apple Silicon Macs can run it via Rosetta 2:

```sh
/usr/sbin/softwareupdate --install-rosetta --agree-to-license
```

Macs predating 2010 (32-bit only) are not supported. A `Bad CPU type in executable` error indicates an incompatible CPU architecture.

### Linux
No special setup required. Extract the archive and run the binary.

---

## Controls

| Key | Action |
|---|---|
| `W` | Thrust forward |
| `S` | Thrust backward |
| `A` | Rotate left |
| `D` | Rotate right |
| `Space` | Shoot |
| Close window / `Ctrl+C` | Exit |

---

## Gameplay Notes

- **Lives:** Start with 3. Losing all lives ends the game and prints the final score to the terminal.
- **Respawn:** On collision, respawn at screen center with a 2-second invincibility window (flashing effect). Respawn timing is tied to the player death sound clip length.
- **Scoring:** Large asteroids (radius > min) are worth 50 points. Smallest-tier asteroids are worth 100.
- **Difficulty:** The active asteroid cap starts at 10 and increases by 1 every 10 seconds — the game ramps continuously.
- **Wrapping:** Player and asteroids wrap at screen edges. Shots do not wrap and are removed on exit.
- **Collision:** Player and asteroids use SAT polygon detection. Shot collision uses a radius check.

---

## Known Issues

**White line rendering artifact** — A white line may occasionally appear across the screen as asteroids wrap around the edge. This is a Pygame polygon drawing artifact during screen-wrap transitions and does not affect gameplay.

---

## For Developers

### CI/CD Pipeline

Releases are built automatically via GitHub Actions (`.github/workflows/build.yml`). A matrix build runs across three OS targets on every version tag push:

```
push tag v*.*.*
  → build on: windows-latest, ubuntu-latest, macos-latest
    → pyinstaller --onedir --add-data "assets:assets"
    → compress to platform-specific zip
    → upload artifacts
  → create GitHub Release with all platform archives attached
```

**Note on path separators:** Windows uses `;` as the `--add-data` separator; Linux/macOS use `:`. The workflow handles this with separate `if: runner.os == 'Windows'` and `if: runner.os != 'Windows'` build steps.

### Creating a Release

```bash
# Commit and push changes
git add .
git commit -m "Your changes"
git push origin main

# Tag to trigger the automated build pipeline
git tag v1.0.0
git push origin v1.0.0
```

GitHub Actions builds executables for all three platforms and attaches them to a new Release automatically.

### Building Locally

```bash
pip install pyinstaller pygame

# Linux/macOS
pyinstaller --onedir --add-data "assets:assets" main.py

# Windows
pyinstaller --onedir --add-data "assets;assets" main.py
```

---

## Credits

| Component | Source |
|---|---|
| Game engine | [Pygame](https://www.pygame.org/) |
| Package manager | [uv](https://github.com/astral-sh/uv) |
| Original game concept | [Asteroids (1979)](https://en.wikipedia.org/wiki/Asteroids_(video_game)) |

### Audio

| Asset | Author | License |
|---|---|---|
| Space Fighter Loop (background music) | Kevin MacLeod · [incompetech.com](http://incompetech.com) | [CC BY 4.0](http://creativecommons.org/licenses/by/4.0/) |
| Retro Blaster Fire (shot SFX) | astrand · [freesound.org/s/328011/](https://freesound.org/s/328011/) | CC0 |
| SFX_Explosion_17.wav (player death SFX) | jalastram · [freesound.org/s/317760/](https://freesound.org/s/317760/) | CC BY 4.0 |
| Explosion 3 (asteroid explosion SFX) | pumodi · [freesound.org/s/150210/](https://freesound.org/s/150210/) | CC0 |
