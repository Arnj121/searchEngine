import numpy as np
import pandas as pd
import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

stopWords = ['i', 'a', 'about', 'an', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'how', 'in', 'is', 'it', 'of', 'on',
             'or', 'that', 'the', 'this', 'to', 'was', 'what', 'when', 'where', 'who', 'will', 'with', 'the', 'www']
lemmatizer = WordNetLemmatizer()
def pos_tagger(nltk_tag):
    if nltk_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None

def preproc_stage_2(sentence):
    pos_tagged = nltk.pos_tag(nltk.word_tokenize(sentence.lower()))
    wordnet_tagged = list(map(lambda x: (x[0], pos_tagger(x[1])), pos_tagged))
    lemmatized_sentence = []
    for word, tag in wordnet_tagged:
        if tag is None and word not in stopWords:
            lemmatized_sentence.append(word)
        elif word not in stopWords:
            lemmatized_sentence.append(lemmatizer.lemmatize(word, tag))
    lemmatized_sentence = " ".join(lemmatized_sentence)
    return lemmatized_sentence

def preproc_stage_1(reads):
    d = reads.strip().lower().split()
    l = []
    for i in d:
        if i.isalnum():
            print('lammetizing word' ,i)
            while i.endswith((',', '.', ';', '?', ')', ']', '}', ':', "\"", "'")):
                i = i[:-1]
            if i.endswith(("'s", "'t")):
                i = i[:-2]
            if i.endswith(("'re", "'ll", "'ve")):
                i = i[:-3]
            while i.startswith(("\"", "'", '{', '[', '(')):
                i = i[1:]
            if '-' in i:
                for j in i.split('-'):
                    l.append(j)
            elif len(i)>1 or (len(i)==1 and i.isnumeric()):
                l.append(i)

        elif '-' in i:
            print('lammetizing word', i)
            for j in i.split('-'):
                    l.append(j)
    return ' '.join(l)

def generate_table(data):
    l = []
    for i in data:
        splitted = i.split(' ')
        for j in splitted:
            if len(j)>1:
                l.append(j)
    uw = set(l)
    uw = list(uw)
    uw.sort()
    # uniquewords = uw
    tempdf = pd.DataFrame(np.array([np.array([0] * len(uw))] * (len(data) + 2)), columns=uw)
    return [tempdf, uw]

def update_freq(df, terms, lotsofdata):
    print(terms)
    for w in terms:
        print('currently proccessing word', w)
        for d in range(len(lotsofdata)):
            df.loc[d, w] = lotsofdata[d].count(w)
        docf = len(df[w]) - list(df[w]).count(0)
        df.loc[len(lotsofdata), w] = docf
        idf = np.log(len(lotsofdata) / docf)
        df.loc[len(lotsofdata) + 1, w] = idf
    return [df,terms]

def cosine_similarity(df,lotsofdata):
    for i in range(len(lotsofdata)):
        print('currently processing document ', i)
        df.iloc[i] = df.iloc[i] * df.iloc[len(lotsofdata) + 1]
        df.iloc[i] = df.iloc[i] / np.sqrt(sum(df.iloc[i] ** 2))
    return df

