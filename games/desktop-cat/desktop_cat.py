import tkinter as tk
import random
import math

# 桌面小猫 2.0
# 功能：
# - 无边框、置顶、透明背景
# - 会随机散步、发呆、睡觉、伸懒腰
# - 左键单击：摸摸小猫
# - 左键拖动：移动小猫
# - 左键双击：切换自动散步 / 原地待着
# - 右键菜单：喂小鱼干、让它睡觉、说句话、退出
#
# 注意：
# - Windows 下透明背景通常正常。
# - 如果在某些系统上看到粉色背景，说明系统不支持 transparentcolor，程序仍可运行。

BG = "#ff00ff"          # 透明色
CAT_ORANGE = "#f2b36d"
CAT_LIGHT = "#ffd59e"
CAT_PINK = "#f7b7b7"
CAT_DARK = "#2f2f2f"

W, H = 240, 220
FPS_DELAY = 35

SPEECHES = [
    "喵~",
    "摸摸头。",
    "我在陪你。",
    "记得喝水。",
    "别太累啦。",
    "今天也辛苦了。",
    "小猫正在巡逻。",
    "可以休息一下。",
    "要不要去吃点东西？",
    "我觉得你需要一杯奶茶。",
]

HAPPY_SPEECHES = [
    "小鱼干！",
    "开心。",
    "再来一条。",
    "你真好。",
    "喵呜~",
]

SLEEP_SPEECHES = [
    "我睡一会儿。",
    "晚安喵。",
    "Zzz...",
]


