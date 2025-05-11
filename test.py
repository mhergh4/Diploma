

# from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
# from flask_mysqldb import MySQL
# from flask_mail import Mail, Message
# from itsdangerous import URLSafeTimedSerializer
# from werkzeug.security import generate_password_hash, check_password_hash
# import requests
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import re
# import secrets
# from datetime import datetime, timedelta
# from threading import Thread
# from concurrent.futures import ThreadPoolExecutor
# import time
# from bs4 import BeautifulSoup
# from urllib.parse import quote
# from translate import Translator
# import random

# from config import SECRET_KEY, MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, MAIL_USERNAME, MAIL_PASSWORD, MAIL_DEFAULT_SENDER
# from utils import generate_keywords, generate_keywords_with_ai, get_top_tags, ask_gemini_for_sites, translate_text_ru_to_en, convert_to_usd
# from parsers import parse_site_products, parse_puma_products, parse_wildberries_products, parse_amazon_products, parse_aliexpress_products, parse_zara_products, parse_adidas_products, parse_apple_products, parse_samsung_products, parse_sony_products

# app = Flask(__name__)
# app.secret_key = SECRET_KEY

# # MySQL Configuration
# app.config['MYSQL_HOST'] = MYSQL_HOST
# app.config['MYSQL_USER'] = MYSQL_USER
# app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
# app.config['MYSQL_DATABASE'] = MYSQL_DATABASE

# mysql = MySQL(app)

# # Email Configuration
# app.config['MAIL_SERVER'] = MAIL_SERVER
# app.config['MAIL_PORT'] = MAIL_PORT
# app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
# app.config['MAIL_USERNAME'] = MAIL_USERNAME
# app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
# app.config['MAIL_DEFAULT_SENDER'] = MAIL_DEFAULT_SENDER

# mail = Mail(app)


# SITE_URLS = {
#     "Apple": "https://www.apple.com/us/search/{query}",
#     "Samsung": "https://www.samsung.com/us/search/searchMain/?listType=g&searchTerm={query}",
#     "Sony": "https://electronics.sony.com/search/{query}",
#     "Wildberries": "https://www.wildberries.am/catalog/0/search.aspx?search={query}",
#     "Amazon": "https://www.amazon.com/s?k={query}",
#     "Nike": "https://www.nike.com/w?q={query}",
#     "Puma": "https://us.puma.com/us/en/search?q={query}",
#     "Zara": "https://www.zara.com/us/search?ajax=true&query={query}",
#     "AliExpress": "https://www.aliexpress.com/wholesale?SearchText={query}",
#     "Adidas": "https://www.adidas.com/us/search?q={query}"
# }


# @app.before_request
# def ensure_login():
#     allowed_routes = ['login', 'register', 'verify_email','forgot_password', 'reset_password', 'test_db', 'static']
#     if 'user_id' not in session and request.endpoint not in allowed_routes:
#         if request.endpoint != 'static':
#             flash('Please log in or register to access the website.', 'warning')
#             return redirect(url_for('login'))


# @app.route('/')
# def home():
#     conn = mysql.connection
#     cursor = conn.cursor()

#     try:
#         cursor.execute("USE my_shop;")
#         user_id = session.get('user_id')
#         if not user_id:
#             flash("Please log in!", "danger")
#             return redirect(url_for('login'))

#         cursor.execute("""
#             SELECT id, title, price, description, image_url, link, brand
#             FROM products
#             WHERE user_id = %s
#             ORDER BY RAND()
#         """, (user_id,))
#         products = cursor.fetchall()

#         cursor.execute("SELECT product_title, product_brand FROM cart WHERE user_id = %s", (user_id,))
#         cart_items = cursor.fetchall()
#         cart_set = {(item[0], item[1]) for item in cart_items}

#         cursor.close()

#         product_list = [
#             {
#                 "id": row[0],
#                 "title": row[1],
#                 "price": row[2],
#                 "description": row[3],
#                 "image_url": row[4],
#                 "link": row[5],
#                 "brand": row[6],
#                 "in_cart": (row[1], row[6]) in cart_set
#             }
#             for row in products
#         ]

#         return render_template('index.html', products=product_list)

#     except Exception as e:
#         print(f"[ERROR] {e}")
#         flash("An error occurred while loading the homepage.", "danger")
#         return redirect(url_for('login'))


# @app.after_request
# def add_no_cache_headers(response):
#     response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
#     response.headers["Pragma"] = "no-cache"
#     response.headers["Expires"] = "0"
#     return response


# @app.route("/product_click", methods=["POST"])
# def product_click():
#     try:
#         print(f"[DEBUG] Headers: {request.headers}")
#         print(f"[DEBUG] Raw Data: {request.get_data(as_text=True)}")

#         data = request.get_json(silent=True)
#         if not data:
#             return jsonify({"status": "error", "message": "No data received"}), 400

#         product_name = data.get("product_name")
#         product_brand = data.get("product_brand")

#         if not product_name or not product_brand:
#             return jsonify({"status": "error", "message": "Invalid product data"}), 400

#         user_id = session.get('user_id')
#         if not user_id:
#             return jsonify({"status": "error", "message": "User not logged in"}), 403

