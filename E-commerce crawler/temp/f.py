from flask import Flask, redirect, url_for, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
# data = None

@app.route('/')
def index():
    name = 'jayant'
    return render_template('index.html', name=name)



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        link = request.form["name"]
        # data = user
        data = crawl(link)
        # return redirect(url_for("user", usr=user))

        return render_template('data.html', data=data)
    else:
        return render_template('login.html')

@app.route('/<usr>')
def user(usr):
    # return f"<h2>{usr}</h2>"
    pass


@app.route('/data')
def data():
    return render_template('data.html', data=data)



def crawl(page_link):   
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
    }
    page = requests.get(page_link, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find(id="productTitle")
    price = soup.find(id="priceblock_ourprice")
    available = soup.find(id="availability")
    seller = soup.find(id="sellerProfileTriggerId")
    rating = soup.find_all('span', class_="a-icon-alt")

    print("Product name = ", title.text.strip())
    print("Price = ", price.text.strip())
    print("available = ", available.text.strip())

    details = {
        'title': title.text.strip(),
        'price': price.text.strip(),
        'available': available.text.strip(),
        'seller': seller.text.strip(),
        'rating': rating[0].text.strip(),
    }

    return details


app.run(debug=True)