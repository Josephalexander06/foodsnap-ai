import requests, os
import sqlite3
import requests , re

API_KEY ='L8J1Jo3KTEr03j6nVb5x8C8GVeTus9l4RvmRnnPX'

dataset_folder = ("dataset/")

food_items = [name for name in os.listdir(dataset_folder)
              if os.path.isdir(os.path.join(dataset_folder,name))]

# print(food_items)
conn =sqlite3.connect('nutrition.db')
cur = conn.cursor()
print("db load..")
cur.execute('''CREATE TABLE IF NOT EXISTS nutrition (
    foodName TEXT PRIMARY KEY,
    calories REAL,
    protein REAL,
    fat REAL,
    carbs REAL,
    serving_size REAL
)''')

# def get_nutrition(food):
#     print(food)
#     try:
#         # Search food
#         search_url = "https://api.nal.usda.gov/fdc/v1/foods/search"
#         search_params = {
#             "query": food,
#             "api_key": API_KEY,
#             "pageSize": 1
#         }

#         search_res = requests.get(search_url, params=search_params)
#         search_res.raise_for_status()
#         search_data = search_res.json()

#         if not search_data.get("foods"):
#             return None

#         food_data = search_data["foods"][0]
#         fdc_id = food_data["fdcId"]
#         print('id',fdc_id)
#         description = food_data.get("description", food)

#         # Get nutrition detail
#         detail_url = f"https://api.nal.usda.gov/fdc/v1/food/{fdc_id}"
#         detail_res = requests.get(detail_url, params={"api_key": API_KEY})
#         detail_data = detail_res.json()

#         nutrient_map = {
#             1008: 0,  # Energy (kcal)
#             1003: 0,  # Protein
#             1004: 0,  # Fat
#             1005: 0   # Carbs
#         }
#         for nutrient in detail_data.get("foodNutrients", []):
#             nid = nutrient.get("nutrient", {}).get("id")
#             val = nutrient.get("amount")
#             if nid in nutrient_map and val is not None:
#                 nutrient_map[nid] = val

#         calories = nutrient_map[1008]
#         protein = nutrient_map[1003]
#         fat = nutrient_map[1004]
#         carbs = nutrient_map[1005]
#         print(calories,protein,fat,carbs)

#         return calories, protein, fat, carbs, description
    
#     except requests.exceptions.RequestException as e:
#         print(f"[Network Error] {e}")
#         return None
#     except Exception as e:
#         print(f"[Other Error] {e}")
#         return None




def clean_food_name(name):
    # Replace underscores, remove digits, strip extras
    name = name.replace("_", " ")
    name = re.sub(r'\d+', '', name)
    return name.strip()


def extract_nutrients(detail_data):
    nutrient_map = {
        1008: 0,  # Energy (kcal)
        1003: 0,  # Protein (g)
        1004: 0,  # Fat (g)
        1005: 0   # Carbs (g)
    }

    for nutrient in detail_data.get("foodNutrients", []):
        nid = nutrient.get("nutrient", {}).get("id")
        val = nutrient.get("amount")
        if nid in nutrient_map and val is not None:
            nutrient_map[nid] = val

    calories = nutrient_map[1008]
    protein = nutrient_map[1003]
    fat     = nutrient_map[1004]
    carbs   = nutrient_map[1005]
    return calories, protein, fat, carbs

def get_nutrition(food_name):
    # print(f"\n🔍 Getting nutrition for: {food_name}")
    search_query = clean_food_name(food_name)
  
    try:
        def search_usda(query, data_type):
            url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={query}&dataType={data_type}&api_key={API_KEY}"
            return requests.get(url).json().get("foods", [])

        results = search_usda(search_query, "Foundation,SR Legacy")

        if not results:
            print(f"[{food_name}] 🔁 Retrying with Survey & Branded...")
            results = search_usda(search_query, "Survey (FNDDS),Branded")
        

        if not results:
            print(f"[{food_name}] ❌ No search results.")
            return 0, 0, 0, 0, 0, ''

        for food in results:
            fdc_id = food.get("fdcId")

            detail_url = f"https://api.nal.usda.gov/fdc/v1/food/{fdc_id}?api_key={API_KEY}"
            detail_data = requests.get(detail_url).json()

            calories, protein, fat, carbs = extract_nutrients(detail_data)

            return calories, protein, fat, carbs, serving_size, serving_unit


        print(f"[{food_name}] ❌ No valid nutrient data found.")
        return 0, 0, 0, 0, 0, ''

    except Exception as e:
        print(f"[{food_name}] ❌ Error: {e}")
        return 0, 0, 0, 0, 0, ''



for food in food_items:
    result = get_nutrition(food)
    if result:
        calories, protein, fat, carbs, serving_size, serving_unit = result  # ✅
        cur.execute("INSERT OR REPLACE INTO nutrition VALUES (?, ?, ?, ?, ?, ?)",
            (food, calories, protein, fat, carbs, serving_size))
        
conn.commit()
conn.close()