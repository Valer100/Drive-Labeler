import tkinter as tk, util, about, change_language, change_theme, strings, custom_ui, subprocess, os, shutil, random, traceback, re, tktooltip, argparse, winreg, sys
from tkinter import ttk, filedialog, messagebox
from PIL import Image, IcoImagePlugin
from icoextract import IconExtractor
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument("--volume", default = None, help = "The letter of the volume you want to customize", required = False)

arguments = parser.parse_args()

window = custom_ui.App()
window.title("Volume Labeler")
window.resizable(False, False)
window.iconbitmap(default = util.internal + "icon.ico")
window.configure(padx = 14, pady = 8)

show_additional_options = False
icon_old = "default"
volumes = [""]
autorun = ""
app_started = False
selected_volume = tk.StringVar(value = "")
hide_autorun = tk.BooleanVar(value = int(util.additional_prefs[0]))
hide_vl_icon = tk.BooleanVar(value = int(util.additional_prefs[1]))
backup_existing_autorun = tk.BooleanVar(value = int(util.additional_prefs[2]))
icon = tk.StringVar(value = "default")


def refresh_volumes():
    global volumes, app_started

    volumes = subprocess.getoutput("fsutil fsinfo drives").split(" ")
    volumes.pop(0)
    volumes.pop()

    selected_volume.set(volumes[0])

    menu = volume["menu"]
    menu.delete(0, "end")

    for string in volumes:
        menu.add_command(label = string, command = lambda value = string: update_volume_info(value))

    if not app_started and arguments.volume != None:
        if util.is_volume_accessible(arguments.volume.upper()):
            update_volume_info(arguments.volume.upper())
        else:
            update_volume_info(volumes[0])
            messagebox.showerror(strings.lang.volume_not_accessible, strings.lang.volume_not_accessible_message)
    else:
        update_volume_info(volumes[0])

    app_started = True


def update_volume_info(volume):
    global icon, autorun

    if util.is_volume_accessible(volume):
        selected_volume.set(volume)

        icon.set("default")
        choose_icon.configure(text = strings.lang.choose_icon, image = "", width = 0)
        icon_from_image.configure(text = strings.lang.create_icon_from_image, image = "", width = 0)

        volume_label = util.get_volume_label(volume)

        label.delete(0, "end")
        label.insert(0, strings.lang.local_disk if volume == "C:\\" and volume_label == "" else strings.lang.volume if volume_label == "" else volume_label)

        if os.path.exists(f"{selected_volume.get()}autorun.inf"):
            autorun_file = open(f"{selected_volume.get()}autorun.inf")
            autorun = autorun_file.read()
            autorun_file.close()

            autorun_lines = autorun.split("\n")

            for line in autorun_lines:
                entry_and_param = line.split("=", 1)

                if len(entry_and_param) == 2:
                    entry = entry_and_param[0].strip().lower()
                    param = entry_and_param[1].strip()

                    if entry == "icon":
                        path_and_index = param.rsplit(",", 1)
                        icon_path = path_and_index[0]

                        if len(path_and_index) == 2: icon_index = int(path_and_index[1].strip())
                        else: icon_index = 0

                        if not icon_path.lower().startswith(volume.lower()):
                            icon_path = volume + icon_path

                        if os.path.exists(icon_path): 
                            icon.set("icon")
                            process_icon(icon_path, icon_index)
                    elif entry == "label":
                        label.delete(0, "end")
                        label.insert(0, param)
    else:
        messagebox.showerror(strings.lang.volume_not_accessible, strings.lang.volume_not_accessible_message)


def destroy_everything(widget):
    for child in widget.winfo_children():
        child.destroy()


def change_app_language():
    old_language = util.language

    change_language.show()
    window.wait_window(change_language.window)

    if old_language != util.language: 
        draw_ui()
        refresh_volumes()


def change_app_theme():
    old_theme = util.theme

    change_theme.show()
    window.wait_window(change_theme.window)

    if old_theme != util.theme:
        custom_ui.update_colors()
        window.set_theme()
        draw_ui()
        refresh_volumes()


