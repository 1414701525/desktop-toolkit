using System.ComponentModel;
using System.Runtime.InteropServices;

namespace AwakeLite;

internal sealed class PowerManager : IDisposable
{
    private const uint ES_CONTINUOUS = 0x80000000;
    private const uint ES_SYSTEM_REQUIRED = 0x00000001;
    private const uint ES_DISPLAY_REQUIRED = 0x00000002;

    public bool IsActive { get; private set; }
    public bool KeepDisplay { get; private set; }

    public void Start(bool keepDisplay)
    {
        // ES_CONTINUOUS keeps the request active until this process changes it.
        // ES_SYSTEM_REQUIRED prevents idle system sleep; ES_DISPLAY_REQUIRED also keeps the display on.
        var flags = ES_CONTINUOUS | ES_SYSTEM_REQUIRED;
        if (keepDisplay)
        {
            flags |= ES_DISPLAY_REQUIRED;
        }

        ApplyExecutionState(flags);
        KeepDisplay = keepDisplay;
        IsActive = true;
    }

    public void Stop()
    {
        ApplyExecutionState(ES_CONTINUOUS);
        IsActive = false;
    }

    public void Refresh()
    {
        if (IsActive)
        {
            Start(KeepDisplay);
        }
    }

    public void Dispose()
    {
        try
        {
            Stop();
        }
        catch
        {
            IsActive = false;
        }
    }

    private static void ApplyExecutionState(uint flags)
    {
        if (SetThreadExecutionState(flags) == 0)
        {
            throw new Win32Exception(Marshal.GetLastWin32Error(), "SetThreadExecutionState 调用失败。");
        }
    }

    [DllImport("kernel32.dll", SetLastError = true)]
    private static extern uint SetThreadExecutionState(uint esFlags);
}
