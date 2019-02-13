import requests
from bs4 import BeautifulSoup
import re
import subprocess
import time

TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub('',text)

def findstuff(url):
#url = input('url: ')
    t = time.time()
    html = requests.get(url).text
    soup = BeautifulSoup(html,'html.parser')
    address = soup.find('div',attrs={'class':"view-address"}).getText()
    dic = {'\r':'','\n':'','\xa0':'',' ':''}
    address = replace_all(address,dic)
    print(f'address: {address}')

    #region
    tabletags = [tag for tag in soup('td',attrs={'class':"td2"})]      #each real estate listing has a table that displays the general information about the listing.
    for n in range(len(tabletags)):
        tabletags[n] = replace_all(remove_tags(str(tabletags[n])),dic)

    region = tabletags[1]                            #the purpose of tabletags is to act as
    print(f'region: {region}')

    #csize
    csize = re.findall(r'([0-9]+)呎',tabletags[6])[0]
    print(f'建築面積: {csize}')

    #rsize
    rsize = re.findall(r'([0-9]+)呎',tabletags[7])[0]
    print(f'實用面積: {rsize}')

    #name
    name = soup.find('title',text=True).get_text(strip=True).split('-')[0]
    print(f'name: {name}')

    #price(done)
    price = re.findall(r'\$([0-9]+)萬',tabletags[8])[0]
    print(f'price: {price}')
    #pricexml = soup('div',attrs={'class':"view-price-div view-price-red"})
    #price = re.findall(r'[0-9]+',str(pricexml))[0]
    #print(f'price: {price}')
    #for price in soup('div',attrs={'class':"view-price-div view-price-red"}):
    #    prices = re.findall(r'[0-9]+',str(price))
    #    if len(prices)>0:
    #        print('售價 {} 萬'.format(prices[0]))

    #pricepsqft
    pricepsqft = re.findall(r'\$([0-9]+.?[0-9]*)元',tabletags[9])[0]
    print(f'pricepsqft: {pricepsqft}')

    #location(done)
    coordinates = '0.0000000000'
    lat = '0.0000000000'
    long = '0.0000000000'
    for x in soup('script',attrs={'type':"text/javascript"},text=True):
        location = re.findall('google.maps.LatLng\(([0-9]*.[0-9]*, [0-9]*.[0-9]*)\)',str(x))
        if len(location)>0:
            x = location[0]
            print(f'''lat = {x.split(', ')[0]}''')
            print(f'''long = {x.split(', ')[1]}''')
            #print(str(location[0]))
    print(time.time()-t)

#address(done)
def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

def main():
    #with open('urlsMacau.txt') as f:
    #    urls = [url.rstrip() for url in f]
    #    for url in urls:
    #        try:findstuff(url)
    #        except KeyboardInterrupt:
    #            raise
    #        except:continue

    findstuff('http://www.malimalihome.net/residential/2121691')

if __name__ == '__main__':
    main()
