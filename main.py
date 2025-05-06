import sys
import random
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton,
    QRadioButton, QGroupBox, QMessageBox, QScrollArea
)
from PyQt6.QtCore import QSize

# Tema ve ikonlar için yardımcı modüller
from ui.styles import get_theme
from ui.icons import get_icon
from add_recipe import RecipeAdder

# Tarif işlemleri için yardımcı fonksiyonlar
from utils.helpers import load_data, get_user_ingredients, score_recipe_match, filter_matches, format_recipe

# Tarif ve yapılış bilgilerini yükle
recipes, preparations = load_data()

class CookWiseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CookWise - Akıllı Yemek Öneri Sistemi")
        self.setGeometry(100, 100, 700, 550)
        self.init_ui()

    # Arayüz bileşenlerini oluştur
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

        # Sonuçların gösterileceği grup kutusu
        self.results_groupbox = QGroupBox("Önerilen Yemekler")
        self.results_layout = QVBoxLayout()
        self.results_groupbox.setLayout(self.results_layout)

        # Sonuçları kaydırılabilir hale getir
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.results_groupbox)
        layout.addWidget(scroll_area)

        # "Yemek Öner" butonu
        suggest_button = QPushButton("🍽️ Yemek Öner!", self)
        suggest_button.setIcon(get_icon("chef"))
        suggest_button.setIconSize(QSize(30, 30))
        suggest_button.setStyleSheet(get_theme("light"))
        suggest_button.clicked.connect(self.on_submit)
        layout.addWidget(suggest_button)

        # "Tarifi Göster" butonu (başta gizli)
        self.show_recipe_button = QPushButton("📖 Tarifi Göster", self)
        self.show_recipe_button.setIcon(get_icon("book"))
        self.show_recipe_button.setIconSize(QSize(30, 30))
        self.show_recipe_button.setStyleSheet(get_theme("light"))
        self.show_recipe_button.setVisible(False)
        self.show_recipe_button.clicked.connect(self.show_selected_recipe)
        layout.addWidget(self.show_recipe_button)

        # Yeni tarif ekleme butonu
        add_recipe_button = QPushButton("📝 Add New Recipe", self)
        add_recipe_button.setStyleSheet("font-size: 14px; padding: 8px;")
        add_recipe_button.clicked.connect(self.open_add_recipe_window)
        layout.addWidget(add_recipe_button)

        # Alt bilgi
        footer = QLabel("© 2025 CookWise AI")
        footer.setStyleSheet("font-size: 10px; color: gray;")
        layout.addWidget(footer)

        self.setLayout(layout)

    # "Yemek Öner" butonuna basıldığında çalışır
    def on_submit(self):
        user_input = self.input_entry.text().strip()

        # Önceki sonuçları temizle
        while self.results_layout.count():
            child = self.results_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if not user_input:
            QMessageBox.warning(self, "Malzeme girmediniz", "Lütfen en az bir malzeme girin.")
            return

        user_ingredients = get_user_ingredients(user_input)

        # Yalnızca "su", "tuz" gibi geçersiz malzeme girildiyse uyar
        if len(user_ingredients) == 0:
            QMessageBox.warning(self, "Yetersiz Malzeme", "Geçerli malzeme girmediniz. 'su' ve 'tuz' gibi malzemeler tek başına geçersizdir.")
            return

        # Eşleşmeleri bul ve filtrele
        matches = score_recipe_match(user_ingredients, recipes)
        filtered = filter_matches(user_ingredients, matches)

        # Hiç eşleşme yoksa rastgele öner
        if not filtered:
            QMessageBox.information(self, "Yemek bulunamadı", "Girilen kriterlere uygun yemek bulunamadı. Rastgele bir yemek öneriliyor.")
            dish = random.choice(list(recipes.keys()))
            self.show_recipe(dish, missing=[])
            return

        # En fazla 5 sonucu kullanıcıya sun
        for dish, score, missing, matched, total in filtered[:5]:
            display = f"{dish} ({score}/{len(total)} eşleşme)"
            if missing:
                display += f" | Eksik: {', '.join(missing)}"
            radio_button = QRadioButton(display, self)
            radio_button.setStyleSheet("font-size: 16px; padding: 5px;")
            radio_button.setProperty("dish", dish)
            self.results_layout.addWidget(radio_button)

        self.show_recipe_button.setVisible(True)

    # Seçilen yemeğin tarifini göster
    def show_recipe(self, dish, missing=None):
        prep = preparations.get(dish, "Tarif bulunamadı.")
        recipe_text = format_recipe(prep)
        recipe_window = QMessageBox(self)
        recipe_window.setWindowTitle(f"{dish} Tarifi")
        recipe_window.setText(recipe_text)
        if missing:
            recipe_window.setInformativeText(f"⚠️ Eksik malzemeler: {', '.join(missing)}")
        recipe_window.exec()

    # Seçili yemeğin tarifini gösteren butonun işlevi
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

    # Yeni tarif ekleme penceresini açar
    def open_add_recipe_window(self):
        self.recipe_adder = RecipeAdder(on_recipe_added=self.update_recipes)
        self.recipe_adder.show()

    # Yeni tarif eklendiğinde verileri yeniden yükler
    def update_recipes(self):
        global recipes, preparations
        recipes, preparations = load_data()
        QMessageBox.information(self, "Başarı", "Yeni yemek başarıyla eklendi ve veri güncellendi!")

# Uygulama başlatılır
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CookWiseApp()
    window.setStyleSheet(get_theme("light"))
    window.show()
    sys.exit(app.exec())
