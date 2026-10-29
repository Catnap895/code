# yeetus.py
# Requirements: pip install opencv-python pillow  (tkinter ships with Python)

# ================= CONFIG =================
VIDEO_PATH   = "fall_up_stairs.mp4"      # your dancing furry mp4
SHUTDOWN     = False                  # False = don't shut down, just play and exit
EAT_KEYS     = False                   # True = swallow all keybinds on startup
EAT_KEYBIND  = "<F9>"                 # keybind to toggle key-eating on/off at runtime
MESSAGE      = "YEETUS DELETUS! SAY HI TO JESUS!"
# ==========================================

import os
import sys
import threading
import tkinter as tk
import tkinter.font as tkfont

try:
    import cv2
except ImportError:
    cv2 = None
try:
    from PIL import Image
except ImportError:
    Image = None

ASCII_CHARS = " .:-=+*#%@"

# --- 1. Message box ---
def show_message():
    try:
        import tkinter.messagebox as mb
        root = tk.Tk()
        root.withdraw()
        mb.showinfo("A Very Important Message", MESSAGE)
        root.destroy()
    except Exception:
        print(MESSAGE)

# --- 2. Shutdown ---
def shutdown():
    if not SHUTDOWN:
        return
    if sys.platform == "win32":
        os.system('shutdown /s /t 5 /c "YEETUS DELETUS"')
    elif sys.platform == "darwin":
        os.system("osascript -e 'tell app \"System Events\" to shut down'")
    else:
        os.system("shutdown -h now")

# --- 3. Fullscreen white window with ASCII video ---
def run_ascii_video():
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.configure(bg="white")
    root.attributes("-topmost", True)

    label = tk.Label(root, bg="white", fg="black", font=("Courier", 8))
    label.pack(expand=True)

    # --- key eating state ---
    eating = {"on": EAT_KEYS}

    def toggle_eat(_event=None):
        eating["on"] = not eating["on"]
        label.config(fg="red" if not eating["on"] else "black")
        root.title("key-eating: " + ("ON" if eating["on"] else "OFF"))

    def swallow(event):
        if eating["on"]:
            return "break"          # eat the event, don't let it propagate
        return None                 # keys pass through normally

    # emergency escape works regardless (Esc / Ctrl+C)
    def on_escape(_e): root.destroy(); sys.exit(0)
    root.bind("<Escape>", on_escape)
    root.bind("<Control-c>", on_escape)

    # toggle keybind always works too
    root.bind(EAT_KEYBIND, toggle_eat)

    # eat everything else when enabled
    EATEN = ("<Key>", "<Any-KeyPress>", "<Button-1>", "<Button-2>", "<Button-3>",
             "<ButtonRelease>", "<Motion>", "<Wheel>", "<FocusIn>", "<FocusOut>")
    for seq in EATEN:
        try:
            root.bind_all(seq, swallow)
        except Exception:
            pass

    # --- ASCII video ---
    cap = None
    if cv2 is not None:
        cap = cv2.VideoCapture(VIDEO_PATH)
        if not cap.isOpened():
            cap = None

    if cap is None:
        label.config(text=MESSAGE + "\n(video not found or cv2 missing, enjoy the white screen)")
        root.update()
    else:
        fps = cap.get(cv2.CAP_PROP_FPS) or 30
        delay = max(1, int(1000 / fps))

        def frame_loop():
            ret, frame = cap.read()
            if not ret:
                cap.release()
                root.after(500, finish)
                return
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            h, w = gray.shape
            target_w = 220
            target_h = max(1, int(h * target_w / w * 0.5))
            small = cv2.resize(gray, (target_w, target_h))
            lo, hi = small.min(), small.max()
            if hi == lo: hi = lo + 1
            norm = (small.astype(float) - lo) / (hi - lo)
            idx = ((1.0 - norm) * (len(ASCII_CHARS) - 1)).astype(int)
            art = "\n".join("".join(ASCII_CHARS[i] for i in row) for row in idx)
            label.config(text=art)
            root.after(delay, frame_loop)

        frame_loop()

    def finish():
        root.destroy()
        shutdown()

    root.mainloop()

if __name__ == "__main__":
    show_message()
    run_ascii_video()