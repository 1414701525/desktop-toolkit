# 30-Second Reaction Challenge

A simple tkinter click game: tap as many randomly appearing targets as you can in 30 seconds.

## Run

```bash
python game.py
```

## Rules

- Targets appear at random positions on the canvas
- Click a target to score +1 and increase your combo
- Miss a click and the combo resets
- Targets shrink as your score increases
- After 30 seconds, a rating is shown based on your final score

## Implementation

- tkinter Canvas with dual-layer circle targets
- `root.after()`-driven countdown and animation loop
- Floating text feedback ("+1" / "Miss")
- Distance-based hit detection
