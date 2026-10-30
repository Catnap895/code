import os
import math
import random
import threading
import time
import ctypes
import shutil
import subprocess
import tempfile
from pathlib import Path

import tkinter as tk

# ============================ CONFIG ====================================

CONFIG = {
    # Audio
    "VOLUME": 100,               # ffplay playback volume (0-100)
    # Popup behavior
    "SPAWN_START_DELAY": 0.0,    # seconds before first popup
    "SPAWN_INTERVAL_START": 2.0, # seconds between popup spawns (start)
    "SPAWN_INTERVAL_MIN": 0.25,  # fastest spawn interval
    "SPAWN_ACCELERATION": 0.92,  # interval multiplied by this each spawn
    "MAX_WINDOWS": 40,           # hard cap
    "MOVE_SPEED": 40,            # pixels/second
    "MOVE_INTERVAL_MS": 33,      # movement tick (~30 FPS)
    # Math bomb
    "MATH_BOMB_ENABLED": True,   # CPU math bomb toggle
    "MATH_THREADS": 4,
    "GPU_MATH_ENABLED": True,    # GPU math bomb toggle (needs torch + CUDA)
}

# ========================================================================

MB_ICONWARNING = 0x30

FURRY_WARNINGS = [
    "OMIGOSH!! 🐾 Your ear drums are about to go BYE BYE, cutie~! nyaa~! 🔊",
    "H-hewwo?? 🦊 The bass is gonna NOM NOM on your eardrums! x3",
    "⚠️ ATTENTION FLOOF! ⚠️ Say goodbye to your ear drums, paw friend! UwU",
    "nyaaa~~ 🔊🔥 This audio is NOT otter-safe! Cover your fluffy ears!! >w<",
    "Bork bork!! 🐕 LOUDNESS INCOMING!! Your ears won't be a good boi after this!",
    "mrrow~! 🐱 Disclaimer: no furries were harmed, only your EAR DRUMS! mew mew! :3",
    "OWO WHAT'S THIS?? 🔊 It's the sound of your hearing LEAVING, snuggle muffin~!",
    "*boops your volume slider* 🐾 Sorry not sorry~! EARDRUM DESTRUCTION INCOMING! x3",
    "HONK HONK 🦆 Your ears are about to get RAVAGED by BASS, little floofer!",
    "vewy vewy loud!! 🐰 You have exactly 0 seconds to save your ear drums!! awoo~! 🐺",
]

FURRY_ERROR_TEXTS = [
    "ERROR: EARDRUM.EXE HAS STOPPED RESPONDING 🐾 nyaa~!",
    "FATAL EXCEPTION: too much floof 🔊 your ears could not handle the bass! x3",
    "ERROR 0x0W0: EAR_DRUMS_NOT_FOUND 🦊 they gone, paw friend~!",
    "SYSTEM WARNING: BASS_LEVELS_EXCEED_FLOOF_LIMIT!! >w<",
    "ERROR: could not recover hearing... uwu sowwy!! 🔊",
    "CANNOT COMPLY: ears are now extra fluffy 🐱 mew!",
    "ERROR: AUDIO_TOO_LOUD_ERROR_LOUD_ERROR_LOUD 🐺 awoooooo!!",
    "CRITICAL: your ear drums have left the chat :c bye bye~! x3",
]


# ------------------- audio -------------------

def find_ffmpeg_tool(name: str) -> str | None:
    executable = shutil.which(name)
    if executable is not None:
        return executable

    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data is None:
        return None

    package_root = Path(local_app_data) / "Microsoft" / "WinGet" / "Packages"
    matches = sorted(
        package_root.glob(f"Gyan.FFmpeg.Shared*/*/bin/{name}.exe"),
        reverse=True,
    )
    return str(matches[0]) if matches else None


