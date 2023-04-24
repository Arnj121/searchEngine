from libs.search import *
from libs.indexing import *
import time
from libs.saveLoad import *
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import requests
import time

processedData = []
originaldata=[]
linker = []
dataWPara={}
urlsfrontier=[]
uniquewords = []
df = []
robots=[]
dontVisit=[]
#Document processing and indexing
#vector space model
#niche crawler
#query interface
#term proximity scoring

import requests
from bs4 import BeautifulSoup

def get_links(url):
    response = requests.get(url)
    #print(response.text)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        try:
            if href.startswith('/') and href not in dontVisit:
                links.append('https://www.bbc.com/'+href)
        except AttributeError:
            pass
    return links

def niche_crawl(url, depth):
    if depth == 0:
        return
    links = get_links(url)
    for link in links:
        print('getting links ',link)
        if link not in urlsfrontier:
            urlsfrontier.append(link)
        niche_crawl(link, depth-1)

def processRobots():
    robot = requests.get("https://www.bbc.com/robots.txt")
    sou = BeautifulSoup(robot.text, "lxml")
    #print(type(sou.text))
    for line in sou.text.split('\n'):
         if line.startswith("Disallow"):
            dontVisit.append(line.split()[1])
 
def crawl():
    print(len(urlsfrontier),urlsfrontier)
    cc=0
    for i in urlsfrontier:
        cc+=1
        print('getting link '+str(cc)+'/'+str(len(urlsfrontier))+' ', i)
        content = get_content(i)
        if len(content) > 0:
            c=[]
            originaldata.append(content[0].strip())
            dataWPara[i] = content[1:]
            for j in content:
                print('processing document ', j)
                if len(j.strip())>0:
                    c.append(preproc_stage_2(preproc_stage_1(j)))
            c=' '.join(c)
            print('final result ',c)
            processedData.append(c)
            linker.append(i)

def get_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    content = []
    h =soup.find_all('h1')
    p =soup.find_all('p')
    for i in h:
        content.append(i.text)
    for i in p:
        if not i.text.lower().startswith('last updated'):
            content.append(i.text)
    return content


# def crawler(weblink,depth):
#     global processedData,linker
#     crawl(weblink, depth)
#     print(len(processedData),len(linker))

def indexer():
    global df,uniquewords
    df,uniquewords=generate_table(processedData)
    print(len(uniquewords))
    df, uniquewords=update_freq(df,uniquewords,processedData)
    df =vectorspace(df,processedData)
    print(df)
def saveData():
    save_table(df,'data/data.csv')
    save_documents(originaldata,dataWPara,'data/docs.txt',linker)
    save_words(uniquewords,'data/words.txt')

def loadData():
    global df,uniquewords,originaldata,linker, dataWPara
    df=load_table('data/data.csv')
    uniquewords = load_words('data/words.txt')
    originaldata,linker,dataWPara = load_documents('data/docs.txt')
    print(len(df['12']))
    print('unique words retrieved ', len(uniquewords))
    print('number of links ', len(linker))
    print('number of documents ',len(originaldata))

def search(q):
    l = query_tester(preproc_stage_2(preproc_stage_1(q)),originaldata,linker,uniquewords,df)
    ranks = ranker(l,linker,originaldata)
    dic ={}
    for i in range(len(ranks)):
        dic[i] = ranks[i]
    print(dic)
    return dic

inp = input('>> ')
while inp !='launch':
    if inp == 'start':
        print('starting')
        p = time.time()
        processRobots()
        niche_crawl('https://bbc.com/sport', 1)
        crawl()
        indexer()
        print('total execution time ', str(time.time()-p))
    elif inp == 'save':
        print('saving...')
        saveData()
        print('saved')
    elif inp == 'load':
        print('loading...')
        loadData()
        print('loaded')
    elif inp =='robot':
        processRobots()
    else:
        print('unknown command')
    inp = input('>> ')
# saveLoad()
# search('vegetarian recipe burst flavour plus information substitution and food')