def draw_ui():
    global choose_icon, icon_from_image, refresh, volume, label, arrow, show_additional_options, context_menu_integration, context_menu_integration_tooltip

    show_additional_options = False

    destroy_everything(window)
    strings.load_language(open(util.user_preferences + "\\language", "r").read())

    ttk.Label(window, text = "Volume Labeler", font = ("Segoe UI Semibold", 17)).pack(anchor = "w")

    volume_section = ttk.Frame(window)
    volume_section.pack(fill = "x", anchor = "w", pady = (16, 8))

    ttk.Label(volume_section, text = strings.lang.volume).pack(side = "left")

    if custom_ui.light_theme: refresh = tk.PhotoImage(file = f"{util.internal}icons\\refresh_light.png")
    else: refresh = tk.PhotoImage(file = f"{util.internal}icons\\refresh_dark.png")

    custom_ui.Button(volume_section, width = -1, command = refresh_volumes, image = refresh).pack(side = "right", padx = (8, 0))
    
    volume = custom_ui.OptionMenu(volume_section, selected_volume, *volumes)
    volume.pack(side = "right")

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

    default_icon = ttk.Radiobutton(window, text = strings.lang.default_icon, variable = icon, value = "default", command = choose_icon_)
    default_icon.pack(anchor = "w")

    choose_icon = ttk.Radiobutton(window, text = strings.lang.choose_icon, variable = icon, value = "icon", command = choose_icon_, compound = "left")
    choose_icon.pack(anchor = "w")
    
    icon_from_image = ttk.Radiobutton(window, text = strings.lang.create_icon_from_image, variable = icon, value = "image", command = choose_icon_, compound = "left")
    icon_from_image.pack(anchor = "w")

    if custom_ui.light_theme: arrow = tk.PhotoImage(file = f"{util.internal}icons/dropdown_light.png")
    else: arrow = tk.PhotoImage(file = f"{util.internal}icons/dropdown_dark.png")

    additional_options = custom_ui.Toolbutton(window, text = " " + strings.lang.additional_options, command = lambda: show_hide_additional_options(), anchor = "w", compound = "left", image = arrow)
    additional_options.pack(pady = (14, 0), anchor = "w")
    additional_options.configure(padx = 0)

    additional_options_frame = ttk.Frame(window)
    additional_options_frame.pack(anchor = "w")
    
    def show_hide_additional_options():
        global show_additional_options, arrow
        show_additional_options = not show_additional_options

        for widget in additional_options_frame.winfo_children():
            if custom_ui.light_theme: arrow = tk.PhotoImage(file = f"{util.internal}icons/dropdown{'_up' if show_additional_options else ''}_light.png")
            else: arrow = tk.PhotoImage(file = f"{util.internal}icons/dropdown{'_up' if show_additional_options else ''}_dark.png")
            
            additional_options.configure(image = arrow)

            if show_additional_options: 
                if widget["text"] == strings.lang.hide_autorun:
                    widget.pack(pady = (6, 0), anchor = "w")
                else:
                    widget.pack(anchor = "w")
            else: widget.forget()

        if show_additional_options: additional_options_frame.configure(height = -1)
        else: additional_options_frame.configure(height = 1)

    def save_additional_preferences(): open(util.user_preferences + "\\additional_prefs", "w").write(f"{int(hide_autorun.get())}{int(hide_vl_icon.get())}{int(backup_existing_autorun.get())}")

    ttk.Checkbutton(additional_options_frame, text = strings.lang.hide_autorun, command = save_additional_preferences, variable = hide_autorun)
    ttk.Checkbutton(additional_options_frame, text = strings.lang.hide_vl_icon, command = save_additional_preferences, variable = hide_vl_icon)
    ttk.Checkbutton(additional_options_frame, text = strings.lang.backup_existing_autorun, command = save_additional_preferences, variable = backup_existing_autorun)

    custom_ui.Button(window, text = strings.lang.apply_changes, command = lambda: modify_volume_info(selected_volume.get(), label.get()), default = "active").pack(pady = (16, 0), fill = "x")
    custom_ui.Button(window, text = strings.lang.remove_customizations, command = lambda: remove_personalizations(selected_volume.get())).pack(pady = (8, 0), fill = "x")

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
        context_menu_integration_tooltip = tktooltip.ToolTip(context_menu_integration, strings.lang.context_menu_integration_enabled, follow = True, delay = 1, bg = custom_ui.tooltip_bg, fg = custom_ui.tooltip_fg, parent_kwargs = {"bg":custom_ui.tooltip_bd, "padx": 1, "pady": 1})
    except:
        context_menu_integration.configure(default = "normal")
        context_menu_integration_tooltip = tktooltip.ToolTip(context_menu_integration, strings.lang.context_menu_integration_disabled, follow = True, delay = 1, bg = custom_ui.tooltip_bg, fg = custom_ui.tooltip_fg, parent_kwargs = {"bg":custom_ui.tooltip_bd, "padx": 1, "pady": 1})

    about_app = custom_ui.Toolbutton(settings, text = "\ue946", link = True, icononly = True, anchor = "n", command = about.show, font = ("Segoe UI", 13))
    about_app.pack(anchor = "nw", side = "left", padx = (4, 0))
    
    tktooltip.ToolTip(language, strings.lang.change_language, follow = True, delay = 1, bg = custom_ui.tooltip_bg, fg = custom_ui.tooltip_fg, parent_kwargs = {"bg":custom_ui.tooltip_bd, "padx": 1, "pady": 1})
    tktooltip.ToolTip(theme, strings.lang.change_theme, follow = True, delay = 1, bg = custom_ui.tooltip_bg, fg = custom_ui.tooltip_fg, parent_kwargs = {"bg":custom_ui.tooltip_bd, "padx": 1, "pady": 1})
    tktooltip.ToolTip(about_app, strings.lang.about_this_app, follow = True, delay = 1, bg = custom_ui.tooltip_bg, fg = custom_ui.tooltip_fg, parent_kwargs = {"bg":custom_ui.tooltip_bd, "padx": 1, "pady": 1})

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
        entry.Close()

        context_menu_integration.configure(default = "active")
        context_menu_integration_tooltip = tktooltip.ToolTip(context_menu_integration, strings.lang.context_menu_integration_enabled, follow = True, delay = 1, bg = custom_ui.tooltip_bg, fg = custom_ui.tooltip_fg, parent_kwargs = {"bg":custom_ui.tooltip_bd, "padx": 1, "pady": 1})
        
        messagebox.showinfo(strings.lang.context_menu_integration, strings.lang.context_menu_entry_added)
    else:
        subprocess.call("reg delete \"HKEY_CURRENT_USER\Software\Classes\Drive\shell\Volume Labeler\" /f", shell = True)

        context_menu_integration.configure(default = "normal")
        context_menu_integration_tooltip = tktooltip.ToolTip(context_menu_integration, strings.lang.context_menu_integration_disabled, follow = True, delay = 1, bg = custom_ui.tooltip_bg, fg = custom_ui.tooltip_fg, parent_kwargs = {"bg":custom_ui.tooltip_bd, "padx": 1, "pady": 1})
        
        messagebox.showinfo(strings.lang.context_menu_integration, strings.lang.context_menu_entry_removed)


