import tkinter as tk, util, open_source_licenses, change_language, change_theme, strings, custom_ui, subprocess
from tkinter import ttk, filedialog, messagebox

window = custom_ui.App()
window.title("Volume Labeler")
window.resizable(False, False)
# window.iconbitmap(util.internal + "icon.ico")
window.configure(padx = 14, pady = 8)

volumes = subprocess.getoutput("fsutil fsinfo drives").split(" ")
volumes.pop(0)
volumes.pop()

selected_volume = tk.StringVar(value = volumes[0])
icon = tk.StringVar(value = "default")

def destroy_everything(widget):
    for child in widget.winfo_children():
        child.destroy()

def change_app_language():
    old_language = util.language

    change_language.show()
    window.wait_window(change_language.window)

    if old_language != util.language: draw_ui()

def change_app_theme():
    old_theme = util.theme

    change_theme.show()
    window.wait_window(change_theme.window)

    if old_theme != util.theme:
        custom_ui.update_colors()
        window.set_theme()
        draw_ui()

def draw_ui():
    destroy_everything(window)
    strings.load_language(open(util.user_preferences + "\\language", "r").read())

    ttk.Label(window, text = "Volume Labeler", font = ("Segoe UI Semibold", 17)).pack(anchor = "w")

    volume_section = ttk.Frame(window)
    volume_section.pack(fill = "x", anchor = "w", pady = (16, 8))

    ttk.Label(volume_section, text = "Drive").pack(side = "left")

    volume = custom_ui.OptionMenu(volume_section, selected_volume, *volumes)
    volume.pack(side = "right")

    ttk.Label(window, text = strings.lang.label).pack(pady = 10, anchor = "w")

    label_frame = tk.Frame(window, highlightbackground = custom_ui.entry_bd, highlightcolor = custom_ui.entry_focus,
                          highlightthickness = 1)
    label_frame.pack(anchor = "w")

    label = tk.Entry(label_frame, width = 40, background = custom_ui.entry_bg, 
                    foreground = custom_ui.fg, border = 0, highlightthickness = 2, 
                    highlightcolor = custom_ui.entry_bg, highlightbackground = custom_ui.entry_bg, 
                    insertbackground = custom_ui.fg, insertwidth = 1, selectbackground = custom_ui.entry_select,
                    selectforeground = "#FFFFFF")
    label.pack()

    ttk.Label(window, text = strings.lang.icon).pack(pady = (16, 8), anchor = "w")

    ttk.Radiobutton(window, text = "Default icon", variable = icon, value = "default").pack(anchor = "w")
    ttk.Radiobutton(window, text = "Choose icon", variable = icon, value = "icon").pack(anchor = "w")
    ttk.Radiobutton(window, text = "Create icon from image", variable = icon, value = "image").pack(anchor = "w")

    custom_ui.Button(window, text = strings.lang.execute, command = lambda: modify_volume_info(selected_volume.get(), label.get())).pack(pady = (16, 0), fill = "x")

    ttk.Label(window, text = strings.lang.settings, font = ("Segoe UI Semibold", 14)).pack(anchor = "w", pady = (16, 4))
    custom_ui.Toolbutton(window, text = strings.lang.change_language, command = change_app_language).pack(anchor = "w")
    custom_ui.Toolbutton(window, text = strings.lang.change_theme, command = change_app_theme).pack(anchor = "w")
    custom_ui.Toolbutton(window, text = strings.lang.see_open_source_licenses, command = open_source_licenses.show).pack(anchor = "w")

    window.update()

def modify_volume_info(volume: str, label: str):
    if util.is_volume_accessible(volume):
        try:
            autorun_file = open(f"{volume}autorun.inf", "w")
            autorun_file.write(f"[autorun]\nlabel={label}")
            autorun_file.close()

            messagebox.showinfo(strings.lang.done, strings.lang.operation_complete)
        except PermissionError:
            messagebox.showerror(strings.lang.permission_denied, strings.lang.read_only_volume_message)
    else:
        messagebox.showerror(strings.lang.volume_not_accessible, strings.lang.volume_not_accessible_message)

draw_ui()
custom_ui.sync_colors_with_system(window)
window.mainloop()