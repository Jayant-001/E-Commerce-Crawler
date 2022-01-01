import csv
from matplotlib import pyplot as plt

from flipkart import Flipkart
from amazon import Amazon
from olx import Olx



class Crawler:
    product_name = ''

    def crawl(self):
        self.product_name = input("Enter product name:- ")

        # Fetch data from Flipkart and store them into flipkart.csv
        f = Flipkart(self.product_name)
        f.get_details()
        f.store_data()

        # Fetch data from Amazon and store them into amazon.csv
        a = Amazon(self.product_name)
        a.get_details()
        a.store_data()

        # Fetch data from Olx and store them into olx.csv
        o = Olx(self.product_name)
        o.get_details()
        o.store_data()

c = Crawler()
c.crawl()


class DataReader:
    pass

# read data from CSVs files and show them on bar-plot
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

    try:
        amazon_price = int(amazon_price)
    except ValueError:
        print("\nFor '{}' price not avaible on Amazon.in".format(c.product_name))
        amazon_price = 0
    try:
        flipkart_price = int(flipkart_price)
    except ValueError:
        print("\nFor '{}' price not avaible on Flipkart.in".format(c.product_name))
        flipkart_price = 0
    try: 
        olx_price = int(olx_price)
    except ValueError:
        print("\nFor '{}' price not avaible on OLX.in".format(c.product_name))
        olx_price = 0

    data = {'Amazon': amazon_price, 'Flipkart': flipkart_price, 'Olx': olx_price}
    return data


d = get_data()

x = list(d.keys())
y = list(d.values())

plt.title(c.product_name)
plt.xlabel('Websites name')
plt.ylabel('Product price')
plt.bar(x, y)
plt.show()




