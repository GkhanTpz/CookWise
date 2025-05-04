import json
import random
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QRadioButton, QGroupBox, QMessageBox, QScrollArea
from PyQt6.QtCore import QSize
from ui.styles import get_theme
from ui.icons import get_icon

# Verileri yükle
with open("data/recipes.json", "r", encoding="utf-8") as f:
    recipes = json.load(f)

with open("data/preparations.json", "r", encoding="utf-8") as f:
    preparations = json.load(f)

def get_user_ingredients(input_str):
    return [item.strip().lower() for item in input_str.split(",") if item.strip()]

def score_recipe_match(user_ingredients):
    scored = []
    for dish, data in recipes.items():
        ingredients_lower = [i.lower() for i in data["ingredients"]]
        matched = [u for u in user_ingredients if any(u in ing for ing in ingredients_lower)]
        score = len(matched)
        missing = [ing for ing in ingredients_lower if not any(u in ing for u in user_ingredients)]
        scored.append((dish, score, missing, matched, ingredients_lower))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored

def format_recipe(preparation):
    steps = preparation.split("\n")
    return "\n".join([f"{idx+1}. {step.strip()}" for idx, step in enumerate(steps)])

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

        # Yemek öneri alanı
        self.results_groupbox = QGroupBox("Önerilen Yemekler")
        self.results_layout = QVBoxLayout()
        self.results_groupbox.setLayout(self.results_layout)

        # Scrollable area for results
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.results_groupbox)
        layout.addWidget(scroll_area)

        # Yemek öner butonu
        suggest_button = QPushButton("🍽️ Yemek Öner!", self)
        suggest_button.setIcon(get_icon("chef"))
        suggest_button.setIconSize(QSize(30, 30))  # İkon boyutunu ayarlama
        suggest_button.setStyleSheet(get_theme("light"))  # Tema stilleri burada uygulanıyor
        suggest_button.clicked.connect(self.on_submit)
        layout.addWidget(suggest_button)

        # Tarifi Göster Butonu
        self.show_recipe_button = QPushButton("📖 Tarifi Göster", self)
        self.show_recipe_button.setIcon(get_icon("book"))
        self.show_recipe_button.setIconSize(QSize(30, 30))  # İkon boyutunu ayarlama
        self.show_recipe_button.setStyleSheet(get_theme("light"))  # Tema stilleri burada uygulanıyor
        self.show_recipe_button.setVisible(False)
        self.show_recipe_button.clicked.connect(self.show_selected_recipe)
        layout.addWidget(self.show_recipe_button)

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
        matches = score_recipe_match(user_ingredients)

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
            radio_button.setProperty("dish", dish)  # doğru yemeği takip et
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CookWiseApp()
    window.setStyleSheet(get_theme("light"))  # Burada tema belirleniyor
    window.show()
    sys.exit(app.exec())
