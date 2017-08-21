import os
import json
from nltk.tokenize import wordpunct_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

# Make it work for Python 2+3 and with Unicode
import io
try:
    to_unicode = unicode
except NameError:
    to_unicode = str

stop_words = set(stopwords.words('english'))
stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}']) # remove it if you need punctuation
porter = PorterStemmer()

# Open and read an json file
with open('data.json') as data_file:
    DictionaryOfWords = json.load(data_file)
for word in DictionaryOfWords:
	print word, DictionaryOfWords[word]

print "\n\n"
# Query search
query = "abhishek alekya"
queryList = wordpunct_tokenize(query)

for word in queryList:
	if word not in stop_words:
		print word, DictionaryOfWords[porter.stem(word)]
