#pip install lxml
#pip install pyOpenSSL
import requests
import json
from bs4 import BeautifulSoup as bs
import ssl
import time

'''
The elsevier search is kind of a tree structure:
"keyword --> a list of journals (a journal contain many articles) --> lists of articles
'''


journals = []
articles = []
abstracts = {}
years = ['1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']


def getJournals(url):
    global journals
    
    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    html = requests.get(url)
    data = json.loads(html.content)# response is in json format so we load it into a dictionary
    hits = data['hits']['hits']# target urls are hidden deep inside nested dictionaries and lists
    for hit in hits:
        journals.append(str(hit['_source']['url']+'/most-downloaded-articles'))

    return None

def getArtciels(url):
    global artciles
    
    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    html = requests.get(url)
    bsObj = bs(html.content, features='html.parser')
    
    for link in bsObj.findAll('a'):
        if 'href' in link.attrs:
            rawlink = link.attrs['href']
            if rawlink.startswith('https://www.sciencedirect.com/science/article/pii/'):
                articles.append(rawlink)
    
    return None

    
    
    
    
def getAbstracts(url):
    global abstracts
    global years
    
    # https://www.sciencedirect.com/science/article/pii/S0043135419301794
    # https://api.elsevier.com/content/article/pii/S0043135419301794
    # ?APIKey=ca5ec889b2aa7089a5e27c277cea8e90
    
    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    html = requests.get(url)
    bsObj = bs(html.content, features='lxml')
    
    if bsObj.find('dc:title').text and bsObj.find('dc:identifier').text and bsObj.find('dc:identifier').text[-11:-7] in years:
        title = bsObj.find('dc:title').text
        abstract = bsObj.find('dc:description').text
        abstract = abstract.replace('Abstract', ' ').strip()
        iden = bsObj.find('dc:identifier').text
        
        preKey = iden[-11:-7] + title
        abstracts[preKey] = abstract
        
        
    else:
        pass
    
    return None


start = time.time()



# Search a key word
pre_keyword = input("Please type in your keyword: ")
# https://site-search-api.prod.ecommerce.elsevier.com/search?
# query=catalyst%20for%20water%20splitting&labels=journals&start=0&limit=10&lang=en-xs
keyword = pre_keyword.replace(' ', '%20')
address = 'https://site-search-api.prod.ecommerce.elsevier.com/search?query=' + keyword + '&labels=journals&start=0&limit=800&lang=en-xs'
######################################################################################
####### increase the number following "&limit=" to increase the number of URLs #######
######################################################################################

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
    
getJournals(address)

for url in journals:
    getArtciels(url)

for article in articles:
    link = 'https://api.elsevier.com/content/article/pii/' + article[-17::] + '?APIKey=ca5ec889b2aa7089a5e27c277cea8e90'
    getAbstracts(link)

#filename_year, {'title': title of article, 'abstract' : abstract content}
filenames = []
 
for key,value in abstracts.items():
    if str(pre_keyword) + '_' + key[0:4] + '.json' not in filenames:
        filename = str(pre_keyword) + '_' + key[0:4] + '.json'
        filenames.append(filename)
        
        with open(filename, 'w') as file:
            data = {key[4::]:value}
            file.write(json.dumps(data))
    else:
        #peoblem: new abstract overwrites, so in the end each file only has one abstract
        filename = str(pre_keyword) + '_' + key[0:4] + '.json'
        
        with open(filename, 'a') as file:
            data = {key[4::]:value}
            file.write(json.dumps(data))

     
end = time.time()

print(end-start)






