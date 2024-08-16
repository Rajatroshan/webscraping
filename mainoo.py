import requests
from bs4 import BeautifulSoup
import mysql.connector

# MySQL connection setup
def create_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="rajatkumar123",
        database="byte"
    )

# Function to insert data into MySQL
def insert_data(cursor, category, url, ring_name, ring_price, img_url):
    insert_query = """
    INSERT INTO rings (category, url, ring_name, ring_price, img_url)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (category, url, ring_name, ring_price, img_url))

def scrape_ring_details(cursor, category, full_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(full_url, headers=headers)
    if response.status_code != 200:
        print("Failed to retrieve the webpage")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    
    rings = soup.find_all('div', class_='inner pd-gray-bg')
    for ring in rings:
        name_tag = ring.find('h2', class_='p-name')
        ring_name = name_tag.get_text(strip=True) if name_tag else "N/A"
        
        price_tag = ring.find('span', class_='new-price')
        ring_price = price_tag.get_text(strip=True).replace('Rs.', '₹') if price_tag else "N/A"
        
        img_div = ring.find('div', class_='pr-i lazyload-bg')
        img_url = img_div['data-bg'] if img_div and 'data-bg' in img_div.attrs else "N/A"

        print(f"Ring Name: {ring_name}")
        print(f"Ring Price: {ring_price}")
        print(f"Image URL: {img_url}")
        print("-" * 40)
        
        insert_data(cursor, category, full_url, ring_name, ring_price, img_url)

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
    
    connection = create_db_connection()
    cursor = connection.cursor()
    
    menu_items = soup.find_all('div', class_='menu-item')
    for item in menu_items:
        link_tag = item.find('a')
        if link_tag and 'href' in link_tag.attrs:
            full_url = base_url + link_tag['href']
            title_tag = item.find('h2', class_='title')
            category = title_tag.get_text(strip=True) if title_tag else "No Title"
            
            print(f"Category: {category}")
            print(f"URL: {full_url}")
            scrape_ring_details(cursor, category, full_url)
            print("-" * 40)
            print("-" * 40)
    
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == '__main__':
    scrape_bluestone_homepage()
