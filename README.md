# Flappy Bird Clone (Pygame)

A simple Flappy Bird clone made using Python and Pygame.
This project recreates the classic Flappy Bird gameplay with smooth controls, score tracking, countdown animation, and a clean UI.

---

## Preview

Features included in this version:

* Smooth bird movement
* Gravity and flap mechanics
* Random obstacle generation
* Score system
* High score tracking
* Start screen
* Game over screen
* Countdown before gameplay
* Custom background and bird sprite

---

# Requirements

Before running the project, make sure Python is installed on your system.

You also need the following library:

```bash
pip install pygame
```

---

# Project Structure

```text
flappy-bird/
│
├── main.py
├── background.jpg
├── bird1.png
└── README.md
```

---

# How to Run

1. Clone or download this project.
2. Open the project folder in your terminal.
3. Run the game:

```bash
python main.py
```

---

# Controls

| Key          | Action                 |
| ------------ | ---------------------- |
| SPACE        | Flap / Start / Restart |
| Close Window | Exit Game              |

---

# Gameplay Mechanics

## Bird Physics

The bird is affected by gravity and falls continuously.
Pressing the `SPACE` key gives the bird an upward force.

```python
GRAVITY = 3
FLAP_STRENGTH = -6
```

---

## Obstacles

Pipes are generated with random heights while maintaining a fixed gap between them.

```python
OBSTACLE_GAP = 160
```

The obstacle position resets after leaving the screen.

---

## Scoring System

The player gains one point every time the bird successfully passes an obstacle.

The game also stores the highest score during the session.

---

# Assets Used

The project uses:

* `background.jpg` → game background
* `bird1.png` → bird sprite

You can replace these with your own assets if you want to customize the game.

---

# Screens Included

### Start Screen

Displays the game title and instructions before gameplay begins.

### Countdown Screen

A 3-second countdown before the game starts.

### Game Over Screen

Shows:

* Current score
* Best score
* Restart prompt

---

# Possible Improvements

Some ideas for future updates:

* Add sound effects and background music
* Animate the bird wings
* Add multiple obstacles at once
* Add difficulty scaling
* Save high score permanently using files
* Add pause functionality
* Add mobile support

---

# Technologies Used

* Python
* Pygame

---

# Learning Goals

This project is great for beginners who want to practice:

* Game loops
* Event handling
* Collision detection
* Object movement
* Rendering graphics
* Basic game physics
* UI drawing in Pygame

---

# Author

Made as a beginner-friendly Flappy Bird project using Python and Pygame.
