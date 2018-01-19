import os
import sys
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize, wordpunct_tokenize
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import cPickle as pickle
import json
import io
try:
    to_unicode = unicode
except NameError:
    to_unicode = str


stop_words = set(stopwords.words('english'))
stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}'])
porter = PorterStemmer()

finalvectordictionary = {}
toptwentypercentwords = []
word_file_frequency = {}

#############################################################################
'''
toptwentypercentwords reads following file:

word1
word2
...
...

Top 20% words sorted according to frequency
'''

def read_top_twenty_per_cent_words(filename):
	with open(filename) as file:
		y = file.read()
	global toptwentypercentwords 
	toptwentypercentwords = y.split('\n')
	print (len(toptwentypercentwords))
	print ("**********")
#############################################################################
'''
word_file_frequency reads following file:
{
	w1 : { "f1": freq(w1) in f1, ....., "f_i": freq(w1) in f_i }
	w2 : { "f2": freq(w2) in f2, ....., "f_j": freq(w1) in f_j }
	....
	....
	....
}

'''

def read_all_words_frequency_in_each_file(filename):
	global word_file_frequency
	with open(filename) as file:
		word_file_frequency = json.load(file)

#############################################################################
'''
Arguments of create_docvectors function:
	filename = "/home/folder1/folder2/..../filename"
	fileindex = "0"

How for loop works:
	word = 	w1 from toptwentypercentwords
	x = {"f1": [freq(word) in f1,pos1,..] ....., "f_i": freq(word) in f_i }

	if fileindex is in [f1, f2, ....., fn]
		get freq(word) and append to documentvector

Return:
    documentvector which has length of 20% of words in the corpus
'''
def create_docvectors(filename, fileindex):
	documentvector = []
	global finalvectordictionary
	for word in toptwentypercentwords:
		if (len(word) >= 1):
			x = word_file_frequency[word]
		if(fileindex in x):
            #li = x[fileindex]
			documentvector.append(x[fileindex][0])
		else:
			documentvector.append(0)
	finalvectordictionary[fileindex] = documentvector
#############################################################################
def write_in_jsonfile(finalvectordictionary):
	with io.open('cosine_doc_vectors.json', 'w', encoding='utf8') as outfile:
    		str_ = json.dumps(finalvectordictionary,
                      sort_keys=True,
                      separators=(',', ': '), ensure_ascii=False)
    		outfile.write(to_unicode(str_))

################################################################################

read_top_twenty_per_cent_words('top_twenty_just_words.txt')
read_all_words_frequency_in_each_file('word_frequency_in_each_file.json')

with open('file_paths.json') as data_file:
     dictionary = json.load(data_file)
for key in dictionary:
	create_docvectors(dictionary[key], key)

write_in_jsonfile(finalvectordictionary)
