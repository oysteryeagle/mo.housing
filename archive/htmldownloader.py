import requests
html = requests.get('http://www.malimalihome.net/residential/2935217').text
with open('html4.txt','w+') as f:
    f.write(html)
