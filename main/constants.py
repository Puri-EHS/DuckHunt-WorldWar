import os

# Initialization
OG_GAME_WIDTH = 256
OG_GAME_HEIGHT = 240

SCREEN_SCALE = 3

SCREEN_WIDTH = OG_GAME_WIDTH * SCREEN_SCALE
SCREEN_HEIGHT = OG_GAME_HEIGHT * SCREEN_SCALE

BASE_DIR = "../"
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
MUSIC_DIR = os.path.join(ASSETS_DIR, "music")

# Game
USE_MOUSE = True
FPS = 60


# Asset Paths

# Music
LOBBY_MUSIC_PATH = os.path.join(MUSIC_DIR, "fortnite_lobby.mp3")

# UI
SPLASH_SCREEN_PATH = os.path.join(ASSETS_DIR, "ui/splash_screen.png")
TITLE_SCREEN_PATH = os.path.join(ASSETS_DIR, "ui/duck_hunt_menu_bg.png")

PLAY_BUTTON = os.path.join(ASSETS_DIR, "ui/play_button.png")

