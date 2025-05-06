import json
import random

# JSON dosyalarından tarifleri ve hazırlıkları yükler
def load_data():
    with open("data/recipes.json", "r", encoding="utf-8") as f:
        recipes = json.load(f)

    with open("data/preparations.json", "r", encoding="utf-8") as f:
        preparations = json.load(f)

    return recipes, preparations

# Kullanıcının girdiği malzemeleri temizleyip filtreler
def get_user_ingredients(input_str):
    ignored_ingredients = {"su", "tuz"}
    return [item.strip().lower() for item in input_str.split(",") if item.strip() and item.strip().lower() not in ignored_ingredients]

# Tarifleri eşleşme skorlarına göre sıralar
def score_recipe_match(user_ingredients, recipes):
    scored = []
    for dish, data in recipes.items():
        ingredients_lower = [i.lower() for i in data["ingredients"]]
        matched = [u for u in user_ingredients if any(u in ing for ing in ingredients_lower)]
        score = len(matched)
        missing = [ing for ing in ingredients_lower if not any(u in ing for u in user_ingredients)]
        scored.append((dish, score, missing, matched, ingredients_lower))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored

# Filtreleme kuralı: az malzeme → tam eşleşme, çok malzeme → minimum 3 eşleşme
def filter_matches(user_ingredients, matches):
    filtered = []
    for dish, score, missing, matched, total in matches:
        if len(user_ingredients) >= 3 and score < 3:
            continue
        if len(user_ingredients) in [1, 2] and score != len(user_ingredients):
            continue
        filtered.append((dish, score, missing, matched, total))
    return filtered

# Tarifleri numaralı şekilde biçimlendirir
def format_recipe(preparation):
    steps = preparation.split("\n")
    return "\n".join([f"{idx+1}. {step.strip()}" for idx, step in enumerate(steps)])
