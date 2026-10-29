import tkinter as tk
import random, threading, time, os, sys

# ============ SETTINGS ============
VIDEO_PATH = "fall_up_stairs.mp4"   # put your video here
SHUTDOWN_ENABLED = False               # <-- TOGGLE: True = shuts down when popups finish
NUM_POPUPS = 20                      # all of these stay on screen
POPUP_INTERVAL = 0.05                 # fast spawn = screen fills up quickly
# ==================================

ERRORS = [
    ("FurryOS", "KERNEL_PAW_EXCEPTION_NOT_HANDLED", "STOP CODE: 0x00000FUW", "Your system has encountered too much floof in sector FUX-01. A tail is wedged in the GPU fan."),
    ("Furry Update Service", "Update Failure (0x8007PAWS)", "Windows Furry Update could not install 'Fluffy_Definitions_v9.3' because your fur density exceeds the supported limit.", "Error details: snoot.bump not found (0x8007BOOP)"),
    ("FoxyDefender", "Threat detected!", "FoxyDefender real-time protection detected a serious threat: 'tail_wag.exe' is 100% adorable and cannot be quarantined.", "Recommended action: give head pats immediately."),
    ("System", "Out of memory (WOOF_EXCEPTION)", "The page file is full of fur. Windows requires 4 GB of free belly rubs to continue.", "Stop code: 0x00000MRRP"),
    ("Driver Error", "Display driver stopped responding", "nvfurr.sys has stopped responding and has successfully recovered... but it is very sad about it.", "Error: 0x887000EARS"),
    ("FurryOS", "CRITICAL_FLUFF_FAILURE", "STOP CODE: 0x00000YIP", "A critical component of the floof subsystem has curled up for a nap. Please do not wake the component."),
    ("Bluetooth", "Device pairing failed (0x00007TAIL)", "Could not pair with device 'Fox Ears (Pro)' — the device wiggled out of range while shaking off bath water.", "Try holding the paw button for 5 seconds."),
    ("Recycle Bin", "recycle_bin_full_of_toys.exe", "The Recycle Bin is full of squeaky toys and cannot be emptied. The toys are emotionally attached to the system."),
    ("FoxySoft Systems 🦊", "Ventriloquism Alert", "Your fox has been talking this whole time. Windows is only pretending to understand. (0x8007NYA)"),
    ("Battery", "Low battery (0x00000NAP)", "Battery at 3%. Your device will hibernate soon. It will dream about chasing digital squirrels."),
    ("Windows Security", "FUZZWALL has blocked a program", "Windows Fuzzwall prevented an unverified application ('treats.exe') from accessing your snoot.", "Publisher: Unknown Fluff (Unverified Paws)"),
    ("Storage", "Disk full (0x00000CHONK)", "Drive C: has reached maximum chonk capacity. Delete some old zoomies to free up space."),
]

CUTE_FLOATERS = [
    "♥ UwU so fluffy!! ♥",
    "(◕ᴗ◕✿) boop the snoot!",
    "✧･ﾟ: *✧🐾 hewwo!! ✧*:ﾟ･✧",
    "≽^•⩊•^≼ nya~!!",
    "ʕ•ᴥ•ʔ huggies??",
    "(=^･ω･^=) mrrp!",
    "☆*:.｡.o(≧▽≦)o.｡.:*☆",
    "༼ つ ◕_◕ ༽つ pet me pls",
    "(˶ᵔ ᵕ ᵔ˶) tail wags!!",
    "(´｡• ᵕ •｡`) ♡ uwu",
]

EMOJIS = ["🐾", "🦊", "🐱", "🐶", "🐰", "🐻", "🐼", "🦝", "🐹", "💖", "✨", "🧸"]
PASTELS = ["#ffd1dc", "#ffe4e1", "#fff0f5", "#e6e6fa", "#ffb7b2", "#ffdfd3", "#d4f0ff", "#fffacd"]
FOX_TAG = "🦊 FurryOS v9.9 — made with love (and fur) by FoxySoft Systems 🦊"

