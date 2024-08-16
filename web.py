import requests
from bs4 import BeautifulSoup
import csv

def scrape_website():
    url = "https://www.bluestone.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    products = []

    # Find all product elements
    product_elements = soup.find_all('div', class_='product-item')

    for element in product_elements:
        category = element.find('span', class_='category').text.strip()
        product_name = element.find('h2', class_='product-name').text.strip()
        price = element.find('span', class_='price').text.strip()
        image_url = element.find('img', class_='product-image')['src']

        products.append({
            'category': category,
            'product_name': product_name,
            'price': price,
            'image_url': image_url
        })

    # Save to CSV
    with open('scraped_products.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['category', 'product_name', 'price', 'image_url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for product in products:
            writer.writerow(product)

    print(f"Scraped {len(products)} products and saved to scraped_products.csv")

if __name__ == "__main__":
    scrape_website()