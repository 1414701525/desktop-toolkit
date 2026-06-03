# AwakeLite

AwakeLite 是一个轻量级 Windows 后台防休眠工具。它只在程序运行期间通过 Windows API 临时阻止系统睡眠或屏幕熄灭，不修改系统电源计划，也不模拟鼠标或键盘输入。

## 功能

- 启动后默认开始防休眠。
- 支持"保持屏幕不熄灭"。
- 支持三种运行模式：
  - 无限保持
  - 定时保持：15 分钟、30 分钟、1 小时、2 小时、4 小时
  - 到指定时间：如果时间早于当前时间，会自动理解为明天该时间
- 定时结束后自动暂停防休眠，并恢复 Windows 默认电源管理。
- 关闭窗口或最小化窗口时隐藏到系统托盘。
- 托盘图标双击显示主窗口。
- 托盘右键菜单支持显示窗口、开始/暂停、防屏幕熄灭、快捷模式和退出。
- 运行中和暂停时使用不同托盘图标。
- 支持可选开机自启，写入 HKCU Run 项，不需要管理员权限。
- 使用 `%APPDATA%/AwakeLite/settings.json` 保存设置。

## 运行要求

- Windows
- .NET 8 SDK

## 开发运行

```powershell
cd AwakeLite
dotnet run
```

## 发布单文件 exe

```powershell
dotnet publish -c Release -r win-x64 --self-contained true /p:PublishSingleFile=true /p:PublishTrimmed=false
```

发布后的 exe 通常位于：

```text
bin/Release/net8.0-windows/win-x64/publish/
```

项目文件已设置 `IncludeNativeLibrariesForSelfExtract=true` 和 `DebugType=embedded`，用于让 self-contained 发布结果保持为单个 exe。

## 说明

- 本工具不修改系统电源计划。
- 本工具不模拟鼠标或键盘。
- 退出时会调用 `SetThreadExecutionState(ES_CONTINUOUS)` 恢复 Windows 默认电源管理。
- 如果系统策略或管理员策略强制锁屏/休眠，本工具不保证能绕过。
