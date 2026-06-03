# Desktop Toolkit

一套基于 Python 和 C# 的 Windows 桌面小工具集合，涵盖系统 utility、桌面小游戏和生活辅助工具。

所有项目均为轻量级、无依赖或低依赖的桌面应用，适合学习 Windows 桌面开发、tkinter 自绘、WinForms 定制控件、系统 API 调用等场景。

## 项目列表

### 系统工具

| 项目 | 语言 | 说明 |
|------|------|------|
| [AwakeLite](AwakeLite/) | C# .NET 8 | Windows 防休眠工具，支持定时、托盘、开机自启 |
| [Awake (Python)](Awake/) | Python | 防休眠工具的 Python 实现版本 |

### 桌面小游戏

| 项目 | 语言 | 说明 |
|------|------|------|
| [Reaction Game](games/reaction-game/) | Python | 30 秒反应力点击挑战 |
| [Dodge Game](games/dodge-game/) | Python | 躲避障碍物 + 收集金币 |
| [Desktop Cat](games/desktop-cat/) | Python | 桌面小猫宠物，会散步、睡觉、互动 |

### 生活工具

| 项目 | 语言 | 说明 |
|------|------|------|
| [Food Picker](tools/food-picker/) | Python | 苏州餐厅选择器，支持多维度筛选 |

## 快速开始

### Python 项目

```bash
# 运行任意 Python 项目
python game.py                    # 反应力挑战
python games/dodge-game/dodge.py  # 躲避游戏
python games/desktop-cat/desktop_cat.py  # 桌面小猫
python tools/food-picker/suzhou_food_picker.py  # 餐厅选择器
python Awake/awake_timer.py       # Python 版防休眠
```

Python 项目依赖：
- 标准库 `tkinter`（Python 自带）
- `Awake` 额外需要：`pip install pystray pillow`

### C# 项目

```powershell
cd AwakeLite
dotnet run
```

需要 .NET 8 SDK。

## 打包发布

### Python 项目（PyInstaller）

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name AppName script.py
```

### C# 项目（单文件发布）

```powershell
dotnet publish -c Release -r win-x64 --self-contained true /p:PublishSingleFile=true
```

## 技术要点

- **Windows API 集成**：`SetThreadExecutionState` 防休眠、注册表开机自启、全局热键注册
- **系统托盘**：Python `pystray` / C# `NotifyIcon`，支持右键菜单、图标动态切换
- **自绘 UI**：tkinter Canvas 动画、WinForms 自定义圆角控件（`RoundedPanel`、`RoundedButton`、`ToggleCheckBox`）
- **游戏循环**：`root.after()` 驱动的帧循环、碰撞检测、难度递增
- **数据驱动设计**：餐厅选择器使用结构化 JSON 数据 + 多维筛选

## 项目结构

```
desktop-toolkit/
├── AwakeLite/          # C# 防休眠工具
├── Awake/              # Python 防休眠工具
├── games/
│   ├── reaction-game/  # 反应力挑战
│   ├── dodge-game/     # 躲避游戏
│   └── desktop-cat/    # 桌面小猫
├── tools/
│   └── food-picker/    # 餐厅选择器
└── docs/               # 文档
```

## License

[MIT](LICENSE)
