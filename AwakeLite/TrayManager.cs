namespace AwakeLite;

internal sealed class ModeChangedEventArgs : EventArgs
{
    public ModeChangedEventArgs(AwakeRunMode mode, int? durationMinutes = null)
    {
        Mode = mode;
        DurationMinutes = durationMinutes;
    }

    public AwakeRunMode Mode { get; }
    public int? DurationMinutes { get; }
}

internal sealed class TrayManager : IDisposable
{
    private readonly NotifyIcon notifyIcon;
    private readonly ContextMenuStrip contextMenu;
    private readonly ToolStripMenuItem showMenuItem;
    private readonly ToolStripMenuItem toggleAwakeMenuItem;
    private readonly ToolStripMenuItem keepDisplayMenuItem;
    private readonly ToolStripMenuItem modeMenuItem;
    private readonly ToolStripMenuItem infiniteModeMenuItem;
    private readonly ToolStripMenuItem timed30MenuItem;
    private readonly ToolStripMenuItem timed60MenuItem;
    private readonly ToolStripMenuItem timed120MenuItem;
    private readonly ToolStripMenuItem exitMenuItem;
    private Icon? currentIcon;
    private bool disposed;

    public TrayManager()
    {
        contextMenu = new ContextMenuStrip
        {
            BackColor = Color.FromArgb(31, 41, 55),
            ForeColor = Color.FromArgb(249, 250, 251),
            ShowCheckMargin = true,
            ShowImageMargin = false
        };

        showMenuItem = new ToolStripMenuItem("显示窗口");
        toggleAwakeMenuItem = new ToolStripMenuItem("暂停防休眠");
        keepDisplayMenuItem = new ToolStripMenuItem("保持屏幕不熄灭") { CheckOnClick = false };
        modeMenuItem = new ToolStripMenuItem("模式");
        infiniteModeMenuItem = new ToolStripMenuItem("无限保持");
        timed30MenuItem = new ToolStripMenuItem("定时 30 分钟");
        timed60MenuItem = new ToolStripMenuItem("定时 1 小时");
        timed120MenuItem = new ToolStripMenuItem("定时 2 小时");
        exitMenuItem = new ToolStripMenuItem("退出");

        showMenuItem.Click += (_, _) => ShowRequested?.Invoke(this, EventArgs.Empty);
        toggleAwakeMenuItem.Click += (_, _) => ToggleAwakeRequested?.Invoke(this, EventArgs.Empty);
        keepDisplayMenuItem.Click += (_, _) => ToggleKeepDisplayRequested?.Invoke(this, EventArgs.Empty);
        infiniteModeMenuItem.Click += (_, _) => ModeChangedRequested?.Invoke(this, new ModeChangedEventArgs(AwakeRunMode.Infinite));
        timed30MenuItem.Click += (_, _) => ModeChangedRequested?.Invoke(this, new ModeChangedEventArgs(AwakeRunMode.Timed, 30));
        timed60MenuItem.Click += (_, _) => ModeChangedRequested?.Invoke(this, new ModeChangedEventArgs(AwakeRunMode.Timed, 60));
        timed120MenuItem.Click += (_, _) => ModeChangedRequested?.Invoke(this, new ModeChangedEventArgs(AwakeRunMode.Timed, 120));
        exitMenuItem.Click += (_, _) => ExitRequested?.Invoke(this, EventArgs.Empty);

        modeMenuItem.DropDownItems.AddRange([infiniteModeMenuItem, timed30MenuItem, timed60MenuItem, timed120MenuItem]);
        contextMenu.Items.AddRange([
            showMenuItem,
            toggleAwakeMenuItem,
            keepDisplayMenuItem,
            modeMenuItem,
            new ToolStripSeparator(),
            exitMenuItem
        ]);

        currentIcon = IconFactory.CreateTrayIcon(isAwake: true);
        notifyIcon = new NotifyIcon
        {
            ContextMenuStrip = contextMenu,
            Icon = currentIcon,
            Text = "AwakeLite - 正在保持清醒",
            Visible = true
        };
        notifyIcon.DoubleClick += (_, _) => ShowRequested?.Invoke(this, EventArgs.Empty);
    }

    public event EventHandler? ShowRequested;
    public event EventHandler? ToggleAwakeRequested;
    public event EventHandler? ToggleKeepDisplayRequested;
    public event EventHandler<ModeChangedEventArgs>? ModeChangedRequested;
    public event EventHandler? ExitRequested;

    public void UpdateState(bool isAwake, bool keepDisplay, string modeText)
    {
        toggleAwakeMenuItem.Text = isAwake ? "暂停防休眠" : "开始防休眠";
        keepDisplayMenuItem.Checked = keepDisplay;
        notifyIcon.Text = TrimNotifyText(isAwake ? $"AwakeLite - 正在保持清醒 ({modeText})" : "AwakeLite - 已暂停");

        var oldIcon = currentIcon;
        currentIcon = IconFactory.CreateTrayIcon(isAwake);
        notifyIcon.Icon = currentIcon;
        oldIcon?.Dispose();
    }

    public void UpdateMode(AwakeRunMode mode, int durationMinutes)
    {
        infiniteModeMenuItem.Checked = mode == AwakeRunMode.Infinite;
        timed30MenuItem.Checked = mode == AwakeRunMode.Timed && durationMinutes == 30;
        timed60MenuItem.Checked = mode == AwakeRunMode.Timed && durationMinutes == 60;
        timed120MenuItem.Checked = mode == AwakeRunMode.Timed && durationMinutes == 120;
    }

    public void HideIcon()
    {
        notifyIcon.Visible = false;
    }

    public void Dispose()
    {
        if (disposed)
        {
            return;
        }

        disposed = true;
        notifyIcon.Visible = false;
        notifyIcon.Dispose();
        contextMenu.Dispose();
        currentIcon?.Dispose();
    }

    private static string TrimNotifyText(string text)
    {
        return text.Length <= 63 ? text : text[..63];
    }
}
