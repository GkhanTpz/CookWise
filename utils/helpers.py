import json
import random

def load_data():
    with open("data/recipes.json", "r", encoding="utf-8") as f:
        recipes = json.load(f)

    with open("data/preparations.json", "r", encoding="utf-8") as f:
        preparations = json.load(f)

    return recipes, preparations

def get_user_ingredients(input_str):
    return [item.strip().lower() for item in input_str.split(",") if item.strip()]

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

def format_recipe(preparation):
    steps = preparation.split("\n")
    return "\n".join([f"{idx+1}. {step.strip()}" for idx, step in enumerate(steps)])
