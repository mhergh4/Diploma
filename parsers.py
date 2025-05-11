# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup
# from urllib.parse import quote
# import time

# from utils import extract_price, is_within_budget, setup_selenium, translate_text_ru_to_en, convert_to_usd
# from app import save_products_to_db


# def wait_for_elements(driver, timeout, selector):
#     try:
#         WebDriverWait(driver, timeout).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, selector))
#         )
#         print(f"[DEBUG] Elements with selector '{selector}' successfully found.")
#     except Exception as e:
#         print(f"[ERROR] Failed to wait for elements with selector '{selector}': {e}")
#         raise


# def parse_nike_products(driver, user_id, products, shopping_budget, save_to_shop=False):
#     try:
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, ".product-card"))
#         )
#         print("[DEBUG] Product cards successfully loaded on Nike.")

#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         items = soup.select(".product-card")
#         print(f"[DEBUG] Found {len(items)} product cards on Nike.")

#         for item in items:
#             try:
#                 title_element = item.select_one(".product-card__title")
#                 title = title_element.text.strip() if title_element else "Unknown Product"

#                 price_element = item.select_one(".product-price")
#                 price_value = extract_price(price_element.text.strip()) if price_element else None

#                 img_element = item.select_one("img.product-card__hero-image")
#                 image_url = img_element["src"] if img_element else "/static/images/default-product.jpg"

#                 description_element = item.select_one(".product-card__subtitle")
#                 description = description_element.text.strip() if description_element else "No description available."

#                 link_element = item.select_one("a.product-card__img-link-overlay")
#                 link = link_element["href"] if link_element else "#"
#                 if not link.startswith("http"):
#                     link = f"https://www.nike.com{link}"

#                 if price_value and not is_within_budget(price_value, shopping_budget):
#                     continue

#                 product = {
#                     "title": title[:255],
#                     "price": price_value,
#                     "description": description[:255],
#                     "image_url": image_url[:255],
#                     "link": link[:255],
#                     "brand": "Nike"
#                 }

#                 products.append(product)
#                 save_products_to_db(user_id, product, save_to_shop)

#             except Exception as e:
#                 print(f"[ERROR] Error processing product card on Nike: {e}")

#     except Exception as e:
#         print(f"[ERROR] Error processing Nike website: {e}")


# def parse_apple_products(driver, user_id, products, shopping_budget, query, save_to_shop):
#     APPLE_CATEGORY_URLS = {
#         "mac": "https://www.apple.com/shop/buy-mac",
#         "iphone": "https://www.apple.com/shop/buy-iphone",
#         "ipad": "https://www.apple.com/shop/buy-ipad",
#         "watch": "https://www.apple.com/shop/buy-watch",
#         "vision": "https://www.apple.com/shop/buy-vision",
#         "accessories": "https://www.apple.com/us/search/{query}?src=alp",
#     }

#     matched_category = next((c for c in APPLE_CATEGORY_URLS if c in query.lower()), "accessories")
#     url = APPLE_CATEGORY_URLS[matched_category].format(query=quote(query))

#     print(f"[DEBUG] Opening URL: {url}")

#     try:
#         driver.get(url)
#         time.sleep(3)

#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         items = soup.select(".rf-producttile")

#         print(f"[DEBUG] Found {len(items)} products on Apple.")

#         for item in items:
#             try:
#                 title_element = item.select_one(".rf-producttile-name a")
#                 title = title_element.text.strip() if title_element else "Unknown Product"

#                 price_element = item.select_one(".rf-producttile-pricecurrent")
#                 price_value = extract_price(price_element.text.strip()) if price_element else None

#                 link_element = title_element
#                 link = link_element["href"] if link_element else "#"
#                 if not link.startswith("http"):
#                     link = f"https://www.apple.com{link}"

#                 img_element = item.select_one(".rc-inline-gallery img")
#                 image_url = img_element["src"] if img_element else "/static/images/default-product.jpg"

#                 if price_value and not is_within_budget(price_value, shopping_budget):
#                     continue

