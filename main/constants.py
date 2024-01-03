import os

# Initialization
OG_GAME_WIDTH = 256 # 768
OG_GAME_HEIGHT = 240 # 720

SCREEN_SCALE = 3

SCREEN_WIDTH = OG_GAME_WIDTH * SCREEN_SCALE
SCREEN_HEIGHT = OG_GAME_HEIGHT * SCREEN_SCALE

BASE_DIR = ""
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
MUSIC_DIR = os.path.join(ASSETS_DIR, "music")

# Game
USE_MOUSE = True
FPS = 60


# Asset Paths

# Music
LOBBY_MUSIC_PATH = os.path.join(MUSIC_DIR, "fortnite_lobby.mp3")

# Sound
SOUND_DIR = os.path.join(ASSETS_DIR, "sounds")

SHOOT_SOUND_PATH = os.path.join(SOUND_DIR, "gun_shoot.mp3")


# UI
SPLASH_SCREEN_PATH = os.path.join(ASSETS_DIR, "ui/splash_screen.png")
TITLE_SCREEN_PATH = os.path.join(ASSETS_DIR, "ui/duck_hunt_menu_bg.png")
LOADING_SCREEN_PATH = os.path.join(ASSETS_DIR, "ui/earf.png")

PLAY_BUTTON = os.path.join(ASSETS_DIR, "ui/play_button.png")
CROSSHAIR = os.path.join(ASSETS_DIR, "ui/crosshair.png")
CONNOTFOUND = os.path.join(ASSETS_DIR, "ui/con_not_found.png")


#Enemies
ENEMIES_DIR = os.path.join(ASSETS_DIR, "enemies")
TARGET_PATH = os.path.join(ENEMIES_DIR, "target.png")
VANILA_DUCK_PATH = os.path.join(ENEMIES_DIR, "pigeon_front.png")


#Environment
ENVIRONMENT_DIR = os.path.join(ASSETS_DIR, "environment")

SAVANNA = os.path.join(ENVIRONMENT_DIR, "savanna.png")
SAVANNA_BUSH_BACK = os.path.join(ENVIRONMENT_DIR, "savanna_bush_back.png")
SAVANNA_BUSH_FRONT = os.path.join(ENVIRONMENT_DIR, "savanna_bush_front.png")

#Weapons
WEAPONS_DIR = os.path.join(ASSETS_DIR, "weapons")
HIT_BAR_FRAME = os.path.join(WEAPONS_DIR, "hit_point_ui.png")
HIT_BAR = os.path.join(WEAPONS_DIR, "bar.png")
HIT_EFFECT = os.path.join(WEAPONS_DIR, "hit_img.png")

AMMO_4 = os.path.join(WEAPONS_DIR, "ammo_level_4.png")
AMMO_3 = os.path.join(WEAPONS_DIR, "ammo_level_3.png")
AMMO_2= os.path.join(WEAPONS_DIR, "ammo_level_2.png")
AMMO_1 = os.path.join(WEAPONS_DIR, "ammo_level_1.png")
AMMO_0 = os.path.join(WEAPONS_DIR, "ammo_level_0.png")

GUN = os.path.join(WEAPONS_DIR, "gun.png")


