"""
Decryptor - requires the private key the 'victim' was never given.
Run:  python foxed_decryptor.py private_key.pem
"""
import sys
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
import hashlib

SANDBOX = Path.home() / "OneDrive" / "Desktop" / "fox_sandbox"

def main():
    if len(sys.argv) != 2:
        print("Usage: python foxed_decryptor.py private_key.pem")
        sys.exit(1)

    private_key = serialization.load_pem_private_key(
        Path(sys.argv[1]).read_bytes(), password=None)

    # Unwrap the AES key using the private key
    wrapped = (SANDBOX / "key.key").read_bytes()
    aes_key = private_key.decrypt(
        wrapped,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    f = Fernet(aes_key)

    # Walk and undo every .f0x3d file
    for path in SANDBOX.rglob("*.f0x3d"):
        data = path.read_bytes()
        plain = f.decrypt(data)
        real_name = path.with_suffix(path.suffix.replace(".f0x3d", ""))
        real_name.write_bytes(plain)
        path.unlink()
        print(f"  restored {real_name.name}")

    print("Done. All files restored. Give the fox a nugget.")

if __name__ == "__main__":
    main()