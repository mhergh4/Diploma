# import re
# from itertools import combinations
# import google.generativeai as genai
# from urllib.parse import quote
# import random
# import time
# from translate import Translator
# import requests

# def generate_keywords_with_ai(product_name):
#     try:
#         model = genai.GenerativeModel("gemini-1.5-flash")
#         prompt = (
#             f"Given the product name '{product_name}', generate a list of relevant search keywords. "
#             "Provide keywords separated by commas."
#         )

#         response = model.generate_content(prompt)
#         ai_keywords = response.text.strip().split(",")
#         ai_keywords = [kw.strip().lower() for kw in ai_keywords if kw.strip()]

#         print(f"[DEBUG] Gemini AI Keywords for '{product_name}': {ai_keywords}")
#         return ai_keywords
#     except Exception as e:
#         print(f"[ERROR] Error querying Gemini: {e}")
#         return []

# def generate_keywords(product_name):
#     import re
#     from itertools import combinations

#     clean_name = re.sub(r"[^\w\s]", "", product_name)
#     words = clean_name.split()

#     keywords = set(words)
#     for i in range(2, min(4, len(words) + 1)):
#         keywords.update(" ".join(combo) for combo in combinations(words, i))

#     keywords = [kw.lower() for kw in keywords if len(kw) > 2]

#     ai_generated_keywords = generate_keywords_with_ai(product_name)

#     return list(set(keywords + ai_generated_keywords))

# def get_top_tags(user_id, limit=5):
#     print(f"[DEBUG] Getting top tags for user_id={user_id}")

#     from app import mysql

#     conn = mysql.connection
#     cursor = conn.cursor()
#     cursor.execute("USE my_shop;")

#     cursor.execute("""
#         SELECT tag, weight, DATEDIFF(NOW(), last_interaction) AS days_since_interaction
#         FROM preferences_tags
#         WHERE user_id = %s
#         ORDER BY (weight - (days_since_interaction / 10)) DESC
#         LIMIT %s;
#     """, (user_id, limit))

#     results = cursor.fetchall()
#     top_tags = [row[0] for row in results]

#     cursor.close()
#     print(f"[DEBUG] Top tags (after processing): {top_tags}")
#     return top_tags


# def ask_gemini_for_sites(tag):
#     try:
#         model = genai.GenerativeModel("gemini-1.5-flash")
#         prompt = (
#             f"Given the product tag '{tag}', determine which of the following sites are the most relevant for searching this product: "
#             "Amazon, Wildberries, Puma, Nike, Samsung, Apple, Sony, Zara, AliExpress, Adidas. "
#             "Provide only the site names, separated by commas."
#         )

#         response = model.generate_content(prompt)
#         sites = response.text.strip().split(",")

#         valid_sites = {"Amazon", "Wildberries", "Puma", "Nike", "Samsung", "Apple", "Sony", "Zara", "AliExpress", "Adidas"}
#         sites = [site.strip() for site in sites if site.strip() in valid_sites]

#         print(f"[DEBUG] Gemini selected sites for '{tag}': {sites}")
#         return sites
#     except Exception as e:
#         print(f"[ERROR] Error while querying Gemini: {e}")
#         return []


# def extract_price(price_text):
#     price_text = price_text.replace('$', '').replace('USD', '').replace('AMD', '').replace('֏', '').replace('руб.', '').replace('RUB', '').strip()
#     try:
#         if ' - ' in price_text:
#             low_price, high_price = map(float, price_text.split(' - '))
#             return (low_price + high_price) / 2
#         return float(''.join(c for c in price_text if c.isdigit() or c == '.'))
#     except ValueError:
#         return None


# def is_within_budget(price_value, shopping_budget):
#     if shopping_budget is None:
#         return True

#     if not isinstance(shopping_budget, str):
#         return True

#     budget_range = shopping_budget.split('_')
#     if len(budget_range) == 2:
#         try:
#             min_budget, max_budget = map(int, budget_range)
#             return min_budget <= price_value <= max_budget
#         except ValueError:
#             return True
#     return True


# def setup_selenium(disable_images=False):
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_argument("--headless")
#     chrome_options.add_argument("--disable-gpu")
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     chrome_options.add_argument("--disable-extensions")
#     chrome_options.add_argument("--disable-images")
#     chrome_options.add_argument("start-maximized")
#     chrome_options.add_argument("--enable-unsafe-swiftshader")
#     chrome_options.add_argument("--disable-webgl")
#     chrome_options.add_argument("--disable-blink-features=AutomationControlled")
#     chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
#     chrome_options.add_argument("--disable-notifications")
#     if disable_images:
#         prefs = {"profile.managed_default_content_settings.images": 2}
#         chrome_options.add_experimental_option("prefs", prefs)

#     driver = webdriver.Chrome(options=chrome_options)
#     return driver


# def translate_text_ru_to_en(text):
#     """
#     Translates text from Russian to English.
#     If translation fails, returns the original text.
#     """
#     try:
#         translator = Translator(from_lang="ru", to_lang="en")
#         translated_text = translator.translate(text)
#         if not translated_text or translated_text == text:
#             raise ValueError("Translation failed")
#         return translated_text
#     except Exception as e:
#         print(f"[ERROR] Error during text translation: {e}")
#         return text


# def convert_to_usd(price_in_rub):
#     """
#     Converts price from Russian rubles to US dollars using API.
#     If API is unavailable, uses a fixed exchange rate.
#     """
#     try:
#         response = requests.get("https://api.exchangerate-api.com/v4/latest/RUB")
#         response.raise_for_status()
#         data = response.json()
#         usd_rate = data.get('rates', {}).get('USD')

#         if not usd_rate:
#             raise ValueError("USD rate not found")

#         return round(price_in_rub * usd_rate, 2)
#     except Exception as e:
#         print(f"[ERROR] Error during price conversion: {e}")
#         return round(price_in_rub * 0.012, 2)