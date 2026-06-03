namespace AwakeLite;

public partial class MainForm : Form
{
    private readonly PowerManager powerManager;
    private readonly TrayManager trayManager;
    private readonly SettingsManager settingsManager;
    private readonly System.Windows.Forms.Timer countdownTimer;
    private AppSettings settings;
    private DateTime? currentEndTime;
    private bool isExiting;
    private bool isInitializing = true;

    public MainForm()
    {
        InitializeComponent();

        settingsManager = new SettingsManager();
        settings = settingsManager.Load();
        powerManager = new PowerManager();
        trayManager = new TrayManager();
        countdownTimer = new System.Windows.Forms.Timer { Interval = 1000 };
        countdownTimer.Tick += CountdownTimer_Tick;

        WireTrayEvents();
        ApplySettingsToUi();
        isInitializing = false;

        if (settings.StartWithAwake)
        {
            StartAwake();
        }
        else
        {
            StopAwake();
        }

        UpdateUi();
    }

    private void WireTrayEvents()
    {
        trayManager.ShowRequested += (_, _) => ShowMainWindow();
        trayManager.ToggleAwakeRequested += (_, _) => ToggleAwake();
        trayManager.ToggleKeepDisplayRequested += (_, _) =>
        {
            keepDisplayCheckBox.Checked = !keepDisplayCheckBox.Checked;
        };
        trayManager.ModeChangedRequested += (_, e) =>
        {
            SetMode(e.Mode, e.DurationMinutes);
            if (!powerManager.IsActive)
            {
                StartAwake();
            }
        };
        trayManager.ExitRequested += (_, _) => ExitApplication();
    }

    private void ApplySettingsToUi()
    {
        keepDisplayCheckBox.Checked = settings.KeepDisplay;
        startWithAwakeCheckBox.Checked = settings.StartWithAwake;
        startupCheckBox.Checked = StartupManager.IsEnabled();

        modeComboBox.SelectedIndex = settings.LastMode switch
        {
            AwakeRunMode.Timed => 1,
            AwakeRunMode.UntilTime => 2,
            _ => 0
        };

        durationComboBox.SelectedIndex = settings.LastDurationMinutes switch
        {
            15 => 0,
            30 => 1,
            60 => 2,
            120 => 3,
            240 => 4,
            _ => 1
        };

        if (TimeSpan.TryParse(settings.LastUntilTime, out var untilTime))
        {
            untilTimePicker.Value = DateTime.Today.Add(untilTime);
        }
        else
        {
            untilTimePicker.Value = DateTime.Today.AddHours(18).AddMinutes(30);
        }

        if (settings.WindowLocation is not null)
        {
            StartPosition = FormStartPosition.Manual;
            Location = new Point(settings.WindowLocation.X, settings.WindowLocation.Y);
        }

        UpdateModeInputState();
    }

    private void ToggleAwakeButton_Click(object? sender, EventArgs e)
    {
        ToggleAwake();
    }

    private void HideToTrayButton_Click(object? sender, EventArgs e)
    {
        HideToTray();
    }

    private void KeepDisplayCheckBox_CheckedChanged(object? sender, EventArgs e)
    {
        if (isInitializing)
        {
            return;
        }

        settings.KeepDisplay = keepDisplayCheckBox.Checked;
        SaveSettingsQuietly();

        if (powerManager.IsActive)
        {
            powerManager.Start(keepDisplayCheckBox.Checked);
        }

        UpdateUi();
    }

    private void StartWithAwakeCheckBox_CheckedChanged(object? sender, EventArgs e)
    {
        if (isInitializing)
        {
            return;
        }

        settings.StartWithAwake = startWithAwakeCheckBox.Checked;
        SaveSettingsQuietly();
    }

    private void StartupCheckBox_CheckedChanged(object? sender, EventArgs e)
    {
        if (isInitializing)
        {
            return;
        }

        try
        {
            StartupManager.SetEnabled(startupCheckBox.Checked);
            settings.StartWithWindows = startupCheckBox.Checked;
            SaveSettingsQuietly();
        }
        catch (Exception ex)
        {
            startupCheckBox.CheckedChanged -= StartupCheckBox_CheckedChanged;
            startupCheckBox.Checked = !startupCheckBox.Checked;
            startupCheckBox.CheckedChanged += StartupCheckBox_CheckedChanged;

            MessageBox.Show(
                this,
                $"开机自启设置失败：{ex.Message}",
                "AwakeLite",
                MessageBoxButtons.OK,
                MessageBoxIcon.Warning);
        }
    }

