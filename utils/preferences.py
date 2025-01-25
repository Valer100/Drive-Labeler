import os, getpass, strings

user_preferences = f"C:\\Users\\{getpass.getuser()}\\AppData\\Local\\Volume Labeler"
roaming = f"C:\\Users\\{getpass.getuser()}\\AppData\\Roaming\\Volume Labeler"

if not os.path.exists(user_preferences): os.mkdir(user_preferences)
if not os.path.exists(roaming): os.mkdir(roaming)
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