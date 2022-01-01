import csv
import requests
from bs4 import BeautifulSoup

aname = input("Enter product name:- ")

def get_url():

    name = aname
    name = name.replace(' ', '+')
    temp = 'https://www.amazon.in/s?k={}&ref=nb_sb_noss'
    url = temp.format(name)
    url += '&page{}'

    return url


def get_pages():
    page_list = []
    temp = get_url()

    for i in range(1):

        if i == 0:
            page_list.append(temp)
        else:
            ss = get_soup(temp)
            nextBtn = ss.find_all('li', class_='a-last')

            next_link = nextBtn[0].a.get('href')
            next_url = get_url().format(next_link)
            temp = next_url
            page_list.append(temp)

    return page_list


def get_soup(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
    }
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


def get_items():
    items = []
    page = get_pages()

    for i in range(len(page)):
        temp = get_soup(page[i])
        item = temp.find_all('div', {'data-component-type': 's-search-result'})
        
        for a in item:
            items.append(a)
    return(items)


def get_details():
    items = get_items()
    details = []
    p_title = ' '
    p_rating = ''
    p_review = '' 
    p_price = ''
    p_delivery_date = ''
    p_delivery_type = ''
    p_link = ''

    for item in items:

        # Title
        title = item.h2.a.text
        p_title = title.strip()

        # Rating
        try:
            rating = item.find('span', class_='a-icon-alt')
            p_rating = rating.text
        except AttributeError:
            p_rating = 'rating not available'

        # Review count
        try:
            review = item.find('span', class_='a-size-base')
            p_review = review.text
        except AttributeError:
            p_review = 'review not available'

        # Price
        try:
            parent = item.find('span', class_="a-price")
            price = parent.find('span', class_='a-offscreen')
            p_price = price.text
        except AttributeError:
            p_price = 'price not available'

        # Delivery Date 
        try:
            delivery_date = item.find('span', class_='a-text-bold')
            p_delivery_date = delivery_date.text
        except AttributeError:
            p_delivery_date = 'delivery date not available'

        # Delivery type
        try:
            delivery_type = item.find('span', {"aria-label": "FREE Delivery by Amazon"})
            p_delivery_type = delivery_type.text.strip()
        except:
            try:
                delivery_type = item.find('span', {"aria-label": "FREE Delivery over ₹499. Fulfilled by Amazon."})
                p_delivery_type = delivery_type.text.strip()
            except AttributeError:
                p_delivery_type = "Delivery type not available"

        # Buy link
        parent = item.h2.a
        title_link = parent.get('href')
        buy_link = "https://www.amazon.in/" + title_link
        p_link = buy_link

        d = (p_title, p_price, p_rating, p_review, p_delivery_date, p_delivery_type, p_link)
        details.append(d)

    return details
    

data = get_details()

with open('amazon.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Title', 'Price', 'Rating', 'Reviews', 'Delivery date', 'Delivery type', 'Product link'])
    writer.writerows(data)




print("\n\n-------------------------------------------------------------------Amazon Data fetched successfully-------------------------------------------------------------------\n\n")
