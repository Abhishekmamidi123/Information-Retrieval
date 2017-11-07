import os
import sys
import json
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize, wordpunct_tokenize
stop_words = set(stopwords.words('english'))
stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}']) # remove it if you need punctuation
porter = PorterStemmer()
import io
try:
    to_unicode = unicode
except NameError:
    to_unicode = str

DictionaryOfWords = {}
queryList = []
queryDict = {}
files = []  # list has files that consists of all query words.
# Load data
with open('data.json') as data_file:
    DictionaryOfWords = json.load(data_file)

# processing the query elements and putting the indexed dataof the query words in the dictionary using preprocessed data (read from data.json).
def preprocess(query):
    dummyList = wordpunct_tokenize(query)
    dummyList = [x.lower() for x in dummyList]
    for word in dummyList:
        if word not in stop_words:
            queryList.append(porter.stem(word))
    for word in queryList:
        if word in DictionaryOfWords:
            queryDict[word] = DictionaryOfWords[word]
        else:
            queryDict[word] = {}

# returns 0/1. If 1-it stores the list of all intersection files.
def getIntersectionFiles():
    global files
    if len(queryList)==0:
        return 0
    else:
        a = queryDict[queryList[0]].viewkeys()
        for i in range(1,len(queryList)):
            b = queryDict[queryList[i]].viewkeys()
            l = a & b
            a = l
        files = list(a)[:-1]
        return 1

def resultFiles():
    resultantFiles=[]
    for filei in files:
        firstword = queryList[0]
        # dummy list contains the indices of the firstword of queryList in filei
        dummy = queryDict[firstword][filei][1:]
        for index in dummy:
            y = index+1
            for i in range(1, len(queryList)-1):
                word = queryList[i]
                if y in queryDict[word][filei]:
                    y=y+1
                else:
                    break
            resultantFiles.append(filei)
    return resultantFiles

query = sys.argv[1]
# query = raw_input()
preprocess(query)
flag = getIntersectionFiles()
if flag==0:
    print "No files found"
else:
    flag=1
    resultantFiles = resultFiles()
    if len(resultantFiles)==0:
        print "No results found"
    else:
        print resultantFiles



















# gf
