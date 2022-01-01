import csv
import requests
from bs4 import BeautifulSoup

from dataWriter import DataWriter

class Flipkart(DataWriter):

    name = ''
    details = []

    # Taking product name by using a constructor
    def __init__(self, name):
        self.name = name


    # Generate a url
    def get_url(self):
        fname = self.name
        fname = fname.replace(' ', '%20')
        url = 'https://www.flipkart.com/search?q={}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
        url = url.format(fname)
        url += '&page{}'
        return url


    # Generate soup for a given url
    def get_soup(self, url):
        url = self.get_url()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
        }
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        return soup


    # Fetch all products details from first type of page
    def get_details(self):
        print("\n Fetching data on Flipkart.in ...")
        page = self.get_url()

        soup = self.get_soup(page)
        items = soup.find_all('div', class_='_13oc-S')

        for item in items:

            # Title
            try:
                title = item.find('div', class_='_4rR01T').text
            except AttributeError:
                self.get_data(page)
                return

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

            # Buy link
            buy_link = item.find('a', class_='_1fQZEK')
            link = buy_link['href']
            link = 'https://www.flipkart.com' + link
            
            d = (title, price, rating, rating_number, link)
            self.details.append(d)


    # It fetch products details from second type of page
    def get_data(self, page):
        soup = self.get_soup(page)
        items = soup.find_all('div', class_='_4ddWXP')
        
        for item in items:
            
            # Title 
            try:
                title = item.find('a', class_='s1Q9rs').text.strip()
            except AttributeError:
                title = 'Title not available'
            
            # Price
            try:
                price = item.find('div', class_='_30jeq3').text.strip()
            except AttributeError:
                price = 'price not available'
            
            # Rating
            try:
                rating = item.find('div', class_='_3LWZlK').text.strip()
            except AttributeError:
                rating = 'rating not available'
            
            # Reviews
            try:
                review = item.find('span', class_='_2_R_DZ').text.strip()
            except AttributeError:
                review = 'reviews not available'
            
            # Buy link
            link = soup.find('a', class_='_2rpwqI')
            link = 'https://www.flipkart.com' + link['href']
            
            d = (title, price, rating, review, link)
            self.details.append(d)
            

    # Store fetched data into a CSV file
    def store_data(self):

        w = DataWriter("Flipkart.csv")
        rowtitle = ["Product Name", "Price", "Rating", "No. of reviews", "Buy link"]
        w.writer(self.details, rowtitle)