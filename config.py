from types import FunctionType
from aiocqhttp.event import Event
from nonebot.default_config import *
from os import path


SUPERUSERS = {114514}#1
COMMAND_START = {'', '/', '!', '／', '！'}
HOST = '0.0.0.0'
PORT = 8080

BASE_PATH = ""
SCORCE_IMG_PATH = path.join(BASE_PATH, "images")
SCORCE_VOICE_PATH = path.join(BASE_PATH, "voices")
SCORCE_VIDEO_PATH = path.join(BASE_PATH, "videos")
PLUGINS_PATH = "plugins/"
