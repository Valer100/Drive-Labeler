import ctypes, shutil, os
from PIL import Image, IcoImagePlugin
from icoextract import IconExtractor
from utils import preferences


def pick_icon(initial_icon_file_path: str = "C:\\Windows\\System32\\shell32.dll") -> tuple[str, int]:
    icon_file_buffer = ctypes.create_unicode_buffer(260)
    icon_index = ctypes.c_int(0)

    ctypes.windll.kernel32.lstrcpyW(icon_file_buffer, initial_icon_file_path)

    result = ctypes.windll.shell32.PickIconDlg(None, icon_file_buffer, ctypes.sizeof(icon_file_buffer), ctypes.byref(icon_index))
    if result: return (icon_file_buffer.value, icon_index.value)


def extract_icon(path: str, index: str) -> None:
    if not path.endswith(".ico"):
        try:
            extractor = IconExtractor(path)
            extractor.export_icon(preferences.roaming + "\\icon.ico", index)
        except:
            extractor = IconExtractor(path.replace("System32", "SystemResources") + ".mun")
            extractor.export_icon(preferences.roaming + "\\icon.ico", index)
    else:
        shutil.copyfile(path, preferences.roaming + "\\icon.ico")

    img = IcoImagePlugin.IcoImageFile(preferences.roaming + "\\icon.ico")

    closest_size = min(
        img.info["sizes"],
        key = lambda size: (size[0] - 32) ** 2 + (size[1] - 32) ** 2
    )

    img.size = closest_size
    img.load()
    img = img.resize((32, 32), Image.Resampling.LANCZOS)
    img.save(preferences.roaming + "\\preview.png")
    img.close()


def convert_image_to_icon(path: str) -> None:
    img = Image.open(path)
    img.save(fp = preferences.roaming + "\\icon.ico", format = "ICO", sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128)])

    preview_img = img.resize((32, int(img.height * 32 / img.width)), Image.Resampling.LANCZOS)
    preview_img.save(preferences.roaming + "\\preview.png")
    preview_img.close()

    img.close()


def tint_image(image_path, output_path, color):
    color = color.lstrip('#')  # Remove the '#' if present
    rgb_color = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))

    img = Image.open(image_path).convert("RGBA")
    pixels = img.load()

    for y in range(img.height):
        for x in range(img.width):
            _, _, _, alpha = pixels[x, y]
            if alpha > 0:
                pixels[x, y] = rgb_color + (alpha,)
    
    img.save(output_path)