    private void ModeComboBox_SelectedIndexChanged(object? sender, EventArgs e)
    {
        if (isInitializing)
        {
            return;
        }

        settings.LastMode = CurrentMode;
        UpdateModeInputState();
        RestartCurrentSessionIfRunning();
        SaveSettingsQuietly();
        UpdateUi();
    }

    private void DurationComboBox_SelectedIndexChanged(object? sender, EventArgs e)
    {
        if (isInitializing)
        {
            return;
        }

        settings.LastDurationMinutes = CurrentDurationMinutes;
        RestartCurrentSessionIfRunning();
        SaveSettingsQuietly();
        UpdateUi();
    }

    private void UntilTimePicker_ValueChanged(object? sender, EventArgs e)
    {
        if (isInitializing)
        {
            return;
        }

        settings.LastUntilTime = untilTimePicker.Value.ToString("HH:mm");
        RestartCurrentSessionIfRunning();
        SaveSettingsQuietly();
        UpdateUi();
    }

    private void CountdownTimer_Tick(object? sender, EventArgs e)
    {
        if (!powerManager.IsActive || currentEndTime is null)
        {
            countdownTimer.Stop();
            UpdateUi();
            return;
        }

        if (DateTime.Now >= currentEndTime.Value)
        {
            StopAwake();
        }

        UpdateUi();
    }

    private void MainForm_FormClosing(object? sender, FormClosingEventArgs e)
    {
        if (!isExiting)
        {
            e.Cancel = true;
            HideToTray();
            return;
        }

        SaveWindowLocation();
        SaveSettingsQuietly();
    }

    private void MainForm_Resize(object? sender, EventArgs e)
    {
        if (WindowState == FormWindowState.Minimized)
        {
            HideToTray();
        }
    }

    private AwakeRunMode CurrentMode => modeComboBox.SelectedIndex switch
    {
        1 => AwakeRunMode.Timed,
        2 => AwakeRunMode.UntilTime,
        _ => AwakeRunMode.Infinite
    };

    private int CurrentDurationMinutes => durationComboBox.SelectedIndex switch
    {
        0 => 15,
        1 => 30,
        2 => 60,
        3 => 120,
        4 => 240,
        _ => 30
    };

    private void ToggleAwake()
    {
        if (powerManager.IsActive)
        {
            StopAwake();
        }
        else
        {
            StartAwake();
        }

        UpdateUi();
    }

    private void StartAwake()
    {
        try
        {
            settings.LastMode = CurrentMode;
            settings.LastDurationMinutes = CurrentDurationMinutes;
            settings.LastUntilTime = untilTimePicker.Value.ToString("HH:mm");
            currentEndTime = CalculateEndTime();

            powerManager.Start(keepDisplayCheckBox.Checked);

            if (currentEndTime is null)
            {
                countdownTimer.Stop();
            }
            else
            {
                countdownTimer.Start();
            }

            SaveSettingsQuietly();
        }
        catch (Exception ex)
        {
            MessageBox.Show(
                this,
                ex.Message,
                "AwakeLite",
                MessageBoxButtons.OK,
                MessageBoxIcon.Error);
        }
    }

    private void StopAwake()
    {
        try
        {
            countdownTimer.Stop();
            currentEndTime = null;
            powerManager.Stop();
        }
        catch (Exception ex)
        {
            MessageBox.Show(
                this,
                ex.Message,
                "AwakeLite",
                MessageBoxButtons.OK,
                MessageBoxIcon.Error);
        }
    }

    private DateTime? CalculateEndTime()
    {
        var now = DateTime.Now;

        return CurrentMode switch
        {
            AwakeRunMode.Timed => now.AddMinutes(CurrentDurationMinutes),
            AwakeRunMode.UntilTime => CalculateUntilTime(now),
            _ => null
        };
    }

    private DateTime CalculateUntilTime(DateTime now)
    {
        var selected = untilTimePicker.Value;
        var endTime = new DateTime(now.Year, now.Month, now.Day, selected.Hour, selected.Minute, 0);
        return endTime <= now ? endTime.AddDays(1) : endTime;
    }

    private void SetMode(AwakeRunMode mode, int? durationMinutes)
    {
        modeComboBox.SelectedIndex = mode switch
        {
            AwakeRunMode.Timed => 1,
            AwakeRunMode.UntilTime => 2,
            _ => 0
        };

        if (durationMinutes.HasValue)
        {
            durationComboBox.SelectedIndex = durationMinutes.Value switch
            {
                15 => 0,
                30 => 1,
                60 => 2,
                120 => 3,
                240 => 4,
                _ => durationComboBox.SelectedIndex
            };
        }

        settings.LastMode = CurrentMode;
        settings.LastDurationMinutes = CurrentDurationMinutes;
        UpdateModeInputState();
        RestartCurrentSessionIfRunning();
        SaveSettingsQuietly();
        UpdateUi();
    }

