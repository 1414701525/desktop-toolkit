import tkinter as tk
import random
import time

WIDTH = 560
HEIGHT = 640
PLAYER_SIZE = 34


class DodgeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("躲避小游戏")
        self.root.resizable(False, False)

        self.status = tk.Label(
            root,
            text="按空格开始 | WASD / 方向键移动 | P 暂停",
            font=("Microsoft YaHei", 12)
        )
        self.status.pack(pady=8)

        self.canvas = tk.Canvas(
            root,
            width=WIDTH,
            height=HEIGHT,
            bg="#f7f7fb",
            highlightthickness=0
        )
        self.canvas.pack(padx=12, pady=6)

        self.keys = set()
        self.running = False
        self.paused = False

        self.player = None
        self.player_x = WIDTH // 2
        self.player_y = HEIGHT - 70

        self.objects = []
        self.score = 0
        self.lives = 3
        self.shield = 0
        self.start_time = 0

        root.bind("<KeyPress>", self.key_down)
        root.bind("<KeyRelease>", self.key_up)

        self.draw_start_screen()

    def draw_start_screen(self):
        self.canvas.delete("all")
        self.canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2 - 60,
            text="躲避小游戏",
            font=("Microsoft YaHei", 26, "bold"),
            fill="#333"
        )
        self.canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2,
            text="躲开红色障碍\n吃黄色金币加分\n蓝色护盾可挡一次伤害",
            font=("Microsoft YaHei", 14),
            fill="#555",
            justify="center"
        )
        self.canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2 + 95,
            text="按空格开始",
            font=("Microsoft YaHei", 16, "bold"),
            fill="#222"
        )

    def start_game(self):
        self.canvas.delete("all")
        self.objects.clear()

        self.running = True
        self.paused = False
        self.score = 0
        self.lives = 3
        self.shield = 0
        self.start_time = time.time()

        self.player_x = WIDTH // 2
        self.player_y = HEIGHT - 70

        self.player = self.canvas.create_rectangle(
            self.player_x - PLAYER_SIZE // 2,
            self.player_y - PLAYER_SIZE // 2,
            self.player_x + PLAYER_SIZE // 2,
            self.player_y + PLAYER_SIZE // 2,
            fill="#4a90e2",
            outline=""
        )

        self.spawn_object()
        self.game_loop()

    def key_down(self, event):
        key = event.keysym.lower()
        self.keys.add(key)

        if key == "space" and not self.running:
            self.start_game()

        if key == "p" and self.running:
            self.paused = not self.paused
            if self.paused:
                self.status.config(text="已暂停，按 P 继续")
            else:
                self.status.config(text="继续游戏")

    def key_up(self, event):
        self.keys.discard(event.keysym.lower())

    def move_player(self):
        speed = 7
        dx = 0
        dy = 0

        if "a" in self.keys or "left" in self.keys:
            dx -= speed
        if "d" in self.keys or "right" in self.keys:
            dx += speed
        if "w" in self.keys or "up" in self.keys:
            dy -= speed
        if "s" in self.keys or "down" in self.keys:
            dy += speed

        self.player_x += dx
        self.player_y += dy

        half = PLAYER_SIZE // 2
        self.player_x = max(half, min(WIDTH - half, self.player_x))
        self.player_y = max(half, min(HEIGHT - half, self.player_y))

        self.canvas.coords(
            self.player,
            self.player_x - half,
            self.player_y - half,
            self.player_x + half,
            self.player_y + half
        )

    def spawn_object(self):
        if not self.running:
            return

        if self.paused:
            self.root.after(300, self.spawn_object)
            return

        elapsed = time.time() - self.start_time
        difficulty = min(8, elapsed / 12)

        obj_type = random.choices(
            ["rock", "coin", "shield"],
            weights=[72, 22, 6],
            k=1
        )[0]

        size = random.randint(24, 42)
        x = random.randint(size, WIDTH - size)
        y = -size

        if obj_type == "rock":
            item = self.canvas.create_rectangle(
                x - size // 2,
                y - size // 2,
                x + size // 2,
                y + size // 2,
                fill="#e85d5d",
                outline=""
            )
            speed = random.uniform(3.2, 5.2) + difficulty * 0.45

        elif obj_type == "coin":
            item = self.canvas.create_oval(
                x - size // 2,
                y - size // 2,
                x + size // 2,
                y + size // 2,
                fill="#f6c945",
                outline=""
            )
            speed = random.uniform(2.8, 4.4) + difficulty * 0.35

        else:
            item = self.canvas.create_oval(
                x - size // 2,
                y - size // 2,
                x + size // 2,
                y + size // 2,
                fill="#5cc8ff",
                outline=""
            )
            speed = random.uniform(2.6, 4.0) + difficulty * 0.25

        self.objects.append({
            "id": item,
            "type": obj_type,
            "speed": speed
        })

        interval = int(max(220, 760 - elapsed * 8))
        self.root.after(interval, self.spawn_object)

    def game_loop(self):
        if not self.running:
            return

        if self.paused:
            self.root.after(16, self.game_loop)
            return

        self.move_player()
        self.move_objects()
        self.check_collision()
        self.update_status()

        self.root.after(16, self.game_loop)

    def move_objects(self):
        for obj in self.objects[:]:
            self.canvas.move(obj["id"], 0, obj["speed"])
            coords = self.canvas.coords(obj["id"])

            if coords and coords[1] > HEIGHT + 60:
                self.canvas.delete(obj["id"])
                self.objects.remove(obj)

    def check_collision(self):
        player_box = self.canvas.bbox(self.player)

        for obj in self.objects[:]:
            obj_box = self.canvas.bbox(obj["id"])

            if not obj_box:
                continue

            if self.overlap(player_box, obj_box):
                self.canvas.delete(obj["id"])
                self.objects.remove(obj)

                if obj["type"] == "rock":
                    if self.shield > 0:
                        self.shield -= 1
                        self.flash("#5cc8ff")
                    else:
                        self.lives -= 1
                        self.flash("#ffb3b3")

                    if self.lives <= 0:
                        self.end_game()

                elif obj["type"] == "coin":
                    self.score += 10
                    self.show_float_text("+10", "#b58a00")

                elif obj["type"] == "shield":
                    self.shield += 1
                    self.show_float_text("护盾 +1", "#0077aa")

    def overlap(self, a, b):
        return not (
            a[2] < b[0] or
            a[0] > b[2] or
            a[3] < b[1] or
            a[1] > b[3]
        )

    def show_float_text(self, text, color):
        item = self.canvas.create_text(
            self.player_x,
            self.player_y - 35,
            text=text,
            font=("Microsoft YaHei", 14, "bold"),
            fill=color
        )

        def move_up(step=0):
            if step >= 18:
                self.canvas.delete(item)
                return
            self.canvas.move(item, 0, -2)
            self.root.after(25, lambda: move_up(step + 1))

        move_up()

    def flash(self, color):
        old = self.canvas["bg"]
        self.canvas.config(bg=color)
        self.root.after(90, lambda: self.canvas.config(bg=old))

    def update_status(self):
        elapsed = int(time.time() - self.start_time)
        total_score = self.score + elapsed
        self.status.config(
            text=f"分数：{total_score}    生命：{self.lives}    护盾：{self.shield}    时间：{elapsed}s"
        )

    def end_game(self):
        self.running = False

        elapsed = int(time.time() - self.start_time)
        final_score = self.score + elapsed

        self.canvas.create_rectangle(
            60,
            HEIGHT // 2 - 110,
            WIDTH - 60,
            HEIGHT // 2 + 120,
            fill="white",
            outline="#ddd"
        )

        if final_score >= 180:
            comment = "很强，反应速度拉满。"
        elif final_score >= 100:
            comment = "不错，已经有点手感了。"
        else:
            comment = "差一点，再来一把。"

        self.canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2 - 50,
            text="游戏结束",
            font=("Microsoft YaHei", 24, "bold"),
            fill="#333"
        )
        self.canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2 + 5,
            text=f"最终分数：{final_score}",
            font=("Microsoft YaHei", 16),
            fill="#333"
        )
        self.canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2 + 45,
            text=comment,
            font=("Microsoft YaHei", 13),
            fill="#555"
        )
        self.canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2 + 85,
            text="按空格重新开始",
            font=("Microsoft YaHei", 13, "bold"),
            fill="#222"
        )


root = tk.Tk()
game = DodgeGame(root)
root.mainloop()