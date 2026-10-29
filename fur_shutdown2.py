import tkinter as tk
import random, threading, time, os, sys

# ============ SETTINGS ============
NUM_POPUPS = 320
POPUP_INTERVAL = 0.04
MOVE_INTERVAL = 0.05
MOVE_MODE = "drift"     # "drift" = bounce around, "teleport" = jump anywhere
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
    if sys.platform == "win32":
        import ctypes
        u = ctypes.windll.user32
        u.SetProcessDPIAware()
        return u.GetSystemMetrics(0), u.GetSystemMetrics(1)
    r = tk.Tk(); r.withdraw()
    w, h = r.winfo_screenwidth(), r.winfo_screenheight(); r.destroy()
    return w, h

SW, SH = screen_size()
BOX_W, BOX_H = 450, 220

# ================= WINDOWS =================
def find_hwnd_by_title(target_title, my_pid, timeout=5.0):
    """Reliably find our MessageBox HWND: EnumWindows + EXACT title + PID check."""
    import ctypes
    from ctypes import wintypes
    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32

    EnumWindowsProc = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    deadline = time.time() + timeout

    while time.time() < deadline:
        result = []
        @EnumWindowsProc
        def cb(hwnd, lParam):
            length = user32.GetWindowTextLengthW(hwnd)
            if length == 0:
                return True
            buf = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buf, length + 1)
            if buf.value == target_title:          # exact match, no prefix races
                pid = wintypes.DWORD()
                user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
                if pid.value == my_pid:            # definitely OUR dialog (#32770)
                    result.append(hwnd)
                    return False
            return True
        user32.EnumWindows(cb, 0)
        if result:
            return result[0]
        time.sleep(0.05)
    return None

def move_loop(hwnd, start_x, start_y):
    import ctypes
    from ctypes import wintypes
    user32 = ctypes.windll.user32
    SWP_NOSIZE, SWP_NOZORDER = 0x0001, 0x0004
    SWP_NOACTIVATE = 0x0010

    dx = random.choice([-1, 1]) * random.randint(5, 14)
    dy = random.choice([-1, 1]) * random.randint(5, 14)
    x, y = start_x, start_y
    while user32.IsWindow(hwnd):
        if MOVE_MODE == "teleport":
            x = random.randint(0, max(SW - BOX_W, 0))
            y = random.randint(0, max(SH - BOX_H, 0))
        else:
            x += dx; y += dy
            if x < 0 or x > SW - BOX_W: dx = -dx; x = max(0, min(x, SW - BOX_W))
            if y < 0 or y > SH - BOX_H: dy = -dy; y = max(0, min(y, SH - BOX_H))
        user32.SetWindowPos(hwnd, 0, int(x), int(y), 0, 0, SWP_NOSIZE | SWP_NOZORDER | SWP_NOACTIVATE)
        time.sleep(MOVE_INTERVAL)

def spawn_native_error():
    import ctypes
    from ctypes import wintypes
    user32 = ctypes.windll.user32

    title, msg = random.choice(NATIVE_ERRORS)
    uniq = f"{title}  §{random.randint(100000, 999999)}"   # guaranteed-unique title
    start_x = random.randint(0, max(SW - BOX_W, 0))
    start_y = random.randint(0, max(SH - BOX_H, 0))

    my_pid = os.getpid()
    mover = threading.Thread(target=lambda: (
        (lambda h: h and move_loop(h, start_x, start_y))(
            find_hwnd_by_title(uniq, my_pid)
        )
    ), daemon=True)
    mover.start()

    MB_ICONERROR, MB_SYSTEMMODAL, MB_SETFOREGROUND = 0x00000010, 0x00001000, 0x00010000
    flags = MB_ICONERROR | MB_SYSTEMMODAL | MB_SETFOREGROUND
    if random.random() < 0.25:
        flags |= 0x00000004
    user32.MessageBoxW(0, msg, uniq, flags)

# ================= NON-WINDOWS FALLBACK =================
def clone_error(title, msg):
    w = tk.Tk()
    w.title(title)
    w.attributes("-topmost", True)
    w.resizable(False, False)
    x, y = random.randint(0, max(SW - 450, 0)), random.randint(0, max(SH - 220, 0))
    w.geometry(f"+{x}+{y}")
    w.configure(bg="#f0f0f0")
    body = tk.Frame(w, bg="#f0f0f0"); body.pack(fill="both", expand=True, padx=16, pady=16)
    tk.Label(body, text="🦊" if random.random() < 0.3 else "⛔",
             font=("Segoe UI Emoji", 28), bg="#f0f0f0").pack(side="left", padx=(0, 14))
    tk.Label(body, text=msg, font=("DejaVu Sans", 9), bg="#f0f0f0", wraplength=320,
             justify="left").pack(side="left", fill="both", expand=True)
    btns = tk.Frame(w, bg="#f0f0f0"); btns.pack(fill="x", pady=(0, 12))
    inner = tk.Frame(btns, bg="#f0f0f0"); inner.pack()
    tk.Button(inner, text="OK", width=10).pack(side="left", padx=3)
    if random.random() < 0.4:
        tk.Button(inner, text="Cancel", width=10).pack(side="left", padx=3)
    dx, dy = random.choice([-1, 1]) * 8, random.choice([-1, 1]) * 8
    def roam():
        try:
            nonlocal x, y, dx, dy
            if MOVE_MODE == "teleport":
                x, y = random.randint(0, max(SW - 450, 0)), random.randint(0, max(SH - 220, 0))
            else:
                x, y = x + dx, y + dy
                if x < 0 or x > SW - 450: dx = -dx
                if y < 0 or y > SH - 220: dy = -dy
            w.geometry(f"+{x}+{y}")
            w.after(int(MOVE_INTERVAL * 1000), roam)
        except tk.TclError:
            pass
    roam()
    w.mainloop()

def spawn_error():
    if sys.platform == "win32":
        threading.Thread(target=spawn_native_error, daemon=True).start()
    else:
        title, msg = random.choice(NATIVE_ERRORS)
        threading.Thread(target=clone_error, args=(title, msg), daemon=True).start()

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
    tk.Label(w, text="Deploying floof errors to every corner of your screen... 🐾",
             font=("Segoe UI", 11), bg="#1b0f2e", fg="#9b8ec4").pack(pady=(30, 0))
    w.after(4000, w.destroy)
    w.mainloop()

def error_storm():
    for i in range(NUM_POPUPS):
        spawn_error()
        time.sleep(POPUP_INTERVAL)

def main():
    print(FOX_TAG)
    scare_screen()
    threading.Thread(target=error_storm, daemon=True).start()
    while threading.active_count() > 1:
        time.sleep(1)

if __name__ == "__main__":
    main()