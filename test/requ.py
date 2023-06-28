import requests
from bs4 import BeautifulSoup

URL = 'https://musescore.com/user/12461571/scores/3291706'

res = requests.get(URL)

soup = BeautifulSoup(res.content, 'html.parser')

with open('htmll.txt', 'wb') as f:
    f.write(soup.encode_contents())
