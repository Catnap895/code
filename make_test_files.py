"""Create harmless placeholder files for testing file-handling code.

Run with: python make_test_files.py
Files are written only to a generated_test_files folder beside this script.
The files contain plain text; they are not valid documents, media, archives, or databases.
"""

from pathlib import Path
import secrets


EXTENSIONS = (
    ".doc", ".docx", ".pdf", ".xls", ".xlsx", ".pptx",
    ".jpg", ".png", ".mp4", ".mp3",
    ".zip", ".iso",
    ".sql", ".mdb", ".db",
    ".json", ".xml", ".cfg", ".ini",
)
FILES_PER_EXTENSION = 3
OUTPUT_DIR = Path(__file__).with_name("generated_test_files")


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    created = 0

    for extension in EXTENSIONS:
        for _ in range(FILES_PER_EXTENSION):
            path = OUTPUT_DIR / f"test_{secrets.token_hex(6)}{extension}"
            while path.exists():
                path = OUTPUT_DIR / f"test_{secrets.token_hex(6)}{extension}"
            path.write_text(
                "Harmless test fixture. This is plain text, not real file content.\n",
                encoding="utf-8",
            )
            created += 1

    print(f"Created {created} placeholder files in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