#                 product = {
#                     "title": title[:255],
#                     "price": price_value,
#                     "description": "Apple product",
#                     "image_url": image_url[:255],
#                     "link": link[:255],
#                     "brand": "Apple"
#                 }

#                 products.append(product)
#                 save_products_to_db(user_id, product, save_to_shop)

#             except Exception as e:
#                 print(f"[ERROR] Error processing product card on Apple: {e}")

#     except Exception as e:
#         print(f"[ERROR] Error processing Apple website: {e}")


# def parse_main_apple_products(soup, user_id, products, shopping_budget, save_to_shop):
#     items = soup.select(".rf-cards-scroller-itemview")
#     print(f"[DEBUG] Found {len(items)} products in main Apple category.")

#     for item in items:
#         try:
#             title_element = item.select_one(".rf-hcard-content-title")
#             title = title_element.text.strip() if title_element and title_element.text.strip() else "Unknown Product"

#             price_element = item.select_one(".rf-hcard-content-info .rf-hcard-scrim-price")
#             price_text = next((span.text.strip() for span in price_element.find_all("span") if span.text.strip()), "N/A") if price_element else "N/A"
#             price_value = extract_price(price_text)

#             link_element = item.select_one("a.rf-hcard-cta")
#             link = f"https://www.apple.com{link_element['href']}" if link_element and link_element.get("href") else "#"

#             img_element = item.select_one(".rf-hcard-img-wrapper img")
#             image_url = img_element["src"] if img_element and img_element.get("src") else "/static/images/default-product.jpg"

#             if price_value and not is_within_budget(price_value, shopping_budget):
#                 continue

#             product = {
#                 "title": title,
#                 "price": price_value,
#                 "description": "Apple product description not available.",
#                 "image_url": image_url,
#                 "link": link,
#                 "brand": "Apple"
#             }

#             products.append(product)
#             print(f"[DEBUG] Added product: {title}")

#         except Exception as e:
#             print(f"[ERROR] Error processing product card: {e}")

#     save_products_to_db(user_id, products, save_to_shop)


# def parse_accessories(soup, user_id, products, shopping_budget, save_to_shop):
#     items = soup.select(".rf-producttile")
#     print(f"[DEBUG] Found {len(items)} products in accessories category.")

#     for item in items:
#         try:
#             title_element = item.select_one(".rf-producttile-name a")
#             title = title_element.text.strip() if title_element and title_element.text.strip() else "Unknown Accessory"

#             price_element = item.select_one(".rf-producttile-pricecurrent")
#             price_text = price_element.text.strip() if price_element else "N/A"
#             price_value = extract_price(price_text)

#             link_element = title_element
#             link = f"https://www.apple.com{link_element['href']}" if link_element and link_element.get("href") else "#"

#             img_element = item.select_one(".rc-inline-gallery img")
#             image_url = img_element["src"] if img_element and img_element.get("src") else "/static/images/default-product.jpg"

#             if price_value and not is_within_budget(price_value, shopping_budget):
#                 continue

#             product = {
#                 "title": title,
#                 "price": price_value,
#                 "description": "Accessory description not available.",
#                 "image_url": image_url,
#                 "link": link,
#                 "brand": "Apple"
#             }
#             products.append(product)
#             print(f"[DEBUG] Added accessory: {title}")

#         except Exception as e:
#             print(f"[ERROR] Error processing accessory: {e}")

#     save_products_to_db(user_id, products, save_to_shop)


# def parse_samsung_products(driver, user_id, products, shopping_budget, save_to_shop=False):
#     try:
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, "div[class^='ProductCard__container__']"))
#         )
#         print("[DEBUG] Product cards successfully loaded on Samsung.")

#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         items = soup.select("div[class^='ProductCard__container__']")
#         print(f"[DEBUG] Found {len(items)} product cards on Samsung.")

#         for item in items:
#             try:
#                 title_element = item.select_one("[class^='ProductCard__title__']")
#                 title = title_element.text.strip() if title_element else "Unknown Product"

