# HGSoft Dynamic Wallpaper Maker

[Magyar leírás](#magyar) | [English Description](#english)

---

<a name="magyar"></a>
## 🇭🇺 Magyar

**HGSoft Dynamic Wallpaper Maker** egy könnyű, letisztult PySide6 (Qt6) alapú grafikus alkalmazás KDE Plasma felhasználók számára. Segítségével másodpercek alatt készíthetsz világos és sötét képekből álló, a KDE Plasma által natívan támogatott dinamikus háttérkép-csomagokat.

### 🌟 Főbb jellemzők
* **KDE Plasma integráció:** Szabványos KPackageStructure és metadata.json struktúrát generál a ~/.local/share/wallpapers/ könyvtárba.
* **Tökéletes előnézeti kép:** Automatikusan legyártja a screenshot.png fájlt, így a KDE Rendszerbeállításokban a háttérkép-választó rácsban tiszta, skálázott miniatűr jelenik meg.
* **Kétnyelvű felület:** Angol és magyar nyelv támogatása azonnali váltási lehetőséggel és beállítás-mentéssel (~/.config/HGSoft/DynamicWallpaperMaker.json).
* **Reszponzív GUI:** Dinamikusan skálázódó kép-előnézet az ablak átméretezésekor, és automatikus mező-nullázás sikeres generálás után.
* **Disztribúció-független telepítő:** Automatikusan felismeri a csomagkezelőt (pacman, dnf, apt, zypper), és telepíti a szükséges Qt6/PySide6 függőségeket.

---

### 🚀 Telepítés

#### 1. Kiadási csomag használatával (.tar.gz)
Töltsd le a legfrissebb kiadást a Releases oldalról, majd futtasd a következő parancsokat a terminálban:

tar -xzvf HGSoft-DynamicWallpaperMaker-1.0.0.tar.gz
cd HGSoft-DynamicWallpaperMaker-1.0.0
./install.sh

#### 2. Telepítés forráskódból
Klónozd a tárolót és futtasd a telepítő szkriptet:

git clone https://github.com/HuNorthMan/HGSoft-DynamicWallpaperMaker.git
cd HGSoft-DynamicWallpaperMaker
chmod +x install.sh
./install.sh

A telepítő a szoftvert a ~/.HGSoft/DynamicWallpaperMaker/ könyvtárba helyezi el, és létrehoz egy indítóikont az alkalmazásmenüben.

---

### 📄 Licenc
Ez a projekt az MIT licenc alatt érhető el.

---

<a name="english"></a>
## 🇬🇧 English

**HGSoft Dynamic Wallpaper Maker** is a lightweight, clean PySide6 (Qt6) GUI application built for KDE Plasma users. It allows you to create native KDE Plasma light/dark dynamic wallpaper packages in seconds.

### 🌟 Key Features
* **Native KDE Plasma Integration:** Generates standard KPackageStructure wallpaper packages with metadata.json directly into ~/.local/share/wallpapers/.
* **Perfect Thumbnail Preview:** Automatically generates a screenshot.png file, ensuring a crisp and properly scaled preview in the KDE System Settings wallpaper picker grid.
* **Multi-language Support:** Supports English and Hungarian with instant language switching and preference saving (~/.config/HGSoft/DynamicWallpaperMaker.json).
* **Responsive GUI:** Dynamic image preview scaling on window resize and automatic field reset after successful package generation.
* **Distro-Agnostic Installer:** Automatically detects package managers (pacman, dnf, apt, zypper) and installs required Qt6/PySide6 dependencies.

---

### 🚀 Installation

#### 1. Using Release Archive (.tar.gz)
Download the latest archive from the Releases page, then run the following commands in your terminal:

tar -xzvf HGSoft-DynamicWallpaperMaker-1.0.0.tar.gz
cd HGSoft-DynamicWallpaperMaker-1.0.0
./install.sh

#### 2. Installing from Source
Clone the repository and run the installer script:

git clone https://github.com/HuNorthMan/HGSoft-DynamicWallpaperMaker.git
cd HGSoft-DynamicWallpaperMaker
chmod +x install.sh
./install.sh

The installer deploys the application to ~/.HGSoft/DynamicWallpaperMaker/ and registers a desktop entry in your application menu.

---

### 📄 License
This project is licensed under the MIT License.