def process_icon(path, index):
    global icon_from_image, choose_icon, preview

    if not path.endswith(".ico"):
        try:
            extractor = IconExtractor(path)
            extractor.export_icon(util.roaming + "\\icon.ico", index)
        except:
            extractor = IconExtractor(path.replace("System32", "SystemResources") + ".mun")
            extractor.export_icon(util.roaming + "\\icon.ico", index)
    else:
        shutil.copyfile(path, util.roaming + "\\icon.ico")

    img = IcoImagePlugin.IcoImageFile(util.roaming + "\\icon.ico")

    closest_size = min(
        img.info["sizes"],
        key = lambda size: (size[0] - 32) ** 2 + (size[1] - 32) ** 2
    )

    img.size = closest_size
    img.load()
    img = img.resize((32, 32), Image.Resampling.LANCZOS)
    img.save(util.roaming + "\preview.png")
    img.close()

    preview = tk.PhotoImage(file = util.roaming + "\preview.png")
    choose_icon.configure(image = preview, text = f"{os.path.basename(path)}, {index}", width = 30)
    icon_from_image.configure(text = strings.lang.create_icon_from_image, image = "", width = 0)


def choose_icon_():
    global preview, icon_old

    match icon.get():
        case "default":
            choose_icon.configure(text = strings.lang.choose_icon, image = "", width = 0)
            icon_from_image.configure(text = strings.lang.create_icon_from_image, image = "", width = 0)
        case "icon":
            try:
                icon_path, icon_index = util.pick_icon()
                process_icon(icon_path, icon_index)                
            except:
                icon.set(icon_old)
        case "image":
            image = filedialog.askopenfile(title = strings.lang.choose_image, filetypes = [(strings.lang.images, (".png", ".jpg", ".jpeg", ".bmp", ".gif"))])

            if not image is None:
                icon_path = image.name

                img = Image.open(icon_path)
                img.save(fp = util.roaming + "\icon.ico", format = "ICO", sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128)])

                preview_img = img.resize((32, int(img.height * 32 / img.width)), Image.Resampling.LANCZOS)
                preview_img.save(util.roaming + "\preview.png")
                preview_img.close()

                img.close()

                preview = tk.PhotoImage(file = util.roaming + "\preview.png")
                icon_from_image.configure(image = preview, text = os.path.basename(icon_path), width = 30)
                
                choose_icon.configure(text = strings.lang.choose_icon, image = "", width = 0)
            else:
                icon.set(icon_old)
        
    icon_old = icon.get()


