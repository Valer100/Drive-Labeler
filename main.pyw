import tkinter as tk, util, open_source_licenses, change_language, change_theme, strings, custom_ui, subprocess, os, shutil, random, traceback, re
from tkinter import ttk, filedialog, messagebox
from PIL import Image
from icoextract import IconExtractor

window = custom_ui.App()
window.title("Volume Labeler")
window.resizable(False, False)
window.iconbitmap(default = util.internal + "icon.ico")
window.configure(padx = 14, pady = 8)

icon_old = "default"
volumes = [""]
autorun = ""
selected_volume = tk.StringVar(value = "")
hide_autorun = tk.BooleanVar(value = True)
hide_vl_icon = tk.BooleanVar(value = True)
icon = tk.StringVar(value = "default")

def refresh_volumes():
    global volumes

    volumes = subprocess.getoutput("fsutil fsinfo drives").split(" ")
    volumes.pop(0)
    volumes.pop()

    selected_volume.set(volumes[0])

    menu = volume["menu"]
    menu.delete(0, "end")

    for string in volumes:
        menu.add_command(label = string, command = lambda value = string: update_volume_info(value))

    update_volume_info(volumes[0])


def update_volume_info(volume):
    global icon, autorun

    if util.is_volume_accessible(volume):
        selected_volume.set(volume)

        icon.set("default")
        choose_icon.configure(text = strings.lang.choose_icon, image = "", width = 0)
        icon_from_image.configure(text = strings.lang.create_icon_from_image, image = "", width = 0)

        volume_label = subprocess.getoutput(f"for /f \"tokens=5*\" %A in ('vol {volume[0:2]}') do @if \"%B\"==\"\" (timeout /t 0 > nul) else echo %B").replace("\nERROR: Input redirection is not supported, exiting the process immediately.", "")

        label.delete(0, "end")
        label.insert(0, strings.lang.local_disk if volume == "C:\\" and volume_label == "no label." else strings.lang.volume if volume_label == "no label." else volume_label)

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
    global choose_icon, icon_from_image, refresh, volume, label

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
    label_frame.pack(anchor = "w")

    label = tk.Entry(label_frame, width = 40, background = custom_ui.entry_bg, 
                    foreground = custom_ui.fg, border = 0, highlightthickness = 2, 
                    highlightcolor = custom_ui.entry_bg, highlightbackground = custom_ui.entry_bg, 
                    insertbackground = custom_ui.fg, insertwidth = 1, selectbackground = custom_ui.entry_select,
                    selectforeground = "#FFFFFF")
    label.pack()

    ttk.Label(window, text = strings.lang.icon).pack(pady = (16, 8), anchor = "w")

    default_icon = ttk.Radiobutton(window, text = strings.lang.default_icon, variable = icon, value = "default", command = choose_icon_)
    default_icon.pack(anchor = "w")

    choose_icon = ttk.Radiobutton(window, text = strings.lang.choose_icon, variable = icon, value = "icon", command = choose_icon_, compound = "left")
    choose_icon.pack(anchor = "w")
    
    icon_from_image = ttk.Radiobutton(window, text = strings.lang.create_icon_from_image, variable = icon, value = "image", command = choose_icon_, compound = "left")
    icon_from_image.pack(anchor = "w")

    ttk.Label(window, text = strings.lang.additional_options).pack(pady = (16, 8), anchor = "w")
    
    ttk.Checkbutton(window, text = strings.lang.hide_autorun, variable = hide_autorun).pack(anchor = "w")
    ttk.Checkbutton(window, text = strings.lang.hide_vl_icon, variable = hide_vl_icon).pack(anchor = "w")

    custom_ui.Button(window, text = strings.lang.apply_changes, command = lambda: modify_volume_info(selected_volume.get(), label.get()), default = "active").pack(pady = (16, 0), fill = "x")
    custom_ui.Button(window, text = strings.lang.remove_customizations, command = lambda: remove_personalizations(selected_volume.get())).pack(pady = (8, 0), fill = "x")

    ttk.Label(window, text = strings.lang.settings, font = ("Segoe UI Semibold", 14)).pack(anchor = "w", pady = (16, 4))
    custom_ui.Toolbutton(window, text = strings.lang.change_language, link = True, command = change_app_language).pack(anchor = "w")
    custom_ui.Toolbutton(window, text = strings.lang.change_theme, link = True, command = change_app_theme).pack(anchor = "w")
    custom_ui.Toolbutton(window, text = strings.lang.see_open_source_licenses, link = True, command = open_source_licenses.show).pack(anchor = "w")

    window.update()


def process_icon(path, index):
    global icon_from_image, choose_icon, preview

    img = Image.open(util.extract_icon(path, index))
    img = img.resize((32, 32), Image.Resampling.LANCZOS)
    img.save(util.roaming + "\preview.png")
    img.close()

    if not path.endswith(".ico"):
        try:
            extractor = IconExtractor(path)
            extractor.export_icon(util.roaming + "\\icon.ico", index)
        except:
            extractor = IconExtractor(path.replace("System32", "SystemResources") + ".mun")
            extractor.export_icon(util.roaming + "\\icon.ico", index)
    else:
        shutil.copyfile(path, util.roaming + "\\icon.ico")

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
            except Exception as e:
                print(e)
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
        

        if not icon.get() == "default":
            id = random.randint(1000000, 9999999)

            if os.path.exists(f"{volume}\\vl_icon"):
                subprocess.call(f"rmdir /s /q \"{volume}\\vl_icon\"", shell = True)

            os.mkdir(f"{volume}\\vl_icon")
            shutil.copyfile(util.roaming + "\\icon.ico", f"{volume}\\vl_icon\\icon{id}.ico")

            if hide_vl_icon.get():
                subprocess.call(f"attrib +H \"{volume}\\vl_icon\"", shell = True)


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
                subprocess.call(f"attrib -H \"{volume}\\autorun.inf\"", shell = True)

                autorun_file = open(f"{selected_volume.get()}autorun.inf", "w")
                autorun_file.write(autorun_new)
                autorun_file.close()
            
                if hide_autorun.get():
                    subprocess.call(f"attrib +H \"{volume}\\autorun.inf\"", shell = True)

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

                subprocess.call(f"attrib -H \"{volume}\\autorun.inf\"", shell = True)
                autorun_file = open(f"{volume}autorun.inf", "w")
                autorun_file.write(autorun)
                autorun_file.close()

                if hide_autorun.get():
                    subprocess.call(f"attrib +H \"{volume}\\autorun.inf\"", shell = True)

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
    confirmed = messagebox.askyesno(strings.lang.remove_customizations, strings.lang.remove_customizations_message)

    if confirmed:
        if util.is_volume_accessible(volume):
            try:
                if os.path.exists(f"{volume}\\autorun.inf"):
                    os.remove(f"{volume}\\autorun.inf")

                if os.path.exists(f"{volume}\\vl_icon"):
                    subprocess.call(f"rmdir /s /q \"{volume}\\vl_icon\"", shell = True)

                update_volume_info(volume)
                messagebox.showinfo(strings.lang.done, strings.lang.operation_complete)
            except PermissionError:
                messagebox.showerror(strings.lang.permission_denied, strings.lang.read_only_volume_message)
            except Exception as e:
                messagebox.showerror(strings.lang.error, strings.lang.failure_message + "".join(traceback.format_tb(e.__traceback__)))
        else:
            messagebox.showerror(strings.lang.volume_not_accessible, strings.lang.volume_not_accessible_message)


draw_ui()
refresh_volumes()
custom_ui.sync_colors_with_system(window)
window.mainloop()