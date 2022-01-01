import csv
from matplotlib import pyplot as plt


def get_data():

    with open('amazon.csv', 'r') as d:
        r = csv.reader(d)
        l = list(r)
        amazon_price = l[1][1]
        amazon_price = amazon_price[3:].replace(',','')
        d.close()


    with open('flipkart.csv', 'r') as d:
        r = csv.reader(d)
        l = list(r)
        flipkart_price = l[1][1]
        flipkart_price = flipkart_price[3:].replace(',','')
        d.close()


    with open('olx.csv', 'r') as d:
        r = csv.reader(d)
        l = list(r)
        olx_price = l[1][1]
        olx_price = olx_price[4:].replace(',','')
        d.close()

    data = {'Amazon': int(amazon_price), 'Flipkart': int(flipkart_price), 'Olx': int(olx_price)}
    return data


d = get_data()

x = list(d.keys())
y = list(d.values())

plt.bar(x, y)
plt.show()


