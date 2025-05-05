import json
import random

# Bu dosya, yemek tariflerini yükleyip, kullanıcı tarafından girilen malzemelere göre yemek eşleşmelerini hesaplar.
# Ayrıca, yemek tariflerinin adım adım formatlanmasını sağlar.
def load_data():
    with open("data/recipes.json", "r", encoding="utf-8") as f:
        recipes = json.load(f)  # Yemek tariflerini ve malzemeleri içeren json dosyasını okur.

    with open("data/preparations.json", "r", encoding="utf-8") as f:
        preparations = json.load(f)  # Yemeklerin yapılış tariflerini içeren json dosyasını okur.

    return recipes, preparations  # Yüklenen tarif ve hazırlık bilgilerini döndürür.

def get_user_ingredients(input_str):
    return [item.strip().lower() for item in input_str.split(",") if item.strip()]  # Kullanıcının girdiği malzemeleri temizler ve küçük harfe dönüştürür.

def score_recipe_match(user_ingredients, recipes):
    scored = []  # Eşleşme skoru listesi oluşturur.
    for dish, data in recipes.items():
        ingredients_lower = [i.lower() for i in data["ingredients"]]  # Yemeğin malzemelerini küçük harfe çevirir.
        matched = [u for u in user_ingredients if any(u in ing for ing in ingredients_lower)]  # Kullanıcının girdiği malzemelerle eşleşenleri bulur.
        score = len(matched)  # Eşleşen malzemelerin sayısını skor olarak kullanır.
        missing = [ing for ing in ingredients_lower if not any(u in ing for u in user_ingredients)]  # Eksik malzemeleri bulur.
        scored.append((dish, score, missing, matched, ingredients_lower))  # Skor, eksik malzemeler ve eşleşen malzemelerle birlikte yemeği kaydeder.
    scored.sort(key=lambda x: x[1], reverse=True)  # Yemekleri skorlarına göre azalan sırayla sıralar.
    return scored  # Sıralı eşleşme sonuçlarını döndürür.

def format_recipe(preparation):
    steps = preparation.split("\n")  # Tarifi satırlara böler.
    return "\n".join([f"{idx+1}. {step.strip()}" for idx, step in enumerate(steps)])  # Her bir adımı numaralandırarak birleştirir.
