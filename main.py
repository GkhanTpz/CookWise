import sys
import random
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton,
    QRadioButton, QGroupBox, QMessageBox, QScrollArea
)
from PyQt6.QtCore import QSize

from ui.styles import get_theme
from ui.icons import get_icon
from add_recipe import RecipeAdder

# helpers.py'den gerekli fonksiyonları import ediyoruz
from utils.helpers import load_data, get_user_ingredients, score_recipe_match, format_recipe

# Verileri yükle
recipes, preparations = load_data()

class CookWiseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CookWise - Akıllı Yemek Öneri Sistemi")
        self.setGeometry(100, 100, 700, 550)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Başlık
        title = QLabel("CookWise - Akıllı Yemek Öneri Sistemi")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        # Malzeme giriş alanı
        self.input_entry = QLineEdit(self)
        self.input_entry.setPlaceholderText("Elinizdeki malzemeleri virgülle ayırarak girin:")
        self.input_entry.setStyleSheet("font-size: 16px; padding: 10px;")
        layout.addWidget(self.input_entry)

        # Öneri kutusu (scrollable)
        self.results_groupbox = QGroupBox("Önerilen Yemekler")
        self.results_layout = QVBoxLayout()
        self.results_groupbox.setLayout(self.results_layout)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.results_groupbox)
        layout.addWidget(scroll_area)

        # Yemek öner butonu
        suggest_button = QPushButton("🍽️ Yemek Öner!", self)
        suggest_button.setIcon(get_icon("chef"))
        suggest_button.setIconSize(QSize(30, 30))
        suggest_button.setStyleSheet(get_theme("light"))
        suggest_button.clicked.connect(self.on_submit)
        layout.addWidget(suggest_button)

        # Tarifi Göster Butonu
        self.show_recipe_button = QPushButton("📖 Tarifi Göster", self)
        self.show_recipe_button.setIcon(get_icon("book"))
        self.show_recipe_button.setIconSize(QSize(30, 30))
        self.show_recipe_button.setStyleSheet(get_theme("light"))
        self.show_recipe_button.setVisible(False)
        self.show_recipe_button.clicked.connect(self.show_selected_recipe)
        layout.addWidget(self.show_recipe_button)

        # Yeni Tarif Ekle Butonu
        add_recipe_button = QPushButton("📝 Add New Recipe", self)
        add_recipe_button.setStyleSheet("font-size: 14px; padding: 8px;")
        add_recipe_button.clicked.connect(self.open_add_recipe_window)
        layout.addWidget(add_recipe_button)

        # Footer
        footer = QLabel("© 2025 CookWise AI")
        footer.setStyleSheet("font-size: 10px; color: gray;")
        layout.addWidget(footer)

        self.setLayout(layout)

    def on_submit(self):
        user_input = self.input_entry.text().strip()

        # Önceki önerileri temizle
        while self.results_layout.count():
            child = self.results_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if not user_input:
            QMessageBox.warning(self, "Malzeme girmediniz", "Lütfen en az bir malzeme girin.")
            return

        user_ingredients = get_user_ingredients(user_input)
        matches = score_recipe_match(user_ingredients, recipes)

        if not matches or matches[0][1] == 0:
            QMessageBox.information(self, "Yemek bulunamadı", "Uygun bir yemek bulunamadı. Rastgele bir yemek öneriliyor.")
            dish = random.choice(list(recipes.keys()))
            self.show_recipe(dish, missing=[])
            return

        # Eşleşen yemekleri göster
        for dish, score, missing, matched, total in matches[:5]:
            display = f"{dish} ({score}/{len(total)} eşleşme)"
            if missing:
                display += f" | Eksik: {', '.join(missing)}"
            radio_button = QRadioButton(display, self)
            radio_button.setStyleSheet("font-size: 16px; padding: 5px;")
            radio_button.setProperty("dish", dish)
            self.results_layout.addWidget(radio_button)

        self.show_recipe_button.setVisible(True)

    def show_recipe(self, dish, missing=None):
        prep = preparations.get(dish, "Tarif bulunamadı.")
        recipe_text = format_recipe(prep)
        recipe_window = QMessageBox(self)
        recipe_window.setWindowTitle(f"{dish} Tarifi")
        recipe_window.setText(recipe_text)
        if missing:
            recipe_window.setInformativeText(f"⚠️ Eksik malzemeler: {', '.join(missing)}")
        recipe_window.exec()

    def show_selected_recipe(self):
        selected_dish = None
        for i in range(self.results_layout.count()):
            item = self.results_layout.itemAt(i)
            widget = item.widget()
            if isinstance(widget, QRadioButton) and widget.isChecked():
                selected_dish = widget.property("dish")
                break

        if selected_dish:
            self.show_recipe(selected_dish)
        else:
            QMessageBox.warning(self, "Yemek Seçin", "Lütfen bir yemek seçin.")

    def open_add_recipe_window(self):
        self.recipe_adder = RecipeAdder(on_recipe_added=self.update_recipes)
        self.recipe_adder.show()

    def update_recipes(self):
        global recipes, preparations
        recipes, preparations = load_data()
        QMessageBox.information(self, "Başarı", "Yeni yemek başarıyla eklendi ve veri güncellendi!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CookWiseApp()
    window.setStyleSheet(get_theme("light"))
    window.show()
    sys.exit(app.exec())
