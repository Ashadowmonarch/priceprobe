import requests
from bs4 import BeautifulSoup
import random

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59'
]

def searchAmazon(searchedItem):
    headers = {
        'User-Agent': random.choice(user_agents)
    }

    search_url = f"https://www.amazon.ca/s?k={searchedItem.replace(' ', '+')}"
    response = requests.get(search_url, headers=headers)
    response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code

    soup = BeautifulSoup(response.content, 'html.parser')
    top_five_products = soup.select('.s-main-slot .s-result-item')[:5]

    collectedItemsContainer = []

    for product in top_five_products:
        productHeaderText = product.select_one(".a-size-base-plus")
        productHeaderText = productHeaderText.text.strip() if productHeaderText else "No title"

        productPriceWhole = product.select_one(".a-price-whole")
        productPriceFraction = product.select_one(".a-price-fraction")
        if productPriceWhole and productPriceFraction:
            productPrice = f"{productPriceWhole.text.strip()}.{productPriceFraction.text.strip()}"
        else:
            productPrice = "Unavailable"

        productLink = product.select_one(".s-product-image-container .a-link-normal")
        productLink = f"https://www.amazon.ca{productLink['href']}" if productLink else "No link"

        productImage = product.select_one(".s-product-image-container img")
        productImage = productImage['src'] if productImage else "No image"

        collectedItemsContainer.append([productHeaderText, productPrice, productLink, productImage])

    return collectedItemsContainer

# Example usage