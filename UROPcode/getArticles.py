#from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup as bs
import ssl

address = 'https://www.journals.elsevier.com/water-research/most-downloaded-articles'
articles = []

def getArtciels(url):
    global artciles
    
    html = requests.get(url)
    bsObj = bs(html.content, features='html.parser')
    
    for link in bsObj.findAll('a'):
        if 'href' in link.attrs:
            rawlink = link.attrs['href']
            if rawlink.startswith('https://www.sciencedirect.com/science/article/pii/'):
                articles.append(rawlink)
    
    return None

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
         
getArtciels(address)
#print(articles)

#####----------working well so far----------#####

abstracts = {}

def getAbstracts(url):
    global abstracts
    
    html = requests.get(url)
    bsObj = bs(html.content, features='html.parser')
    print(bsObj.find('h1',{'id':'screen-reader-main-title'}).attrs)
    
    return None

getAbstracts(articles[0])