def modify_volume_info(volume: str, label: str):
    if util.is_volume_accessible(volume):
        if not icon.get() == "default" and not os.path.exists(util.roaming + "\\icon.ico"):
            messagebox.showerror(strings.lang.error, strings.lang.missing_icon_file)
            return
        

        try:
            if not icon.get() == "default":
                id = random.randint(1000000, 9999999)

                if os.path.exists(f"{volume}vl_icon"):
                    subprocess.call(f"rmdir /s /q \"{volume}vl_icon\"", shell = True)

                os.mkdir(f"{volume}vl_icon")
                shutil.copyfile(util.roaming + "\\icon.ico", f"{volume}vl_icon\\icon{id}.ico")

                readme_file = open(f"{volume}vl_icon\\! {strings.lang.readme}.txt", "w", encoding = "utf-8")
                readme_file.write(strings.lang.icon_folder)
                readme_file.close()

                if hide_vl_icon.get():
                    subprocess.call(f"attrib +H \"{volume}vl_icon\"", shell = True)

            if os.path.exists(f"{volume}autorun.inf") and backup_existing_autorun.get():
                if not os.path.exists(f"{volume}autorun_backups"):
                    os.mkdir(f"{volume}autorun_backups")

                subprocess.call(f"attrib -H \"{volume}autorun.inf\"", shell = True)
                shutil.copyfile(f"{volume}autorun.inf", f"{volume}autorun_backups\\autorun_{str(datetime.now()).replace('-', '_').replace(':', '_')}.inf")

                readme_file = open(f"{volume}autorun_backups\\{strings.lang.readme}.txt", "w", encoding = "utf-8")
                readme_file.write(strings.lang.autorun_backup)
                readme_file.close()
        except PermissionError:
            messagebox.showerror(strings.lang.permission_denied, strings.lang.read_only_volume_message)


        def modify_existing_autorun_file():
            autorun_file = open(f"{selected_volume.get()}autorun.inf")
            autorun = autorun_file.read()
            autorun_file.close()

            autorun_new = ""
            autorun_lines = autorun.split("\n")

            icon_changed = False
            label_changed = False

            for line in autorun_lines:
                entry_and_param = line.split("=", 1)

                if len(entry_and_param) == 2:
                    entry = entry_and_param[0].strip().lower()

                    if entry == "icon": 
                        if not icon.get() == "default":
                            autorun_new += f"\nicon=vl_icon\icon{id}.ico,0"
                            icon_changed = True
                    elif entry == "label": 
                        autorun_new += f"\nlabel={label}"
                        label_changed = True
                    else: autorun_new += "\n" + line
                else:
                    autorun_new += "\n" + line

            if not icon_changed and not icon.get() == "default": 
                autorun_new = re.sub(r"(?i)^\[autorun(?:\.[a-zA-Z0-9_]+)?\]", lambda match: f"{match.group(0)}\nicon=vl_icon\icon{id}.ico,0", autorun_new, flags = re.MULTILINE)
            
            if not label_changed: 
                autorun_new = re.sub(r"(?i)^\[autorun(?:\.[a-zA-Z0-9_]+)?\]", lambda match: f"{match.group(0)}\nlabel={label}", autorun_new, flags = re.MULTILINE)
            
            autorun_new = autorun_new.strip()

            try:
                subprocess.call(f"attrib -H \"{volume}autorun.inf\"", shell = True)

                autorun_file = open(f"{selected_volume.get()}autorun.inf", "w")
                autorun_file.write(autorun_new)
                autorun_file.close()
            
                if hide_autorun.get():
                    subprocess.call(f"attrib +H \"{volume}autorun.inf\"", shell = True)

                messagebox.showinfo(strings.lang.done, strings.lang.operation_complete)
            except PermissionError:
                messagebox.showerror(strings.lang.permission_denied, strings.lang.read_only_volume_message)
            except UnicodeEncodeError:
                messagebox.showerror(strings.lang.error, strings.lang.unicode_not_supported)
            except:
                messagebox.showerror(strings.lang.error, strings.lang.failure_message + traceback.format_exc())
        

        def create_new_autorun_file():
            try:
                autorun = f"[autorun]\nlabel={label}"
                if not icon.get() == "default": autorun += f"\nicon=vl_icon\\icon{id}.ico,0"

                subprocess.call(f"attrib -H \"{volume}autorun.inf\"", shell = True)

                autorun_file = open(f"{volume}autorun.inf", "w")
                autorun_file.write(autorun)
                autorun_file.close()

                if hide_autorun.get():
                    subprocess.call(f"attrib +H \"{volume}autorun.inf\"", shell = True)

                messagebox.showinfo(strings.lang.done, strings.lang.operation_complete)
            except PermissionError:
                messagebox.showerror(strings.lang.permission_denied, strings.lang.read_only_volume_message)
            except UnicodeEncodeError:
                messagebox.showerror(strings.lang.error, strings.lang.unicode_not_supported)
            except:
                messagebox.showerror(strings.lang.error, strings.lang.failure_message + traceback.format_exc())


        if os.path.exists(f"{volume}autorun.inf"):
            autorun_file = open(f"{volume}autorun.inf")
            autorun = autorun_file.read()
            autorun_file.close()

            if re.search(r"(?i)^\[autorun(?:\.[a-zA-Z0-9_]+)?\]", autorun):
                modify_existing_autorun_file()
            else:
                create_new_autorun_file()
        else:
            create_new_autorun_file()
    else:
        messagebox.showerror(strings.lang.volume_not_accessible, strings.lang.volume_not_accessible_message)


