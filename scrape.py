import newspaper
from newspaper import Article
import tweepy

from lxml import html
import requests

from access import consumer_key, consumer_secret

def month_year_urls(m, y):
    base = 'https://www.vox.com/archives/vox-sentences/'
    vs = Article(base + str(y) + '/' + str(m))
    vs.download()
    lines = vs.html.split('\n')
    urls = [l.split('href="')[1].split('">')[0] for l in lines if 'data-analytics-link="" href=' in l]
    return urls

def collect_urls(month=12, year=2019):
    '''
       Collect urls up to the specified month and year. (Use this one!)
    '''
    urls = []

    # handle 2015-last year
    for y in range(2015, year):
        for m in range(1, 13):
            page = month_year_urls(m, y)
            urls += page

    # handle this year
    for m in range(1, month + 1):
        page = month_year_urls(m, year)
        urls += page

    # handle 2014.
    for m in range(1, 13):
        page = month_year_urls(m, 2014)
        urls += page

    return list(set(urls))

def collect_urls_alt(base='https://www.vox.com/2014/10/18/7000531/vox-sentences/archives/'):
    # may have to run this multiple times because of rate-limiting
    
    #base = 'https://www.vox.com/vox-sentences/archives/'
    urls = []

    i = 1
    while True:
        vs = Article(base + str(i))
        vs.download()
        lines = vs.html.split('\n')
        page = [l.split('href="')[1].split('">')[0] for l in lines if 'data-analytics-link="article" href=' in l]
        print(base + str(i))
        print(page)
        print()
        if len(page) is 0 or page[0] in urls:
            break

        urls += page
        i += 1

    #return list(set(urls))
    return urls

def scrape_tweet(url):
    r = requests.get(url)
    return html.fromstring(r.content).xpath('//div[contains(@class, "permalink-tweet-container")]//p[contains(@class, "tweet-text")]//text()')[0]

def scrape_thread(url):
    #auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    #api = tweepy.API(auth)
    pass

if __name__ == "__main__":
    #urls = collect_urls()
    #print(len(urls))
    #out = open('urls.txt', 'w')
    #for url in urls:
    #    out.write(url + '\n')
    #out.close()
