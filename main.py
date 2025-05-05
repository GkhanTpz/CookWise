import sys
import random
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton,
    QRadioButton, QGroupBox, QMessageBox, QScrollArea
)
from PyQt6.QtCore import QSize

from ui.styles import get_theme  # UI tema stilini yükler
from ui.icons import get_icon  # İkonları yükler
from add_recipe import RecipeAdder  # Yeni tarif ekleme penceresini içerir

# helpers.py'den gerekli fonksiyonları import ediyoruz
from utils.helpers import load_data, get_user_ingredients, score_recipe_match, format_recipe

# Verileri yükle
recipes, preparations = load_data()  # Tarife ve hazırlıklara ait verileri JSON dosyasından yükler

class CookWiseApp(QWidget):
    # Uygulama ana penceresi
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CookWise - Akıllı Yemek Öneri Sistemi")  # Pencere başlığı
        self.setGeometry(100, 100, 700, 550)  # Pencere boyutları
        self.init_ui()  # UI bileşenlerini başlat

    def init_ui(self):
        layout = QVBoxLayout()

        # Başlık
        title = QLabel("CookWise - Akıllı Yemek Öneri Sistemi")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")  # Başlık stilini ayarlama
        layout.addWidget(title)

        # Malzeme giriş alanı
        self.input_entry = QLineEdit(self)
        self.input_entry.setPlaceholderText("Elinizdeki malzemeleri virgülle ayırarak girin:")  # Placeholder text
        self.input_entry.setStyleSheet("font-size: 16px; padding: 10px;")  # Stil ayarları
        layout.addWidget(self.input_entry)

        # Öneri kutusu (scrollable)
        self.results_groupbox = QGroupBox("Önerilen Yemekler")
        self.results_layout = QVBoxLayout()
        self.results_groupbox.setLayout(self.results_layout)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.results_groupbox)  # Öneriler scrollable yapılır
        layout.addWidget(scroll_area)

        # Yemek öner butonu
        suggest_button = QPushButton("🍽️ Yemek Öner!", self)
        suggest_button.setIcon(get_icon("chef"))
        suggest_button.setIconSize(QSize(30, 30))  # İkon boyutu
        suggest_button.setStyleSheet(get_theme("light"))  # UI tema stili
        suggest_button.clicked.connect(self.on_submit)  # Tıklama olayına bağlanır
        layout.addWidget(suggest_button)

        # Tarifi Göster Butonu
        self.show_recipe_button = QPushButton("📖 Tarifi Göster", self)
        self.show_recipe_button.setIcon(get_icon("book"))
        self.show_recipe_button.setIconSize(QSize(30, 30))  # İkon boyutu
        self.show_recipe_button.setStyleSheet(get_theme("light"))  # Tema stili
        self.show_recipe_button.setVisible(False)  # Başlangıçta gizli
        self.show_recipe_button.clicked.connect(self.show_selected_recipe)  # Tıklama olayına bağlanır
        layout.addWidget(self.show_recipe_button)

        # Yeni Tarif Ekle Butonu
        add_recipe_button = QPushButton("📝 Add New Recipe", self)
        add_recipe_button.setStyleSheet("font-size: 14px; padding: 8px;")  # Buton stilini ayarlama
        add_recipe_button.clicked.connect(self.open_add_recipe_window)  # Butona tıklanması ile yeni tarif penceresini aç
        layout.addWidget(add_recipe_button)

        # Footer
        footer = QLabel("© 2025 CookWise AI")
        footer.setStyleSheet("font-size: 10px; color: gray;")  # Footer stilini ayarlama
        layout.addWidget(footer)

        self.setLayout(layout)  # Layout'u pencereye ekle

    def on_submit(self):
        user_input = self.input_entry.text().strip()  # Kullanıcıdan alınan malzeme girişi

        # Önceki önerileri temizle
        while self.results_layout.count():
            child = self.results_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Eğer kullanıcı herhangi bir malzeme girmezse uyarı ver
        if not user_input:
            QMessageBox.warning(self, "Malzeme girmediniz", "Lütfen en az bir malzeme girin.")
            return

        # Kullanıcı malzemelerine göre yemekleri eşleştir
        user_ingredients = get_user_ingredients(user_input)
        matches = score_recipe_match(user_ingredients, recipes)

        # Eşleşen yemek bulunmazsa, rastgele bir yemek öner
        if not matches or matches[0][1] == 0:
            QMessageBox.information(self, "Yemek bulunamadı", "Uygun bir yemek bulunamadı. Rastgele bir yemek öneriliyor.")
            dish = random.choice(list(recipes.keys()))
            self.show_recipe(dish, missing=[])  # Rastgele yemek göster
            return

        # Eşleşen yemekleri ekrana yazdır
        for dish, score, missing, matched, total in matches[:5]:  # En iyi 5 yemek önerisi
            display = f"{dish} ({score}/{len(total)} eşleşme)"
            if missing:
                display += f" | Eksik: {', '.join(missing)}"  # Eksik malzemeler varsa ekle
            radio_button = QRadioButton(display, self)  # Seçilebilir radyo butonu ekle
            radio_button.setStyleSheet("font-size: 16px; padding: 5px;")
            radio_button.setProperty("dish", dish)  # Yemek ismini radyo butonuna sakla
            self.results_layout.addWidget(radio_button)

        # Tarifi göster butonunu görünür hale getir
        self.show_recipe_button.setVisible(True)

    def show_recipe(self, dish, missing=None):
        # Tarifin adım adım gösterilmesi
        prep = preparations.get(dish, "Tarif bulunamadı.")
        recipe_text = format_recipe(prep)  # Tarif formatını düzenle
        recipe_window = QMessageBox(self)
        recipe_window.setWindowTitle(f"{dish} Tarifi")  # Başlık
        recipe_window.setText(recipe_text)  # Tarifi pencereye yerleştir
        if missing:
            recipe_window.setInformativeText(f"⚠️ Eksik malzemeler: {', '.join(missing)}")  # Eksik malzemeleri ekle
        recipe_window.exec()  # Pencereyi göster

    def show_selected_recipe(self):
        selected_dish = None
        # Kullanıcı seçili yemek bilgisini al
        for i in range(self.results_layout.count()):
            item = self.results_layout.itemAt(i)
            widget = item.widget()
            if isinstance(widget, QRadioButton) and widget.isChecked():
                selected_dish = widget.property("dish")
                break

        # Seçilen yemek varsa tarifini göster, yoksa uyarı ver
        if selected_dish:
            self.show_recipe(selected_dish)
        else:
            QMessageBox.warning(self, "Yemek Seçin", "Lütfen bir yemek seçin.")

    def open_add_recipe_window(self):
        # Yeni tarif ekleme penceresini aç
        self.recipe_adder = RecipeAdder(on_recipe_added=self.update_recipes)
        self.recipe_adder.show()

    def update_recipes(self):
        global recipes, preparations
        # Yeni tarif ekledikten sonra verileri tekrar yükle
        recipes, preparations = load_data()
        QMessageBox.information(self, "Başarı", "Yeni yemek başarıyla eklendi ve veri güncellendi!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CookWiseApp()  # Uygulama penceresini oluştur
    window.setStyleSheet(get_theme("light"))  # Tema stilini ayarla
    window.show()  # Pencereyi göster
    sys.exit(app.exec())  # Uygulamayı çalıştır