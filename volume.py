import strings, os, util, random, re, shutil, traceback, datetime
from tkinter import messagebox

def modify_volume_info(
    volume: str, 
    label: str, 
    default_icon: bool = False, 
    icon_path: str = util.roaming + "\\icon.ico", 
    hide_autorun: bool = True, 
    hide_vl_icon: bool = True, 
    backup_existing_autorun: bool = True
):
    
    if os.path.exists(volume):
        if not default_icon == "default" and not os.path.exists(icon_path):
            messagebox.showerror(strings.lang.error, strings.lang.missing_icon_file)
            return
        

        try:
            if not default_icon:
                id = random.randint(1000000, 9999999)

                if os.path.exists(f"{volume}vl_icon"):
                    shutil.rmtree(f"{volume}vl_icon")

                os.mkdir(f"{volume}vl_icon")
                shutil.copyfile(icon_path, f"{volume}vl_icon\\icon{id}.ico")

                readme_file = open(f"{volume}vl_icon\\! {strings.lang.readme}.txt", "w", encoding = "utf-8")
                readme_file.write(strings.lang.icon_folder)
                readme_file.close()

                if hide_vl_icon: 
                    util.add_hidden_attribute(f"{volume}vl_icon")

            if os.path.exists(f"{volume}autorun.inf") and backup_existing_autorun:
                if not os.path.exists(f"{volume}autorun_backups"): 
                    os.mkdir(f"{volume}autorun_backups")

                util.remove_hidden_attribute(f"{volume}autorun.inf")
                shutil.copyfile(f"{volume}autorun.inf", f"{volume}autorun_backups\\autorun_{str(datetime.now()).replace('-', '_').replace(':', '_')}.inf")

                readme_file = open(f"{volume}autorun_backups\\! {strings.lang.readme}.txt", "w", encoding = "utf-8")
                readme_file.write(strings.lang.autorun_backup)
                readme_file.close()
        except PermissionError:
            messagebox.showerror(strings.lang.permission_denied, strings.lang.permission_denied_message)


        def modify_existing_autorun_file():
            autorun_file = open(f"{volume}autorun.inf")
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
                        if not default_icon == "default":
                            autorun_new += f"\nicon=vl_icon\\icon{id}.ico,0"
                            icon_changed = True
                    elif entry == "label": 
                        autorun_new += f"\nlabel={label}"
                        label_changed = True
                    else: autorun_new += "\n" + line
                else:
                    autorun_new += "\n" + line

            
            if not icon_changed and not default_icon == "default": 
                autorun_new, replacements = re.subn(r"(?i)^\[autorun(?:\.[a-zA-Z0-9_]+)?\]", lambda match: f"{match.group(0)}\nicon=vl_icon\\icon{id}.ico,0", autorun_new, flags = re.MULTILINE)
                if replacements > 0: icon_changed = True
            
            if not label_changed: 
                autorun_new, replacements = re.subn(r"(?i)^\[autorun(?:\.[a-zA-Z0-9_]+)?\]", lambda match: f"{match.group(0)}\nlabel={label}", autorun_new, flags = re.MULTILINE)
                if replacements > 0: label_changed = True

            if not (icon_changed or label_changed):
                autorun_new += f"\n\n[autorun]\nlabel={label}"
                if not default_icon == "default": autorun_new += f"\nicon=vl_icon\\icon{id}.ico,0"

            autorun_new = autorun_new.strip()

            try:
                util.remove_hidden_attribute(f"{volume}autorun.inf")

                autorun_file = open(f"{volume}autorun.inf", "w")
                autorun_file.write(autorun_new)
                autorun_file.close()
            
                if hide_autorun:
                    util.add_hidden_attribute(f"{volume}autorun.inf")

                messagebox.showinfo(strings.lang.done, strings.lang.operation_complete)
            except PermissionError:
                messagebox.showerror(strings.lang.permission_denied, strings.lang.permission_denied_message)
            except UnicodeEncodeError:
                messagebox.showerror(strings.lang.error, strings.lang.unicode_not_supported)
            except:
                messagebox.showerror(strings.lang.error, strings.lang.failure_message + traceback.format_exc())
        

        def create_new_autorun_file():
            try:
                autorun = f"[autorun]\nlabel={label}"
                if not default_icon == "default": autorun += f"\nicon=vl_icon\\icon{id}.ico,0"

                util.remove_hidden_attribute(f"{volume}autorun.inf")

                autorun_file = open(f"{volume}autorun.inf", "w")
                autorun_file.write(autorun)
                autorun_file.close()

                if hide_autorun:
                    util.add_hidden_attribute(f"{volume}autorun.inf")

                messagebox.showinfo(strings.lang.done, strings.lang.operation_complete)
            except PermissionError:
                messagebox.showerror(strings.lang.permission_denied, strings.lang.permission_denied_message)
            except UnicodeEncodeError:
                messagebox.showerror(strings.lang.error, strings.lang.unicode_not_supported)
            except:
                messagebox.showerror(strings.lang.error, strings.lang.failure_message + traceback.format_exc())


        if os.path.exists(f"{volume}autorun.inf"):
            autorun_file = open(f"{volume}autorun.inf")
            autorun = autorun_file.read()
            autorun_file.close()

            if re.search("(?i)^\\[[^\\]]+\\]", autorun):
                modify_existing_autorun_file()
            else:
                create_new_autorun_file()
        else:
            create_new_autorun_file()
    else:
        messagebox.showerror(strings.lang.volume_not_accessible, strings.lang.volume_not_accessible_message)


def remove_personalizations(volume: str, backup_existing_autorun: bool = True):
    confirmed = messagebox.askyesno(strings.lang.remove_customizations, strings.lang.remove_customizations_message, icon = "warning")

    if confirmed:
        if os.path.exists(volume):
            try:
                if os.path.exists(f"{volume}autorun.inf") and backup_existing_autorun:
                    if not os.path.exists(f"{volume}autorun_backups"):
                        os.mkdir(f"{volume}autorun_backups")

                    util.remove_hidden_attribute(f"{volume}autorun.inf")
                    shutil.copyfile(f"{volume}autorun.inf", f"{volume}autorun_backups\\autorun_{str(datetime.now()).replace('-', '_').replace(':', '_')}.inf")

                    readme_file = open(f"{volume}autorun_backups\\! {strings.lang.readme}.txt", "w", encoding = "utf-8")
                    readme_file.write(strings.lang.autorun_backup)
                    readme_file.close()

                if os.path.exists(f"{volume}autorun.inf"):
                    os.remove(f"{volume}autorun.inf")

                if os.path.exists(f"{volume}vl_icon"):
                    shutil.rmtree(f"{volume}vl_icon")

                messagebox.showinfo(strings.lang.done, strings.lang.operation_complete)
            except PermissionError:
                messagebox.showerror(strings.lang.permission_denied, strings.lang.permission_denied_message)
            except:
                messagebox.showerror(strings.lang.error, strings.lang.failure_message + traceback.format_exc())
        else:
            messagebox.showerror(strings.lang.volume_not_accessible, strings.lang.volume_not_accessible_message)