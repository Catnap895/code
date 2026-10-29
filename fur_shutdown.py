import tkinter as tk
import random, threading, time, os, sys

# ============ SETTINGS ============
NUM_POPUPS = 60
POPUP_INTERVAL = 0.04
MOVE_INTERVAL = 0.35    # how often each window jumps/moves to a new spot
MOVE_MODE = "drift"     # "drift" = smooth wiggles, "teleport" = jump anywhere on screen
# ==================================

NATIVE_ERRORS = [
    ("FurryOS", "kernel-paw.exe — Application Error\n\nThe instruction at 0x00000FUW referenced memory at 0x0000FLOOF. The memory could not be \"floof\".\n\nClick on OK to terminate the program.\nClick on CANCEL to pet the fox instead."),
    ("System Error", "Stop code: KERNEL_PAW_EXCEPTION_NOT_HANDLED\n\nWhat failed: nvfurr.sys\n\nYour PC ran into a problem with too much floof and needs to restart. We're just collecting some tail data, and then we'll restart for you."),
    ("Microsoft Furry Visual C++ Runtime Library", "Runtime Error!\n\nProgram: C:\\Windows\\System32\\tail_wag.exe\n\nR6034\nAn application has made an attempt to load the C runtime library incorrectly. Please contact the application's support team (the fox is the support team)."),
    ("Windows", "Windows cannot find 'snoot_bump.exe'. Make sure you typed the name correctly, and then try again. Also the snoot was booped. (0x8007BOOP)"),
    ("Error", "The procedure entry point Fluffy_Definitions_v9.3 could not be located in the dynamic link library C:\\Windows\\SYSTEM32\\furrdll.dll."),
    ("FoxyDefender Threats found", "Threats found: 1\n\nName: tail_wag.exe\nSeverity: Severe (100% adorable)\nDetails: This threat cannot be quarantined because it is too fluffy.\n\nRecommended action: give head pats immediately."),
    ("Microsoft Furry Store", "This app can't open.\n\nThere was a problem and 'Fur Central' can't be opened. Try again later. The fox is napping. (0x8007NAP)"),
    ("Disk Full Error", "There is not enough space on Drive C:.\n\nDrive C: has reached maximum chonk capacity. You need an additional 4 GB of belly rubs to free up space. (0x8007CHONK)"),
    ("Windows Update", "We couldn't complete the updates\nUndoing changes made to your fur.\n\nDon't turn off your computer. Don't pet the fox either. Ok fine, pet the fox."),
    ("Device Not Recognized", "USB Device Not Recognized.\n\nThe last USB device you connected to this computer malfunctioned — it was a fox and it chewed through the cable. Windows does not recognize the chew marks."),
    ("Not Responding", "C:\\Windows\\explorer.paw is not responding.\n\nIf you close the program, you might lose information. The program is busy chasing a digital squirrel. End now? Wait for the zoomies to finish?"),
    ("Out of Memory", "Out of memory or system resources. Close some windows and try again.\n\nNote: all 320 windows are made of fur. Closing is impossible. (0xE06D7363, or as the fox says: nyet)"),
]

FOX_TAG = "🦊 FoxySoft Systems — FurryOS v9.9"

def screen_size():
    try:
        import ctypes
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    except Exception:
        root = tk.Tk(); root.withdraw()
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.destroy()
        return w, h

SW, SH = screen_size()

# ---------------- WINDOWS: real MessageBox, moved around via Win32 ----------------
def move_window_loop(title):
    """Keep relocating a native MessageBox by its HWND."""
    if sys.platform != "win32":
        return
    import ctypes
    user32 = ctypes.windll.user32
    hwnd = None
    # wait for the box to appear
    for _ in range(50):
        hwnd = user32.FindWindowW(None, title)
        if hwnd:
            break
        time.sleep(0.02)
    if not hwnd:
        return

    SWP_NOSIZE = 0x0001
    SWP_NOZORDER = 0x0004
    dx, dy = random.choice([-1, 1]) * random.randint(4, 10), random.choice([-1, 1]) * random.randint(4, 10)

    while True:
        if not user32.IsWindow(hwnd):
            break  # user closed it (or died trying)
        if MOVE_MODE == "teleport":
            x = random.randint(0, max(SW - 450, 0))
            y = random.randint(0, max(SH - 250, 0))
        else:  # drift + bounce off edges
            x, y = ctypes.c_int(), ctypes.c_int()
            # read current position
            rect = ctypes.wintypes.RECT() if hasattr(ctypes, "wintypes") else None
            try:
                import ctypes.wintypes
                rect = ctypes.wintypes.RECT()
                user32.GetWindowRect(hwnd, ctypes.byref(rect))
                x, y = rect.left + dx, rect.top + dy
                if x < 0 or x > SW - 450: dx = -dx
                if y < 0 or y > SH - 250: dy = -dy
            except Exception:
                x, y = random.randint(0, SW - 450), random.randint(0, SH - 250)
        user32.SetWindowPos(hwnd, 0, int(x), int(y), 0, 0, SWP_NOSIZE | SWP_NOZORDER)
        time.sleep(MOVE_INTERVAL)

