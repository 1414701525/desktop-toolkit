# Dodge Game

A tkinter dodge game: steer a blue square to avoid red obstacles, collect yellow coins, and pick up blue shields.

## Run

```bash
python dodge.py
```

## Controls

- WASD or Arrow Keys to move
- Space to start
- P to pause / resume

## Game Elements

- 🔴 Red obstacle — lose 1 life on hit
- 🟡 Yellow coin — +10 points
- 🔵 Blue shield — blocks one hit
- 3 lives total; game over when all lost

## Difficulty Curve

- Spawn rate increases over time
- Fall speed increases over time
- Final score = coins collected + survival time

## Implementation

- AABB rectangle overlap for collision detection
- Difficulty curve: `min(8, elapsed / 12)` controls spawn interval and speed
- Weighted random: obstacles 72%, coins 22%, shields 6%
- Screen flash feedback on hit / pickup
