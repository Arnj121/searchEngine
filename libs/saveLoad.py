import pandas as pd

def load_table(path):
    df = pd.read_csv(path)
    df = df.iloc[:, 1:]
    return df

def load_documents(path):
    docs=[]
    links=[]
    data = open(path, 'r')
    temp = data.read().split('\n')
    temp2 = []
    datap={}
    for i in temp:
        temp2.append(i.split('||'))
    for i in temp2:
        if len(i) >= 2:
            docs.append(i[0])
            links.append(i[-1])
            datap[i[1]] = i[1:-1]
    return [docs,links,datap]

def load_words(path):
    data = open(path, 'r')
    data = data.read().split(',')
    return data

def save_table(df, path):
    df.to_csv(path)

def save_documents(data,datap,path,linker):
    temp = []
    for i in range(len(data)):
        p=''
        for j in data[i]:
            if ord(j)<128:
                p+=j
        d=[]
        for k in datap[linker[i]]:
            t = ''
            for n in k:
                if ord(n)<128 and ord(n)!=10:
                    t+=n
            if len(t)>0:
                d.append(t)
        p+='||'+'||'.join(d)
        temp.append(p +'||'+ linker[i])
    with open(path, 'w') as f:
        f.write('\n'.join(temp))

def save_words(data,path):
    with open(path, 'w') as f:
        temp=[]
        for i in data:
            p=''
            for j in i:
                if ord(j)<128:
                    p+=j
                else:
                    p=''
                    break
            if len(p)>0:
                temp.append(p)
        f.write(','.join(temp))