#         print(f"[DEBUG] Product clicked: {product_name} ({product_brand}), user_id={user_id}")

#         tags = generate_keywords(product_name) + [product_brand.lower()]

        
#         conn = mysql.connection
#         cursor = conn.cursor()
#         cursor.execute("USE my_shop;")

#         for tag in tags:
#             cursor.execute("""
#                 INSERT INTO preferences_tags (user_id, tag, weight, last_interaction)
#                 VALUES (%s, %s, 1, NOW())
#                 ON DUPLICATE KEY UPDATE
#                 weight = weight + 1,
#                 last_interaction = NOW()
#             """, (user_id, tag.lower()))

#         conn.commit()
#         cursor.close()

#         return jsonify({"status": "success"}), 200

#     except Exception as e:
#         print(f"[ERROR] Error processing product_click: {e}")
#         return jsonify({"status": "error", "message": str(e)}), 500


# @app.before_request
# def clean_old_tags():
#         conn = mysql.connection
#         cursor = conn.cursor()
#         cursor.execute("USE my_shop;")

#         cursor.execute("""
#             DELETE FROM preferences_tags
#             WHERE last_interaction < NOW() - INTERVAL 60 DAY
#             AND weight < 3
#         """)

#         conn.commit()
#         cursor.close()


# def fetch_products_for_home(user_id, preferences):
#     if not user_id:
#         print("[ERROR] user_id is missing in fetch_products_for_home!")
#         return []

#     print(f"[DEBUG] Fetching tags for user_id: {user_id}")
#     top_tags = get_top_tags(user_id)
#     print(f"[DEBUG] Retrieved tags: {top_tags}")

#     if not top_tags:
#         top_tags = []
#         for key in ['preferred_categories', 'preferred_devices']:
#             pref_value = preferences.get(key, '')
#             if isinstance(pref_value, str):
#                 top_tags.extend(pref_value.split(','))

#     USER_AGENTS = [
#         'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
#         'Mozilla/5.0 (X11; Linux x86_64)'
#     ]

#     products = []

#     for query in top_tags:
#         sites_to_search = ask_gemini_for_sites(query)

#         for site_name in sites_to_search:
#             if site_name not in SITE_URLS:
#                 print(f"[WARNING] No URL template for {site_name}!")
#                 continue

#             search_url_template = SITE_URLS[site_name]

#             try:
#                 search_url = search_url_template.format(query=quote(query))
#                 headers = {'User-Agent': random.choice(USER_AGENTS)}
#                 time.sleep(2)

#                 response = requests.get(search_url, headers=headers, timeout=30)
#                 response.raise_for_status()

#                 site_products = parse_site_products(session.get('user_id'), site_name, search_url, query=query) # <--- parse_site_products может вызывать save_products_to_db
#                 products.extend(site_products)

#             except Exception as e:
#                 print(f"[ERROR] Error processing {site_name}: {e}")

#     return products[:200]



# def background_fetch_products():
#     """Runs the product fetching process for all users."""
#     with app.app_context():
#         while True:
#             print("[INFO] Starting product fetching...")
#             try:
#                 conn = mysql.connection
#                 cursor = conn.cursor()
#                 cursor.execute("USE my_shop;")
#                 cursor.execute("SELECT DISTINCT id FROM users;")
#                 user_ids = [row[0] for row in cursor.fetchall()]
#                 cursor.close()
#                 print(f"[DEBUG] Found {len(user_ids)} users.")

#                 with ThreadPoolExecutor(max_workers=5) as executor:
#                     executor.map(fetch_and_save_products_for_user, user_ids)

#                 print("[INFO] Product fetching completed.")
#             except Exception as e:
#                 print(f"[ERROR] Error during product fetching: {e}")

#             time.sleep(600)


# def save_products_to_db(user_id, product, save_to_shop=False):
#     with app.app_context():
#         try:
#             conn = mysql.connection
#             cursor = conn.cursor()
#             cursor.execute("USE my_shop;")

#             if not isinstance(product, dict):
#                 print(f"[ERROR] Error: product is not a dictionary! Received: {type(product)}")
#                 return

#             required_keys = ["title", "price", "description", "image_url", "link", "brand"]
#             for key in required_keys:
#                 if key not in product:
#                     print(f"[ERROR] In product missing key: {key}")
#                     return

#             title = product["title"][:255].strip() if product["title"] else None
#             image_url = product["image_url"][:255].strip() if product["image_url"] else None
#             link = product["link"][:255].strip() if product["link"] else None
#             brand = product["brand"][:100].strip() if product["brand"] else "Unknown Brand"
#             description = product["description"][:500].strip() if product["description"] else None

#             try:
#                 price = float(product["price"]) if product["price"] else None
#             except (ValueError, TypeError):
#                 print(f"[WARNING] Product skipped (incorrect price): {product['title']} -> {product['price']}")
#                 return

#             if not title or not price or not image_url:
#                 print(f"[WARNING] Product skipped (missing name, price or image): {product}")
#                 return

#             table_name = "shop_products" if save_to_shop else "products"

#             cursor.execute(f"""
#                 SELECT id FROM {table_name}
#                 WHERE user_id = %s AND title = %s AND brand = %s
#             """, (user_id, title, brand))
#             existing_product = cursor.fetchone()

