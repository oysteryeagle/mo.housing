from bs4 import BeautifulSoup
import requests

html = requests.get('http://www.malimalihome.net/residential/2939440').text
soup = BeautifulSoup(html,'html.parser')
#title
title = soup.find('title',text=True).get_text(strip=True).split('-')[0]
print(title)
