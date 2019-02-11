import requests
from bs4 import BeautifulSoup
import re
import subprocess

TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub('',text)
SPACES = re.compile(r' ')
def remove_spaces(text):
    return SPACES.sub('',text)
def findstuff(url):
#url = input('url: ')
    html = requests.get(url).text
    soup = BeautifulSoup(html,'html.parser')
    address = soup.find('div',attrs={'class':"view-address"}).getText()
    dic = {'\r':'','\n':'','\xa0':'',' ':''}
    address = replace_all(address,dic)
    print(address)

    #price(done)
    for price in soup('span',attrs={'class':"price"}):
        prices = re.findall(r'[0-9]+',str(price))
        if len(prices)>0:
            print('售價 {} 萬'.format(prices[0]))

    #location(done)
    for x in soup('script',attrs={'type':"text/javascript"},text=True):
        location = re.findall('google.maps.LatLng\(([0-9]*.[0-9]*, [0-9]*.[0-9]*)\)',str(x))
        if len(location)>0:
            print('location: {}'.format(location[0]))
#address(done)
def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text
def main():
    firstPage = 'http://www.malimalihome.net/residential?status=1&photo=1&orderby=2'
    urls = list()
    html = requests.get(firstPage).text
    for url in re.findall('http://www.malimalihome.net/residential/[0-9]+',html):
        if url not in urls:
            urls.append(url)
    for url in urls:
        findstuff(url)
    pageNum = 2
    while 1:
        urls = list()
        genericPage = f'http://www.malimalihome.net/residential?status=1&photo=1&orderby=2&page={pageNum}'
        html = requests.get(genericPage).text
        for url in re.findall('http://www.malimalihome.net/residential/[0-9]+',html):
            if url not in urls:
                urls.append(url)
        pageNum += 1
        for url in urls:
            findstuff(url)
        print()

if __name__ == '__main__':
    main()