def spawn_native_error():
    title, msg = random.choice(NATIVE_ERRORS)
    # unique-ish title so FindWindow finds the right box
    title = f"{title}  [{random.randint(1000,9999)}]"
    threading.Thread(target=move_window_loop, args=(title,), daemon=True).start()

    if sys.platform == "win32":
        import ctypes
        MB_ICONERROR = 0x00000010
        MB_SYSTEMMODAL = 0x00001000
        MB_SETFOREGROUND = 0x00010000
        flags = MB_ICONERROR | MB_SYSTEMMODAL | MB_SETFOREGROUND
        if random.random() < 0.25:
            flags |= 0x00000004  # OK/Cancel
        ctypes.windll.user32.MessageBoxW(0, msg, title, flags)
    else:
        clone_error(title.split("  [")[0], msg)

# ---------------- NON-WINDOWS FALLBACK: Tk clone that drifts ----------------
def clone_error(title, msg):
    w = tk.Tk()
    w.title(title)
    w.attributes("-topmost", True)
    w.resizable(False, False)
    x, y = random.randint(0, max(SW - 450, 0)), random.randint(0, max(SH - 250, 0))
    w.geometry(f"+{x}+{y}")
    w.configure(bg="#f0f0f0")

    body = tk.Frame(w, bg="#f0f0f0")
    body.pack(fill="both", expand=True, padx=16, pady=16)
    tk.Label(body, text="🦊" if random.random() < 0.3 else "⛔",
             font=("Segoe UI Emoji", 28), bg="#f0f0f0").pack(side="left", padx=(0, 14))
    tk.Label(body, text=msg, font=("Segoe UI", 9), bg="#f0f0f0", wraplength=320,
             justify="left").pack(side="left", fill="both", expand=True)
    btns = tk.Frame(w, bg="#f0f0f0"); btns.pack(fill="x", pady=(0, 12))
    inner = tk.Frame(btns, bg="#f0f0f0"); inner.pack()
    tk.Button(inner, text="OK", width=10).pack(side="left", padx=3)
    if random.random() < 0.4:
        tk.Button(inner, text="Cancel", width=10).pack(side="left", padx=3)

    dx, dy = random.choice([-1, 1]) * random.randint(4, 10), random.choice([-1, 1]) * random.randint(4, 10)
    def roam():
        try:
            nonlocal x, y, dx, dy
            if MOVE_MODE == "teleport":
                x, y = random.randint(0, max(SW - 450, 0)), random.randint(0, max(SH - 250, 0))
            else:
                x, y = x + dx, y + dy
                if x < 0 or x > SW - 450: dx = -dx
                if y < 0 or y > SH - 250: dy = -dy
            w.geometry(f"+{x}+{y}")
            w.after(int(MOVE_INTERVAL * 1000), roam)
        except tk.TclError:
            pass
    roam()
    w.mainloop()

def scare_screen():
    w = tk.Tk()
    w.attributes("-fullscreen", True)
    w.attributes("-topmost", True)
    w.configure(bg="#1b0f2e")
    tk.Label(w, text="🦊", font=("Segoe UI Emoji", 90), bg="#1b0f2e").pack(pady=(120, 10))
    tk.Label(w, text="⚠️ Your PC is about to die ⚠️", font=("Segoe UI", 34, "bold"),
             bg="#1b0f2e", fg="#ff5c8a").pack()
    tk.Label(w, text="...of cuteness overload. We are so sorry. UwU",
             font=("Segoe UI", 14), bg="#1b0f2e", fg="#ffd1dc").pack(pady=10)
    tk.Label(w, text="Deploying roaming floof errors across all screen regions... 🐾",
             font=("Segoe UI", 11), bg="#1b0f2e", fg="#9b8ec4").pack(pady=(30, 0))
    w.after(4000, w.destroy)
    w.mainloop()

def error_storm():
    for i in range(NUM_POPUPS):
        threading.Thread(target=spawn_native_error, daemon=True).start()
        time.sleep(POPUP_INTERVAL)

def main():
    print(FOX_TAG)
    scare_screen()
    threading.Thread(target=error_storm, daemon=True).start()
    while threading.active_count() > 1:
        time.sleep(1)

if __name__ == "__main__":
    main()