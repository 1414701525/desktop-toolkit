using System.Drawing.Drawing2D;

namespace AwakeLite;

internal sealed class RoundedPanel : Panel
{
    public int Radius { get; set; } = 18;
    public Color FillColor { get; set; } = Color.FromArgb(31, 41, 55);
    public Color BorderColor { get; set; } = Color.FromArgb(55, 65, 81);

    public RoundedPanel()
    {
        BackColor = Color.Transparent;
        DoubleBuffered = true;
    }

    protected override void OnPaint(PaintEventArgs e)
    {
        e.Graphics.SmoothingMode = SmoothingMode.AntiAlias;
        using var path = CreatePath(ClientRectangle, Radius);
        using var fill = new SolidBrush(FillColor);
        using var border = new Pen(BorderColor);
        e.Graphics.FillPath(fill, path);
        e.Graphics.DrawPath(border, path);
    }

    private static GraphicsPath CreatePath(Rectangle bounds, int radius)
    {
        var rect = new Rectangle(bounds.X, bounds.Y, bounds.Width - 1, bounds.Height - 1);
        var d = radius * 2;
        var path = new GraphicsPath();
        path.AddArc(rect.X, rect.Y, d, d, 180, 90);
        path.AddArc(rect.Right - d, rect.Y, d, d, 270, 90);
        path.AddArc(rect.Right - d, rect.Bottom - d, d, d, 0, 90);
        path.AddArc(rect.X, rect.Bottom - d, d, d, 90, 90);
        path.CloseFigure();
        return path;
    }
}

internal sealed class RoundedButton : Button
{
    private bool hovered;
    private bool pressed;

    public int Radius { get; set; } = 13;
    public Color HoverColor { get; set; } = Color.FromArgb(5, 150, 105);
    public Color PressedColor { get; set; } = Color.FromArgb(4, 120, 87);
    public Color BorderColor { get; set; } = Color.Transparent;

    public RoundedButton()
    {
        Cursor = Cursors.Hand;
        FlatStyle = FlatStyle.Flat;
        FlatAppearance.BorderSize = 0;
        SetStyle(ControlStyles.UserPaint | ControlStyles.AllPaintingInWmPaint | ControlStyles.OptimizedDoubleBuffer, true);
    }

    protected override void OnMouseEnter(EventArgs e)
    {
        hovered = true;
        Invalidate();
        base.OnMouseEnter(e);
    }

    protected override void OnMouseLeave(EventArgs e)
    {
        hovered = false;
        pressed = false;
        Invalidate();
        base.OnMouseLeave(e);
    }

    protected override void OnMouseDown(MouseEventArgs mevent)
    {
        pressed = true;
        Invalidate();
        base.OnMouseDown(mevent);
    }

    protected override void OnMouseUp(MouseEventArgs mevent)
    {
        pressed = false;
        Invalidate();
        base.OnMouseUp(mevent);
    }

    protected override void OnPaint(PaintEventArgs e)
    {
        e.Graphics.SmoothingMode = SmoothingMode.AntiAlias;
        var color = pressed ? PressedColor : hovered ? HoverColor : BackColor;
        using var path = CreatePath(ClientRectangle, Radius);
        using var fill = new SolidBrush(color);
        e.Graphics.FillPath(fill, path);

        if (BorderColor != Color.Transparent)
        {
            using var border = new Pen(BorderColor);
            e.Graphics.DrawPath(border, path);
        }

        TextRenderer.DrawText(
            e.Graphics,
            Text,
            Font,
            ClientRectangle,
            ForeColor,
            TextFormatFlags.HorizontalCenter | TextFormatFlags.VerticalCenter | TextFormatFlags.EndEllipsis);
    }

    private static GraphicsPath CreatePath(Rectangle bounds, int radius)
    {
        var rect = new Rectangle(bounds.X, bounds.Y, bounds.Width - 1, bounds.Height - 1);
        var d = radius * 2;
        var path = new GraphicsPath();
        path.AddArc(rect.X, rect.Y, d, d, 180, 90);
        path.AddArc(rect.Right - d, rect.Y, d, d, 270, 90);
        path.AddArc(rect.Right - d, rect.Bottom - d, d, d, 0, 90);
        path.AddArc(rect.X, rect.Bottom - d, d, d, 90, 90);
        path.CloseFigure();
        return path;
    }
}

internal sealed class ToggleCheckBox : CheckBox
{
    public Color AccentColor { get; set; } = Color.FromArgb(16, 185, 129);
    public Color OffColor { get; set; } = Color.FromArgb(75, 85, 99);
    public Color TextColor { get; set; } = Color.FromArgb(209, 213, 219);

    public ToggleCheckBox()
    {
        AutoSize = false;
        Cursor = Cursors.Hand;
        SetStyle(ControlStyles.UserPaint | ControlStyles.AllPaintingInWmPaint | ControlStyles.OptimizedDoubleBuffer, true);
    }

    protected override void OnPaint(PaintEventArgs e)
    {
        e.Graphics.SmoothingMode = SmoothingMode.AntiAlias;
        var parentColor = Parent is RoundedPanel panel
            ? panel.FillColor
            : Parent?.BackColor ?? Color.FromArgb(31, 41, 55);
        e.Graphics.Clear(parentColor);

        var track = new Rectangle(0, 5, 34, 18);
        using var trackPath = new GraphicsPath();
        trackPath.AddArc(track.X, track.Y, track.Height, track.Height, 90, 180);
        trackPath.AddArc(track.Right - track.Height, track.Y, track.Height, track.Height, 270, 180);
        trackPath.CloseFigure();

        using var trackBrush = new SolidBrush(Checked ? AccentColor : OffColor);
        using var knobBrush = new SolidBrush(Color.FromArgb(249, 250, 251));
        e.Graphics.FillPath(trackBrush, trackPath);
        e.Graphics.FillEllipse(knobBrush, Checked ? 18 : 3, 8, 12, 12);

        TextRenderer.DrawText(
            e.Graphics,
            Text,
            Font,
            new Rectangle(44, 0, Width - 44, Height),
            TextColor,
            TextFormatFlags.Left | TextFormatFlags.VerticalCenter | TextFormatFlags.EndEllipsis);
    }
}
