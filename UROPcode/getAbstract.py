import requests
from bs4 import BeautifulSoup as bs
import ssl


abstracts = {}

def getAbstracts(url):
    global abstracts
    
    # https://www.sciencedirect.com/science/article/pii/S0043135419301794
    # https://api.elsevier.com/content/article/pii/S0043135419301794
    # ?APIKey=ca5ec889b2aa7089a5e27c277cea8e90
    
    html = requests.get(url)
    bsObj = bs(html.content, features='lxml')
    
    title = bsObj.find('dc:title').text
    abstract = bsObj.find('dc:description').text
    abstract = abstract.replace('Abstract', ' ').strip()

    abstracts[title] = abstract
    
    return None


address = 'https://api.elsevier.com/content/article/pii/S0043135419301794?APIKey=ca5ec889b2aa7089a5e27c277cea8e90'
getAbstracts(address)
print(abstracts)

'''

print(title)
abstract = getAbstracts(address)[1]
print(abstract)
'''