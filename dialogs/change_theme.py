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
    window.configure(padx = 16, pady = 0)

    theme = tk.StringVar(value = preferences.theme)

    header = ttk.Frame(window)
    header.pack(anchor = "w", pady = (4, 8))

    ttk.Label(header, text = "\ue771 ", font = ("Segoe UI", 17), padding = (0, 5, 0, 0)).pack(side = "left")
    ttk.Label(header, text = strings.lang.change_theme + " ", font = ("Segoe UI Semibold", 17)).pack(side = "left")

    custom_ui.Radiobutton(window, text = strings.lang.lang_system_default + "  ", value = "default", variable = theme).pack(anchor = "w")
    custom_ui.Radiobutton(window, text = strings.lang.light_theme + "  ", value = "light", variable = theme).pack(anchor = "w")
    custom_ui.Radiobutton(window, text = strings.lang.dark_theme + "  ", value = "dark", variable = theme).pack(anchor = "w")

    buttons = ttk.Frame(window)
    buttons.pack(pady = 16, fill = "x")

    def apply_theme():
        open(preferences.user_preferences + "\\theme", "w").write(theme.get())
        preferences.theme = theme.get()
        window.destroy()

    buttons.grid_columnconfigure(index = [0, 1], weight = 1)

    ttk.Button(buttons, text = strings.lang.cancel, command = window.destroy).grid(row = 0, column = 0, padx = (0, 4), sticky = "ew")
    ttk.Button(buttons, text = strings.lang.ok, default = "active", command = apply_theme).grid(row = 0, column = 1, padx = (4, 0), sticky = "ew")

    window.resizable(False, False)
    window.focus_set()