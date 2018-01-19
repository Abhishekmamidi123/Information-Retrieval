import os
import sys
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize, wordpunct_tokenize
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import pickle
import json
import io
import numpy as np
import math
try:
    to_unicode = unicode
except NameError:
    to_unicode = str

stop_words = set(stopwords.words('english'))
stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}'])
#PorterStemmer = porter()
porter = PorterStemmer()
dictionary = {}
word_file_frequency = {}

with open('filePaths.json') as data_file:
	#global dictionary
	dictionary = json.load(data_file)

with open('data.json') as file:
	#global word_file_frequency
	word_file_frequency = json.load(file)

##########################################################
'''
Creating tf_vectors for each document
'''
N=0 # No of documents in the corpus
tf_vectors = {}

for key in dictionary:
	N += 1
	tf_for_doc = []
	for word in word_file_frequency:
		dic = word_file_frequency[word]
		if(key in dic):
			tf_for_doc.append(1+math.log(dic[key][0]))
		else:
			tf_for_doc.append(0)
	tf_vectors[key] = tf_for_doc
##########################################################
'''
Creating idf_vector
'''
idf_vectors = []

for word in word_file_frequency:
    #dict = word_file_frequency[word]
	idf_vectors.append( math.log(float(N)/float(len(word_file_frequency[word].keys())-1)))
###########################################################

tf_idf_vector = {}
idf_vector_np = np.array(idf_vectors)

for key in dictionary:
	tf_vector_np = np.array(tf_vectors[key])
	tf_idf_vector[key] = list(np.multiply(tf_vector_np, idf_vector_np))
############################################################
with io.open('tf_idf_vectors.json', 'w', encoding='utf8') as outfile:
    str_ = json.dumps(tf_idf_vector,
    		sort_keys=True,
            separators=(',', ': '), ensure_ascii=False)

    outfile.write(to_unicode(str_))
