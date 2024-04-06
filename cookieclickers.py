from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
import time

URL = "https://orteil.dashnet.org/cookieclicker/"
PRODUCT_PRICE_PREFIX = "productPrice"
PRODUCT_PREFIX = "product"


def word_to_number(word):
    number_dict = {
        "million": 10 ** 6,
        "billion": 10 ** 9,
        "trillion": 10 ** 12,
        "quadrillion": 10 ** 15,
        "quintillion": 10 ** 18,
        "sextillion": (10 ** 21),
        "septillion": (10 ** 24),
        "octillion": (10 ** 27),
        "nonillion": (10 ** 30),
        "decillion": (10 ** 33),
        "undecillion": (10 ** 36),
        "duodecillion": (10 ** 39),
        "tredecillion": (10 ** 42),
        "quattuordecillion": (10 ** 45),
        "quindecillion": (10 ** 48),
        "sexdecillion": (10 ** 51),
        "septendecillion": (10 ** 54),
        "octodecillion": (10 ** 57),
        "novemdecillion": (10 ** 60),
        "vigintillion": (10 ** 63),
        # Add more prefixes as needed
    }

    if "ion" in word:
        word.replace(",", "")
    else:
        for key, value in number_dict.items():
            if key in word:
                return int(word.replace(key, "").strip()) * value

    return word


service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.maximize_window()
driver.get(URL)

WebDriverWait(driver, 10).until(
    ec.presence_of_element_located(
        (By.CSS_SELECTOR, "#langSelect-EN"))
)

english = driver.find_element(By.CSS_SELECTOR, "#langSelect-EN")
english.click()

time.sleep(5)

WebDriverWait(driver, 15).until(
    ec.presence_of_element_located(
        (By.CSS_SELECTOR, "#bigCookie"))
)

WebDriverWait(driver, 10).until(
    ec.presence_of_element_located(
        (By.ID, "cookies"))
)

cookie = driver.find_element(By.CSS_SELECTOR, "#bigCookie")
time.sleep(3)

while True:
    cookie.click()
    cookie_number = driver.find_element(By.ID, "cookies")
    num_text = cookie_number.text
    modified_text = num_text.rsplit("0", 1)[0].rstrip()
    num = int(''.join(filter(str.isdigit, modified_text)))
    print(num)

    for i in range(21):
        try:
            product_price = word_to_number(driver.find_element(By.ID, f"{PRODUCT_PRICE_PREFIX}{i}").text)

            if not product_price.isdigit():
                continue

            product_price = int(product_price)

            if num >= product_price:
                WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located(
                     (By.ID, f"{PRODUCT_PREFIX}{i}"))
                )
                time.sleep(1)
                product = driver.find_element(By.ID, f"{PRODUCT_PREFIX}{i}")
                product.click()
        except NoSuchElementException:
            continue