#                 link_element = item.select_one("[class^='ProductCard__image__'] a")
#                 link = link_element["href"] if link_element else "#"
#                 if not link.startswith("http"):
#                     link = f"https://www.samsung.com{link}"

#                 img_element = item.select_one("[class^='ProductCard__image__'] img")
#                 image_url = img_element["src"] if img_element and img_element.get("src") else "/static/images/default-product.jpg"

#                 price_element = item.select_one("[class^='ProductCard__priceDetails__']")
#                 price_text = price_element.text.strip() if price_element else "N/A"
#                 price_value = extract_price(price_text)

#                 description_element = item.select_one("[class^='ProductOption__selectedColor__']")
#                 description = description_element.text.strip() if description_element else "No description available."

#                 if price_value and not is_within_budget(price_value, shopping_budget):
#                     continue

#                 product = {
#                     "title": title,
#                     "price": price_value,
#                     "description": description,
#                     "image_url": image_url,
#                     "link": link,
#                     "brand": "Samsung"
#                 }

#                 products.append(product)
#                 print(f"[DEBUG] Added product: {title}")
#                 save_products_to_db(user_id, product, save_to_shop)

#             except Exception as e:
#                 print(f"[ERROR] Error processing product card on Samsung: {e}")

#     except Exception as e:
#         print(f"[ERROR] Error waiting for elements on Samsung: {e}")


# def parse_sony_products(driver, user_id, products, shopping_budget, save_to_shop=False):
#     try:
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, "div.custom-product-grid-item"))
#         )
#         print("[DEBUG] Product cards successfully loaded on Sony.")

#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         items = soup.select("div.custom-product-grid-item")
#         print(f"[DEBUG] Found {len(items)} product cards on Sony.")

#         for item in items:
#             try:
#                 title_element = item.select_one(".custom-product-grid-item__info p")
#                 title = title_element.text.strip() if title_element else "Unknown Product"

#                 link_element = item.select_one(".custom-product-grid-item__info")
#                 link = link_element["href"] if link_element else "#"
#                 if not link.startswith("http"):
#                     link = f"https://electronics.sony.com{link}"

#                 img_element = item.select_one("img")
#                 image_url = img_element["src"] if img_element else "/static/images/default-product.jpg"

#                 availability_element = item.select_one('.estimate span')
#                 description = availability_element.text.strip() if availability_element else "No availability information"

#                 price_element = item.select_one('.product-item-pricing__price')
#                 price_value = extract_price(price_element.text.strip()) if price_element else None

#                 if price_value and not is_within_budget(price_value, shopping_budget):
#                     continue

#                 product = {
#                     "title": title,
#                     "price": price_value,
#                     "description": description,
#                     "image_url": image_url,
#                     "link": link,
#                     "brand": "Sony"
#                 }

#                 products.append(product)
#                 save_products_to_db(user_id, product, save_to_shop)

#             except Exception as e:
#                 print(f"[ERROR] Error processing product card on Sony: {e}")

#     except Exception as e:
#         print(f"[ERROR] Error processing Sony website: {e}")


# def parse_puma_products(driver, user_id, products, shopping_budget, save_to_shop=False):
#     """
#     Parses products from the Puma website and adds them to the product list.
#     """
#     try:
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, "li[data-test-id='product-list-item']"))
#         )
#         print("[DEBUG] Product cards successfully loaded on Puma.")

#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         items = soup.select("li[data-test-id='product-list-item']")
#         print(f"[DEBUG] Found {len(items)} product cards on Puma.")

#         for item in items:
#             try:
#                 title_element = item.select_one("h3")
#                 title = title_element.text.strip() if title_element else "Unknown Product"

#                 description_element = item.select_one("span.w-full.text-base.text-puma-gray-60")
#                 description = description_element.text.strip() if description_element else "No description available."

#                 price_element = item.select_one("span[data-test-id='price']")
#                 price_value = extract_price(price_element.text.strip()) if price_element else None

