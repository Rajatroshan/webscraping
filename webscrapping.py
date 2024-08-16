import requests 
from bs4 import BeautifulSoup

url="https://www.bluestone.com/"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

r=requests.get(url,headers=headers)
soup=BeautifulSoup(r.content,'html.parser')
#print(soup.prettify())
# a_tags = soup.find_all('a')
# for a_tag in a_tags:
#     print(a_tag.get_text(strip=True))
categories = soup.find_all('a', class_='category')
for category in categories:
    print(category.get_text(strip=True))