def prepare_audio(mp3_path: Path, wav_path: Path, ffmpeg: str) -> bool:
    """Boost the bass hard but keep it audible (no full-scale clipping)."""
    convert = subprocess.run(
        [
            ffmpeg,
            "-nostdin",
            "-hide_banner",
            "-loglevel", "error",
            "-y",
            "-i", str(mp3_path),
            "-af",
            (
                "equalizer=f=60:t=q:w=2:g=12,"
                "equalizer=f=100:t=q:w=1:g=8,"
                "bass=gain=10,"
                "volume=3:precision=double"
            ),
            "-ac", "2",
            "-ar", "44100",
            "-c:a", "pcm_s16le",
            str(wav_path),
        ],
        check=False,
    )
    return convert.returncode == 0


def playback_loop(ffplay: str, wav_path: Path, stop_event: threading.Event) -> None:
    """Play the boosted audio on loop forever until the stop event is set."""
    while not stop_event.is_set():
        proc = subprocess.Popen(
            [
                ffplay,
                "-hide_banner",
                "-loglevel", "error",
                "-nodisp",
                "-autoexit",
                "-volume", str(CONFIG["VOLUME"]),
                str(wav_path),
            ]
        )
        while proc.poll() is None:
            if stop_event.is_set():
                proc.terminate()
                return
            time.sleep(0.1)


# ------------------- math bomb -------------------

def cpu_math_bomb(stop_event: threading.Event) -> None:
    x = 1.0000001
    while not stop_event.is_set():
        for _ in range(100_000):
            x = x * x % 1.7976931348623157e308
            x += 0.0000001
        if x > 1e10 or x < 1e-10:
            x = 1.0000001


def gpu_math_bomb(stop_event: threading.Event) -> None:
    try:
        import torch
    except ImportError:
        print("GPU_MATH_ENABLED is on but torch is not installed — skipping GPU bomb.")
        return

    if not torch.cuda.is_available():
        print("No CUDA GPU found — skipping GPU bomb.")
        return

    device = torch.device("cuda")
    a = torch.randn(2048, 2048, device=device)
    b = torch.randn(2048, 2048, device=device)
    while not stop_event.is_set():
        c = torch.matmul(a, b)
        a = c * 0.000001


# ------------------- popup window system -------------------

class PopupManager:
    def __init__(self, root: tk.Tk, stop_event: threading.Event):
        self.root = root
        self.stop_event = stop_event
        self.windows: list[dict] = []
        self.spawn_interval = CONFIG["SPAWN_INTERVAL_START"]
        self.shutting_down = False

        self.screen_w = self.root.winfo_screenwidth()
        self.screen_h = self.root.winfo_screenheight()

        # bind_all catches Escape no matter which window has focus
        self.root.bind_all("<Escape>", self.shutdown)

        if CONFIG["SPAWN_START_DELAY"] > 0:
            self.root.after(int(CONFIG["SPAWN_START_DELAY"] * 1000), self._schedule_spawn)
        else:
            self._schedule_spawn()
        self._schedule_move()

    def _spawn_one(self) -> None:
        if self.shutting_down:
            return

        if len(self.windows) < CONFIG["MAX_WINDOWS"]:
            try:
                self._create_popup()
            except Exception as e:
                print(f"Popup spawn failed: {e}")

        self.spawn_interval = max(
            CONFIG["SPAWN_INTERVAL_MIN"],
            self.spawn_interval * CONFIG["SPAWN_ACCELERATION"],
        )
        self._schedule_spawn()

    def _create_popup(self) -> None:
        text = random.choice(FURRY_ERROR_TEXTS)
        win = tk.Toplevel(self.root)

        # 1) position and size it FIRST, while still a normal window
        x = random.randint(0, max(1, self.screen_w - 320))
        y = random.randint(0, max(1, self.screen_h - 160))
        win.geometry(f"300x120+{x}+{y}")

        label = tk.Label(
            win,
            text=f"FUNNY SOUND ERROR!! x3\n\n{text}",
            bg="#1a1a2e",
            fg="#ff6b9d",
            font=("Segoe UI", 10, "bold"),
            padx=12,
            pady=8,
            justify="left",
            wraplength=270,
        )
        label.pack(fill="both", expand=True)

        # 2) force it to map, THEN strip the title bar
        win.update_idletasks()
        win.overrideredirect(True)
        win.lift()
        win.attributes("-topmost", True)

        # 3) per-window Escape binding as a fallback
        win.bind("<Escape>", self.shutdown)
        label.bind("<Escape>", self.shutdown)

        angle = random.uniform(0, 2 * math.pi)
        self.windows.append(
            {
                "win": win,
                "dx": math.cos(angle),
                "dy": math.sin(angle),
            }
        )

    def _schedule_spawn(self) -> None:
        self.root.after(int(self.spawn_interval * 1000), self._spawn_one)

    def _schedule_move(self) -> None:
        self.root.after(CONFIG["MOVE_INTERVAL_MS"], self._move_tick)

    def _move_tick(self) -> None:
        if self.shutting_down:
            return
        step = CONFIG["MOVE_SPEED"] * (CONFIG["MOVE_INTERVAL_MS"] / 1000.0)

        for item in self.windows:
            win = item["win"]
            try:
                if not win.winfo_exists():
                    continue
            except tk.TclError:
                continue
            x = win.winfo_x()
            y = win.winfo_y()
            nx = x + item["dx"] * step
            ny = y + item["dy"] * step

            w = 300
            h = 120
            if nx <= 0 or nx + w >= self.screen_w:
                item["dx"] *= -1
                nx = max(0, min(nx, self.screen_w - w))
            if ny <= 0 or ny + h >= self.screen_h:
                item["dy"] *= -1
                ny = max(0, min(ny, self.screen_h - h))

            try:
                win.geometry(f"+{int(nx)}+{int(ny)}")
            except tk.TclError:
                pass

        self._schedule_move()

    def shutdown(self, event=None) -> None:
        if self.shutting_down:
            return
        self.shutting_down = True
        self.stop_event.set()
        try:
            self.root.destroy()
        except tk.TclError:
            pass


