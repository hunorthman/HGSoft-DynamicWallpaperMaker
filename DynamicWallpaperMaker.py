import sys
import os
import json
import shutil
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QGroupBox,
    QToolButton, QMenu, QSizePolicy
)
from PySide6.QtCore import Qt, QStandardPaths
from PySide6.QtGui import QPixmap, QIcon, QAction, QActionGroup, QResizeEvent

from translations import TRANSLATIONS, load_language_preference, save_language_preference


class DynamicWallpaperApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_lang = load_language_preference()
        self.light_img_path = ""
        self.dark_img_path = ""

        self.setMinimumSize(640, 500)
        
        # Window Icon beállítása (SVG vagy PNG)
        icon_path = os.path.join(os.path.dirname(__file__), "icon.svg")
        if not os.path.exists(icon_path):
            icon_path = os.path.join(os.path.dirname(__file__), "icon.png")

        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.init_ui()
        self.retranslate_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Top Bar (Csomag neve + Fogaskerék menü)
        top_bar_layout = QHBoxLayout()

        self.name_label = QLabel()
        self.name_input = QLineEdit()
        top_bar_layout.addWidget(self.name_label)
        top_bar_layout.addWidget(self.name_input)

        # Fogaskerék Gomb
        self.settings_btn = QToolButton()
        icon = QIcon.fromTheme("preferences-system")
        if not icon.isNull():
            self.settings_btn.setIcon(icon)
        else:
            self.settings_btn.setText("⚙")

        self.settings_btn.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.build_settings_menu()
        top_bar_layout.addWidget(self.settings_btn)

        main_layout.addLayout(top_bar_layout)

        # Képválasztó szekció
        images_layout = QHBoxLayout()

        # Világos kép box
        self.light_box = QGroupBox()
        light_box_layout = QVBoxLayout(self.light_box)
        
        self.light_preview = QLabel()
        self.light_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.light_preview.setStyleSheet("border: 2px dashed #555; background-color: rgba(0,0,0,0.1);")
        self.light_preview.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.light_preview.setMinimumHeight(180)

        self.btn_light = QPushButton()
        self.btn_light.clicked.connect(self.select_light_image)
        
        light_box_layout.addWidget(self.light_preview)
        light_box_layout.addWidget(self.btn_light)
        images_layout.addWidget(self.light_box)

        # Sötét kép box
        self.dark_box = QGroupBox()
        dark_box_layout = QVBoxLayout(self.dark_box)
        
        self.dark_preview = QLabel()
        self.dark_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dark_preview.setStyleSheet("border: 2px dashed #555; background-color: rgba(0,0,0,0.1);")
        self.dark_preview.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.dark_preview.setMinimumHeight(180)

        self.btn_dark = QPushButton()
        self.btn_dark.clicked.connect(self.select_dark_image)
        
        dark_box_layout.addWidget(self.dark_preview)
        dark_box_layout.addWidget(self.btn_dark)
        images_layout.addWidget(self.dark_box)

        main_layout.addLayout(images_layout)

        # Generálás gomb
        self.btn_generate = QPushButton()
        self.btn_generate.setStyleSheet("font-weight: bold; padding: 12px; font-size: 14px;")
        self.btn_generate.clicked.connect(self.generate_wallpaper_package)
        main_layout.addWidget(self.btn_generate)

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        # Ablak átméretezésekor újraigazítjuk az előnézeti képeket
        if self.light_img_path:
            self.update_preview(self.light_preview, self.light_img_path)
        if self.dark_img_path:
            self.update_preview(self.dark_preview, self.dark_img_path)

    def build_settings_menu(self):
        menu = QMenu(self)

        self.lang_menu = QMenu(menu)
        self.lang_action_group = QActionGroup(self)
        self.lang_action_group.setExclusive(True)

        self.act_en = QAction("English", self, checkable=True)
        self.act_hu = QAction("Magyar", self, checkable=True)

        if self.current_lang == "hu":
            self.act_hu.setChecked(True)
        else:
            self.act_en.setChecked(True)

        self.act_en.triggered.connect(lambda: self.change_language("en"))
        self.act_hu.triggered.connect(lambda: self.change_language("hu"))

        self.lang_action_group.addAction(self.act_en)
        self.lang_action_group.addAction(self.act_hu)

        self.lang_menu.addAction(self.act_en)
        self.lang_menu.addAction(self.act_hu)

        menu.addMenu(self.lang_menu)
        menu.addSeparator()

        self.act_about = QAction(self)
        self.act_about.triggered.connect(self.show_about_dialog)
        menu.addAction(self.act_about)

        self.settings_btn.setMenu(menu)

    def change_language(self, lang_code):
        self.current_lang = lang_code
        save_language_preference(lang_code)
        self.retranslate_ui()

    def retranslate_ui(self):
        t = TRANSLATIONS.get(self.current_lang, TRANSLATIONS["en"])

        self.setWindowTitle(t["title"])
        self.name_label.setText(t["pkg_name"])
        self.name_input.setPlaceholderText(t["pkg_placeholder"])

        self.light_box.setTitle(t["light_box"])
        self.dark_box.setTitle(t["dark_box"])

        if not self.light_img_path:
            self.light_preview.setText(t["no_image"])
        if not self.dark_img_path:
            self.dark_preview.setText(t["no_image"])

        self.btn_light.setText(t["browse"])
        self.btn_dark.setText(t["browse"])
        self.btn_generate.setText(t["generate"])

        self.lang_menu.setTitle(t["language"])
        self.act_about.setText(t["about"])

    def get_pictures_dir(self):
        """Visszaadja a rendszer alapértelmezett Képek mappájának útvonalát."""
        pictures_dirs = QStandardPaths.standardLocations(QStandardPaths.StandardLocation.PicturesLocation)
        if pictures_dirs:
            return pictures_dirs[0]
        return os.path.expanduser("~")

    def select_light_image(self):
        t = TRANSLATIONS[self.current_lang]
        default_dir = self.get_pictures_dir()
        file_path, _ = QFileDialog.getOpenFileName(
            self, t["light_box"], default_dir, "Images (*.jpg *.jpeg *.png)"
        )
        if file_path:
            self.light_img_path = file_path
            self.update_preview(self.light_preview, file_path)

    def select_dark_image(self):
        t = TRANSLATIONS[self.current_lang]
        default_dir = self.get_pictures_dir()
        file_path, _ = QFileDialog.getOpenFileName(
            self, t["dark_box"], default_dir, "Images (*.jpg *.jpeg *.png)"
        )
        if file_path:
            self.dark_img_path = file_path
            self.update_preview(self.dark_preview, file_path)

    def update_preview(self, label: QLabel, file_path: str):
        pixmap = QPixmap(file_path)
        if not pixmap.isNull():
            target_width = max(label.width() - 10, 100)
            target_height = max(label.height() - 10, 100)
            scaled = pixmap.scaled(
                target_width, 
                target_height, 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            )
            label.setPixmap(scaled)

    def clear_fields(self):
        """Minden opciót alaphelyzetbe állít a sikeres mentés után."""
        t = TRANSLATIONS[self.current_lang]
        self.name_input.clear()
        self.light_img_path = ""
        self.dark_img_path = ""
        self.light_preview.clear()
        self.dark_preview.clear()
        self.light_preview.setText(t["no_image"])
        self.dark_preview.setText(t["no_image"])

    def show_about_dialog(self):
        t = TRANSLATIONS[self.current_lang]
        
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(t["about_title"])
        msg_box.setText(t["about_text"])

        icon_path = os.path.join(os.path.dirname(__file__), "icon.svg")
        if not os.path.exists(icon_path):
            icon_path = os.path.join(os.path.dirname(__file__), "icon.png")

        if os.path.exists(icon_path):
            msg_box.setIconPixmap(QPixmap(icon_path).scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

        msg_box.exec()

    def generate_wallpaper_package(self):
        t = TRANSLATIONS[self.current_lang]
        pkg_name = self.name_input.text().strip()

        if not pkg_name:
            QMessageBox.warning(self, t["err_title"], t["err_no_name"])
            return

        if not self.light_img_path or not self.dark_img_path:
            QMessageBox.warning(self, t["err_title"], t["err_no_images"])
            return

        home_dir = os.path.expanduser("~")
        dest_dir = os.path.join(home_dir, ".local", "share", "wallpapers", pkg_name)

        images_dir = os.path.join(dest_dir, "contents", "images")
        images_dark_dir = os.path.join(dest_dir, "contents", "images_dark")
        contents_dir = os.path.join(dest_dir, "contents")

        try:
            os.makedirs(images_dir, exist_ok=True)
            os.makedirs(images_dark_dir, exist_ok=True)

            light_ext = os.path.splitext(self.light_img_path)[1].lower() or ".jpg"
            dark_ext = os.path.splitext(self.dark_img_path)[1].lower() or ".jpg"

            light_dest = os.path.join(images_dir, f"1920x1080{light_ext}")
            dark_dest = os.path.join(images_dark_dir, f"1920x1080{dark_ext}")
            
            shutil.copy(self.light_img_path, light_dest)
            shutil.copy(self.dark_img_path, dark_dest)

            # Előnézeti kép (screenshot.png) generálása a KDE Plasma számára
            screenshot_path = os.path.join(contents_dir, "screenshot.png")
            light_pixmap = QPixmap(self.light_img_path)
            if not light_pixmap.isNull():
                scaled_preview = light_pixmap.scaled(400, 225, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
                scaled_preview.save(screenshot_path, "PNG")

            user_name = os.environ.get("USER", "HGSoft")
            metadata = {
                "KPlugin": {
                    "Authors": [{"Name": user_name}],
                    "Id": pkg_name,
                    "License": "CC-BY-SA-4.0",
                    "Name": pkg_name
                },
                "KPackageStructure": "KDE/Wallpaper"
            }

            metadata_path = os.path.join(dest_dir, "metadata.json")
            with open(metadata_path, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=4)

            QMessageBox.information(
                self, 
                t["success_title"], 
                t["success_msg"].format(dest=dest_dir)
            )

            self.clear_fields()

        except Exception as e:
            QMessageBox.critical(self, t["err_title"], f"{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DynamicWallpaperApp()
    window.show()
    sys.exit(app.exec())