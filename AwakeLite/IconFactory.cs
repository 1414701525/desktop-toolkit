using System.Drawing.Drawing2D;
using System.Runtime.InteropServices;

namespace AwakeLite;

internal static class IconFactory
{
    public static Icon CreateTrayIcon(bool isAwake)
    {
        using var bitmap = new Bitmap(32, 32);
        using (var graphics = Graphics.FromImage(bitmap))
        {
            graphics.SmoothingMode = SmoothingMode.AntiAlias;
            graphics.Clear(Color.Transparent);

            var fill = isAwake ? Color.FromArgb(16, 185, 129) : Color.FromArgb(156, 163, 175);
            using var shadowBrush = new SolidBrush(Color.FromArgb(90, 0, 0, 0));
            using var fillBrush = new SolidBrush(fill);
            using var highlightBrush = new SolidBrush(Color.FromArgb(235, 249, 250, 251));
            using var borderPen = new Pen(Color.FromArgb(17, 24, 39), 2);

            graphics.FillEllipse(shadowBrush, 7, 8, 20, 20);
            graphics.FillEllipse(fillBrush, 5, 4, 22, 22);
            graphics.DrawEllipse(borderPen, 5, 4, 22, 22);
            graphics.FillEllipse(highlightBrush, 11, 9, 5, 5);
        }

        var handle = bitmap.GetHicon();
        try
        {
            using var icon = Icon.FromHandle(handle);
            return (Icon)icon.Clone();
        }
        finally
        {
            DestroyIcon(handle);
        }
    }

    [DllImport("user32.dll", SetLastError = true)]
    private static extern bool DestroyIcon(IntPtr hIcon);
}