#             if existing_product:
#                 print(f"[INFO] Product '{title}' already exists for user {user_id} in {table_name}, skipping addition.")
#             else:
#                 cursor.execute(f"""
#                     INSERT INTO {table_name} (user_id, title, price, description, image_url, link, brand)
#                     VALUES (%s, %s, %s, %s, %s, %s, %s)
#                 """, (user_id, title, price, description, image_url, link, brand))

#                 conn.commit()
#                 print(f"[DEBUG] Successfully saved product for user_id {user_id} in {table_name}: {title}")

#             cursor.close()

#         except Exception as e:
#             print(f"[ERROR] Error saving products to database: {e}")


# def fetch_and_save_products_for_user(user_id, save_to_shop=False):
#     """Fetches products for a specific user."""
#     with app.app_context():
#         try:
#             conn = mysql.connection
#             cursor = conn.cursor()
#             cursor.execute("USE my_shop;")
#             cursor.execute("SELECT * FROM preferences_tags WHERE user_id = %s", (user_id,))
#             user_data = cursor.fetchone()
#             if not user_data:
#                 print(f"[INFO] No preferences for user {user_id}, skipping...")
#                 return
#             preferences = {desc[0]: value for desc, value in zip([col[0] for col in cursor.description], user_data)}
#             print(f"[INFO] Loading products for user {user_id}")
#             products = fetch_products_for_home(user_id, preferences)
#             for product in products:
#                 save_products_to_db(user_id, product, save_to_shop) # <--- save_products_to_db вызывается здесь!
#             conn.commit()
#             print(f"[INFO] Fetching completed for user {user_id}")
#         except Exception as e:
#             print(f"[ERROR] Error loading products for user_id={user_id}: {e}")
#         finally:
#             cursor.close()
#             conn.close()


# Thread(target=background_fetch_products, daemon=True).start()


# @app.route('/about')
# def about():
#     return render_template('about.html')


# @app.route('/shop', methods=['GET'])
# def shop():
#     user_id = session.get('user_id')
#     conn = mysql.connection
#     cursor = conn.cursor()

#     try:
#         cursor.execute("USE my_shop;")

#         min_price = request.args.get('min_price', type=float)
#         max_price = request.args.get('max_price', type=float)
#         price_range = request.args.get('price_range')
#         sort_price = request.args.get('sort_price')
#         title_query = request.args.get('title_query', '').strip()
#         sort_title = request.args.get('sort_title')
#         brand = request.args.get('brand', '')
#         description_query = request.args.get('description_query', '').strip()

#         known_brands = ["Amazon", "Nike", "Puma", "Samsung", "Sony", "Wildberries",
#                         "Apple", "Zara", "AliExpress", "Adidas"]

#         query_sql = "SELECT title, price, image_url, link, brand, description FROM shop_products WHERE user_id = %s"
#         params = [user_id]

#         if min_price is not None:
#             query_sql += " AND price >= %s"
#             params.append(min_price)

#         if max_price is not None:
#             query_sql += " AND price <= %s"
#             params.append(max_price)

#         if price_range:
#             price_ranges = {
#                 "0-50": (0, 50),
#                 "50-100": (50, 100),
#                 "100-200": (100, 200)
#             }
#             if price_range in price_ranges:
#                 min_r, max_r = price_ranges[price_range]
#                 query_sql += " AND price BETWEEN %s AND %s"
#                 params.extend([min_r, max_r])

#         if title_query:
#             query_sql += " AND title LIKE %s"
#             params.append(f"%{title_query}%")

#         if brand and brand.lower() != "all":
#             query_sql += " AND (brand = %s OR description LIKE %s)"
#             params.append(brand)
#             params.append(f"%{brand}%")

#         if description_query:
#             query_sql += " AND description LIKE %s"
#             params.append(f"%{description_query}%")

#         if sort_price == "asc":
#             query_sql += " ORDER BY price ASC"
#         elif sort_price == "desc":
#             query_sql += " ORDER BY price DESC"
#         elif sort_title == "asc":
#             query_sql += " ORDER BY title ASC"
#         elif sort_title == "desc":
#             query_sql += " ORDER BY title DESC"
#         else:
#             query_sql += " ORDER BY RAND()"

#         cursor.execute(query_sql, tuple(params))
#         results = cursor.fetchall()

#         products = [
#             {
#                 "title": row[0],
#                 "price": row[1],
#                 "image_url": row[2],
#                 "link": row[3],
#                 "brand": row[4],
#                 "description": row[5]
#             }
#             for row in results
#         ]

#         return render_template('shop.html', products=products, known_brands=known_brands, query="")

#     except Exception as e:
#         print(f"[ERROR] {e}")
#         return render_template('shop.html', products=[], known_brands=[], query="")

#     finally:
#         cursor.close()


# @app.route('/search', methods=['GET'])
# def search():
#     query = request.args.get('q', '').strip()
#     user_id = session.get('user_id')

#     if not query:
#         return jsonify({"status": "error", "message": "Empty search query"}), 400

   
#     conn = mysql.connection
#     cursor = conn.cursor()
#     cursor.execute("USE my_shop;")

