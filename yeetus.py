# yeetus.py
# Requirements: pip install opencv-python pillow  (tkinter ships with Python)

# ================= CONFIG =================
VIDEO_PATH   = "fall_up_stairs.mp4"
SHUTDOWN     = False
EAT_KEYS     = False
EAT_KEYBIND  = "<F9>"
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
FONT_SIZE = 8


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

    # --- Font and automatic screen resizing ---
    font = tkfont.Font(
        root=root,
        family="Courier New",
        size=FONT_SIZE
    )

    label = tk.Label(
        root,
        bg="white",
        fg="black",
        font=font,
        justify="center",
        anchor="center",
        padx=0,
        pady=0,
    )
    label.pack(expand=True, fill="both")

    root.update_idletasks()

    cell_width = max(1, font.measure("M"))
    cell_height = max(1, font.metrics("linespace"))

    max_columns = max(
        1,
        (root.winfo_screenwidth() - 8) // cell_width
    )
    max_rows = max(
        1,
        (root.winfo_screenheight() - 8) // cell_height
    )

    # --- key eating state ---
    eating = {"on": EAT_KEYS}

    def toggle_eat(_event=None):
        eating["on"] = not eating["on"]
        label.config(fg="red" if not eating["on"] else "black")
        root.title("key-eating: " + ("ON" if eating["on"] else "OFF"))

    def swallow(event):
        if eating["on"]:
            return "break"
        return None

    # emergency escape works regardless (Esc / Ctrl+C)
    def on_escape(_e):
        root.destroy()
        sys.exit(0)

    root.bind("<Escape>", on_escape)
    root.bind("<Control-c>", on_escape)

    # toggle keybind always works too
    root.bind(EAT_KEYBIND, toggle_eat)

    # eat everything else when enabled
    EATEN = (
        "<Key>",
        "<Any-KeyPress>",
        "<Button-1>",
        "<Button-2>",
        "<Button-3>",
        "<ButtonRelease>",
        "<Motion>",
        "<Wheel>",
        "<FocusIn>",
        "<FocusOut>"
    )

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

    def finish():
        root.destroy()
        shutdown()

    if cap is None:
        label.config(
            text=MESSAGE +
            "\n(video not found or cv2 missing, enjoy the white screen)"
        )
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

            # --- AUTOMATIC RESIZING ---
            # Account for character width and height
            # so the video keeps its original aspect ratio.

            char_aspect = (w / h) * (cell_height / cell_width)

            columns = min(
                max_columns,
                max(1, round(max_rows * char_aspect))
            )

            rows = min(
                max_rows,
                max(1, round(columns / char_aspect))
            )

            # Resize frame to available character cells
            small = cv2.resize(
                gray,
                (columns, rows),
                interpolation=cv2.INTER_AREA
            )

            # --- ASCII conversion ---
            lo, hi = int(small.min()), int(small.max())

            if hi == lo:
                idx = small * 0
            else:
                idx = (
                    (hi - small).astype("float32")
                    / (hi - lo)
                    * (len(ASCII_CHARS) - 1)
                ).astype("int32")

            art = "\n".join(
                "".join(ASCII_CHARS[i] for i in row)
                for row in idx
            )

            label.config(text=art)

            root.after(delay, frame_loop)

        frame_loop()

    root.mainloop()


if __name__ == "__main__":
    show_message()
    run_ascii_video()