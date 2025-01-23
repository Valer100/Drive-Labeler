import tkinter as tk, strings, custom_ui, subprocess, os, traceback, tktooltip, argparse, winreg, sys
from tkinter import ttk, filedialog, messagebox
from utils import volume, icon, preferences
from dialogs import change_language, change_theme, about

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

        choose_icon.configure(text = strings.lang.choose_icon, image = "", width = 0)
        icon_from_image.configure(text = strings.lang.create_icon_from_image, image = "", width = 0)

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
        messagebox.showerror(strings.lang.error, strings.lang.failure_message + traceback.format_exc())


def remove_volume_customizations():
    try:
        confirmed = messagebox.askyesno(strings.lang.remove_customizations, strings.lang.remove_customizations_message, icon = "warning")

        if confirmed:
            volume.remove_volume_customizations(volume = selected_volume.get(), backup_existing_autorun = backup_existing_autorun.get())
    except volume.VolumeNotAccessibleError:
        messagebox.showerror(strings.lang.volume_not_accessible, strings.lang.volume_not_accessible_message)
    except PermissionError:
        messagebox.showerror(strings.lang.permission_denied, strings.lang.permission_denied_message)


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
        draw_ui()
        refresh_volumes_list()


def draw_ui():
    global choose_icon, icon_from_image, refresh, volume_dropdown, label, arrow, show_additional_options, context_menu_integration, context_menu_integration_tooltip
    show_additional_options = False

    destroy_everything(window)
    strings.load_language(open(preferences.user_preferences + "\\language", "r").read())

    ttk.Label(window, text = "Volume Labeler", font = ("Segoe UI Semibold", 17)).pack(anchor = "w")

    volume_section = ttk.Frame(window)
    volume_section.pack(fill = "x", anchor = "w", pady = (16, 8))

    ttk.Label(volume_section, text = strings.lang.volume).pack(side = "left")

    if custom_ui.light_theme: refresh = tk.PhotoImage(file = f"{preferences.internal}icons\\refresh_light.png")
    else: refresh = tk.PhotoImage(file = f"{preferences.internal}icons\\refresh_dark.png")

    refresh_volumes = custom_ui.Button(volume_section, width = -1, command = refresh_volumes_list, image = refresh)
    refresh_volumes.pack(side = "right", padx = (8, 0))

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

    default_icon = ttk.Radiobutton(window, text = strings.lang.default_icon, variable = icon_type, value = "default", command = choose_icon_)
    default_icon.pack(anchor = "w")

    choose_icon = ttk.Radiobutton(window, text = strings.lang.choose_icon, variable = icon_type, value = "icon", command = choose_icon_, compound = "left")
    choose_icon.pack(anchor = "w")
    
    icon_from_image = ttk.Radiobutton(window, text = strings.lang.create_icon_from_image, variable = icon_type, value = "image", command = choose_icon_, compound = "left")
    icon_from_image.pack(anchor = "w")

    if custom_ui.light_theme: arrow = tk.PhotoImage(file = f"{preferences.internal}icons/dropdown_light.png")
    else: arrow = tk.PhotoImage(file = f"{preferences.internal}icons/dropdown_dark.png")

    additional_options = custom_ui.Toolbutton(window, text = " " + strings.lang.additional_options, command = lambda: show_hide_additional_options(), anchor = "w", compound = "left", image = arrow)
    additional_options.pack(pady = (14, 0), anchor = "w")
    additional_options.configure(padx = 0)

    additional_options_frame = ttk.Frame(window)
    additional_options_frame.pack(anchor = "w")
    
    def show_hide_additional_options():
        global show_additional_options, arrow
        show_additional_options = not show_additional_options

        for widget in additional_options_frame.winfo_children():
            if custom_ui.light_theme: arrow = tk.PhotoImage(file = f"{preferences.internal}icons/dropdown{'_up' if show_additional_options else ''}_light.png")
            else: arrow = tk.PhotoImage(file = f"{preferences.internal}icons/dropdown{'_up' if show_additional_options else ''}_dark.png")
            
            additional_options.configure(image = arrow)

            if show_additional_options: 
                if widget["text"] == strings.lang.hide_autorun:
                    widget.pack(pady = (6, 0), anchor = "w")
                else:
                    widget.pack(anchor = "w")
            else: widget.forget()

        if show_additional_options: additional_options_frame.configure(height = -1)
        else: additional_options_frame.configure(height = 1)

    def save_additional_preferences(): open(preferences.user_preferences + "\\additional_prefs", "w").write(f"{int(hide_autorun.get())}{int(hide_vl_icon.get())}{int(backup_existing_autorun.get())}")

    ttk.Checkbutton(additional_options_frame, text = strings.lang.hide_autorun, command = save_additional_preferences, variable = hide_autorun)
    ttk.Checkbutton(additional_options_frame, text = strings.lang.hide_vl_icon, command = save_additional_preferences, variable = hide_vl_icon)
    ttk.Checkbutton(additional_options_frame, text = strings.lang.backup_existing_autorun, command = save_additional_preferences, variable = backup_existing_autorun)

    custom_ui.Button(window, text = strings.lang.apply_changes, command = modify_volume_info, default = "active").pack(pady = (16, 0), fill = "x")
    custom_ui.Button(window, text = strings.lang.remove_customizations, command = remove_volume_customizations).pack(pady = (8, 0), fill = "x")

    settings = ttk.Frame(window, height = 26)
    settings.pack(anchor = "w", pady = (20, 2), fill = "x")
    settings.pack_propagate(False)
    
    language = custom_ui.Toolbutton(settings, text = "\ue774", link = True, icononly = True, anchor = "n", command = change_app_language, font = ("Segoe UI", 12))
    language.pack(anchor = "nw", side = "left")

    theme = custom_ui.Toolbutton(settings, text = "\ue771", link = True, icononly = True, anchor = "n", command = change_app_theme, font = ("Segoe UI", 12))
    theme.pack(anchor = "nw", side = "left", padx = (4, 0))

    context_menu_integration = custom_ui.Toolbutton(settings, text = "\ue71d", link = True, icononly = True, anchor = "n", command = add_remove_context_menu_entry, font = ("Segoe UI", 12))
    context_menu_integration.pack(anchor = "nw", side = "left", padx = (4, 0))

    try:
        entry = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Classes\\Drive\\shell\\Volume Labeler", 0, winreg.KEY_ALL_ACCESS)

        if not winreg.QueryValueEx(entry, "")[0] == strings.lang.customize_with_volume_labeler:
            winreg.SetValueEx(entry, "", 0, winreg.REG_SZ, strings.lang.customize_with_volume_labeler)
            
        entry.Close()

        context_menu_integration.configure(default = "active")
        context_menu_integration_tooltip = tktooltip.ToolTip(context_menu_integration, strings.lang.context_menu_integration_enabled, follow = False, delay = 1, bg = custom_ui.tooltip_bg, fg = custom_ui.tooltip_fg, parent_kwargs = {"bg":custom_ui.tooltip_bd, "padx": 1, "pady": 1})
    except:
        context_menu_integration.configure(default = "normal")
        context_menu_integration_tooltip = tktooltip.ToolTip(context_menu_integration, strings.lang.context_menu_integration_disabled, follow = False, delay = 1, bg = custom_ui.tooltip_bg, fg = custom_ui.tooltip_fg, parent_kwargs = {"bg":custom_ui.tooltip_bd, "padx": 1, "pady": 1})

    about_app = custom_ui.Toolbutton(settings, text = "\ue946", link = True, icononly = True, anchor = "n", command = about.show, font = ("Segoe UI", 13))
    about_app.pack(anchor = "nw", side = "left", padx = (4, 0))
    
    tktooltip.ToolTip(language, strings.lang.change_language, follow = False, delay = 1, bg = custom_ui.tooltip_bg, fg = custom_ui.tooltip_fg, parent_kwargs = {"bg":custom_ui.tooltip_bd, "padx": 1, "pady": 1})
    tktooltip.ToolTip(theme, strings.lang.change_theme, follow = False, delay = 1, bg = custom_ui.tooltip_bg, fg = custom_ui.tooltip_fg, parent_kwargs = {"bg":custom_ui.tooltip_bd, "padx": 1, "pady": 1})
    tktooltip.ToolTip(about_app, strings.lang.about_this_app, follow = False, delay = 1, bg = custom_ui.tooltip_bg, fg = custom_ui.tooltip_fg, parent_kwargs = {"bg":custom_ui.tooltip_bd, "padx": 1, "pady": 1})

    window.update()


