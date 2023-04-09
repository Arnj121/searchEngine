import pandas as pd

def load_table(path):
    df = pd.read_csv(path)
    df = df.iloc[:, 1:]
    return df

def load_documents(path):
    docs=[],links=[]
    data = open(path, 'r')
    temp = data.read().split('\n')
    temp2 = []
    for i in temp:
        temp2.append(i.split('||'))
    for i in temp2:
        # print(i)
        docs.append(i[0])
        links.append(i[1])
    return [docs,links]

def load_words(path):
    data = open(path, 'r')
    data = data.read().split(',')
    return data

def save_table(df, path):
    df.to_csv(path)

def save_documents(data,path):
    temp = []
    for i in range(len(data)):
        temp.append(data[i] + '||' + linker[i])
    with open(path, 'w') as f:
        f.write('\n'.join(temp))

def save_words(data,path):
    with open(path, 'w') as f:
        f.write(','.join(data))