#     try:
#         cursor.execute("DELETE FROM shop_products WHERE user_id = %s", (user_id,))

#         cursor.execute("""
#             INSERT INTO shop_products (user_id, title, price, image_url, link, brand, description)
#             SELECT %s, title, price, image_url, link, brand, description
#             FROM products
#             WHERE title LIKE %s OR brand LIKE %s OR description LIKE %s
#         """, (user_id, f"%{query}%", f"%{query}%", f"%{query}%"))

#         conn.commit()
#         print(f"[DEBUG] Local database search complete. Now requesting AI for sites...")

#         search_external_sites_with_ai(query, user_id)

#         return shop()

#     except Exception as e:
#         print(f"[ERROR] {e}")
#         return jsonify({"status": "error", "message": str(e)})

#     finally:
#         cursor.close()


# def search_external_sites_with_ai(query, user_id):
#     """Requests AI for sites to search for products and starts parsing."""
#     with app.app_context():
#         print(f"[INFO] Determining sites for '{query}' via AI...")

#         sites_to_search = ask_gemini_for_sites(query)

#         if not sites_to_search:
#             print("[WARNING] AI did not suggest any sites for search. Aborting.")
#             return

#         print(f"[INFO] AI selected sites: {sites_to_search}")

#         with ThreadPoolExecutor(max_workers=3) as executor:
#             futures = [
#                 executor.submit(parse_site_products_for_shop, user_id, site, SITE_URLS[site].format(query=query))
#                 for site in sites_to_search if site in SITE_URLS
#             ]

#             products = []
#             for future in futures:
#                 try:
#                     products.extend(future.result())
#                 except Exception as e:
#                     print(f"[ERROR] Error during site parsing: {e}")

#         print(f"[INFO] Found {len(products)} products after AI search.")



# def parse_site_products_for_shop(user_id, site_name, search_url, shopping_budget=None, query=None):
#     """Parses products using Selenium and directly adds them to the shop database."""
#     save_to_shop = True
#     products = []
#     driver = setup_selenium() # <--- setup_selenium() скорее всего контекст не требует
#     print(f"[DEBUG] In parse_site_products: site={site_name}, save_to_shop={save_to_shop}")

#     try:
#         if site_name == "Apple":
#             if query is None:
#                 print(f"[DEBUG] Query is required for Apple.")
#                 return products
#             parse_apple_products(driver, user_id, products, shopping_budget, query, save_to_shop) # <--- Вызываем парсеры ВНУТРИ контекста
#         else:
#             print(f"[DEBUG] Opening URL: {search_url}")
#             driver.get(search_url)

#             if site_name == "Nike":
#                 parse_nike_products(driver, user_id, products, shopping_budget, save_to_shop) # <--- Вызываем парсеры ВНУТРИ контекста
#             elif site_name == "Samsung":
#                 parse_samsung_products(driver, user_id, products, shopping_budget, save_to_shop) # <--- Вызываем парсеры ВНУТРИ контекста
#             elif site_name == "Sony":
#                 parse_sony_products(driver, user_id, products, shopping_budget, save_to_shop) # <--- Вызываем парсеры ВНУТРИ контекста
#             elif site_name == "Puma":
#                 parse_puma_products(driver, user_id, products, shopping_budget, save_to_shop) # <--- Вызываем парсеры ВНУТРИ контекста
#             elif site_name == "Wildberries":
#                 parse_wildberries_products(driver, user_id, products, shopping_budget, save_to_shop) # <--- ВАЖНО! Вызываем parse_wildberries_products ВНУТРИ контекста
#             elif site_name == "Amazon":
#                 parse_amazon_products(driver, user_id, products, shopping_budget, save_to_shop) # <--- Вызываем парсеры ВНУТРИ контекста
#             elif site_name == "Zara":
#                 parse_zara_products(driver, products, shopping_budget) # <--- Вызываем парсеры ВНУТРИ контекста
#             elif site_name == "AliExpress":
#                 parse_aliexpress_products(driver, products, shopping_budget) # <--- Вызываем парсеры ВНУТРИ контекста
#             elif site_name == "Adidas":
#                 parse_adidas_products(driver, products, shopping_budget) # <--- Вызываем парсеры ВНУТРИ контекста
#             else:
#                 print(f"[DEBUG] Parsing for {site_name} is not implemented.")

#     except Exception as e:
#         print(f"[ERROR] Error processing site {site_name}: {e}")

#     finally:
#         driver.quit()

#     return products


# @app.route('/add_to_cart', methods=['POST'])
# def add_to_cart():
#     conn = mysql.connection
#     cursor = conn.cursor()

#     try:
#         cursor.execute("USE my_shop;")
#         user_id = session.get('user_id')

#         if not user_id:
#             return jsonify({"status": "error", "message": "User not logged in"}), 403

#         data = request.json
#         print("[DEBUG] Received data:", data)

#         if not data:
#             return jsonify({"status": "error", "message": "No data received"}), 400

#         product_title = data.get('title', '').strip()
#         product_price = float(data.get('price', '0') or 0)
#         product_image_url = data.get('image_url', '').strip()
#         product_link = data.get('link', '').strip()
#         product_brand = data.get('brand', '').strip()
#         product_description = data.get('description', 'No description available')

