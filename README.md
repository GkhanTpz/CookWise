# 🍽️ CookWise - Smart Meal Recommendation System

**CookWise** is a Python application that provides **smart meal suggestions** based on the **ingredients you already have**. When users enter their available ingredients, the app recommends the most suitable meals and offers easy access to recipe details. 🍳🥘

---

## 🚀 Features

* **Ingredient-Based Meal Suggestions**: Users input the ingredients they have, and the system suggests meals based on those ingredients. 🥒🍅
* **Recipe Details**: Users can view detailed recipes for the suggested meals. 📖🍴
* **Missing Ingredients**: If there are any missing ingredients in the suggested recipes, the system highlights them. ❌🍞
* **Simple and User-Friendly Interface**: A modern and user-friendly interface built with PyQt6. 💻🎨

---

## 🛠️ Usage

### Requirements

* **Python 3.8+** 🐍
* **PyQt6** (for the GUI) 🎨
* Meal recipes and ingredient lists in **JSON format** 🍲📜

### Installation

1. **Clone the project to your local machine**:

   ```bash
   git clone https://github.com/username/CookWise.git
   cd CookWise
   ```

2. **Create a virtual environment and install dependencies**:

   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Mac/Linux
   pip install -r requirements.txt
   ```

3. **Place the database files** (`recipes.json` and `preparations.json`) **inside the `data/` folder**.

4. **Run the application**:

   ```bash
   python main.py
   ```

---

## 📁 Project Structure

Here’s how the project is organized:

```
CookWise/
│
├── main.py                # Main application file 🖥️
├── add_recipe.py          # Handles adding new recipes to CookWise. 🍲
├── data/
│   ├── recipes.json       # JSON file containing ingredients for meals 🥗
│   └── preparations.json  # JSON file containing cooking instructions 🍽️
├── icons/
│   ├── chef.png           # Chef icon 🍳
│   └── book.png           # Recipe book icon 📚
├── ui/
│   ├── icons.py           # Functions for loading icons 📦
│   └── styles.py          # QSS themes for styling the UI 🎨
└── requirements.txt       # List of required Python packages 📑

```

---

## 💻 Development

To contribute or expand the project, consider the following:

1. **Add New Features**: For example, suggestions based on user preferences or diet options. 🥗🍔
2. **Improve the UI**: Make the user interface more polished with additional themes or animations. 🌟
3. **Update Data**: Add more recipes and ingredients by updating the `recipes.json` and `preparations.json` files. 📈

---

## 🛠️ Technologies

* **Python**: Developed using Python 3. 🐍
* **PyQt6**: GUI created using the PyQt6 framework. 🎨
* **JSON**: Recipe and ingredient data is stored in JSON format. 📑

---

## 🤝 Contributing

If you’d like to contribute, feel free to **submit a pull request** or **report issues**. New feature ideas and bug fixes are always welcome! 🔧

The **CookWise** project was built to make cooking easier and help users quickly find recipes using the ingredients they already have. Feel free to reach out if you have any questions or need assistance. 😊

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
