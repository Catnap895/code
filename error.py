import ctypes

ctypes.windll.user32.MessageBoxW(
    None,
    "A tiny furry hiccup happened. Please try again!",
    "Oopsie!",
    0x10,
)