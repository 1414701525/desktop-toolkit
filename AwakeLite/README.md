# AwakeLite

A lightweight Windows anti-sleep utility. It temporarily prevents system sleep or screen timeout while running, without modifying power plans or simulating input.

## Features

- Start preventing sleep on launch
- Optional "keep display on" mode
- Three run modes:
  - Infinite — keep awake until manually stopped
  - Timed — 15 min, 30 min, 1 hr, 2 hr, or 4 hr
  - Until time — stops at a specific clock time (auto-rolls to next day if past)
- Auto-resume default power management when timer expires
- Minimize / close to system tray
- Double-click tray icon to restore window
- Tray context menu: show, start/pause, keep-display toggle, mode switch, exit
- Dynamic tray icon (active vs. paused)
- Optional startup registration via HKCU Run key (no admin required)
- Settings saved to `%APPDATA%/AwakeLite/settings.json`

## Requirements

- Windows
- .NET 8 SDK

## Run from Source

```powershell
cd AwakeLite
dotnet run
```

## Publish as Single-File EXE

```powershell
dotnet publish -c Release -r win-x64 --self-contained true /p:PublishSingleFile=true /p:PublishTrimmed=false
```

The output EXE is typically at:

```
bin/Release/net8.0-windows/win-x64/publish/
```

The project file sets `IncludeNativeLibrariesForSelfExtract=true` and `DebugType=embedded` to produce a single self-contained EXE.

## Notes

- Does not modify system power plans
- Does not simulate mouse or keyboard input
- Calls `SetThreadExecutionState(ES_CONTINUOUS)` on exit to restore default power management
- Cannot override administrator-enforced lock/sleep policies
