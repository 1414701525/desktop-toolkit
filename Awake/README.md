# Awake (Python)

Python implementation of the Awake anti-sleep tool, using tkinter + pystray.

## Features

- Prevents system sleep while running
- System tray support (requires pystray + Pillow)
- Hide tray icon; Ctrl + Alt + A to restore
- Ctrl + Q as fallback exit
- Low-frequency background refresh to minimize CPU usage

## Dependencies

```bash
pip install pystray pillow
```

## Run

```bash
python awake_timer.py
```

## Build

```bash
pyinstaller --onefile --windowed --name AwakeLite awake_timer.py
```

## Implementation Details

- **Sleep prevention** — `ctypes.windll.kernel32.SetThreadExecutionState`
- **Global hotkey** — `RegisterHotKey` + `GetMessageW` message loop
- **System tray** — `pystray` library with menu and dynamic icon switching
- **UI** — tkinter dark theme, Canvas-drawn moon logo
