#creates a txt file containing the urls to individual pages on malimalihome.com
import requests
from bs4 import BeautifulSoup
import re

def main():
    with open('urls.txt','a+') as f:
        f.seek(0)
        urls = [line.rstrip() for line in f]
        pageNum = 1
        while 1:
            genericPage = f'http://www.malimalihome.net/residential?status=1&region1=3&page={pageNum}'
            print(f'requesting {genericPage}')
            response = requests.get(genericPage)
            if response.status_code != 200:
                print('status code not 200')
                quit()
            html = response.text
            for url in re.findall('http://www.malimalihome.net/residential/[0-9]+',html):
                if url not in urls:
                    urls.append(url)
                    f.write(f'{url}\n')
                    print('POSITIVE',url)
                else:
                    print('NEGATIVE',url)
            pageNum += 1
if __name__ == '__main__':
    main()
