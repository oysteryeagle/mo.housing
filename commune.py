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
    html = requests.get(url).text
    soup = BeautifulSoup(html,'html.parser')
    address = soup.find('div',attrs={'class':"view-address"}).getText()
    dic = {'\r':'','\n':'','\xa0':'',' ':''}
    address = replace_all(address,dic)
    print(address)

    #region
    #region = soup.find('th',text='地區:')
    #region = soup.find('td',attrs={'class':"td2"})
    #print(region)

    #name
    name = soup.find('title',text=True).get_text(strip=True).split('-')[0]
    print(name)

    #price(done)
    t = time.time()
    pricexml = soup('div',attrs={'class':"view-price-div view-price-red"})
    price = re.findall(r'[0-9]+',str(pricexml))[0]
    print(price)
    print(time.time()-t)
    #for price in soup('div',attrs={'class':"view-price-div view-price-red"}):
    #    prices = re.findall(r'[0-9]+',str(price))
    #    if len(prices)>0:
    #        print('售價 {} 萬'.format(prices[0]))


    #location(done)
    for x in soup('script',attrs={'type':"text/javascript"},text=True):
        location = re.findall('google.maps.LatLng\(([0-9]*.[0-9]*, [0-9]*.[0-9]*)\)',str(x))
        if len(location)>0:
            x = location[0]
            print(f'''lat = {x.split(', ')[0]}''')
            print(f'''long = {x.split(', ')[1]}''')
            #print(str(location[0]))

#address(done)
def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

def main():
    #with open('urlsTaipa.txt','r') as f:
    #    urls = [url.rstrip() for url in f]
    #    for url in urls:
    #        findstuff(url)
    #        print(url)
    findstuff('http://www.malimalihome.net/residential/2351203')

if __name__ == '__main__':
    main()
