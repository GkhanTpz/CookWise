import sys
import os
import json
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QTextEdit, QPushButton, QVBoxLayout, QMessageBox
)
from ui.styles import get_theme

# Tariflerin ve hazırlıkların JSON dosya yolları
RECIPES_PATH = os.path.join("data", "recipes.json")
PREPARATIONS_PATH = os.path.join("data", "preparations.json")


class RecipeAdder(QWidget):
    # Bu sınıf, yeni tarif ekleme işlemini yönetir.
    def __init__(self, on_recipe_added=None):  # ✅ callback parametresi ekleniyor
        super().__init__()
        self.setWindowTitle("Add New Recipe - CookWise")  # Pencere başlığı
        self.setGeometry(200, 200, 500, 400)  # Pencere boyutu ve konumu
        self.on_recipe_added = on_recipe_added  # ✅ callback fonksiyonunu saklar
        self.init_ui()  # UI bileşenlerini başlat

    def init_ui(self):
        layout = QVBoxLayout()

        # Yemek adı için etiket ve giriş alanı
        self.name_label = QLabel("🍽️ Dish Name (Required):")
        self.name_input = QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        # Malzemeler için etiket ve giriş alanı
        self.ingredients_label = QLabel("🥕 Ingredients (comma-separated, required):")
        self.ingredients_input = QLineEdit()
        layout.addWidget(self.ingredients_label)
        layout.addWidget(self.ingredients_input)

        # Tarif için etiket ve giriş alanı (isteğe bağlı)
        self.prep_label = QLabel("📋 Preparation (optional):")
        self.prep_input = QTextEdit()
        layout.addWidget(self.prep_label)
        layout.addWidget(self.prep_input)

        # Tarif ekleme butonu
        self.submit_btn = QPushButton("✅ Add Recipe")
        self.submit_btn.clicked.connect(self.save_recipe)  # Butona tıklanması ile save_recipe fonksiyonu çağrılır
        layout.addWidget(self.submit_btn)

        self.setLayout(layout)  # Layout'u pencereye ekler
        self.setStyleSheet(get_theme("light"))  # UI tema stili

    def save_recipe(self):
        # Kullanıcının girdiği bilgileri al
        name = self.name_input.text().strip()  # Yemek adı
        ingredients = [i.strip() for i in self.ingredients_input.text().split(",") if i.strip()]  # Malzemeler
        preparation = self.prep_input.toPlainText().strip()  # Hazırlık tarifi

        # Yemek adı ve malzeme girilmemişse uyarı ver
        if not name or not ingredients:
            QMessageBox.warning(self, "Error", "Dish name and ingredients are required!")
            return

        # Var olan tarifleri ve hazırlıkları yükle
        recipes = {}
        if os.path.exists(RECIPES_PATH):
            with open(RECIPES_PATH, "r", encoding="utf-8") as f:
                recipes = json.load(f)

        preparations = {}
        if os.path.exists(PREPARATIONS_PATH):
            with open(PREPARATIONS_PATH, "r", encoding="utf-8") as f:
                preparations = json.load(f)

        # Yeni tarif verilerini ekle
        recipes[name] = {"ingredients": ingredients}
        if preparation:
            preparations[name] = preparation

        # Yeni tarifleri JSON dosyasına kaydet
        with open(RECIPES_PATH, "w", encoding="utf-8") as f:
            json.dump(recipes, f, indent=4, ensure_ascii=False)

        with open(PREPARATIONS_PATH, "w", encoding="utf-8") as f:
            json.dump(preparations, f, indent=4, ensure_ascii=False)

        # Başarı mesajı göster
        QMessageBox.information(self, "Success", f"'{name}' has been added successfully!")

        # Giriş alanlarını temizle
        self.name_input.clear()
        self.ingredients_input.clear()
        self.prep_input.clear()

        # Eğer callback fonksiyonu verilmişse, çalıştır
        if self.on_recipe_added:
            self.on_recipe_added()  # ✅ callback fonksiyonunu çağır
