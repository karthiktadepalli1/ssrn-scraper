import requests
from ordered_set import OrderedSet
from bs4 import BeautifulSoup
from multiprocessing import Pool
from multiprocessing import cpu_count
import time
import sys

def quickSoup(url):
    try:
        header = {}
        header['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        # page = requests.get(url, headers=header, timeout=10)
        soup = BeautifulSoup(requests.get(url, headers=header, timeout=10).content, 'html.parser')
        return(soup)
    except Exception:
        return(None)


def getPaper(url):
    try:
        article = quickSoup(url)
        t = article.get_text()
        if "The abstract you requested was not found" in t:
            return("{},".format(url))
        title = article.find('h1').get_text().replace("\n", "")
        test_list = OrderedSet(t.split("\n"))
        authors = test_list[0].replace(title, "").replace(" :: SSRN", "").replace(" by ", "").replace(", ", ":")
        date = [line.replace("Last revised: ", "") for line in test_list if "Last revised: " in line]
        if date == []:
            date = [line.replace("Posted: ", "") for line in test_list if "Last revised: " in line]
        date = date[0]
        text = t.split("Abstract\n")[1]
        abstract = "\"{}\"".format(text.split("Suggested Citation:")[0].replace("\n", ""))

        # get paper statistics
        stats = OrderedSet(article.find('div', attrs = {'class': 'box-paper-statics'}).get_text().split("\n"))
        views, dl, rank, refs = "", "", "", ""
        try:
            views = stats[stats.index('Abstract Views') + 1].strip().replace(",", "")
        except:
            pass
        try:
            dl = stats[stats.index('Downloads') + 1].strip().replace(",", "")
        except:
            pass
        try:
            rank = stats[stats.index('rank') + 1].strip().replace(",", "")
        except:
            pass
        try:
            refs = stats[stats.index('References') + 1].strip().replace(",", "")
        except:
            pass
        results = [url, "\"{}\"".format(title), abstract, authors, date, views, dl, rank, refs]
        return(",".join(results))
    except:
        return("{},,,,,,,,".format(url))


def dummyscrape(start, stop):
    numWorkers = cpu_count() * 12
    print(numWorkers)
    p = Pool(numWorkers)
    linkList = ["https://papers.ssrn.com/sol3/papers.cfm?abstract_id=" + str(x) for x in range(start, stop)]

    papers = p.map(getPaper, linkList)
    p.terminate()
    p.join()
    writeString = "\n".join(papers)
    with open('test.csv', 'w+') as f:
        f.write(writeString)

def scrape(start, stop):
    numWorkers = cpu_count() * 12
    p = Pool(numWorkers)
    linkList = ["https://papers.ssrn.com/sol3/papers.cfm?abstract_id={}".format(str(x)) for x in range(start, stop)]

    papers = p.map(getPaper, linkList)
    p.terminate()
    p.join()
    writeString = "\n".join(papers)
    with open('ssrn-links.csv', 'a') as f:
        f.write(writeString)

if __name__ == "__main__":
    # import cProfile
    # import scraper
    # globals().update(vars(scraper))
    # sys.modules['__main__'] = scraper
    # dummyscrape(4000, 4100)
    breaks = [10000 * x for x in range(179, 250)]
    t = time.time()
    for i in range(len(breaks)-1):
        print(breaks[i])
        b = time.time()
        scrape(breaks[i], breaks[i+1])
        print("TIME FOR 1000: " + str(time.time() - b))
        print("TIME SINCE START: " + str(time.time() - t))
