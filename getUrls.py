#creates a txt file containing the urls to individual pages on malimalihome.com
import requests
from bs4 import BeautifulSoup
import re
import time
import random
region = input('region:\n1.Macau\n2.Taipa\n3.Coloane\n')
regionnum = {'1':'3','2':'1','3':'6'}
regionname = {'1':'Macau','2':'Taipa','3':'Coloane'}

def main():
    with open(f'urls{regionname[region]}.txt','a+') as f:
        f.seek(0)
        urls = [line.rstrip() for line in f]
        pageNum = 1
        while 1:
            #'http://www.malimalihome.net/residential?status=1&region1=3&page={pageNum}' Macau
            #'http://www.malimalihome.net/residential?status=1&region1=1&page={pageNum}' Taipa   Stopped at 250
            #'http://www.malimalihome.net/residential?status=1&region1=6&page={pageNum}' Coloane
            genericPage = f'http://www.malimalihome.net/residential?status=1&region1={regionnum[region]}&page={pageNum}'
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
            time.sleep(random.uniform(0,1))
if __name__ == '__main__':
    main()
