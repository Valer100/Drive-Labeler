from . import _info

# Language info
language = "Română"
language_en = "Romanian"
author = "Valer100"

# Main window
settings = "Setări"
volume = "Volum"
label = "Etichetă"
icon = "Pictogramă"
default_icon = "Pictogramă implicită"
choose_icon = "Alege pictograma"
create_icon_from_image = "Creează pictogramă din imagine"
choose_image = "Alege o imagine"
images = "Imagini"
apply_changes = "Aplică modificările"
remove_customizations = "Elimină personalizările"
remove_customizations_message = "Ești sigur(ă)? Toate personalizările făcute volumului prin fișierul \"autorun.inf\" vor fi eliminate."
local_disk = "Disc local"
additional_options = "Opțiuni adiționale"
hide_autorun = "Ascunde fișierul autorun.inf"
hide_vl_icon = "Ascunde folderul vl_icon"
backup_existing_autorun = "Fă backup fișierului autorun.inf (dacă există deja)"
context_menu_integration_disabled = "Integrare în meniul contextual: Dezactivată"
context_menu_integration_enabled = "Integrare în meniul contextual: Activată"
context_menu_integration_not_available_portable = "Integrare în meniul contextual: Indisponibilă în modul portabil"
refresh_volumes_list = "Reîmprospătează lista volumelor"
reset_changes = "Resetează modificările"

# Messages
done = "Gata"
operation_complete = "Informațiile volumului au fost modificate.\n\nDacă volumul se află pe o unitate amovibilă, deconectează unitatea și conecteaz-o înapoi la calculator pentru ca modificările să aibă efect. Dacă nu, modificările vor avea efect la următoarea pornire a calculatorului."
permission_denied = "Permisiune refuzată"
permission_denied_message = "Volumul poate fi doar citit sau nu ai drepturi ca să creezi/modifici fișiere pe el."
volume_not_accessible = "Volum inaccesibil"
volume_not_accessible_message = "Volumul selectat este inaccesibil."
error = "A intervenit o eroare"
failure_message = "Nu s-au putut modifica informațiile volumului.\n\n"
missing_icon_file = "Fișierul pictogramei copiate lipsește."
context_menu_integration = "Integrare în meniul contextual"
context_menu_entry_added = "Intrarea în meniul contextual a fost adăugată cu succes.\n\nNotă: Intrarea în meniul contextual va apărea numai în meniul contextual clasic complet pe Windows 11."
context_menu_entry_removed = "Intrarea în meniul contextual a fost eliminată cu succes."
copy_traceback_success = "Traceback-ul a fost copiat cu succes în clipboard."
ui_reload_required = "Reîncărcare UI necesară"
ui_reload_confirmation = "Această setare necesită o reîncărcare a UI-ului pentru a avea efect. Ai dori să reîncarci UI-ul acum? Toate modificările nesalvate vor fi pierdute."
reset_changes_confirmation = "Ești sigur(ă)? Această acțiune va reseta toate modificările neaplicate pe care le-ai făcut."
apply_changes_exit = "Ai vrea să aplici modificările făcute acestui volum înainte de a ieși?"
apply_changes_change_volume = "Ai vrea să aplici modificările făcute acestui volum înainte de a trece la altul?"

# Files
readme = "CITEȘTE-MĂ!"
autorun_backup = """Acest folder include copii de rezervă ale fișierului `autorun.inf` 
înainte ca Volume Labeler să facă modificări acestuia. Dacă ceva nu a mers cum trebuie
sau vrei să restaurezi setările dinainte de modificare, poți face asta ștergând fișierul 
`autorun.inf` din rădăcina volumului (s-ar putea să fie nevoie să activezi opțiunea
"Arată fișierele ascunse" ca să-l vezi). După aceea, revino în acest folder, copiază unul
dintre fișierele autorun prezente (sunt de forma `autorun_{data și ora}.inf`) în rădăcina 
acestui volum și apoi redenumește-l în autorun.inf."""
icon_folder = """Acest folder conține pictograma care este afișată la acest volum.
Nu șterge/muta/redenumi acest folder sau fișierul pictogramei din el."""

# Other
open_source_licenses = "Licențe open source"
change_language = "Schimbă limba"
change_theme = "Schimbă tema"
light_theme = "Temă luminoasă"
dark_theme = "Temă întunecată"
lang_system_default = "Prestabilită de sistem"
ok = "OK"
cancel = "Anulare"
about_this_app = "Despre această aplicație"
about_title = "Despre Volume Labeler"
version = f"Versiunea {_info.version}"
last_commit = f"(ultimul commit: {_info.last_commit})"
customize_with_volume_labeler = "Personalizează cu Volume Labeler"
issues = "Probleme"
latest_version = "Cea mai recentă versiune"
copy_traceback = "Copiază traceback-ul"
license = "Licență"
translation_made_by = "Traducere făcută de %a"

# Entry context menu
cut = "Decupează"
copy = "Copiază"
paste = "Lipește"
delete = "Șterge"
select_all = "Selectează tot"