    private void RestartCurrentSessionIfRunning()
    {
        if (powerManager.IsActive)
        {
            StartAwake();
        }
        else
        {
            currentEndTime = null;
        }
    }

    private void UpdateModeInputState()
    {
        durationComboBox.Enabled = CurrentMode == AwakeRunMode.Timed;
        untilTimePicker.Enabled = CurrentMode == AwakeRunMode.UntilTime;
    }

    private void UpdateUi()
    {
        var isAwake = powerManager.IsActive;
        var modeText = GetModeText();
        var displayText = keepDisplayCheckBox.Checked ? "屏幕常亮" : "按系统设置熄屏";
        var remainingText = GetRemainingText();

        statusValueLabel.Text = isAwake ? "正在保持清醒" : "已暂停";
        statusValueLabel.ForeColor = isAwake ? Color.FromArgb(16, 185, 129) : Color.FromArgb(239, 68, 68);
        modeValueLabel.Text = modeText;
        displayValueLabel.Text = displayText;
        remainingValueLabel.Text = remainingText;
        toggleAwakeButton.Text = isAwake ? "暂停防休眠" : "开始防休眠";
        toggleAwakeButton.BackColor = isAwake ? Color.FromArgb(239, 68, 68) : Color.FromArgb(16, 185, 129);
        toggleAwakeButton.HoverColor = isAwake ? Color.FromArgb(220, 38, 38) : Color.FromArgb(5, 150, 105);
        toggleAwakeButton.PressedColor = isAwake ? Color.FromArgb(185, 28, 28) : Color.FromArgb(4, 120, 87);
        toggleAwakeButton.Invalidate();

        trayManager.UpdateMode(CurrentMode, CurrentDurationMinutes);
        trayManager.UpdateState(isAwake, keepDisplayCheckBox.Checked, modeText);
    }

    private string GetModeText()
    {
        return CurrentMode switch
        {
            AwakeRunMode.Timed => $"定时 {CurrentDurationMinutes} 分钟",
            AwakeRunMode.UntilTime => currentEndTime is null
                ? $"至 {untilTimePicker.Value:HH:mm}"
                : $"至 {currentEndTime:MM-dd HH:mm}",
            _ => "无限保持"
        };
    }

    private string GetRemainingText()
    {
        if (!powerManager.IsActive)
        {
            return "未运行";
        }

        if (currentEndTime is null)
        {
            return "无限";
        }

        var remaining = currentEndTime.Value - DateTime.Now;
        if (remaining <= TimeSpan.Zero)
        {
            return "00:00";
        }

        return remaining.TotalHours >= 1
            ? $"{(int)remaining.TotalHours:00}:{remaining.Minutes:00}:{remaining.Seconds:00}"
            : $"{remaining.Minutes:00}:{remaining.Seconds:00}";
    }

    private void ShowMainWindow()
    {
        Show();
        WindowState = FormWindowState.Normal;
        Activate();
    }

    private void HideToTray()
    {
        Hide();
    }

    private void ExitApplication()
    {
        isExiting = true;
        StopAwake();
        trayManager.HideIcon();
        trayManager.Dispose();
        SaveWindowLocation();
        SaveSettingsQuietly();
        Application.Exit();
    }

    private void SaveWindowLocation()
    {
        if (WindowState == FormWindowState.Normal)
        {
            settings.WindowLocation = new WindowLocation
            {
                X = Location.X,
                Y = Location.Y
            };
        }
    }

    private void SaveSettingsQuietly()
    {
        try
        {
            settings.KeepDisplay = keepDisplayCheckBox.Checked;
            settings.StartWithAwake = startWithAwakeCheckBox.Checked;
            settings.LastMode = CurrentMode;
            settings.LastDurationMinutes = CurrentDurationMinutes;
            settings.LastUntilTime = untilTimePicker.Value.ToString("HH:mm");
            settings.StartWithWindows = startupCheckBox.Checked;
            settingsManager.Save(settings);
        }
        catch (Exception ex)
        {
            MessageBox.Show(
                this,
                ex.Message,
                "AwakeLite",
                MessageBoxButtons.OK,
                MessageBoxIcon.Warning);
        }
    }

    protected override void Dispose(bool disposing)
    {
        if (disposing)
        {
            countdownTimer.Dispose();
            trayManager.Dispose();
            powerManager.Dispose();
            components?.Dispose();
        }

        base.Dispose(disposing);
    }
}