def remove_personalizations(volume: str):
    confirmed = messagebox.askyesno(strings.lang.remove_customizations, strings.lang.remove_customizations_message, icon = "warning")

    if confirmed:
        if util.is_volume_accessible(volume):
            try:
                if os.path.exists(f"{volume}autorun.inf") and backup_existing_autorun.get():
                    if not os.path.exists(f"{volume}autorun_backups"):
                        os.mkdir(f"{volume}autorun_backups")

                    subprocess.call(f"attrib -H \"{volume}autorun.inf\"", shell = True)
                    shutil.copyfile(f"{volume}autorun.inf", f"{volume}autorun_backups\\autorun_{str(datetime.now()).replace('-', '_').replace(':', '_')}.inf")

                    readme_file = open(f"{volume}autorun_backups\\! {strings.lang.readme}.txt", "w", encoding = "utf-8")
                    readme_file.write(strings.lang.autorun_backup)
                    readme_file.close()

                if os.path.exists(f"{volume}autorun.inf"):
                    os.remove(f"{volume}autorun.inf")

                if os.path.exists(f"{volume}vl_icon"):
                    subprocess.call(f"rmdir /s /q \"{volume}vl_icon\"", shell = True)

                update_volume_info(volume)
                messagebox.showinfo(strings.lang.done, strings.lang.operation_complete)
            except PermissionError:
                messagebox.showerror(strings.lang.permission_denied, strings.lang.read_only_volume_message)
            except:
                messagebox.showerror(strings.lang.error, strings.lang.failure_message + traceback.format_exc())
        else:
            messagebox.showerror(strings.lang.volume_not_accessible, strings.lang.volume_not_accessible_message)


draw_ui()
refresh_volumes()
custom_ui.sync_colors_with_system(window)
window.mainloop()