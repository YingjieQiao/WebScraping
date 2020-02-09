import requests
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import ssl
import time

articles = []
abstracts = {}
years = ['1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']

#############################################################################
### {'title1_year':{'abstract1':{...}},'title2_year':{'abstract2':{...}}} ###
#############################################################################

def ignoreSSL():
    
    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    return None


def getArtciels(url):
    global artciles
    
    ignoreSSL()
    
    html = requests.get(url)
    bsObj = bs(html.content, features='html.parser')
    
    for link in bsObj.findAll('a'):
        if 'href' in link.attrs:
            rawlink = link.attrs['href']
            if rawlink.startswith('/doi/abs'):
                rawlink = 'https://pubs.acs.org' + rawlink
                articles.append(rawlink)
    
    
    return None

def getAbstracts(url):
    global abstracts
    global years
    
    ignoreSSL()
    

    driver = webdriver.PhantomJS(executable_path='D:\\ANACONDAA\\envs\\py3.7\\Library\\bin\\phantomjs')
    driver.get(url)
    
    rawids = driver.find_elements_by_xpath('//*[@id]')
    ids = []
    for ii in rawids:
        the_id = ii.get_attribute('id')
        if the_id not in ids:
            ids.append(the_id)
    print(ids)
    
    element1 = driver.find_element_by_id(id_='intro-text')
    print(element1)
    print('\n')
    #p_element = driver.find_element_by_id(id_='hlFld-Title')
    #print(p_element.text)


    '''
    if bsObj.find('dc:title').text and bsObj.find('dc:identifier').text and bsObj.find('dc:identifier').text[-11:-7] in years:
        title = bsObj.find('dc:title').text
        abstract = bsObj.find('dc:description').text
        abstract = abstract.replace('Abstract', ' ').strip()
        iden = bsObj.find('dc:identifier').text
        
        preKey = iden[-11:-7] + title
        abstracts[preKey] = abstract
     
        
    else:
        pass
    '''
    
    return None


start = time.time()


n = 0
address = 'https://pubs.acs.org/action/doSearch?AllField=photostability&startPage=' + str(n) + '&pageSize=20'

for n in range (0,1): #18
    address = 'https://pubs.acs.org/action/doSearch?AllField=photostability&startPage=' + str(n) + '&pageSize=20'
    getArtciels(address)

for link in articles:
    getAbstracts(link)
    break
    
    
end = time.time()

print('Time elapsed: ' + str(end-start))


