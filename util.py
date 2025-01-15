import icoextract, ctypes, os, getpass, strings, subprocess

if os.path.exists("icon.ico"): internal = ""
else: internal = "_internal\\"

user_preferences = f"C:\\Users\\{getpass.getuser()}\\AppData\\Local\\Volume Labeler"
roaming = f"C:\\Users\\{getpass.getuser()}\\AppData\\Roaming\\Volume Labeler"

if not os.path.exists(user_preferences): os.mkdir(user_preferences)
if not os.path.exists(user_preferences + "\\language"): open(user_preferences + "\\language", "w").write("default")
if not os.path.exists(user_preferences + "\\theme"): open(user_preferences + "\\theme", "w").write("default")
if not os.path.exists(user_preferences + "\\additional_prefs"): open(user_preferences + "\\additional_prefs", "w").write("111")

theme = open(user_preferences + "\\theme", "r").read()
language = open(user_preferences + "\\language", "r").read()
additional_prefs = open(user_preferences + "\\additional_prefs", "r").read()

strings.load_language(language)

from typing import Tuple

def pick_icon() -> Tuple[str, int]:
    icon_file_buffer = ctypes.create_unicode_buffer(260)
    icon_index = ctypes.c_int(0)

    initial_icon_file = "C:\\Windows\\System32\\shell32.dll"
    ctypes.windll.kernel32.lstrcpyW(icon_file_buffer, initial_icon_file)

    result = ctypes.windll.shell32.PickIconDlg(None, icon_file_buffer, ctypes.sizeof(icon_file_buffer), ctypes.byref(icon_index))
    if result: return (icon_file_buffer.value, icon_index.value)

def is_volume_accessible(volume: str):
    volumes = subprocess.getoutput("fsutil fsinfo drives").split(" ")
    volumes.pop(0)
    volumes.pop()

    if volume in volumes: return True
    else: return False