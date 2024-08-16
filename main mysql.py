import requests
from bs4 import BeautifulSoup
import mysql.connector

def store_data(category, jewellery_name, jewellery_price, img_url):
    connection = mysql.connector.connect(
        host='localhost',
        user='root', 
        password='rajatkumar123',  
        database='bluestone'
    )
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO jewellery (category, jewellery_name, jewellery_price, img_url) VALUES (%s, %s, %s, %s)",
        (category, jewellery_name, jewellery_price, img_url)
    )
    connection.commit()
    cursor.close()
    connection.close()

def scrape_ring_details(full_url, title):
    url = full_url
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to retrieve the webpage")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    
    rings = soup.find_all('div', class_='inner pd-gray-bg')
    for ring in rings:
        name_tag = ring.find('h2', class_='p-name')
        if name_tag:
            ring_name = name_tag.get_text(strip=True)
        else:
            ring_name = "N/A"
        
        price_tag = ring.find('span', class_='new-price')
        if price_tag:
            ring_price = price_tag.get_text(strip=True).replace('Rs.', '₹')
        else:
            ring_price = "N/A"
        
        img_div = ring.find('div', class_='pr-i lazyload-bg')
        if img_div and 'data-bg' in img_div.attrs:
            img_url = img_div['data-bg']
        else:
            img_url = "N/A"

        print(f"jewellery Name: {ring_name}")
        print(f"jewellery Price: {ring_price}")
        print(f"Image URL: {img_url}")
        print("-" * 40)
        
        store_data(title, ring_name, ring_price, img_url)

def scrape_bluestone_homepage():
    url = 'https://www.bluestone.com/'
    base_url = 'https://www.bluestone.com'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to retrieve the webpage")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    
    menu_items = soup.find_all('div', class_='menu-item')
    for item in menu_items:
        link_tag = item.find('a')
        if link_tag and 'href' in link_tag.attrs:
            full_url = base_url + link_tag['href']
            title_tag = item.find('h2', class_='title')
            if title_tag:
                title = title_tag.get_text(strip=True)
            else:
                title = "No Title"
            
            print(f"Title: {title}")
            print(f"URL: {full_url}")
            scrape_ring_details(full_url, title)
            print("-" * 40)
            print("-" * 40)

if __name__ == '__main__':
    scrape_bluestone_homepage()
