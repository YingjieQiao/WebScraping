# WebScraping
This is my web scraping learning notes.

With reference to "Web Scraping with Python" by Ryan Mitchell  <br /><br /><br />

 
 <br />
   
## Basic data retrieval
 
 <br />
   
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

[Here](https://github.com/YingjieQiao/WebScraping/blob/master/tagCount.py) is another piece of code I've written for practice. Based on the data from the first 2 pages of https://stackoverflow.com/tags?page=1&tab=popular, it produces a graph with languages on the x-axis and number of tags on the y-axis. In my current approach, I used 2 loops, i.e., created 2 BeautifulSoup objects to get 2 arrays.  
   <br />
Use `for tag in bsObj.findAll('a',{'class':'post-tag'}):` to retrieve the following html (don't have to create the `bs` object layer by layer):   <br />
`<a href="/questions/tagged/java" class="post-tag" title="" rel="tag">java</a>`  
  
 <br />
   
## Crawling across the internet
 
 <br />
   
 
The sample code to crawl across the whole internet in the book is uploaded [here](https://github.com/YingjieQiao/WebScraping/blob/master/keepCrawling_SampleCode.py).
To crawl on a certain website, only webpages under en.wikipedia.org or ieee.org, for example, modify the regular expression for `href`. An example function is commented at the end of the sample code file above.

 
 <br />
   
   
## Downloading files

 <br />
 
 Use `urllib.request.urlretrieve` to download files.
 
 urllib.request.urlretrieve(url, filename=None, reporthook=None, data=None) 
 
 The parameter "filename" here is the name of the file on the local drive.


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
   
## NLTK

 
 <br />
   
NLTK is a powerful NLP library in python.   

 <br />
   

`nltk.word_tokennize(text1)` returns a list consists of the words and punctuations.

`>>> s0 = "This is a cooool #dummysmiley: :-) :-P <3 and some arrows < > -> <--"`

`>>>nltk.word_tokenize(s0)`

returns `['This', 'is', 'a', 'cooool', '#dummysmiley', ':', ':-)', ':-P', '<3', 'and', 'some', 'arrows', '<', '>', '->', '<--']`

<br />
   
`pos_tag` returns the part of speech of a word.
```
>>>from nltk import pos_tag

>>>pos_tag(nltk.word_tokenize(s0))

>>>[('This', 'DT'),('is', 'VBZ'),('a', 'DT'),('cooool', 'JJ'),('#', '#'),
 ('dummysmiley', 'NN'),(':', ':'),(':', ':'),('-', ':'),
 (')', ')'),(':', ':'),('-P', 'JJ'),('<', '$'),('3', 'CD'),
 ('and', 'CC'),('some', 'DT'),('arrows', 'NNS'),('<', 'VBP'),
 ('>', 'SYM'),('-', ':'),('>', 'NN'),('<', 'CD'),('--', ':')]
```


 
 
