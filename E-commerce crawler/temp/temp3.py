import csv
import requests
from bs4 import BeautifulSoup

class Olx:

    name = ''
    details = []

    def __init__(self, name):
        self.name = name

    
    def get_url(self):
        fname = self.name
        fname = fname.replace(' ', '-')
        url = 'https://www.olx.in/items/q-{}?isSearchCall=true'
        url = url.format(fname)
        return url


    def get_soup(self):
        url = self.get_url()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
        }
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        return soup


    def get_details(self):
        soup = self.get_soup()
        items = soup.find_all('li', class_='EIR5N')

        for item in items:

            # Title
            title = item.find('span', class_='_2tW1I').text

            # Price 
            price = item.find('span', class_='_89yzn').text

            # Location
            loc = item.find('span', class_='tjgMj').text

            # Date 
            date = item.find('span', class_='zLvFQ').text

            # Buy link 
            atag = item.find('a', class_='fhlkh')
            link = atag['href']
            link = 'https://www.olx.in' + link
            print(link)
            return

            d = (title, price, loc, date)
            self.details.append(d)

o = Olx('honda bike')
o.get_details()

    # def store_data(self):
    #     with open('temp3.csv', 'w', newline='', encoding='utf-8') as file:
    #         writer = csv.writer(file)
    #         writer.writerow(['Title', 'Price', 'Location', 'Date'])
    #         writer.writerows(self.details)

    #         print("Olx data successfully fetched and stored...")
    