#                 link_element = item.select_one("a[data-test-id='product-list-item-link']")
#                 link = link_element["href"] if link_element else "#"
#                 if not link.startswith("http"):
#                     link = f"https://us.puma.com{link}"

#                 img_element = item.select_one("img")
#                 image_url = img_element["src"] if img_element else "/static/images/default-product.jpg"

#                 if price_value and not is_within_budget(price_value, shopping_budget):
#                     continue

#                 product = {
#                     "title": title,
#                     "price": price_value,
#                     "description": description,
#                     "image_url": image_url,
#                     "link": link,
#                     "brand": "Puma"
#                 }

#                 products.append(product)
#                 save_products_to_db(user_id, product,save_to_shop)

#             except Exception as e:
#                 print(f"[ERROR] Error processing product card on Puma: {e}")

#     except Exception as e:
#         print(f"[ERROR] Error waiting for elements on Puma: {e}")



# def parse_wildberries_products(driver, user_id, products, shopping_budget, save_to_shop=False):
#     """
#     Parses products from the Wildberries website and adds them to the product list.
#     """
#     try:
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, "article.product-card"))
#         )
#         print("[DEBUG] Product cards successfully loaded on Wildberries.")

#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         items = soup.select("article.product-card")
#         print(f"[DEBUG] Found {len(items)} product cards on Wildberries.")

#         for item in items:
#             try:
#                 brand_element = item.select_one("span.product-card__brand")
#                 brand = brand_element.text.strip() if brand_element else "Unknown Brand"

#                 name_element = item.select_one("span.product-card__name")
#                 title_ru = name_element.text.replace("/", "").strip() if name_element else "Unknown Product"
#                 title_en = translate_text_ru_to_en(title_ru)

#                 price_element = item.select_one("div.price ins.price__lower-price")
#                 price_rub = extract_price(price_element.text.strip()) if price_element else None
#                 price_usd = convert_to_usd(price_rub) if price_rub else None

#                 link_element = item.select_one("a.product-card__link")
#                 link = link_element["href"] if link_element else "#"
#                 if not link.startswith("http"):
#                     link = f"https://www.wildberries.ru{link}"

#                 img_element = item.select_one("img.j-thumbnail")
#                 image_url = img_element["src"] if img_element else "/static/images/default-product.jpg"

#                 if price_usd and not is_within_budget(price_usd, shopping_budget):
#                     continue

#                 product = {
#                     "title": title_en,
#                     "price": price_usd,
#                     "description": "Site: Wildberries",
#                     "image_url": image_url,
#                     "link": link,
#                     "brand": brand
#                 }

#                 products.append(product)
#                 save_products_to_db(user_id, product, save_to_shop)

#                 print(f"[DEBUG] Added product: {title_en} (Price: {price_usd} USD)")

#             except Exception as e:
#                 print(f"[ERROR] Error processing product card on Wildberries: {e}")

#     except Exception as e:
#         print(f"[ERROR] Error waiting for elements on Wildberries: {e}")



# def parse_amazon_products(driver,user_id, products, shopping_budget, save_to_shop=False):
#     """
#     Parses products from the Amazon website and adds them to the product list.
#     """
#     try:
#         WebDriverWait(driver, 15).until(
#             EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.s-main-slot div.s-result-item"))
#         )
#         print("[DEBUG] Product cards successfully loaded on Amazon.")

#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         items = soup.select("div.s-main-slot div.s-result-item")
#         print(f"[DEBUG] Found {len(items)} product cards on Amazon.")

#         for item in items:
#             try:
#                 link_element = item.select_one("a.a-link-normal.s-link-style")
#                 title = link_element.text.strip() if link_element else "Unknown Product"

#                 link = link_element["href"] if link_element else "#"
#                 if not link.startswith("http"):
#                     link = f"https://www.amazon.com{link}"

#                 img_element = item.select_one("img.s-image")
#                 image_url = img_element["src"] if img_element else "/static/images/default-product.jpg"

#                 price_element = item.select_one("span.a-price > span.a-offscreen")
#                 price_value = extract_price(price_element.text.strip()) if price_element else None

