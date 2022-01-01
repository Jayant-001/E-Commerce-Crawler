import csv
import requests
from bs4 import BeautifulSoup

name = input("Enter product name: ")
def get_url():
    fname = name
    fname = fname.replace(' ', '%20')
    url = 'https://www.flipkart.com/search?q={}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
    url = url.format(fname)
    url += '&page{}'
    return url


def get_soup(url):
    url = get_url()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup


def get_pages():
    pages = []
    temp = get_url()
    ss = get_soup(temp)
    nav = ss.find_all('nav', class_='yFHi8N')
    links = nav[0].find_all('a', class_='ge-49M')
    
    for link in links:
        l = 'https://www.flipkart.com' + link['href']
        pages.append(l)

    return pages


def get_details():
    data = []
    pages = get_pages()

    for page in pages:
        soup = get_soup(page)
        items = soup.find_all('div', class_='_13oc-S')
        
        for item in items:

            # Title
            title = item.find('div', class_='_4rR01T').text
            
            # Price 
            try:
                price = item.find('div', class_='_30jeq3 _1_WHN1').text
            except AttributeError:
                price = 'price not available'

            # Rating
            try:
                rating = item.find('div', class_='_3LWZlK').text
                rating += ' out of 5'
            except AttributeError:
                rating = "rating not available"

            # Rating number
            try:
                rating_number = item.find('span', class_='_2_R_DZ').text
            except AttributeError:
                rating_number = 'not available'

            # # Offer
            # try:
            #     offer = item.find_all('div', class_='_2ZdXDB')
            #     offer = offer[1].text
            # except AttributeError:
            #     offer = 'offer not available'

            # Buy link
            buy_link = item.find('a', class_='_1fQZEK')
            link = buy_link['href']
            link = 'https://www.flipkart.com' + link
            
            d = (title, price, rating, rating_number, link)
            data.append(d)
    return data


data = get_details()
with open('flipkart.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Product title', 'Product price' 'Product rating', 'Reviews count', 'Buy link'])
    writer.writerows(data)



print("\n\n-------------------------------------------------------------------Data fetched successfully-------------------------------------------------------------------\n\n")
