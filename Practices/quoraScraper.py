from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import random

qn = input("Please type in your question: ")
qn = qn.replace(" ", "-")
qn = "https://www.quora.com/"+qn

    
pages = [] #question links
pages.append(qn)

def getLinks():
    global pages
    
    i = 0
    for page in pages:
        if len(pages) >= 100:
            break
        
        i = random.randint(0,len(pages)-1)
        try:
            html = urlopen(pages[i])
            bsObj = bs(html, features="html.parser")
        except :
            i = random.randint(0,len(pages)-1)
            html = urlopen(pages[i])
            bsObj = bs(html, features="html.parser")
            
        for link in bsObj.findAll('a', {'class':'question_link'}):
            if len(pages) > 100:
                break
            if 'href' in link.attrs:
                if link.attrs['href'] not in pages and len(pages)<100:
                    newPage = "https://www.quora.com/" + link.attrs['href']
                    #print(newPage)
                    pages.append(newPage)
                    #print(len(pages))
    print("Ok!")
    return None
    
 

def getTexts():
    
    playFile = open('testfile.txt', 'wb')
    
    i = 0
    print("Writing...")
    for page in pages:
        try:
            html = urlopen(page)
            bsObj = bs(html, features="html.parser")
        except IncompleteRead:
            html = urlopen(page).partial
            bsObj = bs(html, features="html.parser")
        
        for article in bsObj.findAll('span',{'class':'ui_qtext_rendered_qtext'}):
            playFile.write(article.text.encode(encoding='utf-8', errors='strict') +'\n'.encode(encoding='utf-8', errors='strict'))
        
    playFile.close()
    print("Done!")


getLinks() 
    
getTexts()
            