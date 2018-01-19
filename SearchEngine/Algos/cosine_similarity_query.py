import os
import numpy as np
import sys
import math
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize, wordpunct_tokenize
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import cPickle as pickle
import json
import operator
# Make it work for Python 2+3 and with Unicode
import io
try:
    to_unicode = unicode
except NameError:
    to_unicode = str

stop_words = set(stopwords.words('english'))
stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}'])
porter = PorterStemmer()

'''
Reading Query
'''
query = raw_input().strip()
query = query.split()
q = []
for query_word in query:
    x = wordpunct_tokenize(query_word.lower())
    q.append(x[0])

print (q)
document_vectors =  {}
# Stemming each word in query
stemmedWords = []
for word in q:
	if word not in stop_words:
		stemmedWords.append(porter.stem(word))

# Getting each words frequency in query
check_dictionary = {}
for w in stemmedWords:
	if(w in check_dictionary):
		check_dictionary[w]+=1
	else:
		check_dictionary[w] = 1

toptwentypercentwords = []
with open('top_twenty_just_words.txt') as file:
	y = file.read()
	toptwentypercentwords = y.split('\n')

# Creating "query vector"
query_vector = []
for word in toptwentypercentwords:
	#if(len(word) > 0):
	if(word in check_dictionary):
			query_vector.append(check_dictionary[word])
	else:
		query_vector.append(0)

arr1 = np.array(query_vector)
l1 = np.sqrt(np.sum(np.square(arr1)))


with open('cosine_doc_vectors.json') as file:
	document_vectors = json.load(file)

final_dic = {}
for doc in document_vectors:
	cosine_value = 0
	arr2 = np.array(document_vectors[doc])
	l2 = np.sqrt(np.sum(np.square(arr2)))
	dot_product = np.dot(arr1, arr2)
	cosine_value = (dot_product)/float(l1*l2)
	#print (dot_product)
	if ((math.isnan(float(cosine_value)))):
		cosine_value = float(0)
	final_dic[doc] = cosine_value

with open('file_paths.json') as data_file:
     dictionary = json.load(data_file)
files_list = sorted(final_dic.items(), key = operator.itemgetter(1))
print (files_list)
for i in range(5):
	fileindex = files_list[len(files_list)-1-i][0]
	print (dictionary[fileindex])
