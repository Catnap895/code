# 🦊 9Tails — PyVaultSim

**An educational ransomware simulator by Team 9Tails, written in Python — real crypto, zero malicious behavior, full transparency.**

---

## 🚨 DANGERS — READ BEFORE ANYTHING ELSE

This project deals with **real encryption** and simulates **real ransomware behavior**. Do not take it lightly.

**What can go wrong if misused:**

- 🔐 **Permanent file loss** — files encrypted by this tool are only recoverable with the private key. Lose the key, lose your files. Forever.
- 💣 **System-wide encryption** — if pointed at the wrong directory (or your root drive), it can encrypt your entire system, including OS files, making your machine unbootable.
- 📁 **Backups & network shares** — if you run it against mapped drives, cloud-synced folders, or shared directories, you can destroy your own backups and other people's data.
- 🔑 **Legal consequences** — using this software on systems you do not own or lack written permission to test may be a **serious crime** under laws like the Computer Fraud and Abuse Act (CFAA) or the Computer Misuse Act, with penalties including fines and imprisonment.
- 👤 **You are the only one responsible.** Not your school, not your employer, not your hosting provider — **you**.

## ⚠️ NO RESPONSIBILITY / DISCLAIMER

> ### **9Tails takes ABSOLUTELY NO responsibility for ANY damages, data loss, system destruction, legal trouble, or ANY other consequences — direct or indirect — resulting from the use or misuse of this software.**
>
> This project is provided for **educational and research purposes only**, under the following terms:
>
> - **NO WARRANTY** — this software is provided "as-is", with no guarantee it works, is safe, or is fit for any purpose.
> - **NO LIABILITY** — under no circumstances shall 9Tails be held liable for any claim, damages, or other liability arising from the use of this code, even if advised of the possibility of such damages.
> - **YOUR RISK** — by downloading, copying, running, or even reading this code, you accept **100% of the risk** and **100% of the liability** for anything that happens.
> - **EDUCATIONAL USE ONLY** — this tool must **NEVER** be used on any files, systems, or networks that you do not personally own or do not have **explicit, written permission** to test.
> - **NO SUPPORT FOR MISUSE** — issues asking how to use this tool maliciously will be closed and reported.
>
> **If you cannot accept these terms, delete this repository and do not use the software.**

---

## 📖 About

**9Tails** built PyVaultSim to demonstrate how real-world ransomware works **at a technical level** using legitimate cryptography libraries. It combines:

- **AES-256 (symmetric)** — fast file content encryption
- **RSA-4096 (asymmetric)** — protects the AES key, mirroring the hybrid encryption model used in real ransomware: *your data is locked with AES, but the AES key is locked with RSA*

The goal is to understand the threat model — not to weaponize it.

## ✨ Features

- 🔑 Hybrid encryption: AES for files, RSA for key wrapping
- 🗂️ Recursive directory traversal with configurable file extension filters
- 💾 Encrypted files written with a custom extension (e.g., `.vault`)
- 🧪 Built-in safe test environment: creates dummy files in an isolated sandbox directory
- 🔓 Decryption mode using the recovered private key
- 📜 Detailed logging of every operation (**no network calls at all**)

## 🦊 About 9Tails

**9Tails** is a security research team focused on understanding offensive techniques to build better defenses. Find us on GitHub: `github.com/9tails`


## Running Code
 code will not run without a file on your desktop called fox_sandbox when that is done run python fixed_foxed_sim.py
 to decrypt run python foxed_decrpytor.py private_key.pem


## ⚖️ License

This project is licensed under **Creative Commons**. See the [LICENSE](LICENSE) file for details.

- 📝 **Attribution required** — credit **9Tails** when reusing or sharing, link to the original repo, and note any changes.
- 🚫 Check the LICENSE file for specific terms (commercial use, adaptations, share-alike rules).
- ❌ Provided "as-is" with **no warranties** — this reinforces the disclaimer above.

For more info on Creative Commons licenses, visit [creativecommons.org](https://creativecommons.org).