#         cursor.execute("""
#             INSERT INTO cart (user_id, product_title, product_price, product_description, product_image_url, product_link, product_brand)
#             VALUES (%s, %s, %s, %s, %s, %s, %s)
#         """, (user_id, product_title, product_price, product_description, product_image_url, product_link, product_brand))

#         conn.commit()
#         return jsonify({"status": "success", "message": "Product added to cart"}), 200

#     except Exception as e:
#         print(f"[ERROR] Error adding product to cart: {e}")
#         return jsonify({"status": "error", "message": "Failed to add product to cart"}), 500

#     finally:
#         cursor.close()


# @app.route('/remove_from_cart', methods=['POST'])
# def remove_from_cart():
#     try:
#         user_id = session.get('user_id')
#         if not user_id:
#             return jsonify({"status": "error", "message": "User not logged in"}), 403

#         data = request.json
#         product_id = data.get('id')

#         if not product_id:
#             return jsonify({"status": "error", "message": "Product ID required"}), 400
#         conn = mysql.connection
#         cursor = conn.cursor()
#         cursor.execute("USE my_shop;")
#         cursor.execute("DELETE FROM cart WHERE id = %s AND user_id = %s", (product_id, user_id))
#         conn.commit()
#         cursor.close()

#         return jsonify({"status": "success", "message": "Product removed from cart"}), 200
#     except Exception as e:
#         print(f"[ERROR] {e}")
#         return jsonify({"status": "error", "message": "Failed to remove product from cart"}), 500


# @app.route('/cart', methods=['GET'])
# def get_cart():
#     conn = mysql.connection
#     cursor = conn.cursor()
#     try:
#         cursor.execute("USE my_shop;")
#         user_id = session.get('user_id')
#         if not user_id:
#             return jsonify({"status": "error", "message": "User not logged in"}), 403

#         cursor.execute("""
#             SELECT id, product_title, product_price, product_description, product_image_url, product_link, product_brand
#             FROM cart
#             WHERE user_id = %s
#         """, (user_id,))
#         cart_items = cursor.fetchall()
#         cursor.close()

#         items = [
#             {
#                 "id": row[0],
#                 "title": row[1],
#                 "price": row[2],
#                 "description": row[3],
#                 "image_url": row[4],
#                 "link": row[5],
#                 "brand": row[6]
#             }
#             for row in cart_items
#         ]

#         print(items)

#         return render_template('cart.html', cart_items=items)
#     except Exception as e:
#         print(f"[ERROR] {e}")
#         return jsonify({"status": "error", "message": "Failed to fetch cart items"}), 500

# @app.route("/subscribe", methods=["POST"])
# def subscribe():
#     if "user_id" not in session:
#         return jsonify({"status": "error", "message": "User must be logged in to subscribe."})

#     data = request.get_json()
#     email = data.get("email")
#     user_id = session["user_id"]

#     if not email:
#         return jsonify({"status": "error", "message": "Email is required."})

#     with app.app_context(): 
#         try:
#             conn = mysql.connection
#             cursor = conn.cursor()
#             cursor.execute("USE my_shop;")

#             cursor.execute("SELECT * FROM subscribers WHERE user_id = %s", (user_id,))
#             existing_subscription = cursor.fetchone()

#             if existing_subscription:
#                 return jsonify({"status": "error", "message": "You are already subscribed!"})

#             cursor.execute("INSERT INTO subscribers (user_id, email) VALUES (%s, %s)", (user_id, email))
#             conn.commit()

#             msg = Message("Subscription Confirmed",
#                             recipients=[email],
#                             body="Thank you for subscribing to My Shop's updates and promotions!")

#             mail.send(msg)

#             return jsonify({"status": "success", "message": "Subscription successful!"})

#         except Exception as e:
#             return jsonify({"status": "error", "message": f"Database error: {str(e)}"})

# @app.route('/shop-single')
# def shop_single():
#     return render_template('shop-single.html')


# @app.route("/contact", methods=["GET", "POST"])
# def contact():
#     if request.method == "POST":
#         name = request.form["name"]
#         email = request.form["email"]
#         subject = request.form["subject"]
#         message_body = request.form["message"]

#         msg = Message(subject=f"New Contact Form Message: {subject}",
#                         sender=email,
#                         recipients=["auth.myshop.world@gmail.com"])
#         msg.body = f"Name: {name}\nEmail: {email}\n\n{message_body}"

#         try:
#             mail.send(msg)
#             flash("Your message has been sent successfully!", "success")
#         except Exception as e:
#             print(f"Email sending error: {e}")
#             flash("Error sending message. Please try again later.", "danger")

#         return redirect(url_for("contact"))

#     return render_template("contact.html")


