import os
import numpy as np
import sys
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize, wordpunct_tokenize
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import pickle
import json
import operator
# Make it work for Python 2+3 and with Unicode
import io
try:
    to_unicode = unicode
except NameError:
    to_unicode = str

document_tfidf_vectors = {}

stop_words = set(stopwords.words('english'))
stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}'])
porter = PorterStemmer()

'''
Reading Query
'''
query = input().strip()
query = query.split()
q = []
for query_word in query:
    x = query_word.lower()
    q.append(wordpunct_tokenize(x)[0])
# Stemming each word in query
stemmedWords = []
for word in q:
	if word not in stop_words:
		stemmedWords.append(porter.stem(word))

with open('tf_idf_vectors.json') as file:
	document_tfidf_vectors = json.load(file)

with open('word_frequency_in_each_file.json') as file:
	word_file_frequency = json.load(file)
all_words_list = list(word_file_frequency.keys())

final_dic = {}
for doc_key in document_tfidf_vectors:
	tf_idf = 0
	doc_tfidf = document_tfidf_vectors[doc_key]
	for query_word in stemmedWords:
		index = all_words_list.index(query_word)
		tf_idf += doc_tfidf[index]
	final_dic[doc_key] = tf_idf

with open('file_paths.json') as data_file:
     dictionary = json.load(data_file)
files_list = sorted(final_dic.items(), key = operator.itemgetter(1))

print (files_list)
for i in range(5):
	fileindex = files_list[len(files_list)-1-i][0]
	print (dictionary[fileindex])
