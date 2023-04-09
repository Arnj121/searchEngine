import re
import xml

from libs.search import *
from libs.indexing import *
from libs.saveLoad import *
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import requests
lotsofdata = []
originaldata=[]
linker = []
queue=[]
uniquewords = []
df = []
robots=[]
dontVisit=[]
#Document processing and indexing
#vector space model
#niche crawler
#query interface
#term proximity scoring

def processRobots():
    with open('data/robots.txt','r') as f:
        data=f.read()
        data = data.split('\n')
        for i in data:
                if len(i)>0:
                    j=i.split(' ')
                    if j[0].startswith('Disallow'):
                        dontVisit.append(j[1])
                    elif j[0].startswith('Sitemap'):
                        robots.append(j[1])
    for i in robots:
        if i.startswith('https'):
            print('processing ', i)
            parseXML(i)
def parseXML(arg):
    req = requests.get(arg).content
    xmltext = ET.fromstring(req)
    for j in xmltext.iter():
        text = j.text
        try:
            if text.startswith('https') and text.endswith('.xml'):
                parseXML(j.text)
            elif text.startswith('https://www.bbc.com/news') or text.startswith('https://www.bbc.com/sport'):
                queue.append(j.text)
        except AttributeError:
            pass
def crawl():
    processRobots()
    print(len(queue),queue)
    # if d == 0:
    #     return
    # if url in linker:
    #     return
    cc=0
    for i in queue:
        cc+=1
        print('getting link '+str(cc)+'/'+str(len(queue))+' ', i)
        content = get_content(i)
        if len(content) > 0:
            c=[]
            for j in content:
                print('processing document ', j)
                if len(j.strip())>0:
                    originaldata.append(j.strip())
                    c.append(preproc_stage_2(preproc_stage_1(j)))
            for j in c:
                lotsofdata.append(j)
                linker.append(i)
# def get_links(url):
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'lxml')
#     links = []
#     for link in soup.find_all('a'):
#         href = link.get('href')
#         if href.startswith('http'):
#             links.append(href)
#     return links

def get_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    content = []
    for h in soup.find_all(re.compile('h1')):
        content.append(h.text)
    return content


# def crawler(weblink,depth):
#     global lotsofdata,linker
#     crawl(weblink, depth)
#     print(len(lotsofdata),len(linker))

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
        crawl()
        indexer()
    elif inp == 'save':
        saveData()
        print('saved')
    elif inp == 'load':
        print('loaded')
        loadData()
    elif inp =='robot':
        processRobots()
    else:
        print('unknown command')
    inp = input('>> ')
# saveLoad()
# search('vegetarian recipe burst flavour plus information substitution and food')
