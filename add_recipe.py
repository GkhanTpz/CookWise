import sys
import os
import json
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QTextEdit, QPushButton, QVBoxLayout, QMessageBox)
from ui.styles import get_theme

RECIPES_PATH = os.path.join("data", "recipes.json")
PREPARATIONS_PATH = os.path.join("data", "preparations.json")

class RecipeAdder(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add New Recipe - CookWise")
        self.setGeometry(200, 200, 500, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.name_label = QLabel("🍽️ Dish Name (Required):")
        self.name_input = QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        self.ingredients_label = QLabel("🥕 Ingredients (comma-separated, required):")
        self.ingredients_input = QLineEdit()
        layout.addWidget(self.ingredients_label)
        layout.addWidget(self.ingredients_input)

        self.prep_label = QLabel("📋 Preparation (optional):")
        self.prep_input = QTextEdit()
        layout.addWidget(self.prep_label)
        layout.addWidget(self.prep_input)

        self.submit_btn = QPushButton("✅ Add Recipe")
        self.submit_btn.clicked.connect(self.save_recipe)
        layout.addWidget(self.submit_btn)

        self.setLayout(layout)
        self.setStyleSheet(get_theme("light"))

    def save_recipe(self):
        name = self.name_input.text().strip()
        ingredients = [i.strip() for i in self.ingredients_input.text().split(",") if i.strip()]
        preparation = self.prep_input.toPlainText().strip()

        if not name or not ingredients:
            QMessageBox.warning(self, "Error", "Dish name and ingredients are required!")
            return

        recipes = {}
        if os.path.exists(RECIPES_PATH):
            with open(RECIPES_PATH, "r", encoding="utf-8") as f:
                recipes = json.load(f)

        preparations = {}
        if os.path.exists(PREPARATIONS_PATH):
            with open(PREPARATIONS_PATH, "r", encoding="utf-8") as f:
                preparations = json.load(f)

        # Güncelleme / ekleme
        recipes[name] = {"ingredients": ingredients}
        if preparation:
            preparations[name] = preparation

        with open(RECIPES_PATH, "w", encoding="utf-8") as f:
            json.dump(recipes, f, indent=4, ensure_ascii=False)

        with open(PREPARATIONS_PATH, "w", encoding="utf-8") as f:
            json.dump(preparations, f, indent=4, ensure_ascii=False)

        QMessageBox.information(self, "Success", f"'{name}' has been added successfully!")
        self.name_input.clear()
        self.ingredients_input.clear()
        self.prep_input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RecipeAdder()
    window.show()
    sys.exit(app.exec())
