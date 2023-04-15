from libs.search import *
from libs.indexing import *
from libs.saveLoad import *
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import requests
processedData = []
originaldata=[]
linker = []
dataWPara={}
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
    cc=0
    for i in queue[:100]:
        cc+=1
        print('getting link '+str(cc)+'/'+str(len(queue[:100]))+' ', i)
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
    df =cosine_similarity(df,processedData)
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
while inp !='quit':
    if inp == 'start':
        print('starting')
        crawl()
        indexer()
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
