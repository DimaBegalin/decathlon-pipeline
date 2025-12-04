# src/scraper.py
import time, json, logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("scraper")

CHROME_DRIVER_PATH = None

def create_driver(headless=True):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument("--remote-debugging-port=9222")
    service = Service(CHROME_DRIVER_PATH) if CHROME_DRIVER_PATH else Service()
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def collect_all_product_links(driver, start_url, max_pages=20):
    driver.get(start_url)
    wait = WebDriverWait(driver, 10)

    all_links = set()
    page = 1

    while page <= max_pages:
        time.sleep(2)

        # Собираем карточки товаров
        cards = driver.find_elements(By.CSS_SELECTOR, "a.block.px-4[data-discover='true']")
        for c in cards:
            try:
                href = c.get_attribute("href")
                if href:
                    all_links.add(href)
            except:
                pass

        print(f"[INFO] Page {page}: Collected {len(all_links)} links.")

        # --- Ищем кнопку следующей страницы ---  
        try:
            wait = WebDriverWait(driver, 10)
            # Находим кнопку со стрелкой вправо по уникальному классу или svg
            next_btn = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button.vtmn-btn svg path[d='M9 18L15 12L9 6']")
                )
            )

            # Прокручиваем до кнопки
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_btn)
            time.sleep(0.5)

            # Кликаем button
            next_btn.find_element(By.XPATH, "./ancestor::button").click()

            # Ждём обновление карточек
            wait.until(EC.staleness_of(cards[0]))
            page += 1
            continue

        except Exception:
            print("[INFO] The <Next Page> button was not found. Stopping.")
            break

    return list(all_links)

def scrape_list_page(start_url, headless=True, min_items=150):
    driver = create_driver(headless=headless)
    logger.info("Opening %s", start_url)

    product_links = collect_all_product_links(driver, start_url)
    logger.info("Collected %d product links", len(product_links))

    results = []
    count = 1
    for link in product_links:
        try:
            driver.get(link)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
            )

            # Название товара
            try:
                name = driver.find_element(By.CSS_SELECTOR, "h1.vtmn-typo_title-3").text.strip()
            except:
                name = ""

            # Цена
            try:
                price = driver.find_element(By.CSS_SELECTOR, "span.vtmn-price_variant--accent").text.strip()
            except:
                price = ""

            # SKU
            try:
                sku_elem = driver.find_elements(By.CSS_SELECTOR, "span.vtmn-typo_text-3.text-grey")
                sku = sku_elem[0].text.strip() if sku_elem else ""
            except:
                sku = ""

            # Ссылка на основное изображение
            try:
                img_elem = driver.find_elements(By.CSS_SELECTOR, "img.max-h-full.max-w-full")
                image = img_elem[0].get_attribute("src") if img_elem else ""
            except:
                image = ""

            results.append({
                "url": link,
                "name": name,
                "price": price,
                "sku": sku,
                "image": image
            })
            # --- Print product info to console ---
            logger.info(f"[PRODUCT - {count}] | Name: {name}")
        except Exception as e:
            logger.exception("Error parsing %s: %s", link, e)

        # Прерываем, если набрали минимальное количество товаров
        if len(results) >= min_items:
            break

    driver.quit()

    # Сохраняем в JSON
    with open("data/raw.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    logger.info("Scraping finished. Total items collected: %d", len(results))
    return results

if __name__ == "__main__":
    start = "https://decathlon.kz/142-futbol"
    scrape_list_page(start, headless=False, min_items=150)