def add_remove_context_menu_entry():
    global app_in_context_menu, context_menu_integration, context_menu_integration_tooltip
    context_menu_integration_tooltip.destroy()

    try:
        entry = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Classes\\Drive\\shell\\Volume Labeler")
        entry.Close()
        app_in_context_menu = True
    except:
        app_in_context_menu = False

    app_in_context_menu = not app_in_context_menu

    if app_in_context_menu:
        entry = winreg.CreateKey(winreg.HKEY_CURRENT_USER, "Software\\Classes\\Drive\\shell\\Volume Labeler")
        winreg.SetValueEx(entry, "", 0, winreg.REG_SZ, strings.lang.customize_with_volume_labeler)
        winreg.SetValueEx(entry, "Icon", 0, winreg.REG_SZ, sys.executable)
        entry.Close()

        entry_command = winreg.CreateKey(winreg.HKEY_CURRENT_USER, "Software\\Classes\\Drive\\shell\\Volume Labeler\\command")
        winreg.SetValueEx(entry_command, "", 0, winreg.REG_SZ, f"\"{sys.executable}\" --volume %1")
        entry_command.Close()

        context_menu_integration.configure(default = "active")
        context_menu_integration_tooltip = tktooltip.ToolTip(context_menu_integration, strings.lang.context_menu_integration_enabled, follow = False, delay = 1, bg = custom_ui.tooltip_bg, fg = custom_ui.tooltip_fg, parent_kwargs = {"bg":custom_ui.tooltip_bd, "padx": 1, "pady": 1})
        
        messagebox.showinfo(strings.lang.context_menu_integration, strings.lang.context_menu_entry_added)
    else:
        subprocess.call("reg delete \"HKEY_CURRENT_USER\\Software\\Classes\\Drive\\shell\\Volume Labeler\" /f", shell = True)

        context_menu_integration.configure(default = "normal")
        context_menu_integration_tooltip = tktooltip.ToolTip(context_menu_integration, strings.lang.context_menu_integration_disabled, follow = False, delay = 1, bg = custom_ui.tooltip_bg, fg = custom_ui.tooltip_fg, parent_kwargs = {"bg":custom_ui.tooltip_bd, "padx": 1, "pady": 1})
        
        messagebox.showinfo(strings.lang.context_menu_integration, strings.lang.context_menu_entry_removed)


