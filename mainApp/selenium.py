from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import time

import random

user_agents = [
] # enter your own user agent

# Randomly select a User-Agent for each request

def searchAmazon(searchedItem):
    options = Options()
    options.add_argument(f"--user-agent={'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}")
    options.add_argument("--headless") 
    options.add_argument("--disable-gpu") 
    options.add_argument("--window-size=1920x1080")  

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    params = {
        "latitude": 45.4215,   
        "longitude": -75.6972, 
        "accuracy": 100
    }

    driver.execute_cdp_cmd("Page.setGeolocationOverride", params)

    driver.get("https://www.amazon.ca")

    elem = driver.find_element(By.NAME, "field-keywords")
    elem.clear()
    elem.send_keys(searchedItem)  # CHANGE THIS
    elem.send_keys(Keys.RETURN)

    try:
        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CLASS_NAME, "sg-col-4-of-24")) #CHANGE
        )
        topFiveProducts = driver.find_elements(By.CLASS_NAME,"sg-col-4-of-24")
        
        collectedItemsContainer = []

        for product in range(5):
            productHeaderText = topFiveProducts[product].find_element(By.CLASS_NAME, "a-size-base-plus").text
            try:
                productPriceWhole = topFiveProducts[product].find_element(By.CLASS_NAME, "a-price-whole")
                productPriceFraction = topFiveProducts[product].find_element(By.CLASS_NAME, "a-price-fraction")
                productPrice = f"{productPriceWhole.text}.{productPriceFraction.text}"
            except:
                productPrice = "Unavailable"


            productLink = topFiveProducts[product].find_element(By.CLASS_NAME,"s-product-image-container").find_element(By.CLASS_NAME,"a-link-normal").get_attribute("href")
            productImage = topFiveProducts[product].find_element(By.CLASS_NAME,"s-product-image-container").find_element(By.TAG_NAME,"img").get_attribute("src")
            collectedItemsContainer.append([productHeaderText,productPrice,productLink,productImage])
        return collectedItemsContainer
    except:
        return "Something went wrong"
    time.sleep(1)
    driver.quit()