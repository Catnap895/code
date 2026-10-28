🦊 9Tails — PyVaultSim
An educational ransomware simulator by Team 9Tails, written in Python — real crypto, zero malicious behavior, full transparency.

⚠️ Disclaimer
9Tails takes NO responsibility for any damages, misuse, or consequences resulting from the use of this software. This project is provided for educational and research purposes only. You are solely responsible for how you use it. By using this code, you accept full liability for your actions. DO NOT use this on any files or systems you do not own or have explicit written permission to test.

📖 About
9Tails built PyVaultSim to demonstrate how real-world ransomware works at a technical level using legitimate cryptography libraries. It combines:

AES-256 (symmetric) — fast file content encryption
RSA-4096 (asymmetric) — protects the AES key, mirroring the hybrid encryption model used in real ransomware: your data is locked with AES, but the AES key is locked with RSA
The goal is to understand the threat model — not to weaponize it.

✨ Features
🔑 Hybrid encryption: AES for files, RSA for key wrapping
🗂️ Recursive directory traversal with configurable file extension filters
💾 Encrypted files written with a custom extension (e.g., .vault)
🧪 Built-in safe test environment: creates dummy files in an isolated sandbox directory
🔓 Decryption mode using the recovered private key
📜 Detailed logging of every operation (no network calls at all)
🦊 About 9Tails
9Tails is a security research team focused on understanding offensive techniques to build better defenses. Find us on GitHub: github.com/9tails

⚖️ License
MIT — for educational use only. See the disclaimer above.

