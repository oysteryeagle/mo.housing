import sqlite3
import requests
from bs4 import BeautifulSoup
import re

TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub('',text)

def findstuff(soup):
    address = soup.find('div',attrs={'class':"view-address"}).getText()
    dic = {'\r':'','\n':'','\xa0':'',' ':''}
    address = replace_all(address,dic)  #return
    #print(address)

    #title
    name = soup.find('title',text=True).get_text(strip=True).split('-')[0]  #return
    #print(name)

    #price(done)
    #for price in soup('span',attrs={'class':"price"}):
    #    prices = re.findall(r'[0-9]+',str(price))
    #    if len(prices)>0:
    #        #print('售價 {} 萬'.format(prices[0]))
    #        price = prices[0]  #return
    pricexml = soup('div',attrs={'class':"view-price-div view-price-red"})
    price = re.findall(r'[0-9]+',str(pricexml))[0]

    #location(done)
    coordinates = None
    for x in soup('script',attrs={'type':"text/javascript"},text=True):
        location = re.findall('google.maps.LatLng\(([0-9]*.[0-9]*, [0-9]*.[0-9]*)\)',str(x))
        if len(location)>0:
            coordinates = location[0]
            lat = coordinates.split(', ')[0]
            long = coordinates.split(', ')[1]
    return (name,address,price,lat,long)
#address(done)
def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

def main():
    tic = 0
    with open('urlsColoane.txt','r') as f:
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        #cur.execute('''DROP TABLE IF EXISTS Housing''')
        urls = [url.rstrip() for url in f]
        for url in urls:
            response = requests.get(url)
            html = response.text
            soup = BeautifulSoup(html,'html.parser')
            try:(name,address,price,lat,long) = findstuff(soup)
            except:continue
            cur.execute('''CREATE TABLE IF NOT EXISTS Housing (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, url TEXT UNIQUE,name TEXT,address TEXT,price INTEGER, coordinates INTEGER
            )''')
            cur.execute('''INSERT OR IGNORE INTO Housing (url,name,address,price,lat,long) VALUES (?,?,?,?,?,?)''',(url,name,address,price,lat,long))
            conn.commit()
            tic += 1
            print(url,name,address,price,lat,long)
            #if tic >= 5:
            #    inp = input('committed')
            #    if inp == '':
            #        tic = 0
            #        pass
            #    if inp == 'quit':
            #        quit()
        conn.close()
if __name__ == '__main__':
    main()
