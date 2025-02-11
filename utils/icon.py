import ctypes, shutil
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
        key = lambda size: (size[0] - preferences.icon_size) ** 2 + (size[1] - preferences.icon_size) ** 2
    )

    img.size = closest_size
    img.load()
    img = img.resize((preferences.icon_size, preferences.icon_size), Image.Resampling.LANCZOS)
    img.save(preferences.roaming + "\\preview.png")
    img.close()


def convert_image_to_icon(path: str) -> None:
    img = Image.open(path).convert("RGBA")

    max_side = max(img.size)
    new_img = Image.new("RGBA", (max_side, max_side), (0, 0, 0, 0))

    x_offset = (max_side - img.width) // 2
    y_offset = (max_side - img.height) // 2

    new_img.paste(img, (x_offset, y_offset), img)
    img.close()

    new_img.save(fp = preferences.roaming + "\\icon.ico", format = "ICO", sizes = [(16, 16), (20, 20), (24, 24), (30, 30), (32, 32), (48, 48), (64, 64), (72, 72), (96, 96), (128, 128), (144, 144), (196, 196), (256, 256)])
    new_img = new_img.resize((preferences.icon_size, preferences.icon_size), Image.Resampling.LANCZOS)
    new_img.save(preferences.roaming + "\\preview.png")
    new_img.close()


def extract_and_tint_icon(image_path, output_path, color):
    color = color.lstrip("#")
    rgb_color = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))

    img = IcoImagePlugin.IcoImageFile(image_path)

    closest_size = min(
        img.info["sizes"],
        key = lambda size: (size[0] - preferences.icon_size) ** 2 + (size[1] - preferences.icon_size) ** 2
    )

    img.size = closest_size
    img = img.resize((preferences.icon_size, preferences.icon_size), Image.Resampling.LANCZOS)
    img = img.convert("RGBA")
    pixels = img.load()

    for y in range(img.height):
        for x in range(img.width):
            _, _, _, alpha = pixels[x, y]
            if alpha > 0:
                pixels[x, y] = rgb_color + (alpha,)
    
    img.save(output_path)