def make_fake_error():
    app, title, body, detail = random.choice(ERRORS)
    if random.random() < 0.4:
        detail = f"{detail}\n\n{FOX_TAG}"
    else:
        title = f"{title} 🐾"

    w = tk.Tk()
    w.title(f"{app} — Error")
    w.attributes("-topmost", True)
    w.resizable(False, False)
    x = random.randint(0, max(w.winfo_screenwidth() - 420, 0))
    y = random.randint(0, max(w.winfo_screenheight() - 220, 0))
    w.geometry(f"+{x}+{y}")

    top = tk.Frame(w, bg="#ffffff")
    top.pack(fill="both", expand=True, padx=14, pady=(14, 4))

    icon = tk.Label(top, text="⚠️", font=("Segoe UI Emoji", 30))
    if random.random() < 0.35:
        icon.config(text="🦊")
    icon.pack(side="left", padx=(0, 12))

    msgbox = tk.Frame(top, bg="#ffffff")
    msgbox.pack(side="left", fill="both", expand=True)
    tk.Label(msgbox, text=title, font=("Segoe UI", 10, "bold"), bg="#ffffff",
             fg="#1a1a1a", wraplength=300, justify="left").pack(anchor="w")
    tk.Label(msgbox, text=body, font=("Segoe UI", 9), bg="#ffffff",
             fg="#1a1a1a", wraplength=300, justify="left").pack(anchor="w", pady=(4, 0))
    if detail:
        tk.Label(msgbox, text=detail, font=("Segoe UI", 8), bg="#ffffff",
                 fg="#555555", wraplength=300, justify="left").pack(anchor="w", pady=(6, 0))

    btnbar = tk.Frame(w, bg="#f0f0f0")
    btnbar.pack(fill="x", side="bottom")
    inner = tk.Frame(btnbar, bg="#f0f0f0")
    inner.pack(pady=8)
    tk.Button(inner, text="OK 🐾", width=12).pack(side="left", padx=4)
    if random.random() < 0.5:
        tk.Button(inner, text="Pet instead", width=12).pack(side="left", padx=4)

    w.mainloop()  # window STAYS until closed manually

def make_floater():
    w = tk.Tk()
    w.overrideredirect(True)
    w.attributes("-topmost", True)
    bg = random.choice(PASTELS)
    w.configure(bg=bg)
    sw, sh = w.winfo_screenwidth(), w.winfo_screenheight()
    x, y = random.randint(0, max(sw - 300, 0)), random.randint(0, max(sh - 120, 0))
    w.geometry(f"260x90+{x}+{y}")

    tk.Label(w, text=" ".join(random.choices(EMOJIS, k=5)), font=("Segoe UI Emoji", 20),
             bg=bg, fg="#ff5c8a").pack(pady=(6, 0))
    tk.Label(w, text=random.choice(CUTE_FLOATERS), font=("Comic Sans MS", 11, "bold"),
             bg=bg, fg="#8a5cff").pack()

    def wiggle():
        try:
            w.geometry(f"260x90+{x + random.randint(-3, 3)}+{y + random.randint(-3, 3)}")
            w.after(80, wiggle)
        except tk.TclError:
            pass
    wiggle()
    w.mainloop()

def show_video():
    try:
        if sys.platform == "win32":
            os.startfile(VIDEO_PATH)
        elif sys.platform == "darwin":
            os.system(f'open "{VIDEO_PATH}"')
        else:
            os.system(f'xdg-open "{VIDEO_PATH}"')
        time.sleep(7)  # match your video length
    except Exception as e:
        print("video error:", e)

def popup_storm(on_done):
    """Spawn all popups; every window STAYS. Fires on_done the instant the last one appears."""
    threads = []
    for i in range(NUM_POPUPS):
        target = make_fake_error if random.random() < 0.65 else make_floater
        t = threading.Thread(target=target, daemon=True)
        t.start()
        threads.append(t)
        time.sleep(POPUP_INTERVAL)
        # fire shutdown the MOMENT the last popup hits the screen
        if i == NUM_POPUPS - 1 and on_done:
            on_done()

def boot_screen():
    w = tk.Tk()
    w.title("FurryOS")
    w.attributes("-topmost", True)
    w.geometry("420x160+" + str(w.winfo_screenwidth() // 2 - 210) + "+" + str(w.winfo_screenheight() // 2 - 80))
    w.configure(bg="#0078d7")
    tk.Label(w, text="🦊", font=("Segoe UI Emoji", 40), bg="#0078d7", fg="white").pack(pady=(20, 4))
    tk.Label(w, text="FurryOS is preparing fluffy updates...", font=("Segoe UI", 11),
             bg="#0078d7", fg="white").pack()
    tk.Label(w, text="0xPAWS  — do not turn off your fox", font=("Segoe UI", 9),
             bg="#0078d7", fg="#cfe8ff").pack(pady=(6, 0))
    w.after(3500, w.destroy)
    w.mainloop()

def instant_shutdown():
    if sys.platform == "win32":
        # /t 0 = immediate, no countdown window
        os.system('shutdown /s /t 0')
    elif sys.platform == "darwin":
        os.system("sudo shutdown -h now")
    else:
        os.system("shutdown -h now")

def main():
    print(FOX_TAG)
    boot_screen()
    show_video()

    threading.Thread(target=popup_storm, kwargs={"on_done": instant_shutdown if SHUTDOWN_ENABLED else None},
                     daemon=True).start()

    while threading.active_count() > 1:
        time.sleep(1)

if __name__ == "__main__":
    main()