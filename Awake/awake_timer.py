import time
import ctypes
import platform
import threading
import traceback
import tkinter as tk
from tkinter import messagebox

# Awake Lite / 防休眠后台工具
#
# 功能：
# - 启动后默认保持电脑不休眠。
# - 托盘可用时：关闭窗口不会退出，只会隐藏到系统托盘。
# - 托盘可用时：右键托盘图标选择「退出」才真正退出。
# - 托盘不可用时：窗口内显示失败原因，并允许直接退出，避免卡死。
# - 支持隐藏托盘图标；隐藏后用 Ctrl + Alt + A 唤回窗口和托盘图标。
# - 支持 Ctrl + Q 兜底退出。
# - 后台低频刷新，减少无意义 CPU 占用。
#
# 依赖：
# python -m pip install pystray pillow
#
# 打包：
# python -m PyInstaller --onefile --windowed --name AwakeLite awake_timer.py

IS_WINDOWS = platform.system().lower() == "windows"

ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002

# Ctrl + Alt + A 用于隐藏托盘图标后唤回窗口
WM_HOTKEY = 0x0312
MOD_ALT = 0x0001
MOD_CONTROL = 0x0002
HOTKEY_ID_SHOW = 1001
HOTKEY_VK = ord("A")

TRAY_AVAILABLE = False
TRAY_IMPORT_ERROR = ""

try:
    import pystray
    from pystray import MenuItem as TrayItem
    from PIL import Image, ImageDraw
    TRAY_AVAILABLE = True
except Exception:
    pystray = None
    TrayItem = None
    Image = None
    ImageDraw = None
    TRAY_AVAILABLE = False
    TRAY_IMPORT_ERROR = traceback.format_exc()


class AwakeController:
    def __init__(self):
        self.active = False
        self.keep_display = True

    def enable(self, keep_display=True):
        self.keep_display = keep_display

        if not IS_WINDOWS:
            self.active = True
            return True

        flags = ES_CONTINUOUS | ES_SYSTEM_REQUIRED
        if keep_display:
            flags |= ES_DISPLAY_REQUIRED

        result = ctypes.windll.kernel32.SetThreadExecutionState(flags)
        self.active = bool(result)
        return self.active

    def disable(self):
        if IS_WINDOWS:
            ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
        self.active = False

    def refresh(self):
        if self.active:
            self.enable(self.keep_display)


class MSG(ctypes.Structure):
    _fields_ = [
        ("hwnd", ctypes.c_void_p),
        ("message", ctypes.c_uint),
        ("wParam", ctypes.c_size_t),
        ("lParam", ctypes.c_size_t),
        ("time", ctypes.c_ulong),
        ("pt_x", ctypes.c_long),
        ("pt_y", ctypes.c_long),
    ]


class AwakeLiteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Awake Lite")
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#111827")

        self.controller = AwakeController()
        self.running = False

        self.tray_icon = None
        self.tray_thread = None
        self.tray_ready = False
        self.tray_icon_hidden = False
        self.tray_start_error = ""

        self.exiting = False
        self.last_refresh_time = 0
        self.hotkey_thread = None
        self.hotkey_registered = False

        self.keep_display_var = tk.BooleanVar(value=True)
        self.start_with_awake_var = tk.BooleanVar(value=True)
        self.hide_tray_icon_var = tk.BooleanVar(value=False)

        self.build_ui()
        self.setup_tray()
        self.setup_global_hotkey()

        self.root.protocol("WM_DELETE_WINDOW", self.on_window_close)
        self.root.bind("<Unmap>", self.on_minimize)
        self.root.bind("<Control-q>", lambda event: self.exit_app())
        self.root.bind("<Control-Q>", lambda event: self.exit_app())

        if self.start_with_awake_var.get():
            self.root.after(250, self.start_awake)

        self.root.after(3000, self.low_frequency_tick)

        if not self.is_tray_usable():
            self.root.after(500, self.show_tray_problem_once)

    def build_ui(self):
        shell = tk.Frame(self.root, bg="#111827")
        shell.pack(fill="both", expand=True, padx=22, pady=22)

        top = tk.Frame(shell, bg="#111827")
        top.pack(fill="x")

        self.logo = tk.Canvas(top, width=54, height=54, bg="#111827", highlightthickness=0)
        self.logo.pack(side="left")
        self.draw_logo(active=False)

        title_box = tk.Frame(top, bg="#111827")
        title_box.pack(side="left", padx=(14, 0))

        tk.Label(
            title_box,
            text="Awake Lite",
            font=("Segoe UI", 24, "bold"),
            bg="#111827",
            fg="#f9fafb"
        ).pack(anchor="w")

        tk.Label(
            title_box,
            text="后台防休眠工具",
            font=("Microsoft YaHei", 10),
            bg="#111827",
            fg="#9ca3af"
        ).pack(anchor="w", pady=(2, 0))

        self.card = tk.Frame(shell, bg="#1f2937", highlightbackground="#374151", highlightthickness=1)
        self.card.pack(fill="x", pady=(24, 16))

        self.status_label = tk.Label(
            self.card,
            text="未启动",
            font=("Microsoft YaHei", 22, "bold"),
            bg="#1f2937",
            fg="#e5e7eb"
        )
        self.status_label.pack(pady=(26, 4))

        self.sub_status_label = tk.Label(
            self.card,
            text="点击开始后，电脑将保持清醒。",
            font=("Microsoft YaHei", 10),
            bg="#1f2937",
            fg="#9ca3af",
            wraplength=420,
            justify="center"
        )
        self.sub_status_label.pack(pady=(0, 24))

        btn_row = tk.Frame(shell, bg="#111827")
        btn_row.pack(fill="x", pady=(4, 12))

        self.toggle_button = tk.Button(
            btn_row,
            text="开始保持清醒",
            font=("Microsoft YaHei", 14, "bold"),
            height=2,
            relief="flat",
            bg="#10b981",
            fg="white",
            activebackground="#059669",
            activeforeground="white",
            command=self.toggle_awake
        )
        self.toggle_button.pack(fill="x")

        options = tk.Frame(shell, bg="#111827")
        options.pack(fill="x", pady=(8, 8))

        self.keep_display_cb = tk.Checkbutton(
            options,
            text="保持屏幕不熄灭",
            variable=self.keep_display_var,
            command=self.on_keep_display_changed,
            bg="#111827",
            fg="#d1d5db",
            selectcolor="#1f2937",
            activebackground="#111827",
            activeforeground="#f9fafb",
            font=("Microsoft YaHei", 10)
        )
        self.keep_display_cb.pack(anchor="w", pady=2)

        tk.Checkbutton(
            options,
            text="启动后自动开始防休眠",
            variable=self.start_with_awake_var,
            bg="#111827",
            fg="#d1d5db",
            selectcolor="#1f2937",
            activebackground="#111827",
            activeforeground="#f9fafb",
            font=("Microsoft YaHei", 10)
        ).pack(anchor="w", pady=2)

        self.hide_tray_cb = tk.Checkbutton(
            options,
            text="隐藏托盘图标（Ctrl + Alt + A 唤回）",
            variable=self.hide_tray_icon_var,
            command=self.on_hide_tray_icon_changed,
            bg="#111827",
            fg="#d1d5db",
            selectcolor="#1f2937",
            activebackground="#111827",
            activeforeground="#f9fafb",
            font=("Microsoft YaHei", 10)
        )
        self.hide_tray_cb.pack(anchor="w", pady=2)

        info = tk.Frame(shell, bg="#172033")
        info.pack(fill="x", pady=(12, 0))

        self.info_label = tk.Label(
            info,
            text="正在检测系统托盘……",
            font=("Microsoft YaHei", 9),
            bg="#172033",
            fg="#93c5fd",
            justify="left",
            wraplength=430
        )
        self.info_label.pack(anchor="w", padx=12, pady=10)

        bottom = tk.Frame(shell, bg="#111827")
        bottom.pack(fill="x", side="bottom")

        self.hide_button = tk.Button(
            bottom,
            text="隐藏窗口到托盘",
            font=("Microsoft YaHei", 10),
            relief="flat",
            bg="#374151",
            fg="#e5e7eb",
            activebackground="#4b5563",
            activeforeground="white",
            command=self.hide_to_tray
        )
        self.hide_button.pack(side="left", fill="x", expand=True, padx=(0, 6))

        self.exit_button = tk.Button(
            bottom,
            text="退出程序",
            font=("Microsoft YaHei", 10),
            relief="flat",
            bg="#4b1f2a",
            fg="#fecaca",
            activebackground="#7f1d1d",
            activeforeground="white",
            command=self.exit_app
        )
        self.exit_button.pack(side="left", fill="x", expand=True, padx=(6, 0))

        self.update_info_text()

    def update_info_text(self):
        if self.is_tray_usable():
            platform_text = "Windows 防休眠接口可用" if IS_WINDOWS else "当前系统不是 Windows，防休眠接口可能不可用"
            self.info_label.config(
                text=f"{platform_text}\n关闭窗口会隐藏到系统托盘；右键托盘图标选择「退出」才会退出。\nCtrl + Alt + A 可唤回隐藏窗口/托盘图标。",
                fg="#93c5fd"
            )
            self.hide_button.config(state="normal", text="隐藏窗口到托盘")
            self.hide_tray_cb.config(state="normal")
        else:
            reason = self.short_tray_error()
            self.info_label.config(
                text=f"系统托盘不可用。当前将使用普通窗口模式，关闭窗口会直接退出。\n原因：{reason}\n兜底退出快捷键：Ctrl + Q。",
                fg="#fca5a5"
            )
            self.hide_button.config(state="disabled", text="托盘不可用")
            self.hide_tray_cb.config(state="disabled")

    def short_tray_error(self):
        if not TRAY_AVAILABLE:
            if "No module named 'PIL'" in TRAY_IMPORT_ERROR:
                return "缺少 Pillow，请在同一 Python 环境执行 python -m pip install pillow。"
            if "No module named 'pystray'" in TRAY_IMPORT_ERROR:
                return "缺少 pystray，请在同一 Python 环境执行 python -m pip install pystray。"
            if TRAY_IMPORT_ERROR:
                last_line = TRAY_IMPORT_ERROR.strip().splitlines()[-1]
                return last_line
            return "pystray 或 Pillow 导入失败。"
        if self.tray_start_error:
            return self.tray_start_error.strip().splitlines()[-1]
        return "托盘图标启动失败。"

    def is_tray_usable(self):
        return bool(TRAY_AVAILABLE and self.tray_icon is not None and self.tray_ready)

    def draw_logo(self, active=False):
        c = self.logo
        c.delete("all")
        bg = "#064e3b" if active else "#1f2937"
        ring = "#34d399" if active else "#6b7280"
        moon = "#f9fafb" if active else "#d1d5db"
        c.create_oval(4, 4, 50, 50, fill=bg, outline=ring, width=2)
        c.create_oval(18, 13, 36, 37, fill=moon, outline="")
        c.create_oval(25, 9, 43, 33, fill=bg, outline="")
        if active:
            c.create_oval(38, 38, 45, 45, fill="#34d399", outline="")
        else:
            c.create_oval(38, 38, 45, 45, fill="#9ca3af", outline="")

    def setup_tray(self):
        if not TRAY_AVAILABLE:
            self.update_info_text()
            return

        menu = pystray.Menu(
            TrayItem("显示窗口", self.tray_show_window, default=True),
            TrayItem(
                lambda item: "暂停防休眠" if self.running else "开始防休眠",
                self.tray_toggle_awake
            ),
            TrayItem(
                "保持屏幕不熄灭",
                self.tray_toggle_keep_display,
                checked=lambda item: self.keep_display_var.get()
            ),
            TrayItem("隐藏托盘图标", self.tray_hide_icon),
            pystray.Menu.SEPARATOR,
            TrayItem("退出", self.tray_exit)
        )

        self.tray_icon = pystray.Icon(
            "AwakeLite",
            self.create_tray_image(active=False),
            "Awake Lite - 未启动",
            menu
        )

        try:
            self.tray_icon.run_detached()
            self.tray_ready = True
            self.update_info_text()
            return
        except Exception:
            self.tray_start_error = traceback.format_exc()

        def run_tray():
            try:
                self.tray_icon.run()
                self.tray_ready = True
            except Exception:
                self.tray_ready = False
                self.tray_start_error = traceback.format_exc()
            finally:
                self.root.after(0, self.update_info_text)

        self.tray_thread = threading.Thread(target=run_tray, daemon=True)
        self.tray_thread.start()
        self.tray_ready = True
        self.root.after(300, self.update_info_text)

    def create_tray_image(self, active=False):
        size = 64
        image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        if active:
            base = (16, 185, 129, 255)
            dark = (6, 78, 59, 255)
        else:
            base = (156, 163, 175, 255)
            dark = (31, 41, 55, 255)

        draw.ellipse((5, 5, 59, 59), fill=dark, outline=base, width=4)
        draw.ellipse((23, 15, 43, 45), fill=(249, 250, 251, 255))
        draw.ellipse((31, 11, 51, 41), fill=dark)
        draw.ellipse((43, 43, 54, 54), fill=base)
        return image

    def update_tray(self):
        if not self.is_tray_usable():
            return

        try:
            self.tray_icon.icon = self.create_tray_image(active=self.running)
            self.tray_icon.title = "Awake Lite - 运行中" if self.running else "Awake Lite - 已暂停"
            self.tray_icon.update_menu()
        except Exception:
            pass

    def set_tray_visible(self, visible):
        if not self.is_tray_usable():
            return False

        try:
            self.tray_icon.visible = bool(visible)
            self.tray_icon_hidden = not bool(visible)
            self.hide_tray_icon_var.set(self.tray_icon_hidden)
            return True
        except Exception:
            return False

    def tray_show_window(self, icon=None, item=None):
        self.root.after(0, self.show_window)

    def tray_toggle_awake(self, icon=None, item=None):
        self.root.after(0, self.toggle_awake)

    def tray_toggle_keep_display(self, icon=None, item=None):
        self.root.after(0, self.toggle_keep_display_from_tray)

    def tray_hide_icon(self, icon=None, item=None):
        self.root.after(0, self.hide_tray_icon)

    def tray_exit(self, icon=None, item=None):
        self.root.after(0, self.exit_app)

    def setup_global_hotkey(self):
        if not IS_WINDOWS:
            return

        def hotkey_loop():
            user32 = ctypes.windll.user32
            registered = user32.RegisterHotKey(None, HOTKEY_ID_SHOW, MOD_CONTROL | MOD_ALT, HOTKEY_VK)
            self.hotkey_registered = bool(registered)

            if not registered:
                return

            msg = MSG()
            while not self.exiting:
                ret = user32.GetMessageW(ctypes.byref(msg), None, 0, 0)
                if ret == 0 or ret == -1:
                    break
                if msg.message == WM_HOTKEY and msg.wParam == HOTKEY_ID_SHOW:
                    self.root.after(0, self.restore_from_hotkey)

            try:
                user32.UnregisterHotKey(None, HOTKEY_ID_SHOW)
            except Exception:
                pass

        self.hotkey_thread = threading.Thread(target=hotkey_loop, daemon=True)
        self.hotkey_thread.start()

    def restore_from_hotkey(self):
        if self.tray_icon and self.tray_icon_hidden:
            self.set_tray_visible(True)
        self.show_window()

    def toggle_awake(self):
        if self.running:
            self.stop_awake()
        else:
            self.start_awake()

    def start_awake(self):
        ok = self.controller.enable(keep_display=self.keep_display_var.get())
        if IS_WINDOWS and not ok:
            messagebox.showerror("启动失败", "调用 Windows 防休眠接口失败。")
            return

        self.running = True
        self.status_label.config(text="正在保持清醒", fg="#d1fae5")
        self.sub_status_label.config(text=self.mode_text())
        self.toggle_button.config(text="暂停防休眠", bg="#ef4444", activebackground="#dc2626")
        self.draw_logo(active=True)
        self.update_tray()

    def stop_awake(self):
        self.controller.disable()
        self.running = False
        self.status_label.config(text="已暂停", fg="#e5e7eb")
        self.sub_status_label.config(text="系统将按照默认电源策略休眠。")
        self.toggle_button.config(text="开始保持清醒", bg="#10b981", activebackground="#059669")
        self.draw_logo(active=False)
        self.update_tray()

    def mode_text(self):
        if self.keep_display_var.get():
            return "电脑不会自动睡眠，屏幕也不会自动熄灭。"
        return "电脑不会自动睡眠，但允许屏幕按系统设置熄灭。"

    def on_keep_display_changed(self):
        if self.running:
            self.controller.enable(keep_display=self.keep_display_var.get())
            self.sub_status_label.config(text=self.mode_text())
        self.update_tray()

    def toggle_keep_display_from_tray(self):
        self.keep_display_var.set(not self.keep_display_var.get())
        self.on_keep_display_changed()

    def on_hide_tray_icon_changed(self):
        if self.hide_tray_icon_var.get():
            self.hide_tray_icon()
        else:
            self.show_tray_icon()

    def hide_tray_icon(self):
        if not self.is_tray_usable():
            messagebox.showwarning(
                "托盘不可用",
                f"当前系统托盘不可用，无法隐藏托盘图标。\n\n原因：{self.short_tray_error()}"
            )
            self.hide_tray_icon_var.set(False)
            return

        if IS_WINDOWS:
            message = "托盘图标隐藏后，可以按 Ctrl + Alt + A 唤回窗口和托盘图标。\n\n确定隐藏托盘图标吗？"
        else:
            message = "当前系统没有启用全局唤回快捷键。隐藏托盘图标后可能无法找回窗口。\n\n确定隐藏托盘图标吗？"

        if not messagebox.askyesno("隐藏托盘图标", message):
            self.hide_tray_icon_var.set(False)
            return

        if self.set_tray_visible(False):
            self.info_label.config(
                text="托盘图标已隐藏。按 Ctrl + Alt + A 可唤回窗口和托盘图标。",
                fg="#93c5fd"
            )
        else:
            self.hide_tray_icon_var.set(False)
            messagebox.showwarning("隐藏失败", "当前托盘实现不支持隐藏图标。")

    def show_tray_icon(self):
        if self.set_tray_visible(True):
            self.update_info_text()

    def on_window_close(self):
        if self.is_tray_usable():
            self.hide_to_tray()
        else:
            self.exit_app()

    def hide_to_tray(self):
        if self.exiting:
            return

        if self.is_tray_usable():
            self.root.withdraw()
        else:
            messagebox.showwarning(
                "托盘不可用",
                f"当前系统托盘不可用，无法隐藏到托盘。\n\n原因：{self.short_tray_error()}\n\n将保持窗口显示，你也可以点击「退出程序」。"
            )

    def show_window(self):
        if self.tray_icon and self.tray_icon_hidden:
            self.set_tray_visible(True)

        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    def on_minimize(self, event=None):
        if self.exiting:
            return
        if self.root.state() == "iconic" and self.is_tray_usable():
            self.root.after(100, self.hide_to_tray)

    def low_frequency_tick(self):
        if self.running:
            now = time.time()
            if now - self.last_refresh_time >= 60:
                self.last_refresh_time = now
                self.controller.refresh()
        self.root.after(3000, self.low_frequency_tick)

    def show_tray_problem_once(self):
        if self.is_tray_usable():
            return
        messagebox.showwarning(
            "托盘不可用",
            "系统托盘当前不可用，程序会退回普通窗口模式。\n\n"
            f"原因：{self.short_tray_error()}\n\n"
            "如需托盘功能，请确认依赖安装在当前运行的 Python 环境里：\n"
            "python -m pip install pystray pillow\n\n"
            "如果你运行的是 exe，需要安装依赖后重新打包。"
        )

    def exit_app(self):
        self.exiting = True
        self.controller.disable()

        if self.tray_icon:
            try:
                self.tray_icon.visible = False
                self.tray_icon.stop()
            except Exception:
                pass

        try:
            if IS_WINDOWS and self.hotkey_registered:
                ctypes.windll.user32.UnregisterHotKey(None, HOTKEY_ID_SHOW)
        except Exception:
            pass

        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = AwakeLiteApp(root)
    root.mainloop()