# def format_preferences_for_ai(raw_data):
#     """Formats preferences into text for AI analysis."""
#     questions = [
#         "What products are you interested in?",
#         "What style of clothing do you prefer?",
#         "Which brands and sites do you like?",
#         "What materials do you prefer?",
#         "What devices do you buy most often?",
#         "Do you prefer certain colors?",
#         "How important is eco-friendliness to you?",
#         "What type of footwear do you buy most often?",
#         "What kind of cosmetics do you prefer?",
#         "Are you shopping for a specific purpose?",
#         "What is your shopping budget?",
#         "What home products interest you?",
#         "Do you often buy children's products?",
#         "What type of food products do you prefer?",
#         "How important is delivery to you?",
#         "What payment method do you prefer?",
#         "Are you interested in discounts and promotions?",
#         "Do you use subscription services?",
#         "Do you prefer domestic or imported products?",
#         "How important is the brand to you?"
#     ]

#     formatted_text = []

#     for i, question in enumerate(questions):
#         key = list(raw_data.keys())[i] if i < len(raw_data) else None
#         answer = ', '.join(raw_data.get(key, [])) if key else "No answer"
#         formatted_text.append(f"{question} {answer}")

#     return "\n".join(formatted_text)

# def generate_tags_with_ai(preferences_text):
#     """Sends preferences to AI and gets relevant tags."""
#     try:
#         model = genai.GenerativeModel("gemini-1.5-flash")
#         prompt = (
#             f"Analyze the following user shopping preferences and generate relevant search tags:\n\n{preferences_text}\n\n"
#             "Provide only relevant keywords, separated by commas."
#         )

#         response = model.generate_content(prompt)
#         ai_tags = response.text.strip().split(",")
#         ai_tags = [tag.strip().lower() for tag in ai_tags if tag.strip()]

#         print(f"[DEBUG] Gemini AI Tags: {ai_tags}")
#         return ai_tags
#     except Exception as e:
#         print(f"[ERROR] Error querying Gemini for preferences: {e}")
#         return []



# @app.route('/preferences', methods=['GET', 'POST'])
# def preferences():
#     conn = mysql.connection
#     cursor = conn.cursor()

#     try:
#         cursor.execute("USE my_shop;")
#         user_id = session.get('user_id')
#         if not user_id:
#             flash('User not logged in!', 'danger')
#             return redirect(url_for('login'))

#         if request.method == 'POST':
#             raw_data = request.form.to_dict(flat=False)
#             print("[DEBUG] Raw POST data:", raw_data)

#             form_data = {
#                 "preferred_categories": ','.join(raw_data.get('preferred_categories[]', [])),
#                 "preferred_styles": ','.join(raw_data.get('preferred_styles[]', [])),
#                 "favorite_brands": ','.join(raw_data.get('favorite_brands[]', [])),
#                 "preferred_material": raw_data.get('preferred_material', [''])[0],
#                 "preferred_devices": ','.join(raw_data.get('preferred_devices[]', [])),
#                 "preferred_colors": raw_data.get('preferred_colors', [''])[0],
#                 "eco_preference": raw_data.get('eco_preference', [''])[0],
#                 "preferred_footwear": ','.join(raw_data.get('preferred_footwear[]', [])),
#                 "preferred_cosmetics": ','.join(raw_data.get('preferred_cosmetics[]', [])),
#                 "shopping_purpose": ','.join(raw_data.get('shopping_purpose[]', [])),
#                 "shopping_budget": raw_data.get('shopping_budget', [''])[0],
#                 "home_products": ','.join(raw_data.get('home_products[]', [])),
#                 "kids_products": raw_data.get('kids_products', [''])[0],
#                 "food_products": ','.join(raw_data.get('food_products[]', [])),
#                 "delivery_preference": raw_data.get('delivery_preference', [''])[0],
#                 "payment_method": raw_data.get('payment_method', [''])[0],
#                 "discount_interest": raw_data.get('discount_interest', [''])[0],
#                 "subscription_use": raw_data.get('subscription_use', [''])[0],
#                 "product_origin": raw_data.get('product_origin', [''])[0],
#                 "brand_importance": raw_data.get('brand_importance', [''])[0]
#             }

#             preferences_text = " ".join(
#                 [','.join(values) for values in raw_data.values()]
#             ).strip()

#             ai_tags = generate_tags_with_ai(preferences_text)

#             cursor.execute("SELECT * FROM preferences WHERE user_id = %s", (user_id,))
#             existing_preferences = cursor.fetchone()

#             if existing_preferences:
#                 update_fields = ", ".join([f"{key} = %s" for key in form_data.keys()])
#                 update_query = f"UPDATE preferences SET {update_fields} WHERE user_id = %s"
#                 cursor.execute(update_query, tuple(form_data.values()) + (user_id,))
#                 print(f"Updated preferences for user_id {user_id}")
#             else:
#                 insert_fields = ", ".join(form_data.keys())
#                 placeholders = ", ".join(["%s"] * len(form_data))
#                 insert_query = f"INSERT INTO preferences (user_id, {insert_fields}) VALUES (%s, {placeholders})"
#                 cursor.execute(insert_query, (user_id,) + tuple(form_data.values()))
#                 print(f"Inserted preferences for user_id {user_id}")

#             cursor.execute("DELETE FROM preferences_tags WHERE user_id = %s", (user_id,))
#             for tag in ai_tags:
#                 cursor.execute("""
#                     INSERT INTO preferences_tags (user_id, tag, weight, last_interaction)
#                     VALUES (%s, %s, 5, NOW())
#                     ON DUPLICATE KEY UPDATE
#                     weight = weight + 5,
#                     last_interaction = NOW()
#                 """, (user_id, tag))

