import strings.en_US, strings.ro_RO
import tkinter as tk, strings, custom_ui
from tkinter import ttk
from utils import preferences

strings.load_language(open(preferences.user_preferences + "\\language", "r").read())
window = None

def show():
    global window

    window = custom_ui.Toplevel()
    window.title(strings.lang.change_theme)
    window.resizable(False, False)
    window.configure(padx = 16, pady = 0)

    theme = tk.StringVar(value = preferences.theme)

    header = ttk.Frame(window)
    header.pack(anchor = "w", pady = 8)

    ttk.Label(header, text = "\ue771 ", font = ("Segoe UI", 17), padding = (0, 5, 0, 0)).pack(side = "left")
    ttk.Label(header, width = 20, text = strings.lang.change_theme, font = ("Segoe UI Semibold", 17)).pack(side = "left")

    system_default = tk.Frame(window)
    system_default.pack(fill = "x", pady = 2)
    custom_ui.Radiobutton2(system_default, text = "  " + strings.lang.lang_system_default, value = "default", variable = theme, image = custom_ui.ic_system, compound = "left").pack(anchor = "w", fill = "x")
    
    light_theme = tk.Frame(window)
    light_theme.pack(fill = "x", pady = 2)
    custom_ui.Radiobutton2(light_theme, text = "  " + strings.lang.light_theme, value = "light", variable = theme, image = custom_ui.ic_light_mode, compound = "left").pack(anchor = "w", fill = "x")
    
    dark_theme = tk.Frame(window)
    dark_theme.pack(fill = "x", pady = 2)
    custom_ui.Radiobutton2(dark_theme, text = "  " + strings.lang.dark_theme, value = "dark", variable = theme, image = custom_ui.ic_dark_mode, compound = "left").pack(anchor = "w", fill = "x")

    buttons = ttk.Frame(window)
    buttons.pack(pady = 16, anchor = "e")

    def apply_theme():
        open(preferences.user_preferences + "\\theme", "w").write(theme.get())
        preferences.theme = theme.get()
        window.destroy()

    ok_btn = ttk.Button(buttons, text = strings.lang.ok, default = "active", command = apply_theme).pack(side = "right", padx = (8, 0))
    cancel_btn = ttk.Button(buttons, text = strings.lang.cancel, command = window.destroy).pack(side = "right")

    window.focus_set()