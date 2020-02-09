import requests
#from requests.adapters import HTTPAdapter
#from requests.packages.urllib3.util.retry import Retry
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import ssl
import json
import time

abstracts = {}
keys = []
values = []
i = 0
#years = ['1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']

#############################################################################
### {'title1_year':{'abstract1':{...}},'title2_year':{'abstract2':{...}}} ###
#############################################################################

def ignoreSSL():
    
    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    return None

def getAbstracts(url):
    global keys
    global values
    global i
    
    ignoreSSL()
        
    time.sleep(1)
    
    driver = webdriver.PhantomJS(executable_path='D:\\ANACONDAA\\envs\\py3.7\\Library\\bin\\phantomjs')
    driver.get(url)
    
    
    try:
        element = driver.find_element_by_id(id_='abstractBox')
        values.append(element.text)
    except:
        values.append(0)
    
    print(i)
    return None



def getArticles(url):
    global keys
    global values
    global i
    
    ignoreSSL()
    
    time.sleep(2)
    
    '''
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    '''
    
    html = requests.get(url)

        
    bsObj = bs(html.content, features='html.parser')
    
    
    for link in bsObj.findAll('span',{'class':'hlFld-Title'}):
        keys.append(link.text)
        
    for date in bsObj.findAll('span',{'class':'pub-date-value'}):
        yr = str(date)[-11:-7]
        key = keys[i] + '_' + yr
        keys[i] = key
        i += 1
       
    for link in bsObj.findAll('a'):
        if 'href' in link.attrs:
            rawlink = link.attrs['href']
            if rawlink.startswith('/doi/abs'):
                rawlink = 'https://pubs.acs.org' + rawlink
                getAbstracts(rawlink)
   
    return None


start = time.time()


n = 0
address = 'https://pubs.acs.org/action/doSearch?AllField=material+science&startPage=' + str(n) + '&pageSize=20'

for n in range (2001,4000): 
    address = 'https://pubs.acs.org/action/doSearch?AllField=material+science&startPage=' + str(n) + '&pageSize=20'
    getArticles(address)

print(len(keys))
print(len(values))

j = 0
while j < len(values):
    abstracts[keys[j]] = values[j]
    j += 1
    
with open('ACS_material+science_dict_2.json', 'w') as file1:
    file1.write(json.dumps(abstracts))

with open('ACS_material+science_list_2.json', 'w') as file1:
    file1.write(json.dumps(values))


end = time.time()

print('Time elapsed: ' + str(end-start))


