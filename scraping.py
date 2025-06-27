import requests, os
import sqlite3
import requests , re
#sam
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

def search_usda(query, data_type):
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    params = {
        "query": query+",raw",
        "api_key": API_KEY,
        "dataType": data_type
    }
    res = requests.get(url, params=params)
    res.raise_for_status()
    return res.json().get("foods", [])


def get_food_nutrition(food_name):
    search_query = food_name.strip().lower()

    def get_results(preferred_query, data_type):
        try:
            return search_usda(preferred_query, data_type)
        except Exception:
            return []

    results = get_results(search_query, "Survey (FNDDS),Branded")
    if not results:
        print(f"[{food_name}] 🔁 Retrying with SR Legacy...")
        results = get_results(search_query, "SR Legacy")
    # if not results:
    #     print(f"[{food_name}] 🔁 Retrying with 'raw' in SR...")
    #     results = get_results(search_query + " raw", "SR LEgacy")
    # if not results:
    #     print(f"[{food_name}] 🔁 Retrying with 'raw' in query...")
    #     results = get_results(search_query + " ,raw", "Survey (FNDDS),Branded")

    if not results:
        print(f"[{food_name}] ❌ No results.")
        return 0, 0, 0, 0, 0, ''


    skip_words = ['Tea','hot','WEDGES','red','juice', 'dried', 'chips', 'powder', 'flavored', 'sweetened', 'snack', 'puree', 'babyfood', 'freeze-dried', 'bars', 'syrup', 'cereal']

    for food in results:
        desc = food.get("description", "").lower()
        if any(word in desc for word in skip_words):
            continue
        if 'raw' in desc or 'fresh' in desc or search_query in desc:
            fdc_id = food.get("fdcId")
            description = food.get("description", "")

            print(f"[{food_name}] ✅ Found: {description} (FDC ID: {fdc_id})")
            detail_url = f"https://api.nal.usda.gov/fdc/v1/food/{fdc_id}?api_key={API_KEY}"
            with open("url.text","a") as f:
                f.write(detail_url+'\n')
            # print(detail_url)

            detail_data = requests.get(detail_url).json()
            calories, protein, fat, carbs = extract_nutrients(detail_data)

            print(f"[{food_name}] 🍽 Calories: {calories} kcal | Protein: {protein}g | Fat: {fat}g | Carbs: {carbs}g")
            return calories, protein, fat, carbs, 100, 'g'

    print(f"[{food_name}] ❌ No valid nutrient data found.")
    return 0, 0, 0, 0, 0, ''



for name in food_items:
    food =  name
    # print(food)
    result =get_food_nutrition(food)

    if result:
        calories, protein, fat, carbs, serving_size, serving_unit = result  # ✅
        cur.execute("INSERT OR REPLACE INTO nutrition VALUES (?, ?, ?, ?, ?, ?)",
            (food, calories, protein, fat, carbs, serving_size))
        
conn.commit()
conn.close()

