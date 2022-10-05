import requests
from bs4 import BeautifulSoup

from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://<username>:<password>@cluster0.hvkrheo.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

# 주간 만화 베스트 20
data = requests.get('http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf?range=1&kind=0&orderClick=DAA&mallGb=KOR&linkClass=f',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

books = soup.select('#main_contents > ul > li')
#main_contents > ul > li:nth-child(6) > div.detail > div.review > img
for book in books:
    name = book.select_one('div.detail > div.title > a').text
    link = book.select_one('div.detail > div.title > a').get('href')
    star = book.select_one('div.detail > div.review > img').get('alt').split('5점 만점에 ')[1].split('점')[0]
    rank = book.select_one('div.cover > a > strong').text
    writer = book.select_one('div.detail > div.author').text
    a = writer.split('|')[0].strip().split('저자 더보기')

    for a1 in a:
        result = a1.replace("\r\n\t\t\t\t\t\t\r\n\t\t\t\t\t\t\r\n\t\t\t\t\t\r\n\t\t\t\t\t\r\n\t\t\t\t\t\n", "")
        result2 = result.replace("\n\n","")

    pub = writer.split('|')[1].strip()
    price = book.select_one('div.detail > div.price').text.split('도서')[1].strip().split('[10%↓ + 5% 적립]')[0].strip()
    img = book.select_one('div.cover > a > img').get('src')

    doc = {
        'name':name,
        'rank':rank,
        'writer':result2,
        'publisher':pub,
        'price':price,
        'image':img,
        'link':link,
        'star':int(star)
    }
    #db.comicWeekly.insert_one(doc)
    db.comicWeekly.update_one({'rank': rank}, {'$set': doc})

# 주간 소설 베스트20
data = requests.get('http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf?mallGb=KOR&linkClass=B&range=1&kind=0&orderClick=DAb',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

books = soup.select('#main_contents > ul > li')
#main_contents > ul > li:nth-child(6) > div.detail > div.review > img
for book in books:
    name = book.select_one('div.detail > div.title > a').text
    link = book.select_one('div.detail > div.title > a').get('href')
    star = book.select_one('div.detail > div.review > img').get('alt').split('5점 만점에 ')[1].split('점')[0]
    rank = book.select_one('div.cover > a > strong').text
    writer = book.select_one('div.detail > div.author').text
    a = writer.split('|')[0].strip().split('저자 더보기')

    for a1 in a:
        result = a1.replace("\r\n\t\t\t\t\t\t\r\n\t\t\t\t\t\t\r\n\t\t\t\t\t\r\n\t\t\t\t\t\r\n\t\t\t\t\t\n", "")
        result2 = result.replace("\n\n","")

    pub = writer.split('|')[1].strip()
    price = book.select_one('div.detail > div.price').text.split('도서')[1].strip().split('[10%↓ + 5% 적립]')[0].strip()
    img = book.select_one('div.cover > a > img').get('src')
    doc = {
        'name':name,
        'rank':rank,
        'writer':result2,
        'publisher':pub,
        'price':price,
        'image':img,
        'link':link,
        'star':int(star)
    }
    # db.novelWeekly.insert_one(doc)
    db.novelWeekly.update_one({'rank': rank}, {'$set': doc})

# 월간 만화 베스트20
data = requests.get('http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf?mallGb=KOR&linkClass=f&range=1&kind=2&orderClick=DAd',headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

books = soup.select('#main_contents > ul > li')
#main_contents > ul > li:nth-child(6) > div.detail > div.review > img
for book in books:
    name = book.select_one('div.detail > div.title > a').text
    link = book.select_one('div.detail > div.title > a').get('href')
    star = book.select_one('div.detail > div.review > img').get('alt').split('5점 만점에 ')[1].split('점')[0]
    rank = book.select_one('div.cover > a > strong').text
    writer = book.select_one('div.detail > div.author').text
    a = writer.split('|')[0].strip().split('저자 더보기')

    for a1 in a:
        result = a1.replace("\r\n\t\t\t\t\t\t\r\n\t\t\t\t\t\t\r\n\t\t\t\t\t\r\n\t\t\t\t\t\r\n\t\t\t\t\t\n", "")
        result2 = result.replace("\n\n","")

    pub = writer.split('|')[1].strip()
    price = book.select_one('div.detail > div.price').text.split('도서')[1].strip().split('[10%↓ + 5% 적립]')[0].strip()
    img = book.select_one('div.cover > a > img').get('src')
    doc = {
        'name':name,
        'rank':rank,
        'writer':result2,
        'publisher':pub,
        'price':price,
        'image':img,
        'link':link,
        'star':int(star)
    }
    # db.comicMonthly.insert_one(doc)
    db.comicMonthly.update_one({'rank':rank},{'$set':doc})

# 월간 소설 베스트20
data = requests.get('http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf?range=1&kind=2&orderClick=DAB&mallGb=KOR&linkClass=B',headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

books = soup.select('#main_contents > ul > li')
#main_contents > ul > li:nth-child(6) > div.detail > div.review > img
for book in books:
    name = book.select_one('div.detail > div.title > a').text
    link = book.select_one('div.detail > div.title > a').get('href')
    star = book.select_one('div.detail > div.review > img').get('alt').split('5점 만점에 ')[1].split('점')[0]
    rank = book.select_one('div.cover > a > strong').text
    writer = book.select_one('div.detail > div.author').text
    a = writer.split('|')[0].strip().split('저자 더보기')

    for a1 in a:
        result = a1.replace("\r\n\t\t\t\t\t\t\r\n\t\t\t\t\t\t\r\n\t\t\t\t\t\r\n\t\t\t\t\t\r\n\t\t\t\t\t\n", "")
        result2 = result.replace("\n\n","")

    pub = writer.split('|')[1].strip()
    price = book.select_one('div.detail > div.price').text.split('도서')[1].strip().split('[10%↓ + 5% 적립]')[0].strip()
    img = book.select_one('div.cover > a > img').get('src')
    doc = {
        'name':name,
        'rank':rank,
        'writer':result2,
        'publisher':pub,
        'price':price,
        'image':img,
        'link':link,
        'star':int(star)
    }
    # db.novelMonthly.insert_one(doc)
    db.novelMonthly.update_one({'rank':rank},{'$set':doc})

@app.route("/comic/weekly", methods=["GET"])
def web_weekly_get():
    weekly_list = list(db.comicWeekly.find({}, {'_id': False}))
    return jsonify({'best_sellers1': weekly_list})

@app.route("/novel/weekly", methods=["GET"])
def web_novel_weekly_get():
    weekly_list = list(db.novelWeekly.find({}, {'_id': False}))
    return jsonify({'best_sellers1': weekly_list})

@app.route("/comic/monthly", methods=["GET"])
def web_monthly_get():
    monthly_list = list(db.comicMonthly.find({}, {'_id': False}))
    return jsonify({'best_sellers2': monthly_list})

@app.route("/novel/monthly", methods=["GET"])
def web_novel_monthly_get():
    monthly_list = list(db.novelMonthly.find({}, {'_id': False}))
    return jsonify({'best_sellers2': monthly_list})

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/novel')
def novel():
  return render_template('index2.html')


@app.route('/comic')
def comic():
  return render_template('index1.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5003, debug=True)