# ------------------- main -------------------

def main() -> int:
    script_dir = Path(__file__).resolve().parent
    mp3_path = script_dir / "song.mp3"
    if not mp3_path.is_file():
        print(f"MP3 not found: {mp3_path}")
        print("Put song.mp3 in the same folder as this script.")
        return 1

    ffmpeg = find_ffmpeg_tool("ffmpeg")
    ffplay = find_ffmpeg_tool("ffplay")
    if ffmpeg is None or ffplay is None:
        missing = [n for n, p in (("ffmpeg", ffmpeg), ("ffplay", ffplay)) if p is None]
        print(f"Missing required program(s): {', '.join(missing)}")
        print("Install FFmpeg with: winget install --id Gyan.FFmpeg.Shared --exact")
        print("Then reopen PowerShell and run this script again.")
        return 1

    with tempfile.TemporaryDirectory(prefix="bass_boost_") as temp_dir:
        wav_path = Path(temp_dir) / "boosted.wav"
        if not prepare_audio(mp3_path, wav_path, ffmpeg):
            print("FFmpeg could not process the MP3. Check that the file is a valid audio file.")
            return 1

        print("Starting chaos. Press Escape (click a popup first if needed) to stop. uwu")

        stop_event = threading.Event()

        audio_thread = threading.Thread(
            target=playback_loop, args=(ffplay, wav_path, stop_event), daemon=True
        )
        audio_thread.start()

        if CONFIG["MATH_BOMB_ENABLED"]:
            for i in range(CONFIG["MATH_THREADS"]):
                threading.Thread(
                    target=cpu_math_bomb, args=(stop_event,), daemon=True
                ).start()
            print(f"CPU math bomb running with {CONFIG['MATH_THREADS']} threads.")

        if CONFIG["GPU_MATH_ENABLED"]:
            threading.Thread(target=gpu_math_bomb, args=(stop_event,), daemon=True).start()

        root = tk.Tk()
        root.withdraw()

        manager = PopupManager(root, stop_event)

        try:
            root.mainloop()
        finally:
            stop_event.set()
            audio_thread.join(timeout=2)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())