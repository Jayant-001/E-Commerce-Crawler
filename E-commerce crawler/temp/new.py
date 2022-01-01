import csv
from bs4 import BeautifulSoup
from selenium import webdriver


chromedriver = ".\chromedriver"
driver = webdriver.Chrome(chromedriver)
# driver.get("https://www.amazon.com")


def get_url(search_term):
    temp = 'https://www.amazon.in/s?k={}&ref=nb_sb_noss'
    # temp = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss_2'
    search_term = search_term.replace(' ', '+')

    # add term query to url
    url1 = temp.format(search_term)

    #add page query placeholder
    url1 += '&page{}'

    # return temp.format(search_term)
    return url1

p_url = get_url("redmi k20")
# print(p_url)

driver.get(p_url)

soup = BeautifulSoup(driver.page_source, 'html.parser')

# print(soup.find(id="productTitle"))

results = soup.find_all('div', {'data-component-type': 's-search-result'})


# prototype the record
item = results[0]
atag = item.h2.a
description = atag.text.strip()
url = 'https://www.amazon.com' + atag.get('href')

# print(url)
# print('---')
# print(atag.get('href'))


# geting price
price_parent = item.find('span', 'a-price')
price = price_parent.find('span', 'a-offscreen').text
# print(price)


# geting review
rating = item.i.text
review_count = item.find('span', {'class': 'a-size-base', 'dir': 'auto'}).text
# print(rating, review_count)


# Generalized the pattern
def extract_record(item):

    # description and url
    atag = item.h2.a
    description = atag.text.strip()
    url = 'https://www.amazon.com' + atag.get('href')
    
    try:
        # price
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text
    except AttributeError:
        return 

    try:
        # rank and rating
        rating = item.i.text
        review_count = item.find('span', {'class': 'a-size-base', 'dir': 'auto'}).text
    except AttributeError:
        rating = ''
        review_count = ''

    results = (description, price, rating, review_count, url)

    return results

records = []
result = soup.find_all('div', {'data-component-type': 's-search-result'})

for i in results:
    record = extract_record(i)
    if record:
        records.append(record)


print(records[0])
print('---')
# for row in records:
#     print(row[0], '--', row[1])



