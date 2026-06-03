namespace AwakeLite;

internal enum AwakeRunMode
{
    Infinite,
    Timed,
    UntilTime
}

internal sealed class AppSettings
{
    public bool KeepDisplay { get; set; }
    public bool StartWithAwake { get; set; } = true;
    public AwakeRunMode LastMode { get; set; } = AwakeRunMode.Infinite;
    public int LastDurationMinutes { get; set; } = 30;
    public WindowLocation? WindowLocation { get; set; }
    public bool StartHiddenToTray { get; set; }
    public string Theme { get; set; } = "dark";
    public bool StartWithWindows { get; set; }
    public string LastUntilTime { get; set; } = "18:30";
}

internal sealed class WindowLocation
{
    public int X { get; set; }
    public int Y { get; set; }
}
