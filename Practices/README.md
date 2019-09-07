Here are some scripts about scraping I've written.

<br />  
  
  
## Get the news

<br />  
  
[getTitle.py](https://github.com/YingjieQiao/WebScraping/blob/master/Practices/getTitles.py) retrieves title and corresonding url link on hacker news.

<br />  
  
## Tag count

<br />  
  
Based on the data from the first 2 pages of https://stackoverflow.com/tags?page=1&tab=popular, [tagCount.py](https://github.com/YingjieQiao/WebScraping/blob/master/Practices/tagCount.py) produces a graph with languages on the x-axis and number of tags on the y-axis. In my current approach, I used 2 loops, i.e., created 2 BeautifulSoup objects to get 2 arrays.
 
<br />  
  
## Quora Scraper

<br />  
  
Type in the question you want to search on quora and it will automatically downloads all the answers of 100 relavant questions in one txt file. The [testfile.txt](https://github.com/YingjieQiao/WebScraping/blob/master/Practices/testfile.txt) here is generated running this [script](https://github.com/YingjieQiao/WebScraping/blob/master/Practices/quoraScraper.py).


