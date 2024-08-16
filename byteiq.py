import streamlit as st
import mysql.connector
import requests
from bs4 import BeautifulSoup

# Function to store data in the database
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

# Function to scrape ring details from a given URL
def scrape_ring_details(full_url, title):
    url = full_url
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        st.error("Failed to retrieve the webpage")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    
    rings = soup.find_all('div', class_='inner pd-gray-bg')
    ring_details = []
    for ring in rings:
        name_tag = ring.find('h2', class_='p-name')
        ring_name = name_tag.get_text(strip=True) if name_tag else "N/A"
        
        price_tag = ring.find('span', class_='new-price')
        ring_price = price_tag.get_text(strip=True).replace('Rs.', '₹') if price_tag else "N/A"
        
        img_div = ring.find('div', class_='pr-i lazyload-bg')
        img_url = img_div['data-bg'] if img_div and 'data-bg' in img_div.attrs else "N/A"

        ring_details.append({
            'category': title,
            'name': ring_name,
            'price': ring_price,
            'img_url': img_url
        })
        
        store_data(title, ring_name, ring_price, img_url)
    
    return ring_details

# Function to scrape the Bluestone homepage
def scrape_bluestone_homepage():
    # url = 'https://www.bluestone.com/'
    url=url_input
    base_url = 'https://www.bluestone.com'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        st.error("Failed to retrieve the webpage")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    
    menu_items = soup.find_all('div', class_='menu-item')
    all_ring_details = []
    for item in menu_items:
        link_tag = item.find('a')
        if link_tag and 'href' in link_tag.attrs:
            full_url = base_url + link_tag['href']
            title_tag = item.find('h2', class_='title')
            title = title_tag.get_text(strip=True) if title_tag else "No Title"
            
            ring_details = scrape_ring_details(full_url, title)
            all_ring_details.extend(ring_details)
    
    return all_ring_details

# Function to retrieve all rows from the database
def retrieve_data():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='rajatkumar123',
        database='bluestone'
    )
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM jewellery")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows

# Streamlit UI
st.title("Bluestone Jewellery Scraper")
url_input = st.text_input("Enter a URL:")
if st.button("Scrape Bluestone"):
    with st.spinner('Scraping data...'):
        jewellery_data = scrape_bluestone_homepage()
    
    if jewellery_data:
        for jewellery in jewellery_data:
            st.write(f"**Category:** {jewellery['category']}")
            st.write(f"**Jewellery Name:** {jewellery['name']}")
            st.write(f"**Jewellery Price:** {jewellery['price']}")
            st.write(f"**Image URL:** {jewellery['img_url']}")
            if jewellery['img_url'] != "N/A":
                st.image(jewellery['img_url'], caption=jewellery['name'])
            st.write("-" * 40)

if st.button("Show All Data"):
    with st.spinner('Retrieving data from database...'):
        rows = retrieve_data()
    
    if rows:
        for row in rows:
            st.write(f"**ID:** {row[0]}")
            st.write(f"**Category:** {row[1]}")
            st.write(f"**Jewellery Name:** {row[2]}")
            st.write(f"**Jewellery Price:** {row[3]}")
            st.write(f"**Image URL:** {row[4]}")
            if row[4] != "N/A":
                st.image(row[4], caption=row[2])
            st.write("-" * 40)
