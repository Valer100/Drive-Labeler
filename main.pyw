import tkinter as tk, strings, custom_ui, os, traceback, tktooltip, argparse
from tkinter import ttk, filedialog, messagebox
from utils import volume, icon, preferences, context_menu_entry
from dialogs import change_language, change_theme, about, error
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(True)

os.chdir(os.path.dirname(__file__))
if os.path.exists("icon.ico"): preferences.internal = ""
else: preferences.internal = "_internal\\"

parser = argparse.ArgumentParser()
parser.add_argument("--volume", default = None, help = "The letter of the volume you want to customize", required = False)
arguments = parser.parse_args()

window = custom_ui.App()
window.title("Volume Labeler")
window.resizable(False, False)
window.configure(padx = 14, pady = 8)

icon_pack = "C:\\Windows\\System32\\shell32.dll"
show_additional_options = False
icon_old = "default"
volumes = [""]
autorun = ""
app_started = False
selected_volume = tk.StringVar(value = "")
hide_autorun = tk.BooleanVar(value = int(preferences.additional_prefs[0]))
hide_vl_icon = tk.BooleanVar(value = int(preferences.additional_prefs[1]))
backup_existing_autorun = tk.BooleanVar(value = int(preferences.additional_prefs[2]))
icon_type = tk.StringVar(value = "default")


def refresh_volumes_list():
    global volumes, app_started

    volumes = volume.get_available_drives()
    selected_volume.set(volumes[0])

    menu = volume_dropdown["menu"]
    menu.delete(0, "end")

    for string in volumes:
        menu.add_command(label = string, command = lambda value = string: update_volume_info(value))

    if not app_started and arguments.volume != None:
        if os.path.exists(arguments.volume.upper()):
            update_volume_info(arguments.volume.upper())
        else:
            update_volume_info(volumes[0])
            messagebox.showerror(strings.lang.volume_not_accessible, strings.lang.volume_not_accessible_message)
    else:
        update_volume_info(volumes[0])

    app_started = True


def update_volume_info(vol):
    global icon_old

    if os.path.exists(vol):
        selected_volume.set(vol)
        icon_type.set("default")

        choose_icon.configure(text = "  " + strings.lang.choose_icon, image = custom_ui.ic_icon, width = 0)
        icon_from_image.configure(text = "  " + strings.lang.create_icon_from_image, image = custom_ui.ic_image, width = 0)

        volume_info = volume.get_volume_label_and_icon(vol)

        if not volume_info["icon_path"] == None:
            icon_type.set("icon")
            process_icon(volume_info["icon_path"], volume_info["icon_index"])

        icon_old = icon_type.get()

        label.delete(0, "end")
        label.insert(0, volume_info["label"])
    else:
        messagebox.showerror(strings.lang.volume_not_accessible, strings.lang.volume_not_accessible_message)


def modify_volume_info():
    try:
        volume.modify_volume_info(
            volume = selected_volume.get(), 
            label = label.get(), 
            default_icon = icon_type.get() == "default",
            icon_path = preferences.roaming + "\\icon.ico",
            hide_autorun = hide_autorun.get(),
            hide_vl_icon = hide_vl_icon.get(),
            backup_existing_autorun = backup_existing_autorun.get()
        )

        messagebox.showinfo(strings.lang.done, strings.lang.operation_complete)
    except PermissionError:
        messagebox.showerror(strings.lang.permission_denied, strings.lang.permission_denied_message)
    except UnicodeEncodeError:
        messagebox.showerror(strings.lang.error, strings.lang.unicode_not_supported)
    except volume.VolumeNotAccessibleError:
        messagebox.showerror(strings.lang.volume_not_accessible, strings.lang.volume_not_accessible_message)
    except volume.IconNotFoundError:
        messagebox.showerror(strings.lang.error, strings.lang.missing_icon_file)
    except:
        error.show(traceback.format_exc())


def remove_volume_customizations():
    try:
        confirmed = messagebox.askyesno(strings.lang.remove_customizations, strings.lang.remove_customizations_message, icon = "warning")

        if confirmed:
            volume.remove_volume_customizations(volume = selected_volume.get(), backup_existing_autorun = backup_existing_autorun.get())
            update_volume_info(selected_volume.get())
            messagebox.showinfo(strings.lang.done, strings.lang.operation_complete)
    except volume.VolumeNotAccessibleError:
        messagebox.showerror(strings.lang.volume_not_accessible, strings.lang.volume_not_accessible_message)
    except PermissionError:
        messagebox.showerror(strings.lang.permission_denied, strings.lang.permission_denied_message)
    except:
        error.show(traceback.format_exc())


