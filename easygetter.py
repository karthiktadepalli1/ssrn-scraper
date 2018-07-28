# takes the scraped papers and generates the chosen paper
import random
import requests
from bs4 import BeautifulSoup

paperList = []


def searchAbstract(url, keystring):
    paper = quickSoup(url)
    text = paper.get_text().split("Abstract\n")
    abstract = text[1].split("Suggested Citation:")[0]
    if keystring in abstract:
        return(True)
    else:
        return(False)

def getPaperDetails(url):
    soup = quickSoup(url)
    title = soup.find('h1').get_text()
    text = soup.get_text().split("Abstract\n")
    abstract = text[1].split("Suggested Citation:")[0]

    print(title)
    print(abstract)
    print(url)

def returnPaper(keystring=""):
    random.shuffle(paperList)
    if keystring == "":
        chosen = random.choice(paperList)
    else:
        for paper in paperList:
            if searchAbstract(paper, keystring):
                chosen = paper
    getPaperDetails(chosen)
