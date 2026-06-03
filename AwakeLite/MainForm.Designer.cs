namespace AwakeLite;

partial class MainForm
{
    private System.ComponentModel.IContainer components = null!;
    private Label titleLabel = null!;
    private Label subtitleLabel = null!;
    private RoundedPanel statusPanel = null!;
    private Label statusValueLabel = null!;
    private Label modeLabel = null!;
    private Label modeValueLabel = null!;
    private Label remainingLabel = null!;
    private Label remainingValueLabel = null!;
    private Label displayValueLabel = null!;
    private RoundedButton toggleAwakeButton = null!;
    private RoundedButton hideToTrayButton = null!;
    private RoundedPanel settingsPanel = null!;
    private ToggleCheckBox keepDisplayCheckBox = null!;
    private ToggleCheckBox startWithAwakeCheckBox = null!;
    private ToggleCheckBox startupCheckBox = null!;
    private Label runModeLabel = null!;
    private ComboBox modeComboBox = null!;
    private Label durationLabel = null!;
    private ComboBox durationComboBox = null!;
    private Label untilTimeLabel = null!;
    private DateTimePicker untilTimePicker = null!;
    private Label hintLabel = null!;

    private void InitializeComponent()
    {
        components = new System.ComponentModel.Container();
        titleLabel = new Label();
        subtitleLabel = new Label();
        statusPanel = new RoundedPanel();
        statusValueLabel = new Label();
        modeLabel = new Label();
        modeValueLabel = new Label();
        remainingLabel = new Label();
        remainingValueLabel = new Label();
        displayValueLabel = new Label();
        toggleAwakeButton = new RoundedButton();
        hideToTrayButton = new RoundedButton();
        settingsPanel = new RoundedPanel();
        keepDisplayCheckBox = new ToggleCheckBox();
        startWithAwakeCheckBox = new ToggleCheckBox();
        startupCheckBox = new ToggleCheckBox();
        runModeLabel = new Label();
        modeComboBox = new ComboBox();
        durationLabel = new Label();
        durationComboBox = new ComboBox();
        untilTimeLabel = new Label();
        untilTimePicker = new DateTimePicker();
        hintLabel = new Label();
        statusPanel.SuspendLayout();
        settingsPanel.SuspendLayout();
        SuspendLayout();
        // 
        // titleLabel
        // 
        titleLabel.AutoSize = true;
        titleLabel.Font = new Font("Segoe UI", 20F, FontStyle.Bold);
        titleLabel.ForeColor = Color.FromArgb(249, 250, 251);
        titleLabel.Location = new Point(24, 18);
        titleLabel.Name = "titleLabel";
        titleLabel.Size = new Size(143, 37);
        titleLabel.TabIndex = 0;
        titleLabel.Text = "AwakeLite";
        // 
        // subtitleLabel
        // 
        subtitleLabel.AutoSize = true;
        subtitleLabel.Font = new Font("Segoe UI", 9F);
        subtitleLabel.ForeColor = Color.FromArgb(156, 163, 175);
        subtitleLabel.Location = new Point(27, 55);
        subtitleLabel.Name = "subtitleLabel";
        subtitleLabel.Size = new Size(91, 15);
        subtitleLabel.TabIndex = 1;
        subtitleLabel.Text = "后台防休眠工具";
        // 
        // statusPanel
        // 
        statusPanel.BorderColor = Color.FromArgb(55, 65, 81);
        statusPanel.Controls.Add(statusValueLabel);
        statusPanel.Controls.Add(modeLabel);
        statusPanel.Controls.Add(modeValueLabel);
        statusPanel.Controls.Add(remainingLabel);
        statusPanel.Controls.Add(remainingValueLabel);
        statusPanel.Controls.Add(displayValueLabel);
        statusPanel.FillColor = Color.FromArgb(31, 41, 55);
        statusPanel.Location = new Point(22, 86);
        statusPanel.Name = "statusPanel";
        statusPanel.Radius = 18;
        statusPanel.Size = new Size(386, 102);
        statusPanel.TabIndex = 2;
        // 
        // statusValueLabel
        // 
        statusValueLabel.AutoSize = true;
        statusValueLabel.Font = new Font("Segoe UI", 18F, FontStyle.Bold);
        statusValueLabel.ForeColor = Color.FromArgb(16, 185, 129);
        statusValueLabel.Location = new Point(18, 17);
        statusValueLabel.Name = "statusValueLabel";
        statusValueLabel.Size = new Size(154, 32);
        statusValueLabel.TabIndex = 0;
        statusValueLabel.Text = "正在保持清醒";
        // 
        // modeLabel
        // 
        modeLabel.AutoSize = true;
        modeLabel.Font = new Font("Segoe UI", 8.5F);
        modeLabel.ForeColor = Color.FromArgb(156, 163, 175);
        modeLabel.Location = new Point(20, 62);
        modeLabel.Name = "modeLabel";
        modeLabel.Size = new Size(32, 15);
        modeLabel.TabIndex = 1;
        modeLabel.Text = "模式";
        // 
        // modeValueLabel
        // 
        modeValueLabel.AutoSize = true;
        modeValueLabel.Font = new Font("Segoe UI", 9.5F, FontStyle.Bold);
        modeValueLabel.ForeColor = Color.FromArgb(209, 213, 219);
        modeValueLabel.Location = new Point(58, 61);
        modeValueLabel.Name = "modeValueLabel";
        modeValueLabel.Size = new Size(60, 17);
        modeValueLabel.TabIndex = 2;
        modeValueLabel.Text = "无限保持";
        // 
        // remainingLabel
        // 
        remainingLabel.AutoSize = true;
        remainingLabel.Font = new Font("Segoe UI", 8.5F);
        remainingLabel.ForeColor = Color.FromArgb(156, 163, 175);
        remainingLabel.Location = new Point(224, 22);
        remainingLabel.Name = "remainingLabel";
        remainingLabel.Size = new Size(32, 15);
        remainingLabel.TabIndex = 3;
        remainingLabel.Text = "剩余";
        // 
        // remainingValueLabel
        // 
        remainingValueLabel.Font = new Font("Segoe UI", 15F, FontStyle.Bold);
        remainingValueLabel.ForeColor = Color.FromArgb(249, 250, 251);
        remainingValueLabel.Location = new Point(220, 37);
        remainingValueLabel.Name = "remainingValueLabel";
        remainingValueLabel.Size = new Size(136, 28);
        remainingValueLabel.TabIndex = 4;
        remainingValueLabel.Text = "无限";
        remainingValueLabel.TextAlign = ContentAlignment.MiddleLeft;
        // 
        // displayValueLabel
        // 
        displayValueLabel.Font = new Font("Segoe UI", 8.5F);
        displayValueLabel.ForeColor = Color.FromArgb(156, 163, 175);
        displayValueLabel.Location = new Point(224, 70);
        displayValueLabel.Name = "displayValueLabel";
        displayValueLabel.Size = new Size(140, 17);
        displayValueLabel.TabIndex = 5;
        displayValueLabel.Text = "按系统设置熄屏";
        // 
        // toggleAwakeButton
        // 
        toggleAwakeButton.BackColor = Color.FromArgb(239, 68, 68);
        toggleAwakeButton.BorderColor = Color.Transparent;
        toggleAwakeButton.FlatAppearance.BorderSize = 0;
        toggleAwakeButton.Font = new Font("Segoe UI", 10F, FontStyle.Bold);
        toggleAwakeButton.ForeColor = Color.White;
        toggleAwakeButton.HoverColor = Color.FromArgb(220, 38, 38);
        toggleAwakeButton.Location = new Point(22, 201);
        toggleAwakeButton.Name = "toggleAwakeButton";
        toggleAwakeButton.PressedColor = Color.FromArgb(185, 28, 28);
        toggleAwakeButton.Radius = 13;
        toggleAwakeButton.Size = new Size(246, 38);
        toggleAwakeButton.TabIndex = 3;
        toggleAwakeButton.Text = "暂停防休眠";
        toggleAwakeButton.UseVisualStyleBackColor = false;
        toggleAwakeButton.Click += ToggleAwakeButton_Click;
        // 
        // hideToTrayButton
        // 
        hideToTrayButton.BackColor = Color.FromArgb(31, 41, 55);
        hideToTrayButton.BorderColor = Color.FromArgb(75, 85, 99);
        hideToTrayButton.FlatAppearance.BorderSize = 0;
        hideToTrayButton.Font = new Font("Segoe UI", 9F, FontStyle.Bold);
        hideToTrayButton.ForeColor = Color.FromArgb(209, 213, 219);
        hideToTrayButton.HoverColor = Color.FromArgb(55, 65, 81);
        hideToTrayButton.Location = new Point(278, 201);
        hideToTrayButton.Name = "hideToTrayButton";
        hideToTrayButton.PressedColor = Color.FromArgb(24, 33, 48);
        hideToTrayButton.Radius = 13;
        hideToTrayButton.Size = new Size(130, 38);
        hideToTrayButton.TabIndex = 4;
        hideToTrayButton.Text = "隐藏";
        hideToTrayButton.UseVisualStyleBackColor = false;
        hideToTrayButton.Click += HideToTrayButton_Click;
        // 
        // settingsPanel
        // 
        settingsPanel.BorderColor = Color.FromArgb(55, 65, 81);
        settingsPanel.Controls.Add(keepDisplayCheckBox);
        settingsPanel.Controls.Add(startWithAwakeCheckBox);
        settingsPanel.Controls.Add(startupCheckBox);
        settingsPanel.Controls.Add(runModeLabel);
        settingsPanel.Controls.Add(modeComboBox);
        settingsPanel.Controls.Add(durationLabel);
        settingsPanel.Controls.Add(durationComboBox);
        settingsPanel.Controls.Add(untilTimeLabel);
        settingsPanel.Controls.Add(untilTimePicker);
        settingsPanel.FillColor = Color.FromArgb(31, 41, 55);
        settingsPanel.Location = new Point(22, 253);
        settingsPanel.Name = "settingsPanel";
        settingsPanel.Radius = 18;
        settingsPanel.Size = new Size(386, 108);
        settingsPanel.TabIndex = 5;
        // 
        // keepDisplayCheckBox
        // 
        keepDisplayCheckBox.AccentColor = Color.FromArgb(16, 185, 129);
        keepDisplayCheckBox.Font = new Font("Segoe UI", 8.5F);
        keepDisplayCheckBox.Location = new Point(18, 12);
        keepDisplayCheckBox.Name = "keepDisplayCheckBox";
        keepDisplayCheckBox.OffColor = Color.FromArgb(75, 85, 99);
        keepDisplayCheckBox.Size = new Size(120, 28);
        keepDisplayCheckBox.TabIndex = 0;
        keepDisplayCheckBox.Text = "屏幕常亮";
        keepDisplayCheckBox.TextColor = Color.FromArgb(209, 213, 219);
        keepDisplayCheckBox.CheckedChanged += KeepDisplayCheckBox_CheckedChanged;
        // 
        // startWithAwakeCheckBox
        // 
        startWithAwakeCheckBox.AccentColor = Color.FromArgb(16, 185, 129);
        startWithAwakeCheckBox.Checked = true;
        startWithAwakeCheckBox.CheckState = CheckState.Checked;
        startWithAwakeCheckBox.Font = new Font("Segoe UI", 8.5F);
        startWithAwakeCheckBox.Location = new Point(143, 12);
        startWithAwakeCheckBox.Name = "startWithAwakeCheckBox";
        startWithAwakeCheckBox.OffColor = Color.FromArgb(75, 85, 99);
        startWithAwakeCheckBox.Size = new Size(132, 28);
        startWithAwakeCheckBox.TabIndex = 1;
        startWithAwakeCheckBox.Text = "启动即运行";
        startWithAwakeCheckBox.TextColor = Color.FromArgb(209, 213, 219);
        startWithAwakeCheckBox.CheckedChanged += StartWithAwakeCheckBox_CheckedChanged;
        // 
        // startupCheckBox
        // 
        startupCheckBox.AccentColor = Color.FromArgb(16, 185, 129);
        startupCheckBox.Font = new Font("Segoe UI", 8.5F);
        startupCheckBox.Location = new Point(281, 12);
        startupCheckBox.Name = "startupCheckBox";
        startupCheckBox.OffColor = Color.FromArgb(75, 85, 99);
        startupCheckBox.Size = new Size(92, 28);
        startupCheckBox.TabIndex = 2;
        startupCheckBox.Text = "自启";
        startupCheckBox.TextColor = Color.FromArgb(209, 213, 219);
        startupCheckBox.CheckedChanged += StartupCheckBox_CheckedChanged;
        // 
        // runModeLabel
        // 
        runModeLabel.AutoSize = true;
        runModeLabel.Font = new Font("Segoe UI", 8F);
        runModeLabel.ForeColor = Color.FromArgb(156, 163, 175);
        runModeLabel.Location = new Point(20, 48);
        runModeLabel.Name = "runModeLabel";
        runModeLabel.Size = new Size(31, 13);
        runModeLabel.TabIndex = 3;
        runModeLabel.Text = "模式";
        // 
        // modeComboBox
        // 
        modeComboBox.BackColor = Color.FromArgb(17, 24, 39);
        modeComboBox.DropDownStyle = ComboBoxStyle.DropDownList;
        modeComboBox.FlatStyle = FlatStyle.Flat;
        modeComboBox.ForeColor = Color.FromArgb(249, 250, 251);
        modeComboBox.FormattingEnabled = true;
        modeComboBox.Items.AddRange(new object[] { "无限保持", "定时保持", "到指定时间" });
        modeComboBox.Location = new Point(18, 66);
        modeComboBox.Name = "modeComboBox";
        modeComboBox.Size = new Size(116, 23);
        modeComboBox.TabIndex = 4;
        modeComboBox.SelectedIndexChanged += ModeComboBox_SelectedIndexChanged;
        // 
        // durationLabel
        // 
        durationLabel.AutoSize = true;
        durationLabel.Font = new Font("Segoe UI", 8F);
        durationLabel.ForeColor = Color.FromArgb(156, 163, 175);
        durationLabel.Location = new Point(149, 48);
        durationLabel.Name = "durationLabel";
        durationLabel.Size = new Size(31, 13);
        durationLabel.TabIndex = 5;
        durationLabel.Text = "时长";
        // 
        // durationComboBox
        // 
        durationComboBox.BackColor = Color.FromArgb(17, 24, 39);
        durationComboBox.DropDownStyle = ComboBoxStyle.DropDownList;
        durationComboBox.FlatStyle = FlatStyle.Flat;
        durationComboBox.ForeColor = Color.FromArgb(249, 250, 251);
        durationComboBox.FormattingEnabled = true;
        durationComboBox.Items.AddRange(new object[] { "15 分钟", "30 分钟", "1 小时", "2 小时", "4 小时" });
        durationComboBox.Location = new Point(147, 66);
        durationComboBox.Name = "durationComboBox";
        durationComboBox.Size = new Size(98, 23);
        durationComboBox.TabIndex = 6;
        durationComboBox.SelectedIndexChanged += DurationComboBox_SelectedIndexChanged;
        // 
        // untilTimeLabel
        // 
        untilTimeLabel.AutoSize = true;
        untilTimeLabel.Font = new Font("Segoe UI", 8F);
        untilTimeLabel.ForeColor = Color.FromArgb(156, 163, 175);
        untilTimeLabel.Location = new Point(260, 48);
        untilTimeLabel.Name = "untilTimeLabel";
        untilTimeLabel.Size = new Size(31, 13);
        untilTimeLabel.TabIndex = 7;
        untilTimeLabel.Text = "截止";
        // 
        // untilTimePicker
        // 
        untilTimePicker.CustomFormat = "HH:mm";
        untilTimePicker.Format = DateTimePickerFormat.Custom;
        untilTimePicker.Location = new Point(258, 66);
        untilTimePicker.Name = "untilTimePicker";
        untilTimePicker.ShowUpDown = true;
        untilTimePicker.Size = new Size(82, 23);
        untilTimePicker.TabIndex = 8;
        untilTimePicker.ValueChanged += UntilTimePicker_ValueChanged;
        // 
        // hintLabel
        // 
        hintLabel.Font = new Font("Segoe UI", 8F);
        hintLabel.ForeColor = Color.FromArgb(107, 114, 128);
        hintLabel.Location = new Point(25, 371);
        hintLabel.Name = "hintLabel";
        hintLabel.Size = new Size(382, 18);
        hintLabel.TabIndex = 6;
        hintLabel.Text = "关闭窗口会隐藏到托盘，完全退出请使用托盘菜单。";
        // 
        // MainForm
        // 
        AutoScaleDimensions = new SizeF(7F, 15F);
        AutoScaleMode = AutoScaleMode.Font;
        BackColor = Color.FromArgb(17, 24, 39);
        ClientSize = new Size(430, 398);
        Controls.Add(titleLabel);
        Controls.Add(subtitleLabel);
        Controls.Add(statusPanel);
        Controls.Add(toggleAwakeButton);
        Controls.Add(hideToTrayButton);
        Controls.Add(settingsPanel);
        Controls.Add(hintLabel);
        Font = new Font("Segoe UI", 9F);
        FormBorderStyle = FormBorderStyle.FixedSingle;
        MaximizeBox = false;
        Name = "MainForm";
        StartPosition = FormStartPosition.CenterScreen;
        Text = "AwakeLite";
        FormClosing += MainForm_FormClosing;
        Resize += MainForm_Resize;
        statusPanel.ResumeLayout(false);
        statusPanel.PerformLayout();
        settingsPanel.ResumeLayout(false);
        settingsPanel.PerformLayout();
        ResumeLayout(false);
        PerformLayout();
    }
}
