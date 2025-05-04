import json
from recipes import recipes
from preparations import preparations

# Convert recipe ingredients to JSON format
recipes_json = {}

for dish, ingredients in recipes.items():
    recipes_json[dish] = {
        "ingredients": ingredients,
        "servings": 4  # Default value; can be updated later based on user input
    }

# Write the recipes with ingredients to a JSON file
with open("data/recipes.json", "w", encoding="utf-8") as f:
    json.dump(recipes_json, f, ensure_ascii=False, indent=4)

# Write the preparation instructions to a separate JSON file
with open("data/preparations.json", "w", encoding="utf-8") as f:
    json.dump(preparations, f, ensure_ascii=False, indent=4)

print("JSON files have been successfully created!")
