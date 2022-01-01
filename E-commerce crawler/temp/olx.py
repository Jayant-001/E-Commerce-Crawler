import csv
import requests
from bs4 import BeautifulSoup

name = 'honda bike'
name = name.replace(' ', '-')
url = 'https://www.olx.in/items/q-{}?isSearchCall=true'
url = url.format(name)

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
    }

r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.content, 'html.parser')

def get_details():
    items = soup.find_all('li', class_='EIR5N')
    data = []
    for item in items:

        # Title
        title = item.find('span', class_='_2tW1I').text.strip()

        # Price 
        price = item.find('span', class_='_89yzn').text.strip()

        # Location
        loc = item.find('span', class_='tjgMj').text.strip()

        # Date 
        date = item.find('span', class_='zLvFQ').text.strip()

        # Buy link
        parent = item.a
        link = parent['href']
        link = 'https://www.olx.in' + link

        d = (title, price, loc, date, link)
        data.append(d)
    return data
    
d = get_details()

with open('olx.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Price', 'Location', 'Date', 'Buy link'])
    writer.writerows(d)

print("Data fetched")

