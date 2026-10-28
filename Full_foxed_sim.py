# ---------------------------------------------------------------
# Desktop auto-detect (handles OneDrive vs normal Desktop)
# ---------------------------------------------------------------
desktop = Path.home() / "Desktop"
onedrive_desktop = Path.home() / "OneDrive" / "Desktop"
DESKTOP = onedrive_desktop if onedrive_desktop.exists() else desktop

# ---------------------------------------------------------------
# MODE TOGGLE: "single" or "directory"
# ---------------------------------------------------------------
MODE = "single"      # change to "directory" to encrypt the sandbox folder

# ---------------------------------------------------------------
# SINGLE-FILE TARGET (used only when MODE == "single")
# ---------------------------------------------------------------
TARGET_FILE = DESKTOP / "my_test_file.txt"

# ---------------------------------------------------------------
# SANDBOX DIRECTORY (used only when MODE == "directory")
# ---------------------------------------------------------------
SANDBOX = DESKTOP / "fox_sandbox"

# ---------------------------------------------------------------
# EXTENSIONS ALLOWED
# ---------------------------------------------------------------
EXTS = {
    ".txt", ".doc", ".docx", ".pdf", ".xls", ".xlsx", ".pptx",
    ".jpg", ".png", ".mp4", ".mp3",
    ".zip", ".iso",
    ".sql", ".mdb", ".db",
    ".json", ".xml", ".cfg", ".ini"
}

def get_files():
    """Return either a single target file or all sandbox files."""
    if MODE == "single":
        p = TARGET_FILE
        print(f"[DEBUG] MODE=single, TARGET_FILE={p}, exists={p.exists()}")
        if p.exists() and p.is_file() and p.suffix.lower() in EXTS:
            return [p]
        print(f"[!] TARGET_FILE invalid or unsupported: {p}")
        return []

    elif MODE == "directory":
        print(f"[DEBUG] MODE=directory, scanning SANDBOX={SANDBOX}")
        if not SANDBOX.exists():
            SANDBOX.mkdir(exist_ok=True)
        return [
            p for p in SANDBOX.rglob("*")
            if p.is_file() and p.suffix.lower() in EXTS
        ]

    else:
        print(f"[!] Invalid MODE: {MODE}")
        return []
