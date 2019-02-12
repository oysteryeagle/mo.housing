import sqlite3
import requests
from bs4 import BeautifulSoup
import re

TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub('',text)

def findstuff(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html,'html.parser')
    address = soup.find('div',attrs={'class':"view-address"}).getText()
    dic = {'\r':'','\n':'','\xa0':'',' ':''}
    address = replace_all(address,dic)  #return
    #print(address)

    #region
    tabletags = [tag for tag in soup('td',attrs={'class':"td2"})]
    region = remove_tags(str(tabletags[1]))
    #print(f'region: {region}')

    #name
    name = soup.find('title',text=True).get_text(strip=True).split('-')[0]  #return
    #print(name)

    #price(done)
    pricexml = soup('div',attrs={'class':"view-price-div view-price-red"})
    price = re.findall(r'[0-9]+',str(pricexml))[0]

    #location(done)
    coordinates = '0'
    lat = '0'
    long = '0'
    for x in soup('script',attrs={'type':"text/javascript"},text=True):
        location = re.findall('google.maps.LatLng\(([0-9]*.[0-9]*, [0-9]*.[0-9]*)\)',str(x))
        if len(location)>0:
            coordinates = location[0]
            lat = coordinates.split(', ')[0]
            long = coordinates.split(', ')[1]
    return (name,address,region,price,coordinates,lat,long)
#address(done)
def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

def main():
    with open('urlsMacau.txt','r') as f:
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        #cur.execute('''DROP TABLE IF EXISTS Housing''')
        urls = [url.rstrip() for url in f]
        for url in urls:
            #try:
            (name,address,region,price,coordinates,lat,long) = findstuff(url)
            print(url,name,address,region,price,coordinates,lat,long)
            #except KeyboardInterrupt:
            #    raise
            #except:
            #    print(f'skipped {url}')
            #    continue
            cur.execute('''CREATE TABLE IF NOT EXISTS Housing (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, url TEXT UNIQUE,name TEXT,address TEXT,region TEXT,price INTEGER, coordinates INTEGER
            , lat, long)''')
            cur.execute('''INSERT OR IGNORE INTO Housing (url,name,address,region,price,coordinates,lat,long) VALUES (?,?,?,?,?,?,?,?)''',(url,name,address,region,price,coordinates,lat,long))
            conn.commit()
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
