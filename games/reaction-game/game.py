import tkinter as tk
import random
import math

WIDTH = 520
HEIGHT = 360
GAME_TIME = 30

score = 0
combo = 0
best_combo = 0
time_left = GAME_TIME
running = False

target_x = 0
target_y = 0
target_r = 24
target_id = None


def new_target():
    global target_x, target_y, target_r, target_id

    canvas.delete("target")

    target_r = max(12, 26 - score // 5)
    target_x = random.randint(target_r + 10, WIDTH - target_r - 10)
    target_y = random.randint(target_r + 10, HEIGHT - target_r - 10)

    target_id = canvas.create_oval(
        target_x - target_r,
        target_y - target_r,
        target_x + target_r,
        target_y + target_r,
        fill="#ff7aa2",
        outline="",
        tags="target"
    )

    canvas.create_oval(
        target_x - target_r + 7,
        target_y - target_r + 7,
        target_x + target_r - 7,
        target_y + target_r - 7,
        fill="#ffd1dc",
        outline="",
        tags="target"
    )


def start_game():
    global score, combo, best_combo, time_left, running

    score = 0
    combo = 0
    best_combo = 0
    time_left = GAME_TIME
    running = True

    start_button.config(state="disabled")
    result_label.config(text="")
    update_info()
    new_target()
    countdown()


def countdown():
    global time_left, running

    if not running:
        return

    update_info()

    if time_left <= 0:
        end_game()
        return

    time_left -= 1
    root.after(1000, countdown)


def update_info():
    info_label.config(
        text=f"时间：{time_left}s    分数：{score}    连击：{combo}"
    )


def click_canvas(event):
    global score, combo, best_combo

    if not running:
        return

    distance = math.sqrt((event.x - target_x) ** 2 + (event.y - target_y) ** 2)

    if distance <= target_r:
        score += 1
        combo += 1
        best_combo = max(best_combo, combo)

        show_text("+1", event.x, event.y)
        new_target()
    else:
        combo = 0
        show_text("Miss", event.x, event.y)

    update_info()


def show_text(text, x, y):
    item = canvas.create_text(
        x,
        y,
        text=text,
        font=("Microsoft YaHei", 14, "bold"),
        fill="#444"
    )

    def float_up(step=0):
        if step >= 12:
            canvas.delete(item)
            return
        canvas.move(item, 0, -2)
        root.after(30, lambda: float_up(step + 1))

    float_up()


def end_game():
    global running

    running = False
    canvas.delete("target")
    start_button.config(state="normal")

    if score >= 35:
        comment = "太强了，这手速有点离谱。"
    elif score >= 25:
        comment = "很厉害，反应速度不错。"
    elif score >= 15:
        comment = "还不错，再来一把应该更高。"
    else:
        comment = "手速加载中，建议再挑战一次。"

    result_label.config(
        text=f"游戏结束！\n最终分数：{score}\n最高连击：{best_combo}\n{comment}"
    )


root = tk.Tk()
root.title("30秒反应力挑战")
root.resizable(False, False)

title_label = tk.Label(
    root,
    text="30秒反应力挑战",
    font=("Microsoft YaHei", 18, "bold")
)
title_label.pack(pady=8)

info_label = tk.Label(
    root,
    text=f"时间：{GAME_TIME}s    分数：0    连击：0",
    font=("Microsoft YaHei", 12)
)
info_label.pack()

canvas = tk.Canvas(
    root,
    width=WIDTH,
    height=HEIGHT,
    bg="#fff7fb",
    highlightthickness=0
)
canvas.pack(padx=12, pady=10)
canvas.bind("<Button-1>", click_canvas)

start_button = tk.Button(
    root,
    text="开始游戏",
    font=("Microsoft YaHei", 12),
    width=14,
    command=start_game
)
start_button.pack(pady=4)

result_label = tk.Label(
    root,
    text="",
    font=("Microsoft YaHei", 12),
    justify="center"
)
result_label.pack(pady=8)

root.mainloop()