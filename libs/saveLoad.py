import pandas as pd

def load_table(path):
    global df
    df = pd.read_csv(path)
    df = df.iloc[:, 1:]


def load_documents(path):
    global lotsofdata
    data = open(path, 'r')
    temp = data.read().split('\n')
    temp2 = []
    for i in temp:
        temp2.append(i.split('||'))
    for i in temp2:
        # print(i)
        lotsofdata.append(i[0])
        linker.append(i[1])


def load_words(path):
    global uniquewords
    data = open(path, 'r')
    data = data.read().split(',')
    for i in data:
        uniquewords.append(i)


def save_table(df, path):
    df.to_csv(path)


def save_documents(path):
    temp = []
    for i in range(len(lotsofdata)):
        temp.append(lotsofdata[i] + '||' + linker[i])
    with open(path, 'w') as f:
        f.write('\n'.join(temp))


def save_words(path):
    with open(path, 'w') as f:
        f.write(','.join(uniquewords))
