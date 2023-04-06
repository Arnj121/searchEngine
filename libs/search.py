from libs.indexing import  *


def check_dict(query,uniquewords):
    l = []
    for i in query:
        if i in uniquewords:
            l.append(i)
    return l

def query_tester(query,lotsofdata,linker,uniquewords,df):
    q = preproc_stage_1(query)
    q = preproc_stage_2(q)
    q = q.split(' ')
    q = check_dict(q,uniquewords)
    q.sort()
    print(q)
    dfq = pd.DataFrame(np.array([np.array([0] * len(uniquewords))]), columns=uniquewords)
    print(dfq)
    for w in q:
        dfq.loc[0, w] = q.count(w)
    print(df.iloc[len(lotsofdata) + 1], len(dfq.iloc[0]))
    dfq.iloc[0] = df.iloc[len(lotsofdata) + 1] * dfq.iloc[0]
    dfq.iloc[0] = dfq.iloc[0] / np.sqrt(sum(dfq.iloc[0] ** 2))
    result = []
    for i in range(len(lotsofdata)):
        s = np.dot(df.iloc[i], dfq.iloc[0])
        result.append(s)
    return [linker[result.index(max(result))], result]


def ranker(results, links,lotsofdata):
    dic=[]
    for i in range(len(results)):
        if pd.isna(results[i]):
            dic.append((0, links[i], lotsofdata[i]))
        else:
            dic.append((results[i], links[i], lotsofdata[i]))
    dic.sort(reverse=True)
    return dic