#                 if price_value and not is_within_budget(price_value, shopping_budget):
#                     continue

#                 brand_element = item.select_one("h5.s-line-clamp-1 span")
#                 brand = brand_element.text.strip() if brand_element else "Unknown Brand"

#                 product = {
#                     "title": title[:255],
#                     "price": price_value,
#                     "description": "Amazon Product",
#                     "image_url": image_url[:255],
#                     "link": link[:255],
#                     "brand": brand[:100]
#                 }

#                 products.append(product)
#                 save_products_to_db(user_id, product, save_to_shop)

#             except Exception as e:
#                 print(f"[ERROR] Error processing product card on Amazon: {e}")

#     except Exception as e:
#         print(f"[ERROR] Error processing Amazon website: {e}")



# def parse_aliexpress_products(driver, products, shopping_budget):
#     """
#     Parses products from the AliExpress website and adds them to the product list.
#     """
#     try:
#         WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, "div.red-snippet_RedSnippet__container__hyohn9"))
#         )
#         print("[DEBUG] Product cards successfully loaded on AliExpress.")

#         time.sleep(5)

#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         items = soup.select("div.red-snippet_RedSnippet__container__hyohn9")
#         print(f"[DEBUG] Found {len(items)} product cards on AliExpress.")

#         for item in items:
#             try:
#                 title_element = item.select_one("div.red-snippet_RedSnippet__title__hyohn9")
#                 title = title_element.text.strip() if title_element else "Unknown Product"

#                 link_element = item.select_one("a.red-snippet_RedSnippet__gallery__hyohn9")
#                 link = link_element["href"] if link_element else "#"
#                 if not link.startswith("http"):
#                     link = f"https:{link}"

#                 price_element = item.select_one("div.red-snippet_RedSnippet__priceNew__hyohn9 span")
#                 price_text = price_element.text.strip().replace("$", "") if price_element else None
#                 price_value = float(price_text) if price_text else None

#                 if price_value and not is_within_budget(price_value, shopping_budget):
#                     continue

#                 old_price_element = item.select_one("div.red-snippet_RedSnippet__priceOld__hyohn9 span")
#                 old_price = old_price_element.text.strip().replace("$", "") if old_price_element else "N/A"

#                 img_element = item.select_one("div.gallery_Gallery__picture__15bdcj img")
#                 image_url = img_element["src"] if img_element else "/static/images/default-product.jpg"

#                 products.append({
#                     "title": title,
#                     "price": price_value,
#                     "description": f"Old Price: ${old_price}, Site: AliExpress",
#                     "image_url": image_url,
#                     "link": link,
#                     "brand": "AliExpress"
#                 })
#                 print(f"[DEBUG] Added product: {title}")

#             except Exception as e:
#                 print(f"[ERROR] Error processing product card: {e}")

#     except Exception as e:
#         print(f"[ERROR] Error processing AliExpress website: {e}")


# def parse_zara_products(driver, products, shopping_budget):
#     """
#     Parses products from the Zara website and adds them to the product list.
#     """
#     try:
#         WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, "li.product-grid-product"))
#         )
#         print("[DEBUG] Product cards successfully loaded on Zara.")

#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         items = soup.select("li.product-grid-product")
#         print(f"[DEBUG] Found {len(items)} product cards on Zara.")

#         for item in items:
#             title_element = item.select_one("h2")
#             title = title_element.text.strip() if title_element else "Unknown Product"

#             price_element = item.select_one("div.price .money-amount__main")
#             price_text = price_element.text.strip() if price_element else "N/A"
#             price_value = extract_price(price_text)

#             link_element = item.select_one("a.product-link")
#             link = link_element["href"] if link_element else "#"
#             if not link.startswith("http"):
#                 link = f"https://www.zara.com{link}"

#             img_element = item.select_one("img.media-image__image")
#             image_url = img_element["src"] if img_element and img_element.get("src") else "/static/images/default-product.jpg"

#             if price_value and not is_within_budget(price_value, shopping_budget):
#                 continue

