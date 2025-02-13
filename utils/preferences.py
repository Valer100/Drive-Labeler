import os, getpass, strings, ctypes

if os.path.exists("preferences") and os.path.isdir("preferences"):
    user_preferences = "preferences"
else:
    user_preferences = f"C:\\Users\\{getpass.getuser()}\\AppData\\Local\\Volume Labeler"

roaming = f"C:\\Users\\{getpass.getuser()}\\AppData\\Roaming\\Volume Labeler"

if not os.path.exists(roaming): os.mkdir(roaming)
if not os.path.exists(user_preferences): os.mkdir(user_preferences)
if not os.path.exists(user_preferences + "\\language"): open(user_preferences + "\\language", "w").write("default")
if not os.path.exists(user_preferences + "\\theme"): open(user_preferences + "\\theme", "w").write("default")
if not os.path.exists(user_preferences + "\\additional_prefs"): open(user_preferences + "\\additional_prefs", "w").write("111")

theme = open(user_preferences + "\\theme", "r").read()
language = open(user_preferences + "\\language", "r").read()
additional_prefs = open(user_preferences + "\\additional_prefs", "r").read()

strings.load_language(language)

def limit_string(string: str) -> str:
    if len(string) > 24:
        return "..." + string[-21:]
    
    return string

ctypes.windll.shcore.SetProcessDpiAwareness(1)

dpi = ctypes.c_uint()
monitor_handle = ctypes.windll.user32.MonitorFromPoint(0, 0, 2)
ctypes.windll.shcore.GetDpiForMonitor(monitor_handle, 0, ctypes.byref(dpi), ctypes.byref(dpi))

scale_factor = dpi.value / 96

def get_scaled_value(value: int) -> int:
    return int(value * scale_factor + 0.5)