#             conn.commit()
#             print(f"[DEBUG] Preferences updated and AI tags saved for user_id {user_id}")

#             return redirect(url_for('home'))

#         cursor.execute("SELECT * FROM preferences WHERE user_id = %s", (user_id,))
#         preferences = cursor.fetchone()

#         if preferences:
#             preferences = {desc[0]: value for desc, value in zip(cursor.description, preferences)}
#             print("[DEBUG] Retrieved preferences:", preferences)
#         else:
#             preferences = {}

#     except Exception as e:
#         flash(f"Error while processing preferences: {str(e)}", 'danger')
#         preferences = {}

#     finally:
#         cursor.close()

#     return render_template('preferences.html', preferences=preferences)



# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if session.get('user_id'):
#         return redirect(url_for('home'))

#     if request.method == 'POST':
#         try:
#             required_fields = ['username', 'email', 'password', 'confirm_password']
#             for field in required_fields:
#                 if field not in request.form:
#                     flash(f"Missing field: {field}", 'danger')
#                     return redirect(url_for('register'))

#             username = request.form['username']
#             email = request.form['email']
#             password = request.form['password']
#             confirm_password = request.form['confirm_password']

#             if password != confirm_password:
#                 flash('❌ Passwords do not match.', 'danger')
#                 return redirect(url_for('register'))

#             if not is_strong_password(password):
#                 flash('❌ Password must be at least 8 characters long, contain an uppercase letter, a lowercase letter, a number, and a special character.', 'danger')
#                 return redirect(url_for('register'))

#             hashed_password = generate_password_hash(password)
#             verification_token = secrets.token_urlsafe(32)
#             verification_expires = datetime.now() + timedelta(hours=24)

#             conn = mysql.connection
#             cursor = conn.cursor()
#             cursor.execute("USE my_shop;")

#             try:
#                 cursor.execute(
#                     """
#                     INSERT INTO users (username, email, password_hash, verified, verification_token, verification_expires)
#                     VALUES (%s, %s, %s, %s, %s, %s)
#                     """,
#                     (username, email, hashed_password, False, verification_token, verification_expires)
#                 )
#                 conn.commit()

#                 verification_link = url_for('verify_email', token=verification_token, _external=True)
#                 send_verification_email(email, verification_link)

#                 flash('✅ Registration successful! Check your email to verify your account.', 'success')
#                 return redirect(url_for('login'))

#             except Exception as e:
#                 if "Duplicate entry" in str(e):
#                     flash('Email is already registered. Try logging in.', 'danger')
#                 else:
#                     flash(f"Error during registration: {str(e)}", 'danger')
#                 return redirect(url_for('register'))

#             finally:
#                 cursor.close()

#         except KeyError as e:
#             flash(f"Missing field in the form: {str(e)}", 'danger')
#             return redirect(url_for('register'))

#     return render_template('register.html')

# def send_verification_email(email, verification_link):
#     try:
#         msg = Message('Verify Your Email - My Shop', recipients=[email])
#         msg.body = f"""
#         Welcome to My Shop!

#         Please click the link below to verify your email address and complete your registration:

#         {verification_link}

#         This link is valid for 24 hours.

#         If you didn't request this, please ignore this email.
#         """
#         print(f"Sending email to {email} with link: {verification_link}")
#         mail.send(msg)
#         print("Email sent successfully!")

#         print(f"[DEBUG] Verification email sent to {email}")
#     except Exception as e:
#         print(f"[ERROR] Failed to send email: {e}")



# @app.route('/verify/<token>')
# def verify_email(token):
#     conn = mysql.connection
#     cursor = conn.cursor()

#     try:
#         cursor.execute("USE my_shop;")
#         cursor.execute("SELECT id, verification_expires FROM users WHERE verification_token = %s AND verified = FALSE", (token,))
#         user = cursor.fetchone()

#         if not user:
#             flash('Invalid or expired verification link.', 'danger')
#             return redirect(url_for('register'))

#         expiration_time = user[1]
#         if expiration_time and datetime.now() > expiration_time:
#             flash('Verification link has expired. Please register again.', 'danger')
#             return redirect(url_for('register'))

#         cursor.execute("UPDATE users SET verified = TRUE, verification_token = NULL, verification_expires = NULL WHERE id = %s", (user[0],))
#         conn.commit()
#         flash('✅ Your email has been verified! You can now log in.', 'success')
#         return redirect(url_for('login'))

#     except Exception as e:
#         flash(f"Verification error: {str(e)}", 'danger')
#         return redirect(url_for('register'))

#     finally:
#         cursor.close()



# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if session.get('user_id'):
#         return redirect(url_for('home'))

#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']

#         conn = mysql.connection
#         cursor = conn.cursor()
#         try:
#             cursor.execute("USE my_shop;")
#             cursor.execute("SELECT id, password_hash, verified FROM users WHERE email = %s", (email,))
#             user = cursor.fetchone()

