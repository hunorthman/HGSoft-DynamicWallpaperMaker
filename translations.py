import json
import os

TRANSLATIONS = {
    "en": {
        "title": "HGSoft - Dynamic Wallpaper Maker",
        "pkg_name": "Package Name:",
        "pkg_placeholder": "e.g. MyAwesomeWallpaper",
        "light_box": "Light Wallpaper",
        "dark_box": "Dark Wallpaper",
        "no_image": "No image selected",
        "browse": "Browse...",
        "generate": "Create Dynamic Wallpaper Package",
        "about": "About",
        "language": "Language",
        "err_title": "Error",
        "err_no_name": "Please enter a package name!",
        "err_no_images": "Please select both light and dark images!",
        "success_title": "Success",
        "success_msg": "Dynamic wallpaper package successfully created at:\n\n{dest}",
        "about_title": "About HGSoft Dynamic Wallpaper Maker",
        "about_text": "<b>HGSoft Dynamic Wallpaper Maker</b><br><br>"
                     "A simple utility to create KDE Plasma light/dark dynamic wallpaper packages.<br><br>"
                     "Created by <b>HGSoft</b><br>"
                     "License: MIT"
    },
    "hu": {
        "title": "HGSoft - Dynamic Wallpaper Maker",
        "pkg_name": "Csomag neve:",
        "pkg_placeholder": "Pl.: SajatHatterkep",
        "light_box": "Világos háttérkép (Light)",
        "dark_box": "Sötét háttérkép (Dark)",
        "no_image": "Nincs kép kiválasztva",
        "browse": "Tallózás...",
        "generate": "Dinamikus Háttérkép Csomag Létrehozása",
        "about": "Rólunk / About",
        "language": "Nyelv / Language",
        "err_title": "Hiba",
        "err_no_name": "Kérlek add meg a csomag nevét!",
        "err_no_images": "Kérlek válaszd ki mindkét képet!",
        "success_title": "Siker",
        "success_msg": "A dinamikus háttérkép csomag sikeresen létrejött itt:\n\n{dest}",
        "about_title": "A HGSoft Dynamic Wallpaper Maker-ről",
        "about_text": "<b>HGSoft Dynamic Wallpaper Maker</b><br><br>"
                     "Könnyen használható eszköz KDE Plasma világos/sötét dinamikus háttérkép csomagok készítéséhez.<br><br>"
                     "Fejlesztő: <b>HGSoft</b><br>"
                     "Licenc: MIT"
    }
}

CONFIG_DIR = os.path.expanduser("~/.config/HGSoft")
CONFIG_FILE = os.path.join(CONFIG_DIR, "DynamicWallpaperMaker.json")


def load_language_preference():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("language", "en")
        except Exception:
            pass
    return "en"


def save_language_preference(lang_code):
    try:
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump({"language": lang_code}, f, indent=4)
    except Exception as e:
        print(f"Error saving config: {e}")