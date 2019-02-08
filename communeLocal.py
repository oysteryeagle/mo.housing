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

    #title
    title = soup.find('title',text=True).get_text(strip=True).split('-')[0]
    print(title)

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
    with open('urls.txt','r') as f:
        urls = [url.rstrip() for url in f]
        for url in urls:
            findstuff(url)
            print(url)

if __name__ == '__main__':
    main()