def process_icon(path, index):
    global icon_from_image, choose_icon, preview

    icon.extract_icon(path, index)
    preview = tk.PhotoImage(file = preferences.roaming + "\\preview.png")

    choose_icon.configure(image = preview, text = f"{os.path.basename(path)}, {index}", width = 30)
    icon_from_image.configure(text = strings.lang.create_icon_from_image, image = "", width = 0)


def choose_icon_():
    global preview, icon_old

    match icon_type.get():
        case "default":
            choose_icon.configure(text = strings.lang.choose_icon, image = "", width = 0)
            icon_from_image.configure(text = strings.lang.create_icon_from_image, image = "", width = 0)
        case "icon":
            try:
                icon_path, icon_index = icon.pick_icon()
                process_icon(icon_path, icon_index)                
            except:
                icon_type.set(icon_old)
        case "image":
            image = filedialog.askopenfile(title = strings.lang.choose_image, filetypes = [(strings.lang.images, (".png", ".jpg", ".jpeg", ".bmp", ".gif"))])

            if not image is None:
                icon.convert_image_to_icon(image.name)
                preview = tk.PhotoImage(file = preferences.roaming + "\\preview.png")
                
                icon_from_image.configure(image = preview, text = os.path.basename(icon_path), width = 30)
                choose_icon.configure(text = strings.lang.choose_icon, image = "", width = 0)
            else:
                icon_type.set(icon_old)
        
    icon_old = icon_type.get()


draw_ui()
refresh_volumes_list()
custom_ui.sync_colors_with_system(window)
window.mainloop()