def process_icon(path, index):
    global icon_from_image, choose_icon, preview

    icon.extract_icon(path, index)
    preview = tk.PhotoImage(file = preferences.roaming + "\\preview.png")

    choose_icon.configure(image = preview, text = f"  {preferences.limit_string(os.path.basename(path))}, {index}")
    icon_from_image.configure(text = "  " + strings.lang.create_icon_from_image, image = custom_ui.ic_image)


def choose_icon_():
    global preview, icon_old, icon_pack

    match icon_type.get():
        case "default":
            choose_icon.configure(text = "  " + strings.lang.choose_icon, image = custom_ui.ic_icon)
            icon_from_image.configure(text = "  " + strings.lang.create_icon_from_image, image = custom_ui.ic_image)
        case "icon":
            try:
                icon_path, icon_index = icon.pick_icon(icon_pack)
                process_icon(icon_path, icon_index)
            except:
                icon_type.set(icon_old)

            icon_pack = "C:\\Windows\\System32\\shell32.dll"
            window.after(200, lambda: window.bind("<Shift_L>", enable_new_icon_pack))
        case "image":
            image = filedialog.askopenfile(title = strings.lang.choose_image, filetypes = [(strings.lang.images, (".png", ".jpg", ".jpeg", ".bmp", ".gif"))])

            if not image is None:
                icon.convert_image_to_icon(image.name)
                preview = tk.PhotoImage(file = preferences.roaming + "\\preview.png")
                
                icon_from_image.configure(image = preview, text = "  " + preferences.limit_string(os.path.basename(image.name)))
                choose_icon.configure(text = "  " + strings.lang.choose_icon, image = custom_ui.ic_icon, width = 0)
            else:
                icon_type.set(icon_old)
        
    icon_old = icon_type.get()


def destroy_everything(widget):
    for child in widget.winfo_children():
        child.destroy()


def change_app_language():
    old_language = preferences.language

    change_language.show()
    window.wait_window(change_language.window)

    if old_language != preferences.language: 
        draw_ui()
        refresh_volumes_list()


def change_app_theme():
    old_theme = preferences.theme

    change_theme.show()
    window.wait_window(change_theme.window)

    if old_theme != preferences.theme:
        custom_ui.update_colors()
        window.set_theme()
        custom_ui.update_icons()
        custom_ui.sync_colors(window, update_icons)


def add_remove_context_menu_entry():
    global context_menu_integration, context_menu_integration_tooltip
    context_menu_integration_tooltip.destroy()

    if context_menu_entry.is_context_menu_entry_added():
        context_menu_entry.remove_context_menu_entry()

        context_menu_integration.configure(default = "normal")
        context_menu_integration_tooltip = tktooltip.ToolTip(context_menu_integration, strings.lang.context_menu_integration_disabled, follow = False, delay = 1, bg = custom_ui.tooltip_bg, fg = custom_ui.tooltip_fg, parent_kwargs = {"bg":custom_ui.tooltip_bd, "padx": 1, "pady": 1})
        
        messagebox.showinfo(strings.lang.context_menu_integration, strings.lang.context_menu_entry_removed)
    else:
        context_menu_entry.add_context_menu_entry()

        context_menu_integration.configure(default = "active")
        context_menu_integration_tooltip = tktooltip.ToolTip(context_menu_integration, strings.lang.context_menu_integration_enabled, follow = False, delay = 1, bg = custom_ui.tooltip_bg, fg = custom_ui.tooltip_fg, parent_kwargs = {"bg":custom_ui.tooltip_bd, "padx": 1, "pady": 1})
        
        messagebox.showinfo(strings.lang.context_menu_integration, strings.lang.context_menu_entry_added)


