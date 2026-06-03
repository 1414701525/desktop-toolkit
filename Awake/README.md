# Awake (Python)

Awake 的 Python 实现版本，功能与 AwakeLite（C#）相同，但使用 Python + tkinter + pystray 实现。

## 功能

- 启动后默认保持电脑不休眠
- 支持系统托盘（需安装 pystray + Pillow）
- 支持隐藏托盘图标，Ctrl + Alt + A 唤回
- 支持 Ctrl + Q 兜底退出
- 后台低频刷新，减少 CPU 占用

## 依赖

```bash
pip install pystray pillow
```

## 运行

```bash
python awake_timer.py
```

## 打包

```bash
pyinstaller --onefile --windowed --name AwakeLite awake_timer.py
```

## 技术实现

- **防休眠**：调用 `ctypes.windll.kernel32.SetThreadExecutionState`
- **全局热键**：`RegisterHotKey` + `GetMessageW` 消息循环
- **系统托盘**：`pystray` 库，支持菜单、图标动态切换
- **UI**：tkinter 暗色主题，Canvas 绘制月亮 logo
