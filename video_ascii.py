from pathlib import Path
import tkinter as tk
import tkinter.font as tkfont

try:
    import cv2
except ImportError:
    cv2 = None


VIDEO_PATH = Path(__file__).with_name("fall_up_stairs.mp4")
ASCII_CHARS = " .:-=+*#%@"
FONT_SIZE = 8


def run_ascii_video():
    root = tk.Tk()
    root.title("ASCII Video")
    root.configure(bg="black")
    root.attributes("-fullscreen", True)

    font = tkfont.Font(root=root, family="Courier New", size=FONT_SIZE)
    label = tk.Label(
        root,
        bg="black",
        fg="white",
        font=font,
        justify="center",
        anchor="center",
        padx=0,
        pady=0,
    )
    label.pack(expand=True, fill="both")

    capture = None

    def close(_event=None):
        if capture is not None:
            capture.release()
        root.destroy()

    root.bind("<Escape>", close)
    root.protocol("WM_DELETE_WINDOW", close)

    if cv2 is None:
        label.config(text="OpenCV is required.\nInstall it with: pip install opencv-python")
        root.mainloop()
        return

    capture = cv2.VideoCapture(str(VIDEO_PATH))
    if not capture.isOpened():
        capture.release()
        capture = None
        label.config(text=f"Could not open video:\n{VIDEO_PATH.name}\n\nPress Esc to exit.")
        root.mainloop()
        return

    root.update_idletasks()
    cell_width = max(1, font.measure("M"))
    cell_height = max(1, font.metrics("linespace"))
    max_columns = max(1, (root.winfo_screenwidth() - 8) // cell_width)
    max_rows = max(1, (root.winfo_screenheight() - 8) // cell_height)

    fps = capture.get(cv2.CAP_PROP_FPS)
    delay_ms = max(1, round(1000 / fps)) if fps > 0 else 33

    def show_next_frame():
        if capture is None:
            return

        success, frame = capture.read()
        if not success:
            close()
            return

        height, width = frame.shape[:2]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Fit the image in character cells while accounting for the font's
        # taller-than-wide shape, so the ASCII rendering keeps the video aspect.
        char_aspect = (width / height) * (cell_height / cell_width)
        columns = min(max_columns, max(1, round(max_rows * char_aspect)))
        rows = min(max_rows, max(1, round(columns / char_aspect)))

        small = cv2.resize(gray, (columns, rows), interpolation=cv2.INTER_AREA)
        low, high = int(small.min()), int(small.max())
        if high == low:
            indices = small * 0
        else:
            indices = ((high - small).astype("float32") / (high - low)
                       * (len(ASCII_CHARS) - 1)).astype("int32")

        art = "\n".join(
            "".join(ASCII_CHARS[index] for index in row)
            for row in indices
        )
        label.config(text=art)
        root.after(delay_ms, show_next_frame)

    show_next_frame()
    root.mainloop()


if __name__ == "__main__":
    run_ascii_video()