class DesktopCat:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.config(bg=BG)

        try:
            self.root.wm_attributes("-transparentcolor", BG)
        except Exception:
            pass

        self.canvas = tk.Canvas(
            self.root,
            width=W,
            height=H,
            bg=BG,
            highlightthickness=0,
            bd=0
        )
        self.canvas.pack()

        self.screen_w = self.root.winfo_screenwidth()
        self.screen_h = self.root.winfo_screenheight()

        self.x = self.screen_w - W - 80
        self.y = self.screen_h - H - 80
        self.vx = -2.2
        self.facing = -1
        self.roaming = True

        self.state = "walk"       # walk / idle / sleep / stretch / happy
        self.state_timer = 120
        self.action_lock = 0

        self.tail_phase = 0.0
        self.step_phase = 0.0
        self.breath_phase = 0.0
        self.blink_timer = random.randint(70, 160)
        self.blink_frames = 0

        self.dragging = False
        self.drag_moved = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0

        self.bubble_text = ""
        self.bubble_timer = 0
        self.heart_timer = 0
        self.fish_timer = 0
        self.notice_timer = 0

        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="摸摸小猫", command=self.pet)
        self.menu.add_command(label="喂小鱼干", command=self.feed_fish)
        self.menu.add_command(label="让它睡一会儿", command=self.sleep_now)
        self.menu.add_command(label="说句话", command=self.random_say)
        self.menu.add_separator()
        self.menu.add_command(label="切换散步 / 待着", command=self.toggle_roam)
        self.menu.add_command(label="退出", command=self.quit_app)

        self.root.geometry(f"{W}x{H}+{int(self.x)}+{int(self.y)}")

        self.root.bind("<ButtonPress-1>", self.on_press)
        self.root.bind("<B1-Motion>", self.on_drag)
        self.root.bind("<ButtonRelease-1>", self.on_release)
        self.root.bind("<Double-Button-1>", self.toggle_roam_event)
        self.root.bind("<Button-3>", self.show_menu)

        self.tick()

    def on_press(self, event):
        self.dragging = True
        self.drag_moved = False
        self.drag_offset_x = event.x_root - self.x
        self.drag_offset_y = event.y_root - self.y

    def on_drag(self, event):
        if not self.dragging:
            return

        new_x = event.x_root - self.drag_offset_x
        new_y = event.y_root - self.drag_offset_y

        if abs(new_x - self.x) > 2 or abs(new_y - self.y) > 2:
            self.drag_moved = True

        self.x = max(0, min(self.screen_w - W, new_x))
        self.y = max(0, min(self.screen_h - H, new_y))
        self.root.geometry(f"{W}x{H}+{int(self.x)}+{int(self.y)}")

    def on_release(self, event):
        if self.dragging and not self.drag_moved:
            self.pet()
        self.dragging = False

    def show_menu(self, event):
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def quit_app(self):
        self.root.destroy()

    def say(self, text, duration=95):
        self.bubble_text = text
        self.bubble_timer = duration

    def random_say(self):
        self.say(random.choice(SPEECHES))

    def pet(self):
        self.state = "happy"
        self.action_lock = 80
        self.heart_timer = 70
        self.say(random.choice(["呼噜呼噜。", "舒服。", "再摸一下。", "喵~"]))

    def feed_fish(self):
        self.state = "happy"
        self.action_lock = 100
        self.fish_timer = 90
        self.heart_timer = 90
        self.say(random.choice(HAPPY_SPEECHES))

    def sleep_now(self):
        self.state = "sleep"
        self.action_lock = 260
        self.say(random.choice(SLEEP_SPEECHES), duration=80)

    def toggle_roam_event(self, event=None):
        self.toggle_roam()

    def toggle_roam(self):
        self.roaming = not self.roaming
        if self.roaming:
            self.state = "walk"
            self.say("我去散步啦。")
        else:
            self.state = "idle"
            self.say("那我待在这里。")

    def choose_state(self):
        if self.action_lock > 0:
            return

        self.state_timer -= 1
        if self.state_timer > 0:
            return

        if not self.roaming:
            self.state = random.choices(
                ["idle", "sleep", "stretch"],
                weights=[70, 20, 10],
                k=1
            )[0]
        else:
            self.state = random.choices(
                ["walk", "idle", "sleep", "stretch"],
                weights=[55, 28, 10, 7],
                k=1
            )[0]

        if self.state == "walk":
            self.state_timer = random.randint(100, 220)
            if random.random() < 0.25:
                self.vx *= -1
        elif self.state == "idle":
            self.state_timer = random.randint(70, 180)
        elif self.state == "sleep":
            self.state_timer = random.randint(140, 280)
        else:
            self.state_timer = random.randint(55, 90)

    def update_motion(self):
        if self.action_lock > 0:
            self.action_lock -= 1

        self.choose_state()

        moving = self.roaming and self.state == "walk" and not self.dragging
        if moving:
            self.x += self.vx
            self.facing = 1 if self.vx >= 0 else -1

            if self.x <= 0:
                self.x = 0
                self.vx = abs(self.vx)
                self.facing = 1
            elif self.x >= self.screen_w - W:
                self.x = self.screen_w - W
                self.vx = -abs(self.vx)
                self.facing = -1

            self.root.geometry(f"{W}x{H}+{int(self.x)}+{int(self.y)}")

        self.tail_phase += 0.22
        self.step_phase += 0.2 if moving else 0.06
        self.breath_phase += 0.08

        self.blink_timer -= 1
        if self.blink_frames > 0:
            self.blink_frames -= 1
        elif self.blink_timer <= 0 and self.state != "sleep":
            self.blink_frames = 6
            self.blink_timer = random.randint(80, 190)

        self.bubble_timer = max(0, self.bubble_timer - 1)
        self.heart_timer = max(0, self.heart_timer - 1)
        self.fish_timer = max(0, self.fish_timer - 1)
        self.notice_timer = max(0, self.notice_timer - 1)

    def tick(self):
        self.update_motion()
        self.draw()
        self.root.after(FPS_DELAY, self.tick)

    def draw(self):
        self.canvas.delete("all")

        if self.bubble_timer > 0:
            self.draw_bubble(118, 26, self.bubble_text)

        if self.heart_timer > 0:
            self.draw_heart(178, 58 - (70 - self.heart_timer) * 0.25, scale=0.85)

        if self.fish_timer > 0:
            self.draw_fish(48, 74 + math.sin(self.step_phase) * 3)

        if self.state == "sleep":
            self.draw_sleep_marks()

        self.draw_cat()

    def draw_cat(self):
        c = self.canvas
        facing = self.facing

        is_moving = self.roaming and self.state == "walk" and not self.dragging
        is_sleep = self.state == "sleep"
        is_stretch = self.state == "stretch"
        is_happy = self.state == "happy"

        bob = math.sin(self.step_phase) * 2.0 if is_moving else math.sin(self.breath_phase) * 0.8
        if is_sleep:
            bob = math.sin(self.breath_phase) * 1.0

        body_x = 118
        body_y = 142 + bob
        head_x = 118
        head_y = 94 + bob

        if is_stretch:
            body_y += 6
            head_x += 10 * facing
            head_y += 5

        # 阴影
        c.create_oval(55, 178, 185, 198, fill="#bdbdbd", outline="")

        # 尾巴
        tail_swing = math.sin(self.tail_phase) * (12 if is_moving else 7)
        if is_sleep:
            tail_swing = 0

        if facing == 1:
            tail_points = [
                body_x - 58, body_y + 14,
                body_x - 88, body_y - 8 + tail_swing,
                body_x - 64, body_y - 35 + tail_swing,
            ]
        else:
            tail_points = [
                body_x + 58, body_y + 14,
                body_x + 88, body_y - 8 + tail_swing,
                body_x + 64, body_y - 35 + tail_swing,
            ]
        c.create_line(*tail_points, width=12, fill=CAT_ORANGE, smooth=True, capstyle=tk.ROUND)
        c.create_line(*tail_points, width=5, fill="#f7c27f", smooth=True, capstyle=tk.ROUND)

        # 身体
        if is_sleep:
            c.create_oval(body_x - 62, body_y - 18, body_x + 62, body_y + 42, fill=CAT_ORANGE, outline="")
            c.create_oval(body_x - 40, body_y - 5, body_x + 45, body_y + 42, fill=CAT_LIGHT, outline="")
        elif is_stretch:
            c.create_oval(body_x - 67, body_y - 24, body_x + 70, body_y + 32, fill=CAT_ORANGE, outline="")
            c.create_oval(body_x - 45, body_y - 11, body_x + 50, body_y + 32, fill=CAT_LIGHT, outline="")
        else:
            c.create_oval(body_x - 58, body_y - 32, body_x + 58, body_y + 40, fill=CAT_ORANGE, outline="")
            c.create_oval(body_x - 38, body_y - 16, body_x + 40, body_y + 39, fill=CAT_LIGHT, outline="")

        # 腿和爪
        leg_shift = math.sin(self.step_phase) * 4 if is_moving else 0
        paw_y = body_y + 42
        for px, shift in [(-33, leg_shift), (-12, -leg_shift), (13, leg_shift), (34, -leg_shift)]:
            c.create_line(body_x + px, body_y + 22, body_x + px + shift * 0.3, paw_y + shift * 0.4, width=8, fill=CAT_ORANGE, capstyle=tk.ROUND)
            c.create_oval(body_x + px - 8 + shift * 0.3, paw_y - 2 + shift * 0.4, body_x + px + 8 + shift * 0.3, paw_y + 7 + shift * 0.4, fill=CAT_ORANGE, outline="")

        # 头
        if is_sleep:
            head_y += 8
            head_x -= 12 * facing
        c.create_oval(head_x - 43, head_y - 35, head_x + 43, head_y + 43, fill=CAT_ORANGE, outline="")

        # 耳朵
        c.create_polygon(head_x - 34, head_y - 22, head_x - 21, head_y - 56, head_x - 9, head_y - 20, fill=CAT_ORANGE, outline="")
        c.create_polygon(head_x + 9, head_y - 20, head_x + 21, head_y - 56, head_x + 34, head_y - 22, fill=CAT_ORANGE, outline="")
        c.create_polygon(head_x - 28, head_y - 24, head_x - 21, head_y - 44, head_x - 15, head_y - 23, fill="#f7c0cf", outline="")
        c.create_polygon(head_x + 15, head_y - 23, head_x + 21, head_y - 44, head_x + 28, head_y - 24, fill="#f7c0cf", outline="")

        # 额头花纹
        c.create_line(head_x - 9, head_y - 30, head_x - 4, head_y - 18, width=2, fill="#d98e49", capstyle=tk.ROUND)
        c.create_line(head_x, head_y - 32, head_x, head_y - 18, width=2, fill="#d98e49", capstyle=tk.ROUND)
        c.create_line(head_x + 9, head_y - 30, head_x + 4, head_y - 18, width=2, fill="#d98e49", capstyle=tk.ROUND)

        # 眼睛
        eye_y = head_y + 2
        left_eye_x = head_x - 17
        right_eye_x = head_x + 17
        blink = self.blink_frames > 0

        if is_sleep:
            c.create_arc(left_eye_x - 8, eye_y - 3, left_eye_x + 8, eye_y + 8, start=200, extent=140, style=tk.ARC, width=2, outline=CAT_DARK)
            c.create_arc(right_eye_x - 8, eye_y - 3, right_eye_x + 8, eye_y + 8, start=200, extent=140, style=tk.ARC, width=2, outline=CAT_DARK)
        elif is_happy:
            c.create_arc(left_eye_x - 8, eye_y - 2, left_eye_x + 8, eye_y + 14, start=200, extent=140, style=tk.ARC, width=2, outline=CAT_DARK)
            c.create_arc(right_eye_x - 8, eye_y - 2, right_eye_x + 8, eye_y + 14, start=200, extent=140, style=tk.ARC, width=2, outline=CAT_DARK)
        elif blink:
            c.create_line(left_eye_x - 7, eye_y, left_eye_x + 7, eye_y, width=2, fill=CAT_DARK)
            c.create_line(right_eye_x - 7, eye_y, right_eye_x + 7, eye_y, width=2, fill=CAT_DARK)
        else:
            c.create_oval(left_eye_x - 7, eye_y - 8, left_eye_x + 7, eye_y + 8, fill=CAT_DARK, outline="")
            c.create_oval(right_eye_x - 7, eye_y - 8, right_eye_x + 7, eye_y + 8, fill=CAT_DARK, outline="")
            c.create_oval(left_eye_x - 2, eye_y - 5, left_eye_x + 2, eye_y - 1, fill="white", outline="")
            c.create_oval(right_eye_x - 2, eye_y - 5, right_eye_x + 2, eye_y - 1, fill="white", outline="")

        # 鼻子嘴巴
        nose_y = head_y + 18
        c.create_polygon(head_x - 4, nose_y, head_x + 4, nose_y, head_x, nose_y + 5, fill="#e8929c", outline="")
        c.create_line(head_x, nose_y + 5, head_x, nose_y + 12, width=1.5, fill=CAT_DARK)

        if is_happy:
            c.create_arc(head_x - 16, nose_y + 5, head_x, nose_y + 21, start=200, extent=140, style=tk.ARC, width=1.8, outline=CAT_DARK)
            c.create_arc(head_x, nose_y + 5, head_x + 16, nose_y + 21, start=200, extent=140, style=tk.ARC, width=1.8, outline=CAT_DARK)
        else:
            c.create_line(head_x, nose_y + 12, head_x - 8, nose_y + 16, width=1.5, fill=CAT_DARK, smooth=True)
            c.create_line(head_x, nose_y + 12, head_x + 8, nose_y + 16, width=1.5, fill=CAT_DARK, smooth=True)

        # 胡须
        c.create_line(head_x - 42, nose_y + 1, head_x - 16, nose_y + 3, width=1.2, fill="#555")
        c.create_line(head_x - 43, nose_y + 10, head_x - 16, nose_y + 8, width=1.2, fill="#555")
        c.create_line(head_x + 16, nose_y + 3, head_x + 42, nose_y + 1, width=1.2, fill="#555")
        c.create_line(head_x + 16, nose_y + 8, head_x + 43, nose_y + 10, width=1.2, fill="#555")

        # 腮红
        if not is_sleep:
            c.create_oval(head_x - 35, head_y + 15, head_x - 24, head_y + 25, fill=CAT_PINK, outline="")
            c.create_oval(head_x + 24, head_y + 15, head_x + 35, head_y + 25, fill=CAT_PINK, outline="")

    def draw_bubble(self, cx, cy, text):
        c = self.canvas
        width = max(72, min(170, 13 * len(text)))
        x1 = cx - width // 2
        y1 = cy - 17
        x2 = cx + width // 2
        y2 = cy + 17
        c.create_oval(x1, y1, x2, y2, fill="white", outline="#d9d9d9")
        c.create_polygon(cx - 8, y2 - 3, cx + 5, y2 - 2, cx - 2, y2 + 14, fill="white", outline="#d9d9d9")
        c.create_text(cx, cy, text=text, font=("Microsoft YaHei", 10), fill="#444")

    def draw_heart(self, x, y, scale=1.0):
        c = self.canvas
        s = scale
        points = [
            x, y + 10 * s,
            x - 18 * s, y - 3 * s,
            x - 14 * s, y - 22 * s,
            x, y - 15 * s,
            x + 14 * s, y - 22 * s,
            x + 18 * s, y - 3 * s,
        ]
        c.create_polygon(points, fill="#ff7aa2", outline="", smooth=True)

    def draw_fish(self, x, y):
        c = self.canvas
        c.create_oval(x - 18, y - 8, x + 12, y + 8, fill="#75c7ff", outline="")
        c.create_polygon(x + 10, y, x + 24, y - 10, x + 24, y + 10, fill="#75c7ff", outline="")
        c.create_oval(x - 11, y - 3, x - 7, y + 1, fill="#1c4e70", outline="")

    def draw_sleep_marks(self):
        c = self.canvas
        offset = int((math.sin(self.breath_phase) + 1) * 4)
        c.create_text(171, 45 - offset, text="Z", font=("Microsoft YaHei", 13, "bold"), fill="#7aa6c8")
        c.create_text(190, 30 - offset, text="Z", font=("Microsoft YaHei", 16, "bold"), fill="#7aa6c8")
        c.create_text(211, 13 - offset, text="Z", font=("Microsoft YaHei", 19, "bold"), fill="#7aa6c8")


if __name__ == "__main__":
    root = tk.Tk()
    app = DesktopCat(root)
    root.mainloop()