def draw_ui():
    global choose_icon, icon_from_image, refresh, volume_dropdown, label, show_additional_options, context_menu_integration, context_menu_integration_tooltip, refresh_volumes, additional_options, default_icon, choose_icon, icon_from_image
    show_additional_options = False
    destroy_everything(window)
    strings.load_language(open(preferences.user_preferences + "\\language", "r").read())

    ttk.Label(window, text = "Volume Labeler", font = ("Segoe UI Semibold", 17)).pack(anchor = "w")

    volume_section = ttk.Frame(window)
    volume_section.pack(fill = "x", anchor = "w", pady = (16, 8))

    ttk.Label(volume_section, text = strings.lang.volume).pack(side = "left")

    refresh_volumes_frame = ttk.Frame(volume_section)
    refresh_volumes_frame.pack(side = "right", padx = (8, 0), fill = "both")

    refresh_volumes = custom_ui.Button(refresh_volumes_frame, width = 3, command = refresh_volumes_list, text = "\ue72c", font = ("Segoe MDL2 Assets", 8))
    refresh_volumes.pack(fill = "both", expand = True)

    tktooltip.ToolTip(refresh_volumes, strings.lang.refresh_volumes_list, follow = False, delay = 1, bg = custom_ui.tooltip_bg, fg = custom_ui.tooltip_fg, parent_kwargs = {"bg":custom_ui.tooltip_bd, "padx": 1, "pady": 1})
    
    volume_dropdown = custom_ui.OptionMenu(volume_section, selected_volume, *volumes)
    volume_dropdown.pack(side = "right")

    ttk.Label(window, text = strings.lang.label).pack(pady = 10, anchor = "w")

    label_frame = tk.Frame(window, highlightbackground = custom_ui.entry_bd, highlightcolor = custom_ui.entry_focus,
                          highlightthickness = 1)
    label_frame.pack(anchor = "w", fill = "x")

    label = tk.Entry(label_frame, width = 40, background = custom_ui.entry_bg, 
                    foreground = custom_ui.fg, border = 0, highlightthickness = 2, 
                    highlightcolor = custom_ui.entry_bg, highlightbackground = custom_ui.entry_bg, 
                    insertbackground = custom_ui.fg, insertwidth = 1, selectbackground = custom_ui.entry_select,
                    selectforeground = "#FFFFFF")
    label.pack(fill = "x")

    ttk.Label(window, text = strings.lang.icon).pack(pady = (16, 8), anchor = "w")

    default_icon_frame = tk.Frame(window)
    default_icon_frame.pack(fill = "x", pady = 2)
    default_icon = custom_ui.Radiobutton2(default_icon_frame, text = "  " + strings.lang.default_icon, variable = icon_type, value = "default", command = choose_icon_, image = custom_ui.ic_volume, compound = "left")
    default_icon.pack(anchor = "w", fill = "x")

    choose_icon_frame = tk.Frame(window)
    choose_icon_frame.pack(fill = "x", pady = 2)
    choose_icon = custom_ui.Radiobutton2(choose_icon_frame, text = "  " + strings.lang.choose_icon, variable = icon_type, value = "icon", command = choose_icon_, image = custom_ui.ic_icon, compound = "left")
    choose_icon.pack(anchor = "w", fill = "x")

    icon_from_image_frame = tk.Frame(window)
    icon_from_image_frame.pack(fill = "x", pady = 2)
    icon_from_image = custom_ui.Radiobutton2(icon_from_image_frame, text = "  " + strings.lang.create_icon_from_image, variable = icon_type, value = "image", image = custom_ui.ic_image, command = choose_icon_, compound = "left")
    icon_from_image.pack(anchor = "w", fill = "x")

    additional_options = custom_ui.Toolbutton(window, text = " " + strings.lang.additional_options, command = lambda: show_hide_additional_options(), anchor = "w", compound = "left", image = custom_ui.ic_arrow_down)
    additional_options.pack(pady = (14, 0), anchor = "w")
    additional_options.configure(padx = 0)

    additional_options_frame = ttk.Frame(window)
    additional_options_frame.pack(anchor = "w")
    
    def show_hide_additional_options():
        global show_additional_options, arrow
        show_additional_options = not show_additional_options

        for widget in additional_options_frame.winfo_children():
            if show_additional_options: 
                if widget["text"] == strings.lang.hide_autorun:
                    widget.pack(pady = (6, 0), anchor = "w")
                else:
                    widget.pack(anchor = "w")
            else: widget.forget()

        if show_additional_options: 
            additional_options_frame.configure(height = -1)
            additional_options.configure(image = custom_ui.ic_arrow_up)
        else: 
            additional_options_frame.configure(height = 1)
            additional_options.configure(image = custom_ui.ic_arrow_down)

    def save_additional_preferences(): open(preferences.user_preferences + "\\additional_prefs", "w").write(f"{int(hide_autorun.get())}{int(hide_vl_icon.get())}{int(backup_existing_autorun.get())}")

    ttk.Checkbutton(additional_options_frame, text = strings.lang.hide_autorun, command = save_additional_preferences, variable = hide_autorun)
    ttk.Checkbutton(additional_options_frame, text = strings.lang.hide_vl_icon, command = save_additional_preferences, variable = hide_vl_icon)
    ttk.Checkbutton(additional_options_frame, text = strings.lang.backup_existing_autorun, command = save_additional_preferences, variable = backup_existing_autorun)

    custom_ui.Button(window, text = strings.lang.apply_changes, command = modify_volume_info, default = "active").pack(pady = (16, 0), fill = "x")
    custom_ui.Button(window, text = strings.lang.remove_customizations, command = remove_volume_customizations).pack(pady = (8, 0), fill = "x")

    settings = ttk.Frame(window)
    settings.pack(anchor = "w", pady = (20, 2), fill = "x")
    settings.pack_propagate(False)
    
    language = custom_ui.Toolbutton(settings, text = "\ue774", link = True, icononly = True, anchor = "n", command = change_app_language, font = ("Segoe UI", 12))
    language.pack(anchor = "nw", side = "left")

    theme = custom_ui.Toolbutton(settings, text = "\ue771", link = True, icononly = True, anchor = "n", command = change_app_theme, font = ("Segoe UI", 12))
    theme.pack(anchor = "nw", side = "left", padx = (4, 0))

    context_menu_integration = custom_ui.Toolbutton(settings, text = "\ue71d", link = True, icononly = True, anchor = "n", command = add_remove_context_menu_entry, font = ("Segoe UI", 12))
    context_menu_integration.pack(anchor = "nw", side = "left", padx = (4, 0))

    about_app = custom_ui.Toolbutton(settings, text = "\ue946", link = True, icononly = True, anchor = "n", command = about.show, font = ("Segoe UI", 13))
    about_app.pack(anchor = "nw", side = "left", padx = (4, 0))
    
    language.update()
    settings.configure(height = language.winfo_reqwidth())


    tktooltip.ToolTip(language, strings.lang.change_language, follow = False, delay = 1, bg = custom_ui.tooltip_bg, fg = custom_ui.tooltip_fg, parent_kwargs = {"bg":custom_ui.tooltip_bd, "padx": 1, "pady": 1})
    tktooltip.ToolTip(theme, strings.lang.change_theme, follow = False, delay = 1, bg = custom_ui.tooltip_bg, fg = custom_ui.tooltip_fg, parent_kwargs = {"bg":custom_ui.tooltip_bd, "padx": 1, "pady": 1})
    tktooltip.ToolTip(about_app, strings.lang.about_this_app, follow = False, delay = 1, bg = custom_ui.tooltip_bg, fg = custom_ui.tooltip_fg, parent_kwargs = {"bg":custom_ui.tooltip_bd, "padx": 1, "pady": 1})

    context_menu_entry.update_context_menu_entry_string()

    if context_menu_entry.is_context_menu_entry_added():
        context_menu_integration.configure(default = "active")
        context_menu_integration_tooltip = tktooltip.ToolTip(context_menu_integration, strings.lang.context_menu_integration_enabled, follow = False, delay = 1, bg = custom_ui.tooltip_bg, fg = custom_ui.tooltip_fg, parent_kwargs = {"bg":custom_ui.tooltip_bd, "padx": 1, "pady": 1})
    else:
        context_menu_integration.configure(default = "normal")
        context_menu_integration_tooltip = tktooltip.ToolTip(context_menu_integration, strings.lang.context_menu_integration_disabled, follow = False, delay = 1, bg = custom_ui.tooltip_bg, fg = custom_ui.tooltip_fg, parent_kwargs = {"bg":custom_ui.tooltip_bd, "padx": 1, "pady": 1})

    window.update()


def update_icons():
    if show_additional_options: additional_options.configure(image = custom_ui.ic_arrow_up)
    else: additional_options.configure(image = custom_ui.ic_arrow_down)

    default_icon.configure(image = custom_ui.ic_volume)

    if choose_icon["text"] == "  " + strings.lang.choose_icon:
        choose_icon.configure(image = custom_ui.ic_icon)

    if icon_from_image["text"] == "  " + strings.lang.create_icon_from_image:
        icon_from_image.configure(image = custom_ui.ic_image)


def enable_new_icon_pack(event):
    global icon_pack
    icon_pack = os.path.abspath("icons.icl")

    window.unbind("<Shift_L>")
    window.bind("<KeyRelease-Shift_L>", disable_new_icon_pack)


def disable_new_icon_pack(event):
    global icon_pack
    icon_pack = "C:\\Windows\\System32\\shell32.dll"

    window.unbind("<KeyRelease-_L>")
    window.bind("<Shift_L>", enable_new_icon_pack)


draw_ui()
refresh_volumes_list()
custom_ui.sync_colors_with_system(window, update_icons)

window.bind("<Shift_L>", enable_new_icon_pack)
window.mainloop()