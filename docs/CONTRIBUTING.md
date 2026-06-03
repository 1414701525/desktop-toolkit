# Contributing

Contributions are welcome! Here's how to get started.

## How to Contribute

1. Fork this repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push the branch: `git push origin feature/your-feature`
5. Open a Pull Request

## Development Setup

### Python Projects

```bash
# Python 3.10+ recommended
python --version

# Install dependencies (only Awake needs extras)
pip install pystray pillow

# Run tests
python -m pytest tests/
```

### C# Project

```powershell
# Requires .NET 8 SDK
dotnet --version

# Run
cd AwakeLite
dotnet run

# Publish
dotnet publish -c Release -r win-x64 --self-contained true /p:PublishSingleFile=true
```

## Code Style

### Python

- Follow PEP 8
- Use type hints
- Add docstrings to functions and classes
- Use `snake_case` for variables and functions

### C#

- Follow C# coding conventions
- Use `PascalCase` for classes and methods
- Use `camelCase` for local variables and parameters
- Add XML documentation comments

## Commit Convention

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat` — New feature
- `fix` — Bug fix
- `docs` — Documentation update
- `style` — Code formatting
- `refactor` — Refactoring
- `test` — Adding tests
- `chore` — Build / tooling changes

Example:

```
feat(awake-lite): add custom theme color support

- Add theme config file
- Support dark/light theme switching
- Update tray icon colors

Closes #12
```

## Reporting Issues

Use GitHub Issues to report bugs or suggest features. Please include:

- Description of the issue
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment (OS version, Python/.NET version)

## Pull Request Checklist

- [ ] Code follows project conventions
- [ ] Comments and documentation added where needed
- [ ] All existing tests pass
- [ ] New features include tests
- [ ] Related documentation updated
