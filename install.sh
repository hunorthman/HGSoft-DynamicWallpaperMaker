#!/usr/bin/env bash

APP_NAME="DynamicWallpaperMaker"
INSTALL_DIR="$HOME/.HGSoft/$APP_NAME"
DESKTOP_FILE="$HOME/.local/share/applications/hgsoft-dynamic-wallpaper-maker.desktop"

echo "=========================================="
echo "   HGSoft - $APP_NAME Telepítő"
echo "=========================================="
echo ""

# 1. Csomagkezelő felismerése és függőségek telepítése
detect_and_install_deps() {
    echo "-> Csomagkezelő és függőségek ellenőrzése..."

    if command -v pacman &> /dev/null; then
        echo "   Észlelt csomagkezelő: pacman (Arch / Manjaro / EndeavourOS)"
        sudo pacman -S --needed --noconfirm python pyside6 qt6-base qt6-svg
    elif command -v dnf &> /dev/null; then
        echo "   Észlelt csomagkezelő: dnf (Fedora / RHEL / Nobara)"
        sudo dnf install -y python3 python3-pyside6 qt6-qtbase qt6-qtsvg
    elif command -v apt-get &> /dev/null; then
        echo "   Észlelt csomagkezelő: apt (Ubuntu / Debian / Mint)"
        sudo apt-get update
        sudo apt-get install -y python3 python3-pyside6 python3-pyqt6.qtsvg qt6-base-dev
    elif command -v zypper &> /dev/null; then
        echo "   Észlelt csomagkezelő: zypper (openSUSE)"
        sudo zypper install -y python3 python3-pyside6 qt6-base
    else
        echo "⚠️ Nem sikerült támogatott csomagkezelőt (pacman, dnf, apt, zypper) azonosítani."
        echo "Kérlek győződj meg róla, hogy a Python 3 és a PySide6 manuálisan telepítve van."
    fi
}

detect_and_install_deps

# 2. Telepítési mappa előkészítése
echo ""
echo "-> Telepítési könyvtár előkészítése ($INSTALL_DIR)..."
mkdir -p "$INSTALL_DIR"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# 3. Fájlok másolása
echo "-> Fájlok telepítése..."
cp "$SCRIPT_DIR/app.py" "$INSTALL_DIR/" 2>/dev/null || cp "$SCRIPT_DIR/DynamicWallpaperMaker.py" "$INSTALL_DIR/app.py"
cp "$SCRIPT_DIR/translations.py" "$INSTALL_DIR/"
cp "$SCRIPT_DIR/icon.svg" "$INSTALL_DIR/" 2>/dev/null || cp "$SCRIPT_DIR/icon.png" "$INSTALL_DIR/"

# 4. Egyszerű indító wrapper szkript generálása (VENV NÉLKÜL)
echo "-> Indító szkript (launch.sh) elkészítése..."
cat << EOF > "$INSTALL_DIR/launch.sh"
#!/usr/bin/env bash
DIR="\$( cd "\$( dirname "\${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
python3 "\$DIR/app.py" "\$@"
EOF

chmod +x "$INSTALL_DIR/launch.sh"

# 5. Asztali indítóikon (.desktop) létrehozása
echo "-> Menübejegyzés (.desktop) létrehozása..."
mkdir -p "$HOME/.local/share/applications"

ICON_PATH="$INSTALL_DIR/icon.svg"
if [ ! -f "$ICON_PATH" ]; then
    ICON_PATH="$INSTALL_DIR/icon.png"
fi

cat << EOF > "$DESKTOP_FILE"
[Desktop Entry]
Type=Application
Name=HGSoft Dynamic Wallpaper Maker
Comment=KDE Plasma Dynamic Wallpaper Creator
Exec=$INSTALL_DIR/launch.sh
Icon=$ICON_PATH
Terminal=false
Categories=Utility;Graphics;Settings;
EOF

chmod +x "$DESKTOP_FILE"

echo ""
echo "=========================================="
echo "   Sikeres telepítés!"
echo "=========================================="
echo "A szoftvert elindíthatod az alkalmazásmenüből (HGSoft Dynamic Wallpaper Maker),"
echo "vagy közvetlenül a terminálból: $INSTALL_DIR/launch.sh"
