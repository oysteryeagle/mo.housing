import requests
from bs4 import BeautifulSoup as bs
response = requests.get('http://www.malimalihome.net/residential/2885761')
html = response.text
soup = bs(html,'html.parser')
find = soup.find('div',attrs={'class':"view-address"})
print(type(find))
if type(find) != '''NoneType''':
    print('not')

#http://www.malimalihome.net/residential/2885761    wrong
#http://www.malimalihome.net/residential/2957036    correct
