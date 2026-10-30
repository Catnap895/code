import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import ctypes


def find_ffmpeg_tool(name: str) -> str | None:
    executable = shutil.which(name)
    if executable is not None:
        return executable

    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data is None:
        return None

    package_root = Path(local_app_data) / "Microsoft" / "WinGet" / "Packages"
    matches = sorted(
        package_root.glob(f"Gyan.FFmpeg.Shared*/*/bin/{name}.exe"),
        reverse=True,
    )
    return str(matches[0]) if matches else None


def main() -> int:
    ctypes.windll.user32.MessageBoxW(
    None,
    "SAY GOODBYE TO YOUR EAR DRUMS",
    "SOUND WARNING!",
    0x10,
    )
    script_dir = Path(__file__).resolve().parent
    mp3_path = script_dir / "song.mp3"
    if not mp3_path.is_file():
        print(f"MP3 not found: {mp3_path}")
        print("Put song.mp3 in the same folder as this script.")
        return 1

    ffmpeg = find_ffmpeg_tool("ffmpeg")
    ffplay = find_ffmpeg_tool("ffplay")
    if ffmpeg is None or ffplay is None:
        missing = [name for name, path in (("ffmpeg", ffmpeg), ("ffplay", ffplay)) if path is None]
        print(f"Missing required program(s): {', '.join(missing)}")
        print("Install FFmpeg with: winget install --id Gyan.FFmpeg.Shared --exact")
        print("Then reopen PowerShell and run this script again.")
        return 1

    with tempfile.TemporaryDirectory(prefix="bass_boost_") as temp_dir:
        wav_path = Path(temp_dir) / "boosted.wav"
        convert = subprocess.run(
            [
                ffmpeg,
                "-nostdin",
                "-hide_banner",
                "-loglevel",
                "error",
                "-y",
                "-i",
                str(mp3_path),
                "-af",
                "equalizer=f=100:t=q:w=1:g=5,alimiter=limit=0.8",
                "-ac",
                "2",
                "-ar",
                "44100",
                "-c:a",
                "pcm_s16le",
                str(wav_path),
            ],
            check=False,
        )
        if convert.returncode != 0:
            print("FFmpeg could not process the MP3. Check that the file is a valid audio file.")
            return convert.returncode

        print("Playing bass-boosted audio once at reduced playback volume.")
        playback = subprocess.run(
            [
                ffplay,
                "-hide_banner",
                "-loglevel",
                "error",
                "-nodisp",
                "-autoexit",
                "-volume",
                "40",
                str(wav_path),
            ],
            check=False,
        )
        if playback.returncode != 0:
            print("FFplay could not play the processed audio.")
        return playback.returncode


if __name__ == "__main__":
    raise SystemExit(main())
