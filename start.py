import json
import re
import time
import asyncio
import mysql.connector
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from telegram import Bot

# ChromeDriver-ის ადგილმდებარეობა
chrome_driver_path = "/opt/homebrew/bin/chromedriver"

# Selenium-ის ბრაუზერის ინიციალიზაცია
service = Service(chrome_driver_path)
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome(service=service, options=options)

# Telegram ბოტის ინიციალიზაცია
TOKEN = '6869078564:AAFMqy2lL1psQ-IUX6zMX5rcv252rNnRLkU'
CHAT_ID = '-1002246849151'
bot = Bot(token=TOKEN)

# Connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mamukia",
    database="parser"
)
cursor = connection.cursor(dictionary=True)

# პროდუქტის განახლება MySQL-ში
def update_product(brand, name, photo, price, formated_price, link, product_id):
    sql = """
    UPDATE product
    SET brand = %s, name = %s, photo = %s, price = %s, formated_price = %s, link = %s
    WHERE product_id = %s
    """
    values = (brand, name, photo, price, formated_price, link, product_id)
    cursor.execute(sql, values)
    connection.commit()

# პროდუქტის MySQL მონაცემთა ბაზაში ჩასმა
def insert_product(brand, name, photo, price, formated_price, link, product_id):
    sql = """
    INSERT INTO product (product_id, brand, name, photo, price, formated_price, link)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (product_id, brand, name, photo, price, formated_price, link)
    cursor.execute(sql, values)
    connection.commit()

# ფუნქცია, რომელიც მოძებნის ინფორმაციას product_id-ის მიხედვით
def find_product_by_id(product_id):
    cursor.execute("SELECT * FROM product WHERE product_id = %s", (product_id,))
    result = cursor.fetchone()
    cursor.fetchall()  # თუ დარჩა წაუკითხავი შედეგები, გაუქმება
    return result

# Telegram ბოტის ინიციალიზაცია
TOKEN = '6869078564:AAFMqy2lL1psQ-IUX6zMX5rcv252rNnRLkU'  # შეცვალე შენი ბოტის ტოკენით
CHAT_ID = '-1002246849151'  # შეცვალე შენი ჯგუფის ID-თი
bot = Bot(token=TOKEN)

async def send_product_to_telegram(brand, name, price, old_price, sale, link, photo):
    try:
        message = (
            f"Бренд: {brand}\n"
            f"Продукт: {name}\n"
            f"Цена: {price}\n"
            f"Старая цена: {old_price}\n"
            f"Скидка: - {sale:.2f} %\n"
            f"{link}"
        )
        # Attempt to send the product photo with the caption
        try:
            await bot.send_photo(chat_id=CHAT_ID, photo=photo, caption=message)
        except Exception as e:
            print(f"შეცდომა ფოტოს გაგზავნისას: {e}")

        await asyncio.sleep(1)
    except Exception as e:
        print(f"შეცდომა შეტყობინების გაგზავნისას: {e}")

def clean_price(price_text):
    # Remove spaces and non-digit characters
    return ''.join(filter(str.isdigit, price_text))

# პროდუქციის მონაცემების მოძიების ფუნქცია
def scrape_products(browser):
    items = browser.find_elements(By.CSS_SELECTOR, 'div.product-card__wrapper')

    for item in items:
        try:
            brand = item.find_element(By.CSS_SELECTOR, 'span.product-card__brand').text
            name = item.find_element(By.CSS_SELECTOR, 'span.product-card__name').text
            photo = item.find_element(By.CSS_SELECTOR, 'img.j-thumbnail').get_attribute('src')

            try:
                price = item.find_element(By.CSS_SELECTOR, 'ins.price__lower-price').text
            except:
                price = 'Price not found'

            link = item.find_element(By.CSS_SELECTOR, 'a.product-card__link.j-card-link.j-open-full-product-card').get_attribute('href')
            match = re.search(r'/catalog/(\d+)/', link)
            if match:
                product_id = match.group(1)

            formated_price = clean_price(price)

            found_product = find_product_by_id(product_id)

            if found_product:
                numeric_price = found_product['formated_price']
                percent = (numeric_price * 50) / 100

                print(f"პროცენტი: {percent}, numeric_formated_price: {numeric_price}")

                if percent > float(formated_price):
                    sale = ((numeric_price - float(formated_price)) / numeric_price) * 100
                    print("sent")
                    asyncio.run(send_product_to_telegram(brand, name, price, found_product['price'], sale, link, photo))

                update_product(brand, name, photo, price, formated_price, link, product_id)
            else:
                insert_product(brand, name, photo, price, formated_price, link, product_id)

        except Exception as e:
            print(f"შეცდომა მონაცემების ამოღებისას: {e}")

# მონაცემების ჩამოტვირთვა ვებ-გვერდიდან და MySQL-ში ჩასმა
all_products = []
with open('categories.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    for entry in data:
        base_url = entry.get('url')
        if base_url:
            full_url = f"https://www.wildberries.ru{base_url}?sort=popular"
            for page in range(1, 10):
                url = f"{full_url}&page={page}"
                print(f"ვკრეფთ მონაცემებს გვერდიდან {page}: {url}")
                browser.get(url)
                time.sleep(2)
                scrape_products(browser)

# ბრაუზერის დახურვა
browser.quit()
cursor.close()
connection.close()

print("პროდუქტების მონაცემები წარმატებით შეინახა MySQL-ში!")