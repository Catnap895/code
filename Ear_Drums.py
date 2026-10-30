import ctypes
from pathlib import Path

from pydub import AudioSegment
from pydub.playback import play

script_dir = Path(__file__).resolve().parent
mp3_path = script_dir / "song.mp3"
print(f"Script: {Path(__file__).resolve()}")
print(f"Looking for MP3: {mp3_path}")
if not mp3_path.is_file():
    available_mp3s = sorted(path.name for path in script_dir.glob("*.mp3"))
    details = f" MP3 files in this folder: {', '.join(available_mp3s)}." if available_mp3s else ""
    raise FileNotFoundError(f"Couldn't find {mp3_path}.{details}")

song = AudioSegment.from_mp3(str(mp3_path))

# Mix in the low frequencies with a moderate boost, then leave some peak headroom.
bass = song.low_pass_filter(150).apply_gain(6)
boosted = song.overlay(bass).normalize(headroom=1.0)



ctypes.windll.user32.MessageBoxW(
    None,
    "SAY GOODBYE TO YOUR EAR DRUMS",
    "SOUND WARNING!",
    0x10,
)



play(boosted)