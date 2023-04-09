import re
from libs.search import *
from libs.indexing import *
from libs.saveLoad import *
from bs4 import BeautifulSoup
import requests
lotsofdata = []
originaldata=[]
linker = []
uniquewords = []
df = []

#Document processing and indexing
#vector space model
#niche crawler
#query interface
#term proximity scoring

def crawl(url, d):
    if d == 0:
        return
    if url in linker:
        return
    content = get_content(url)
    if len(content) > 0:
        c=[]
        for i in content:
            if len(i.strip())>0:
                originaldata.append(i.strip())
                c.append(preproc_stage_2(preproc_stage_1(i)))
        for i in c:
            linker.append(url)
            lotsofdata.append(i)
    try:
        links = get_links(url)
        print(url)
        for link in links:
            crawl(link, d - 1)
    except AttributeError:
        pass

def get_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href.startswith('http'):
            links.append(href)
    return links


def get_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    content = []
    for h in soup.find_all(re.compile('^h[1-6]')):
        content.append(h.text)
    return content


def crawler(weblink,depth):
    global lotsofdata,linker
    crawl(weblink, depth)
    print(len(lotsofdata),len(linker))

def indexer():
    global df,uniquewords
    df,uniquewords=generate_table(lotsofdata)
    print(len(uniquewords))
    df, uniquewords=update_freq(df,uniquewords,lotsofdata)
    df =cosine_similarity(df,lotsofdata)
    print(df)
def saveData():
    save_table(df,'/data/data.csv')
    save_documents(originaldata,'/data/docs.txt')
    save_words(uniquewords,'/data/words.txt')

def loadData():
    global df,uniquewords,originaldata,linker
    df=load_table('/data/data.csv')
    originaldata,linker = load_documents('/data/docs.txt')
    uniquewords = load_words('/data/words.txt')

def search(q):
    l = query_tester(preproc_stage_2(preproc_stage_1(q)),lotsofdata,linker,uniquewords,df)
    ranks = ranker(l[1],linker,originaldata)
    dic ={}
    for i in range(len(ranks)):
        dic[i] = ranks[i]
    print(dic)
    return dic

inp = input('>> ')
while inp !='quit':
    if inp == 'start':
        print('starting')
        crawler('https://www.bbc.com/', 2)
        indexer()
    elif inp == 'save':
        saveData()
        print('saved')
    elif inp == 'load':
        print('loaded')
        loadData()
    else:
        print('unknown command')
    inp = input('>> ')
# saveLoad()
# search('vegetarian recipe burst flavour plus information substitution and food')
