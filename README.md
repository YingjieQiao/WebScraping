# WebScraping
This is my web scraping learning notes.

With reference to "Web Scraping with Python" by Ryan Mitchell  <br /><br /><br />


## Basic data retrieval

Sample code from the book, to get urls on a webpage.
```
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("https://en.wikipedia.org/wiki/Kevin_Bacon/")
bsObj = BeautifulSoup(html, features="html.parser")

for link in bsObj.findAll("a"):
    if 'href' in link.attrs:
        print(link.attrs['href'])
```
The bsObj is the html source code of the original website.
The links on most webpages exist in this format: <br />
<a href="https://someurl.com" sometag </a>   <br />

I wrote a piece of code to retrieve title and corresonding url link on [hacker news](https://news.ycombinator.com/) as a practice. [getTitles.py](https://github.com/YingjieQiao/WebScraping/blob/master/getTitles.py)
```
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("https://news.ycombinator.com/").read()
bsObj = BeautifulSoup(html, features="html.parser")

for link in bsObj.findAll('td',{'class':'title'},{'class':'storylink'}):
    print(link.text)
```
The link in the code above is a `tag` object and the `text` attribute and retrieve its text content, deleting the html tags and those parentheses formats. 


## 
