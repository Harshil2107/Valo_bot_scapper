# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import requests
from bs4 import BeautifulSoup
r= requests.get('https://www.vlr.gg/matches')
print(r)
soup = BeautifulSoup(r.content, 'html.parser')
s = soup.find_all('div', class_= 'ml mod-live')
for lines in s:
    print(lines)
