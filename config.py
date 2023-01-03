from win32api import GetSystemMetrics

WIDTH, HEIGHT = (GetSystemMetrics(0), GetSystemMetrics(1))
FPS = 60

WORLD_WIDTH, WORLD_HEIGHT = (4000, 4000)

PLAYER_SIZE = 100
EAT_SIZE = 20

BACKGROUND_COLOR = (15, 15, 15)

PATH_DATA = "data/"
PATH_IMAGE = PATH_DATA + "image/"
PATH_ICON = PATH_DATA + "icon/"