#             products.append({
#                 "title": title,
#                 "price": price_value,
#                 "description": "No description available.",
#                 "image_url": image_url,
#                 "link": link,
#                 "brand": "Zara"
#             })
#             print(f"[DEBUG] Added product: {title}")

#     except Exception as e:
#         print(f"[ERROR] Error processing Zara website: {e}")
#         print("[DEBUG] Page HTML:", driver.page_source[:1000])


# def parse_adidas_products(driver, products, shopping_budget):
#     """
#     Parses products from the Adidas website and adds them to the product list.
#     """
#     try:
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, ".gl-product-card"))
#         )
#         print("[DEBUG] Product cards successfully loaded on Adidas.")

#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         items = soup.select(".gl-product-card")
#         print(f"[DEBUG] Found {len(items)} product cards on Adidas.")

#         for item in items:
#             title_element = item.select_one(".gl-product-card__name")
#             title = title_element.text.strip() if title_element else "Unknown Product"

#             price_element = item.select_one(".gl-product-card__price")
#             price_text = price_element.text.strip() if price_element else "N/A"
#             price_value = extract_price(price_text)

#             img_element = item.select_one("img.gl-product-card__image")
#             image_url = img_element["src"] if img_element and img_element.get("src") else "/static/images/default-product.jpg"

#             link_element = item.select_one("a.gl-product-card__assets-link")
#             link = link_element["href"] if link_element else "#"
#             if not link.startswith("http"):
#                 link = f"https://www.adidas.com{link}"

#             if price_value and not is_within_budget(price_value, shopping_budget):
#                 continue

#             products.append({
#                 "title": title,
#                 "price": price_value,
#                 "description": "No description available.",
#                 "image_url": image_url,
#                 "link": link,
#                 "brand": "Adidas"
#             })
#             print(f"[DEBUG] Added product: {title}")

#     except Exception as e:
#         print(f"[ERROR] Error processing Adidas website: {e}")


# def parse_site_products(user_id, site_name, search_url, shopping_budget=None, query=None, save_to_shop=False):
#     products = []
#     driver = setup_selenium()
#     print(f"[DEBUG] In parse_site_products: site={site_name}, save_to_shop={save_to_shop}")

#     try:
#         if site_name == "Apple":
#             if query is None:
#                 print(f"[DEBUG] Query is required for Apple.")
#                 return products
#             parse_apple_products(driver, user_id, products, shopping_budget, query, save_to_shop)
#         else:
#             print(f"[DEBUG] Opening URL: {search_url}")
#             driver.get(search_url)

#             if site_name == "Nike":
#                 parse_nike_products(driver, user_id, products, shopping_budget, save_to_shop)
#             elif site_name == "Samsung":
#                 parse_samsung_products(driver, user_id, products, shopping_budget, save_to_shop)
#             elif site_name == "Sony":
#                 parse_sony_products(driver, user_id, products, shopping_budget, save_to_shop)
#             elif site_name == "Puma":
#                 parse_puma_products(driver, user_id, products, shopping_budget, save_to_shop)
#             elif site_name == "Wildberries":
#                 parse_wildberries_products(driver, user_id, products, shopping_budget, save_to_shop)
#             elif site_name == "Amazon":
#                 parse_amazon_products(driver, user_id, products, shopping_budget, save_to_shop)
#             elif site_name == "Zara":
#                 parse_zara_products(driver, products, shopping_budget) # Zara parsing, user_id is not passed here as per original code, assuming intentional
#             elif site_name == "AliExpress":
#                 parse_aliexpress_products(driver, products, shopping_budget) # AliExpress parsing, user_id is not passed here as per original code, assuming intentional
#             elif site_name == "Adidas":
#                 parse_adidas_products(driver, products, shopping_budget) # Adidas parsing, user_id is not passed here as per original code, assuming intentional
#             else:
#                 print(f"[DEBUG] Parsing for {site_name} is not implemented.")

#     except Exception as e:
#         print(f"[ERROR] Error processing site {site_name}: {e}")

#     finally:
#         driver.quit()

#     return products