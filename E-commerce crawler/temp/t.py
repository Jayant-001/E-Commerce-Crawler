# import requests
# from bs4 import BeautifulSoup
# from fake_useragent import UserAgent
# import csv

# url = 'https://www.consumerreports.org/cro/a-to-z-index/products/index.htm'
# user_agent = UserAgent()
# page = requests.get(url)  # , headers={'user-agent': user_agent.chrome}

# soup = BeautifulSoup(page.content, 'html.parser')

# divtags = soup.find_all('div', class_='crux-body-copy')

# print(divtags[0].text)


# with open('product_data.csv', 'a') as csv_file:
#     writer = csv.writer(csv_file)

#     for tag in divtags:
#         # print(tag)
#         name = tag.a.text.strip()
#         link = tag.a['href']
#         # print("{} === {}". format(name, link))
#         writer.writerow([name, link])


# import requests
# from bs4 import BeautifulSoup
# from fake_useragent import UserAgent

# page = requests.get('https://www.amazon.in/Apple-MacBook-16-inch-Storage-2-3GHz/dp/B081JWZSSX/ref=sr_1_1?crid=16RTF9HK3VG8Y&dchild=1&keywords=macbook+pro+16+inch&qid=1611765269&sprefix=mac%2Caps%2C378&sr=8-1')
# user_agent = UserAgent()
# soup = BeautifulSoup(page.content, 'html.parser')

# tag = soup.find_all('td', class_='a-span12')
# print(page)
# for t in tag:
#     print(t)


import csv
import requests
from bs4 import BeautifulSoup

print("Enter Product name to get details")
name = input()
url = 'https://www.amazon.in/s?k={}&ref=nb_sb_noss'
name = name.replace(' ', '+')
url = url.format(name)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
}

page = requests.get(url, headers=headers)

soup = BeautifulSoup(page.content, 'html.parser')


results = soup.find_all('div', {'data-component-type': 's-search-result'})

def get_details():
    data = []
    
    for result in results:

        # title
        atag = result.h2.a
        title = atag.text
        
        # price
        try:
            parent = result.find('span', 'a-price')
            price = parent.find('span', 'a-offscreen').text
        except AttributeError:
            price = 'not available'


        try:
            # rating
            rating = result.i.text
            # number of reviews
            review_count = result.find('span', {'class': 'a-size-base', 'dir': 'auto'}).text
        except AttributeError:
            rating = ''
            review_count = ''
            
        t = (title, price, rating, review_count)
        data.append(t)
    return data

t = get_details()
# print(t)

with open('data.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['title', 'price', 'rating', 'review-count'])
    writer.writerows(t)


