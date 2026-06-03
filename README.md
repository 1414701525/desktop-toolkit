# Desktop Toolkit

A collection of lightweight Windows desktop utilities and games built with Python and C#. Covers system tools, mini-games, and everyday helpers — all designed to be small, self-contained, and easy to learn from.

## Projects

### System Utilities

| Project | Language | Description |
|---------|----------|-------------|
| [AwakeLite](AwakeLite/) | C# .NET 8 | Anti-sleep tool with timer, system tray, and startup integration |
| [Awake (Python)](Awake/) | Python | Python implementation of the anti-sleep tool |

### Desktop Games

| Project | Language | Description |
|---------|----------|-------------|
| [Reaction Game](games/reaction-game/) | Python | 30-second click challenge with combo system |
| [Dodge Game](games/dodge-game/) | Python | Dodge obstacles, collect coins and shields |
| [Desktop Cat](games/desktop-cat/) | Python | Animated desktop pet that walks, sleeps, and interacts |

### Everyday Tools

| Project | Language | Description |
|---------|----------|-------------|
| [Food Picker](tools/food-picker/) | Python | Suzhou restaurant picker with multi-dimensional filtering |

## Quick Start

### Python Projects

```bash
python game.py                            # Reaction game
python games/dodge-game/dodge.py          # Dodge game
python games/desktop-cat/desktop_cat.py   # Desktop cat
python tools/food-picker/suzhou_food_picker.py  # Food picker
python Awake/awake_timer.py               # Anti-sleep (Python)
```

Dependencies:
- `tkinter` (built-in with Python)
- `Awake` additionally requires: `pip install pystray pillow`

### C# Project

```powershell
cd AwakeLite
dotnet run
```

Requires .NET 8 SDK.

## Building

### Python (PyInstaller)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name AppName script.py
```

### C# (Single-file publish)

```powershell
dotnet publish -c Release -r win-x64 --self-contained true /p:PublishSingleFile=true
```

## Technical Highlights

- **Windows API integration** — `SetThreadExecutionState` for sleep prevention, registry-based startup, global hotkey registration
- **System tray** — Python `pystray` / C# `NotifyIcon` with context menus and dynamic icon switching
- **Custom UI rendering** — tkinter Canvas animations, WinForms owner-drawn controls (`RoundedPanel`, `RoundedButton`, `ToggleCheckBox`)
- **Game loop design** — `root.after()`-driven frame loop, AABB collision detection, progressive difficulty
- **Data-driven architecture** — restaurant picker uses structured JSON data with multi-field filtering

## Project Structure

```
desktop-toolkit/
├── AwakeLite/          # C# anti-sleep tool
├── Awake/              # Python anti-sleep tool
├── games/
│   ├── reaction-game/  # Click challenge
│   ├── dodge-game/     # Dodge game
│   └── desktop-cat/    # Desktop cat pet
├── tools/
│   └── food-picker/    # Restaurant picker
└── docs/               # Documentation
```

## License

[MIT](LICENSE)
