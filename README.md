# WebScraping
This is my web scraping learning notes.

With reference to "Web Scraping with Python" by Ryan Mitchell, "Automate Boring Stuff with Python" by Al Sweigart and Coursera course "Using Python to Access Web Data" by Prof. Charles Severance. <br /><br /><br />  

 
 <br />
   
## Basic data retrieval
 
 <br />
`webbrowser.open(url, new=0, autoraise=True)` is used to open a website in a browser. `new=0` opens the page in the same browser window if possible, `new=1` opens the page in a new window, `new=2` opens the page in a new tab. 

`webbrowser.open('https://www.google.com/maps/place/' + address)`  


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
The link in the code above is a `tag` object and the `.tex`t gets all the child strings and return concatenated using the given separator. Return type of `.tex`t is unicode object.

[Here](https://github.com/YingjieQiao/WebScraping/blob/master/tagCount.py) is another piece of code I've written for practice. Based on the data from the first 2 pages of https://stackoverflow.com/tags?page=1&tab=popular, it produces a graph with languages on the x-axis and number of tags on the y-axis. In my current approach, I used 2 loops, i.e., created 2 BeautifulSoup objects to get 2 arrays.  
   <br />
Use `for tag in bsObj.findAll('a',{'class':'post-tag'}):` to retrieve the following html (don't have to create the `bs` object layer by layer):   <br />
`<a href="/questions/tagged/java" class="post-tag" title="" rel="tag">java</a>`  
  
  
Also, I find it easier to locate urls in the html source using the following formats.
![css](https://github.com/YingjieQiao/WebScraping/blob/master/css.png) (credit: "Automate Boring Stuff with Python" by Al Sweigart)  
I applied such formatting in re-writing the downloading files sample code using `urllib.request.urlretrieve` later.
 <br />
   

   
   
## Downloading files

 <br />  
   
 Use the `request` module to download files.
 
 
 ```
 import requests, os, bs4


url = 'http://xkcd.com' 
#the downloaded files will be saved in the folder "xkcd" under the same directory as the script
os.makedirs('xkcd', exist_ok=True)


while not url.endswith('#'):
    print('Downloading page %s...' % url)
    res = requests.get(url)                     #use get to open a url
    res.raise_for_status()                      #Raises stored HTTPError, if one occurred. i.e., Raise an exception if a request falis. 
    soup = bs4.BeautifulSoup(res.text)          #.text deletes unnecessary html formats
    
    comicElem = soup.select('#comic img')
    if comicElem == []:
        print('Could not find comic image.')
    else:
        comicUrl = 'http:' + comicElem[0].get('src')
        # Download the image.
        print('Downloading image %s...' % (comicUrl))
        res = requests.get(comicUrl)           #This is the line that downloads the photo. "get" method can be used for downloading.
        res.raise_for_status()
        
        imageFile = open(os.path.join('xkcd', os.path.basename(comicUrl)), 'wb') 
        #"imageFile" is going to be the filename of the downloaded file
        for chunk in res.iter_content(100000):
            #iterates over the response data.
            imageFile.write(chunk)
        imageFile.close()
        
    # Get the Prev button's url.
    prevLink = soup.select('a[rel="prev"]')[0]
    url = 'http://xkcd.com' + prevLink.get('href')
  ```  
  

  
 <br />
 
   
 Use `urllib.request.urlretrieve` to download files.
 
 urllib.request.urlretrieve(url, filename=None, reporthook=None, data=None) 
 
 The parameter "filename" here is the name of the file on the local drive.
 
 The photo downloading code can also be re-written using `urllib.request.urlretrieve`
 
 ```
import os
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from urllib.request import urlretrieve


url = 'http://xkcd.com' 
os.makedirs('redo', exist_ok=True)
#the downloaded files will be saved in the folder "redo" under the same directory as the script

while not url.endswith('#'):
    print('Downloading page %s...' % url)
    html = urlopen(url)
    soup = bs(html)
    
    comicElem = soup.select('#comic img')
    if comicElem == []:
        print('Could not find comic image.')
    else:
        comicUrl = 'http:' + comicElem[0].get('src')
        # Download the image.
        print('Downloading image %s...' % (comicUrl))
        urlretrieve(comicUrl, os.path.join('redo', os.path.basename(comicUrl)))
        
        
        
    # Get the Prev button's url.
    prevLink = soup.select('a[rel="prev"]')[0]
    url = 'http://xkcd.com' + prevLink.get('href')
```



 <br />  
   
## Crawling across the internet
 
 <br />
   
 
The sample code to crawl across the whole internet in the book is uploaded [here](https://github.com/YingjieQiao/WebScraping/blob/master/keepCrawling_SampleCode.py).
To crawl on a certain website, only webpages under en.wikipedia.org or ieee.org, for example, modify the regular expression for `href`. An example function is commented at the end of the sample code file above.

 
 <br />
   
 ## Data cleaning
 
 <br />
   
 
 Use regular expressions to remove escape characters and use filtering to remove Unicode characters.
 `.strip(string.punctuation)` removes any punctuation characters on either side of a word except hyphens because they are bounded by letter characters on either side.
 
 ```
 def cleanInput(content):
    content = re.sub('\n+', " ", content)        #replace all new line characters with one single white space
    content = re.sub('\[[0-9]*\]', "", input)    #remove special symbols and numbers, the / here is to escape special characters
    content = re.sub(' +', " ", content)         #replace all white space characters with one single white space
    content = bytes(content, "UTF-8")            #remove all Unicode characters by encoding with UTF-8
    content = content.decode("ascii", "ignore")
    cleanedInput = []
    input = input.split(' ')
    for item in content:
        content = content.strip(string.punctuation)   #remove punctuations
        if len(item) > 1 or (item.lower() == 'a' or item.lower() == 'i'):   #single character words "I" and "a"
            cleanedInput.append(item)
    return cleanedInput
```
 
 <br />
   

An [n-gram](https://en.wikipedia.org/wiki/N-gram) is a contiguous sequence of n items from a given sample of text or speech.
 ```
 def ngrams(text,n):
    text = cleanInput(text)
    ngrammed = []
    for i in range(len(text)-n+1):
        ngrammed.append(input[i:i+n])
    return ngrammed
 ```
 
 <br />
   

`OrderedDict`, as obvious from its name, is an ordered dictionary.

The `cleanInput` function above obly record the existence of each ngram but not frqeuency. The follwoing code can record the frequency of each ngram along with the ngram itself in an ordered dictionary.
```
from collections import OrderedDict

...

ngrams = ngrams(content, 2)
ngrams = OrderedDict(sorted(ngrams.items(), key=lambda t: t[1], reverse=True))
print(ngrams)
  

```
[Openrefine](http://openrefine.org/) can be applied for more efficient data cleaning. It may be not working on Mac because it has been open sourced which may potentially be regarded as "unsafe" in the eyes of Apple.
 
 
  
 <br />
 
   
   
## Avoid Scraping Traps
 
  
 <br />  
 
The headers can be editted to avoid being blocked by website admin using the code below:

```
import requests
from bs4 import BeautifulSoup

session = requests.Session()
headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}

#this website is useful in checking your http headers
url = "https://www.whatismybrowser.com/developers/what-http-headers-is-my-browser-sending"  
req = session.get(url, headers=headers)
bsObj = BeautifulSoup(req.text)
print(bsObj.find("table",{"class":"table-striped"}).get_text) 
```
   
The "User-agent" in the header is what really matters when the website checks the "humaness" of each visit.
  
Side note: `.text` attribute can give you a better formatting in the output.

  
 <br />  
   
Handling cookies correctly can alleviate many of scraping problems, although cookies
can also be a double-edged sword. Websites that track your progression through a site
using cookies might attempt to cut off scrapers that display abnormal behavior, such
as completing forms too quickly, or visiting too many pages. Although these behaviors
can be disguised by closing and reopening connections to the site, or even changing
your IP address.  

Cookies can also be very necessary to scrape a site. Staying
logged in on a site requires that you be able to hold and present a cookie from page to
page. Some websites don’t even require that you actually log in and get a new version
of a cookie every time—merely holding an old copy of a “logged in” cookie and visiting
the site is enough.  

The following code manipulates cookies using `selenium.webdriver`.
```
from selenium import webdriver

driver = webdriver.PhantomJS(executable_path='<Path to Phantom JS>')
driver.get("http://pythonscraping.com")
driver.implicitly_wait(1)
print(driver.get_cookies())
savedCookies = driver.get_cookies()

driver2 = webdriver.PhantomJS(executable_path='<Path to Phantom JS>')
driver2.get("http://pythonscraping.com")
driver2.delete_all_cookies()

for cookie in savedCookies:
    driver2.add_cookie(cookie)
    driver2.get("http://pythonscraping.com")
    
driver.implicitly_wait(1)
print(driver2.get_cookies())
```  
Technical note: For `driver2`, it must load the website first so that Selenium knows which website
the cookies belong to, even if the act of loading the website does nothing useful
for us.  

  
 <br />  
   
“Hidden” fields in html  can prevent scrapers from sending forms. Such as putting a link in the html source code but adding a `display:None` CSS attribute, creating a hidden input blank or moving a clickable element 500000 pixles to the right, i.e. off the monitor screen.  

Whether the element is present on the page can be determined by the `is_displayed()` function.  

```
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

driver = webdriver.PhantomJS(executable_path='')
driver.get("http://pythonscraping.com/pages/itsatrap.html")

links = driver.find_elements_by_tag_name("a")
for link in links:
    if not link.is_displayed():
        print("The link "+link.get_attribute("href")+" is a trap")
        
fields = driver.find_elements_by_tag_name("input")
for field in fields:
    if not field.is_displayed():
        print("Do not change value of "+field.get_attribute("name"))
        
```  
Although you probably don’t want to visit any hidden links you find, you will want to
make sure that you submit any pre-populated hidden form values (or have Selenium
submit them for you) with the rest of the form. To sum up, it is dangerous to simply
ignore hidden fields, although you must be very careful when interacting with them.
  
 <br />  
   

## Testing
  
 <br />  
   
About `assert`: https://stackoverflow.com/questions/5142418/what-is-the-use-of-assert-in-python

Python’s unit testing module, `unittest`, comes packaged with all standard Pythoninstallations. Just import and extend `unittest.TestCase`, and it will do the following:  

1. Provide `setUp` and `tearDown` functions that run before and after each unit test

2. Provide several types of “assert” statements to allow tests to pass or fail

3. Run all functions that begin with `test_ ` as unit tests, and ignore functions thatare not prepended as tests.


Here is a piece of sample code taken from the book.  
```
from urllib.request import urlopen
from bs4 import BeautifulSoup
import unittest


class TestWikipedia(unittest.TestCase):
    bsObj = None
    def setUpClass():
        global bsObj
        url = "http://en.wikipedia.org/wiki/Monty_Python"
        bsObj = BeautifulSoup(urlopen(url))
        
    def test_titleText(self):
        global bsObj
        pageTitle = bsObj.find("h1").get_text()
        self.assertEqual("Monty Python", pageTitle)
        
    def test_contentExists(self):
        global bsObj
        content = bsObj.find("div",{"id":"mw-content-text"})
        self.assertIsNotNone(content)
```

If needs to do multiple tests, create a function like this:  

```
class TestWikipedia(unittest.TestCase):
    bsObj = None
    url = None
    def test_PageProperties(self):
        global bsObj
        global url
        url = "http://en.wikipedia.org/wiki/Monty_Python"
        
        #Test the first 100 pages we encounter
        for i in range(1, 100):
            bsObj = BeautifulSoup(urlopen(url))
            titles = self.titleMatchesURL()
            self.assertEquals(titles[0], titles[1])
            self.assertTrue(self.contentExists())
            url = self.getNextLink()
        print("Done!")
```  
 
 <br />
   
`selenuim` can also be apllied for testing especially websites written in JavaScrip.  

Although obviously written in the same language, the syntax of Python unittests and
Selenium unit tests have surprisingly little in common. Selenium does not require
that its unit tests be contained as functions within classes; its “assert” statements do
not require parentheses; and tests pass silently, only producing some kind of message
on a failure:  
 
```
driver = webdriver.PhantomJS()
driver.get("http://en.wikipedia.org/wiki/Monty_Python")
assert "Monty Python" in driver.title
driver.close()
```   

When run, this test should produce no output if the title is correct.  

 
 <br />
   
`selenuim` is powerful in interacting with site such as filling and submitting forms automatically, completing drag-and-drop bot-verification, taking screenshots, etc.  







  
 <br />  
   
   
## NLTK

 
 <br />
   
NLTK is a powerful NLP library in python.   

 <br />
   

`nltk.word_tokennize(text1)` returns a list consists of the words and punctuations.

`>>> s0 = "This is a cooool #dummysmiley: :-) :-P <3 and some arrows < > -> <--"`

`>>>nltk.word_tokenize(s0)`

returns `['This', 'is', 'a', 'cooool', '#dummysmiley', ':', ':-)', ':-P', '<3', 'and', 'some', 'arrows', '<', '>', '->', '<--']`

<br />
   
`pos_tag` returns a list ot tuples, `(token, the part of speech of a word)`.
```
>>>from nltk import pos_tag

>>>pos_tag(nltk.word_tokenize(s0))

>>>[('This', 'DT'),('is', 'VBZ'),('a', 'DT'),('cooool', 'JJ'),('#', '#'),
 ('dummysmiley', 'NN'),(':', ':'),(':', ':'),('-', ':'),
 (')', ')'),(':', ':'),('-P', 'JJ'),('<', '$'),('3', 'CD'),
 ('and', 'CC'),('some', 'DT'),('arrows', 'NNS'),('<', 'VBP'),
 ('>', 'SYM'),('-', ':'),('>', 'NN'),('<', 'CD'),('--', ':')]
```

Take note that parsing sentence structure using `poa_tag` can sometimes be ambiguous. This sentence can have 2 total different meanings but only one of the two is returned. For example,
```
s1 = "I saw a man with a telescope"

pos_tag(nltk.word_tokenize(s1))
Out[9]: 
[('I', 'PRP'),
 ('saw', 'VBD'),
 ('a', 'DT'),
 ('man', 'NN'),
 ('with', 'IN'),
 ('a', 'DT'),
 ('telescope', 'NN')]
 ```

![amb](https://github.com/YingjieQiao/WebScraping/blob/master/amb.jpg)
 
 
