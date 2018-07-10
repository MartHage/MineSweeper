import urllib.request
from bs4 import BeautifulSoup
page = urllib.request.urlopen('http://minesweeperonline.com/#')
soup = BeautifulSoup(page, 'html.parser')

print(soup.prettify)