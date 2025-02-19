import os, appdirs, strings, ctypes

if os.path.exists("preferences") and os.path.isdir("preferences"):
    user_preferences = os.path.abspath("preferences")
    is_portable = True
else:
    user_preferences = appdirs.user_config_dir(appname = "Volume Labeler", appauthor = False, roaming = True)
    is_portable = False

temp = user_preferences + "\\temp"

if not os.path.exists(user_preferences): os.mkdir(user_preferences)
if not os.path.exists(temp): os.mkdir(temp)
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