#             if user:
#                 if not user[2]:
#                     flash('Your email is not verified. Check your inbox.', 'warning')
#                     return redirect(url_for('login'))

#                 if check_password_hash(user[1], password):
#                     session['user_id'] = user[0]
#                     flash('Login successful.', 'success')
#                     return redirect(url_for('home'))

#             flash('Invalid email or password.', 'danger')
#         except Exception as e:
#             flash(f"Error during login: {str(e)}", 'danger')
#         finally:
#             cursor.close()

#     return render_template('login.html')



# reset_tokens = {}

# def is_strong_password(password):
#     """Password strength check."""
#     return (
#         len(password) >= 8 and
#         re.search(r'[A-Z]', password) and
#         re.search(r'[a-z]', password) and
#         re.search(r'\d', password) and
#         re.search(r'[!@#$%^&*]', password)
#     )

# @app.route('/forgot-password', methods=['GET', 'POST'])
# def forgot_password():
#     if request.method == 'POST':
#         email = request.form.get('email')

#         conn = mysql.connection
#         cursor = conn.cursor()
#         cursor.execute("USE my_shop;")

#         cursor.execute("SELECT id, last_reset_request FROM users WHERE email = %s", (email,))
#         user = cursor.fetchone()

#         if user:
#             user_id, last_reset_request = user

#             now = datetime.now()
#             if last_reset_request and (now - last_reset_request).total_seconds() < 60:
#                 flash('You can request a reset link once per minute. Please wait.', 'warning')
#             else:
#                 reset_token = secrets.token_urlsafe(32)
#                 reset_expires = now + timedelta(hours=1)

#                 cursor.execute("""
#                     UPDATE users
#                     SET reset_token = %s, reset_expires = %s, last_reset_request = %s
#                     WHERE id = %s
#                 """, (reset_token, reset_expires, now, user_id))
#                 conn.commit()

#                 reset_link = url_for('reset_password', token=reset_token, _external=True)
#                 send_reset_email(email, reset_link)

#                 flash('Password reset email sent! Check your inbox.', 'success')
#         else:
#             flash('No account found with that email.', 'danger')

#         cursor.close()
#         return redirect(url_for('forgot_password'))

#     return render_template('forgot_password.html')


# def send_reset_email(email, reset_link):
#     print(f"Sending email to {email} with reset link: {reset_link}")
#     try:
#         msg = Message('Reset Your Password - My Shop', recipients=[email])
#         msg.body = f"""
#         You requested a password reset. Click the link below to reset your password:
#         {reset_link}

#         If you did not request this, please ignore this email.
#         """
#         mail.send(msg)
#         print("[DEBUG] Reset email sent successfully!")
#     except Exception as e:
#         print(f"[ERROR] Failed to send email: {e}")


# @app.route('/reset-password/<token>', methods=['GET', 'POST'])
# def reset_password(token):
#     print(f"[DEBUG] Reset Password: Token received: {token}")

#     conn = mysql.connection
#     cursor = conn.cursor()
#     cursor.execute("USE my_shop;")

#     cursor.execute("SELECT id, reset_expires FROM users WHERE reset_token = %s", (token,))
#     user = cursor.fetchone()

#     if not user:
#         flash('Invalid or expired reset link.', 'danger')
#         return redirect(url_for('forgot_password'))

#     if user[1] < datetime.now():
#         flash('Reset link expired. Request a new one.', 'danger')
#         return redirect(url_for('forgot_password'))

#     if request.method == 'POST':
#         new_password = request.form.get('password')
#         confirm_password = request.form.get('confirm_password')

#         if new_password != confirm_password:
#             flash('Passwords do not match.', 'danger')
#             return redirect(url_for('reset_password', token=token))

#         if len(new_password) < 8:
#             flash('Password must be at least 8 characters.', 'danger')
#             return redirect(url_for('reset_password', token=token))

#         hashed_password = generate_password_hash(new_password)

#         cursor.execute("UPDATE users SET password_hash = %s, reset_token = NULL, reset_expires = NULL WHERE id = %s",
#                         (hashed_password, user[0]))
#         conn.commit()

#         flash('Your password has been updated. You can now log in.', 'success')
#         cursor.close()
#         return redirect(url_for('login'))

#     cursor.close()
#     return render_template('reset_password.html', token=token)



# @app.route('/routes')
# def show_routes():
#     print(app.url_map)
#     return jsonify([str(rule) for rule in app.url_map.iter_rules()])





# @app.route('/logout')
# def logout():
#     session.pop('user_id', None)
#     flash('You have been logged out.', 'success')

#     response = redirect(url_for('login'))
#     response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
#     response.headers["Pragma"] = "no-cache"
#     response.headers["Expires"] = "0"

#     return response

# @app.route('/test_db')
# def test_db():
#     conn = mysql.connection
#     cursor = conn.cursor()
#     try:
#         cursor.execute("USE my_shop;")
#         cursor.execute("SHOW TABLES;")
#         tables = cursor.fetchall()
#         return f"Tables: {tables}"
#     except Exception as e:
#         return f"Error: {str(e)}"
#     finally:
#         cursor.close()


# if __name__ == '__main__':
#     app.run(host='192.168.1.7', port=5000, debug=True)