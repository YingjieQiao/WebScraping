from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
import matplotlib.style as style
 
tags = []
counts = []

def extract(url):
    html = urlopen(url)
    bsObj = bs(html, features="html.parser")
    
   

    for tag in bsObj.findAll('a',{'class':'post-tag'}):
        tags.append(tag.text)
    for count in bsObj.findAll('span',{'class':'item-multiplier-count'}):
        counts.append(count.text)
    return tags, counts


X = []
y = []

for i in range(1,3):
    url = "https://stackoverflow.com/tags?page=" + str(i) + "&tab=popular"
    extract(url)
    if i == 2:
        X, y = extract(url)

X = X[::-1]
y = y[::-1]
 
plt.figure(1, figsize=(16,16))
bargraph = plt.bar(X,y,width=0.8)
plt.xticks(rotation=270)

plt.show()
