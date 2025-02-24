from . import _info

# Language info
language = "English"
language_en = "English"
author = "Valer100"

# Main window
settings = "Settings"
volume = "Volume"
label = "Label"
icon = "Icon"
default_icon = "Default icon"
choose_icon = "Choose icon"
create_icon_from_image = "Create icon from image"
choose_image = "Choose an image"
images = "Images"
apply_changes = "Apply changes"
remove_customizations = "Remove customizations"
remove_customizations_message = "Are you sure? Every single customization made to the volume through the \"autorun.inf\" file will be removed."
local_disk = "Local Disk"
additional_options = "Additional options"
hide_autorun = "Hide autorun.inf file"
hide_vl_icon = "Hide vl_icon folder"
backup_existing_autorun = "Backup autorun.inf file (if it already exists)"
context_menu_integration_disabled = "Context menu integration: Disabled"
context_menu_integration_enabled = "Context menu integration: Enabled"
context_menu_integration_not_available_portable = "Context menu integration: Unavailable in portable mode"
refresh_volumes_list = "Refresh volumes list"
reset_changes = "Reset changes"

# Messages
done = "Done"
operation_complete = "The volume's information were changed.\n\nIf the volume is on a removable drive, unplug the drive and plug it back into your computer for the changes to take effect. If it isn't, the changes will take effect the next time your computer starts."
permission_denied = "Permission denied"
permission_denied_message = "The volume is read-only or you don't have rights to create/modify files on it."
volume_not_accessible = "Volume not accessible"
volume_not_accessible_message = "The selected volume is not accessible."
error = "An error occurred"
failure_message = "Failed to change the volume's information.\n\n"
missing_icon_file = "The copied icon file is missing."
context_menu_integration = "Context menu integration"
context_menu_entry_added = "The context menu entry was successfully added.\n\nNote: The context menu entry will only appear in the classic full context menu on Windows 11."
context_menu_entry_removed = "The context menu entry was successfully removed."
copy_traceback_success = "The traceback was successfully copied to clipboard."
ui_reload_required = "UI reload required"
ui_reload_confirmation = "This setting requires a UI reload to take effect. Would you like to reload the UI now? All unsaved changes will be lost."
reset_changes_confirmation = "Are you sure? This action will reset all your unapplied changes that you made."
apply_changes_exit = "Would you like to apply the changes made to this volume before exiting?"
apply_changes_change_volume = "Would you like to apply the changes made to this volume before switching to another one?"

# Files
readme = "READ ME!"
autorun_backup = """This folder includes backups of the `autorun.inf` file before Volume Labeler
made changes to it. If something went wrong or you want to restore the settings before 
the modification, you can do so by deleting the `autorun.inf` file in the root of this
volume (you may need to enable the "Show hidden files" option to see it). After that, 
go back to this folder, copy one of the autorun files (they are of the form `autorun_{date and time}.inf`) 
to the root of this volume and then rename it to autorun.inf."""
icon_folder = """This folder contains the icon that's displayed to your volume.
Do not delete/move/rename this folder or the icon file inside it."""

# Other
open_source_licenses = "Open source licenses"
change_language = "Change language"
change_theme = "Change theme"
light_theme = "Light theme"
dark_theme = "Dark theme"
lang_system_default = "System default"
ok = "OK"
cancel = "Cancel"
about_this_app = "About this app"
about_title = "About Volume Labeler"
version = f"Version {_info.version}"
last_commit = f"(last commit: {_info.last_commit})"
customize_with_volume_labeler = "Customize with Volume Labeler"
issues = "Issues"
latest_version = "Latest version"
copy_traceback = "Copy traceback"
license = "License"
translation_made_by = "Translation made by %a"

# Entry context menu
cut = "Cut"
copy = "Copy"
paste = "Paste"
delete = "Delete"
select_all = "Select all"