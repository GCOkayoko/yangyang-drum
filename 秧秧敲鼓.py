"""
秧秧敲鼓 — 双人版（tkinter）
双击运行。点一下播完整段鼓声。
"""
import tkinter as tk
import os, random
from PIL import Image, ImageTk

# 优先用 pygame 播放 WAV；没有则用 winsound 合成音
try:
    import pygame
    pygame.mixer.init()
    HAS_PYGAME = True
except Exception:
    HAS_PYGAME = False

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(BASE, "img")
WAV = os.path.join(BASE, "鼓声.wav")

drum_sound = None
if HAS_PYGAME and os.path.exists(WAV):
    try:
        drum_sound = pygame.mixer.Sound(WAV)
    except Exception:
        pass

def play_drum():
    if drum_sound:
        drum_sound.play()
    else:
        import winsound, threading
        def _beep():
            winsound.Beep(150, 80)
            winsound.Beep(800, 80)
        threading.Thread(target=_beep, daemon=True).start()

W, H = 900, 660
TOTAL1, TOTAL2 = 20, 60
SPEED = 100

root = tk.Tk()
root.title("大鼓 大鼓 敲敲敲")
root.configure(bg="#0a0e17")
root.resizable(False, False)

frames1 = [ImageTk.PhotoImage(Image.open(os.path.join(IMG, f"drum1_frame_{i+1:03d}.png"))) for i in range(TOTAL1)]
frames2 = [ImageTk.PhotoImage(Image.open(os.path.join(IMG, f"frame_{i+1:03d}.png"))) for i in range(TOTAL2)]

canvas = tk.Canvas(root, width=W, height=H, bg="#0a0e17", highlightthickness=0)
canvas.pack()

canvas.create_text(W//2, 30, text="大鼓 大鼓 敲敲敲！！！", fill="#c9a961",
                    font=("Microsoft YaHei", 24, "bold"))

stage1_cx, stage1_cy = W//4, H//2 + 10
stage2_cx, stage2_cy = W*3//4, H//2 + 10
STAGE = 400

for cx, cy in [(stage1_cx, stage1_cy), (stage2_cx, stage2_cy)]:
    for i in range(3):
        s = STAGE - i*12
        canvas.create_rectangle(cx-s//2, cy-s//2, cx+s//2, cy+s//2,
                                outline="#4a90d9", width=1)

canvas.create_text(stage1_cx, stage1_cy-STAGE//2-20, text="◁ 敲鼓1",
                   fill="#888", font=("Microsoft YaHei", 12))
canvas.create_text(stage2_cx, stage2_cy-STAGE//2-20, text="敲鼓2 ▷",
                   fill="#888", font=("Microsoft YaHei", 12))

img1_id = canvas.create_image(stage1_cx, stage1_cy, image=frames1[0])
img2_id = canvas.create_image(stage2_cx, stage2_cy, image=frames2[0])

f1, f2 = 0, 0
auto_on, auto_job = False, None

canvas.create_text(W//2, H-25, text="键盘 F/J 或点击  |  空格 启停自动播放",
                   fill="#666", font=("Microsoft YaHei", 11))

btn_auto_bg = canvas.create_rectangle(W//2-105, H-58, W//2-5, H-28,
                                       fill="#111827", outline="#7a6a3d")
btn_reset_bg = canvas.create_rectangle(W//2+5, H-58, W//2+105, H-28,
                                        fill="#111827", outline="#7a6a3d")
btn_auto_txt = canvas.create_text(W//2-55, H-43, text="▶ 自动播放",
                                   fill="#7a6a3d", font=("Microsoft YaHei", 12))
btn_reset_txt = canvas.create_text(W//2+55, H-43, text="↺ 归零",
                                    fill="#7a6a3d", font=("Microsoft YaHei", 12))

def update_btn():
    if auto_on:
        canvas.itemconfig(btn_auto_bg, outline="#c9a961")
        canvas.itemconfig(btn_auto_txt, fill="#c9a961", text="⏸ 停止")
    else:
        canvas.itemconfig(btn_auto_bg, outline="#7a6a3d")
        canvas.itemconfig(btn_auto_txt, fill="#7a6a3d", text="▶ 自动播放")

# 粒子
particles = []
def spawn_particle():
    x = random.randint(0, W)
    c = canvas.create_oval(x-2, H+10, x+2, H+14, fill="#c9a961", outline="", tags="particle")
    particles.append({"id": c, "x": x, "y": H+10,
                       "vy": -1.5 - random.random()*1.5,
                       "vx": (random.random()-0.5)*0.3,
                       "life": 60 + random.randint(0, 60)})
for _ in range(25):
    spawn_particle()

def update_particles():
    for p in particles[:]:
        p["y"] += p["vy"]; p["x"] += p["vx"]; p["life"] -= 1
        r = 3
        canvas.coords(p["id"], p["x"]-r, p["y"]-r, p["x"]+r, p["y"]+r)
        if p["life"] <= 0 or p["y"] < -20:
            canvas.delete(p["id"])
            particles.remove(p)
            spawn_particle()

# 敲鼓
def hit_drum():
    global f1, f2
    f1 = (f1 + 1) % TOTAL1; f2 = (f2 + 1) % TOTAL2
    canvas.itemconfig(img1_id, image=frames1[f1])
    canvas.itemconfig(img2_id, image=frames2[f2])
    # 特效
    fx1 = canvas.create_text(stage1_cx-30, stage1_cy-60, text="咚",
                              fill="#c9a961", font=("Microsoft YaHei", 22, "bold"), tags="fx")
    fx2 = canvas.create_text(stage2_cx+30, stage2_cy-60, text="嗒",
                              fill="#c9a961", font=("Microsoft YaHei", 22, "bold"), tags="fx")
    root.after(500, lambda: (canvas.delete(fx1), canvas.delete(fx2)))
    for cx, cy in [(stage1_cx, stage1_cy), (stage2_cx, stage2_cy)]:
        flash = canvas.create_rectangle(cx-STAGE//2, cy-STAGE//2,
                                         cx+STAGE//2, cy+STAGE//2,
                                         fill="#c9a961", stipple="gray25",
                                         outline="", tags="flash")
        root.after(80, lambda f=flash: canvas.delete(f))
    play_drum()

def reset_all():
    global f1, f2, auto_on, auto_job
    f1 = f2 = 0
    canvas.itemconfig(img1_id, image=frames1[0])
    canvas.itemconfig(img2_id, image=frames2[0])
    if auto_job:
        root.after_cancel(auto_job); auto_job = None
    auto_on = False
    update_btn()

def toggle_auto():
    global auto_on, auto_job
    auto_on = not auto_on
    update_btn()
    if auto_on:
        def step():
            global auto_job
            if auto_on:
                hit_drum()
                auto_job = root.after(SPEED, step)
        step()
    else:
        if auto_job:
            root.after_cancel(auto_job); auto_job = None

# 事件
def on_key_press(event):
    if event.keysym.lower() in ('f', 'j'):
        hit_drum()
    elif event.keysym == 'space':
        toggle_auto()

root.bind("<Key>", on_key_press)

def on_click(event):
    x, y = event.x, event.y
    if W//2-105 <= x <= W//2-5 and H-58 <= y <= H-28:
        toggle_auto()
    elif W//2+5 <= x <= W//2+105 and H-58 <= y <= H-28:
        reset_all()
    else:
        hit_drum()

canvas.bind("<Button-1>", on_click)

def loop():
    update_particles()
    root.after(40, loop)

loop()
root.mainloop()
