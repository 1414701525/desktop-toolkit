# Desktop Cat

A borderless, transparent-background desktop pet that wanders across the screen, dozes off, and responds to interaction.

## Run

```bash
python desktop_cat.py
```

## Interactions

- **Left click** — Pet the cat
- **Left drag** — Move the cat
- **Left double-click** — Toggle auto-walk / stay put
- **Right-click menu** — Feed fish, put to sleep, say something, quit

## State Machine

- `walk` — Random roaming, reverses at screen edges
- `idle` — Standing still
- `sleep` — Sleeping with Zzz animation
- `stretch` — Stretching
- `happy` — Post-pet/feed state with heart / fish animations

## Implementation

- `overrideredirect(True)` + `transparentcolor` for borderless transparent window
- Canvas-drawn cat: body, head, ears, eyes (with blink), tail (with swing), whiskers, blush
- Sine-wave driven breathing, walking bob, and tail swing animations
- Weighted random state transitions
- Speech bubble + heart / fish particle effects
