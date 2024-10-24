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

# List of User-Agents
user_agents = [
    # Add multiple user agents here as strings, example:
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
    # You can add more User-Agents here
]

# Function to randomly select a User-Agent
def get_random_user_agent():
    return random.choice(user_agents) if user_agents else "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"

def searchAmazon(searchedItem):
    options = Options()

    # Apply the selected user agent
    user_agent = get_random_user_agent()
    options.add_argument(f"--user-agent={user_agent}")
    
    # Optional: Headless mode (remove this if you want to see the browser window)
    options.add_argument("--headless")  
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")  

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    # Set geolocation (optional)
    params = {
        "latitude": 45.4215,   
        "longitude": -75.6972, 
        "accuracy": 100
    }
    driver.execute_cdp_cmd("Page.setGeolocationOverride", params)

    # Open Amazon and search for the item
    driver.get("https://www.amazon.ca")
    elem = driver.find_element(By.NAME, "field-keywords")
    elem.clear()
    elem.send_keys(searchedItem)
    elem.send_keys(Keys.RETURN)

    # Try to fetch the top 5 products
    try:
        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CLASS_NAME, "sg-col-4-of-24"))
        )
        topFiveProducts = driver.find_elements(By.CLASS_NAME, "sg-col-4-of-24")
        
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
            collectedItemsContainer.append([productHeaderText, productPrice, productLink, productImage])

        return collectedItemsContainer
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Something went wrong"
    finally:
        time.sleep(1)
        driver.quit()

# Example usage
searched_item = "laptop"
result = searchAmazon(searched_item)
print(result)
