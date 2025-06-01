# Flapping Bird

A Python implementation of the classic Flappy Bird game using Pygame.

## Features

- Simple and addictive gameplay
- Smooth bird movement with gravity physics
- Randomly generated pipes with varying gaps
- Score tracking system
- Sound effects for flapping, scoring, and collisions
- Background music for immersion
- Game over screen with restart option
- Difficulty scaling as the game progresses

## Requirements

- Python 3.x
- Pygame library

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/flapping-bird.git
   cd flapping-bird
   ```

2. Install the required dependencies:
   ```
   pip install pygame
   ```

3. Run the game:
   ```
   python main.py
   ```

## How to Play

- Press SPACE to make the bird flap upward
- Navigate through the gaps between pipes
- Each successfully passed pipe earns you one point
- Avoid hitting pipes, the ground, or flying too high
- Press SPACE to restart after game over
- Press ESC to quit the game

## Project Structure

```
flapping-bird/
├── main.py           # Main game file
├── assets/           # Game assets directory
│   ├── images/       # Images for the game
│   │   ├── bird.png
│   │   ├── pipe_top.png
│   │   └── pipe_bottom.png
│   └── sounds/       # Sound effects and music
│       ├── flap.wav
│       ├── point.wav
│       ├── hit.wav
│       └── background.wav
└── README.md         # This file
```

## Customization

You can modify the game constants in `main.py` to adjust:
- Screen dimensions
- Gravity strength
- Flap power
- Pipe speed and gap size
- Game difficulty progression

## License

This project is open source and available under the MIT License.
