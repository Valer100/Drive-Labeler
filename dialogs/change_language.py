import strings.en_US, strings.ro_RO
import tkinter as tk, strings, custom_ui
from tkinter import ttk
from utils import preferences

strings.load_language(open(preferences.user_preferences + "\\language", "r").read())
window = None

def show():
    global window

    window = custom_ui.Toplevel()
    window.title(strings.lang.change_language)
    window.resizable(False, False)
    window.configure(padx = 16, pady = 0)

    language = tk.StringVar(value = preferences.language)

    header = ttk.Frame(window)
    header.pack(anchor = "w", pady = 8)

    ttk.Label(header, text = "\ue774 ", font = ("Segoe UI Semibold", 17), padding = (0, 5, 0, 0)).pack(side = "left")
    ttk.Label(header, width = 25, text = strings.lang.change_language, font = ("Segoe UI Semibold", 17)).pack(side = "left")

    ttk.Radiobutton(window, text = strings.lang.lang_system_default, value = "default", variable = language).pack(anchor = "w")
    ttk.Radiobutton(window, text = strings.en_US.language, value = "en_US", variable = language).pack(anchor = "w")
    ttk.Radiobutton(window, text = strings.ro_RO.language, value = "ro_RO", variable = language).pack(anchor = "w")

    buttons = ttk.Frame(window)
    buttons.pack(pady = 16, anchor = "e")

    def apply_language():
        open(preferences.user_preferences + "\\language", "w").write(language.get())
        preferences.language = language.get()

        window.destroy()

    ok_btn = ttk.Button(buttons, text = strings.lang.ok, default = "active", command = apply_language).pack(side = "right", padx = (8, 0))
    cancel_btn = ttk.Button(buttons, text = strings.lang.cancel, command = window.destroy).pack(side = "right")

    window.focus_set()