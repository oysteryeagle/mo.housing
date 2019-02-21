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
    tabletags = [tag for tag in soup('td',attrs={'class':"td2"})]      #each real estate listing has a table that displays the general information about the listing.
    for n in range(len(tabletags)):
        tabletags[n] = replace_all(remove_tags(str(tabletags[n])),dic)
    region = tabletags[1] #return

    #csize
    csize = re.findall(r'([0-9]+)呎',tabletags[6]) #return
    if len(csize)>0:
        csize = csize[0]
    else:csize = 'NULL'

    #rsize
    rsize = re.findall(r'([0-9]+)呎',tabletags[7])
    if len(rsize)>0:
        rsize = rsize[0]
    else:
        rsize = 'NULL'

    #name
    name = soup.find('title',text=True).get_text(strip=True).split('-')[0]  #return

    #price(done)
    price = re.findall(r'\$([0-9]+)萬',tabletags[8])[0] #return

    #pricepsqft
    pricepsqft = re.findall(r'\$([0-9]+.?[0-9]*)元',tabletags[9]) #return
    if len(pricepsqft)>0:
        pricepsqft = pricepsqft[0]
    else:
        pricepsqft = 'NULL'

    #location(done)
    coordinates = '0.0000000000'
    lat = '0.0000000000'
    long = '0.0000000000'
    for x in soup('script',attrs={'type':"text/javascript"},text=True):
        location = re.findall('google.maps.LatLng\(([0-9]*.[0-9]*, [0-9]*.[0-9]*)\)',str(x))
        if len(location)>0:
            coordinates = location[0]
            lat = coordinates.split(', ')[0]
            long = coordinates.split(', ')[1]
    return (name,address,region,csize,rsize,price,pricepsqft,coordinates,lat,long)
#address(done)
def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

def main():
    with open('urlsColoane.txt','r') as f:
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        #cur.execute('''DROP TABLE IF EXISTS Housing''')
        urls = [url.rstrip() for url in f]
        for url in urls:
            try:
                (name,address,region,csize,rsize,price,pricepsqft,coordinates,lat,long) = findstuff(url)
                print(url,name,address,region,csize,rsize,price,pricepsqft,coordinates,lat,long)
            except KeyboardInterrupt:
                raise
            except:
                print(f'skipped {url}')
                continue
            cur.execute('''CREATE TABLE IF NOT EXISTS Housing (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, url TEXT UNIQUE,name TEXT,address TEXT,
            region TEXT,csize INTEGER,rsize INTEGER,price INTEGER,pricepsqft FLOAT,coordinates INTEGER
            , lat, long)''')
            cur.execute('''INSERT OR IGNORE INTO Housing (url,name,address,
            region,csize,rsize,price,pricepsqft,coordinates,lat,long) VALUES
             (?,?,?,?,?,?,?,?,?,?,?)''',(url,name,address,region,csize,rsize,price,pricepsqft,coordinates,lat,long))
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
