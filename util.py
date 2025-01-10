import win32ui, win32gui, ctypes, os, getpass, strings, subprocess
from PIL import Image

# if os.path.exists("icon.ico"): internal = ""
# else: internal = "_internal\\"

internal = ""

user_preferences = f"C:\\Users\\{getpass.getuser()}\\AppData\\Roaming\\Volume Labeler"

if not os.path.exists(user_preferences): os.mkdir(user_preferences)
if not os.path.exists(user_preferences + "\\language"): open(user_preferences + "\\language", "w").write("default")
if not os.path.exists(user_preferences + "\\theme"): open(user_preferences + "\\theme", "w").write("default")

theme = open(user_preferences + "\\theme", "r").read()
language = open(user_preferences + "\\language", "r").read()

strings.load_language(language)

def pick_icon() -> str:
    icon_file_buffer = ctypes.create_unicode_buffer(260)
    icon_index = ctypes.c_int(0)

    initial_icon_file = "C:\\Windows\\System32\\shell32.dll"
    ctypes.windll.kernel32.lstrcpyW(icon_file_buffer, initial_icon_file)

    result = ctypes.windll.shell32.PickIconDlg(None, icon_file_buffer, ctypes.sizeof(icon_file_buffer), ctypes.byref(icon_index))
    if result: return (icon_file_buffer.value, icon_index.value)

def extract_icon(path: str, index: int = 0):
    # Modified from https://gist.github.com/chyyran/7314682

    large, small = win32gui.ExtractIconEx(path, index)
    hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))

    icon_bmp = win32ui.CreateBitmap()
    icon_bmp.CreateCompatibleBitmap(hdc, 32, 32)

    hdc = hdc.CreateCompatibleDC()
    hdc.SelectObject(icon_bmp)
    hdc.DrawIcon((0,0), large[0])

    icon_info = icon_bmp.GetInfo()
    icon_buffer = icon_bmp.GetBitmapBits(True)
    icon = Image.frombuffer('RGBA', (icon_info['bmWidth'], icon_info['bmHeight']), icon_buffer, 'raw', 'BGRA', 0, 1)

    win32gui.DestroyIcon(small[0])
    return icon

def is_drive_accessible(drive: str):
    drives = subprocess.getoutput("fsutil fsinfo drives").split(" ")
    drives.pop(0)
    drives.pop()

    if drive in drives: return True
    else: return False