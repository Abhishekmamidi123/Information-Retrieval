# Assignment:
# 1. Given a set of files with data in it.
# 2. A Query is given and the respective file_names should be displayed.

# Process:
# Find PathOfFiles.
# Extract data from xml files.
# Apply tokenization on the data.
# Remove stopwords(english) from the data.
# Apply Stemming on every word.
# Create an index table of words with frequency and the file numbers to which the word belong.
# Sort the words and merge the repeating words.
# Based on the query given, print the respective filenames.


import os
import sys
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize, wordpunct_tokenize
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
# import cPickle as pickle
import json
# Make it work for Python 2+3 and with Unicode
import io
try:
    to_unicode = unicode
except NameError:
    to_unicode = str

stemmedWords = []
Files = {}
# The main dictionary in which all the data is stored.
DictionaryOfWords = {}
stop_words = set(stopwords.words('english'))
stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}']) # remove it if you need punctuation
porter = PorterStemmer()

# Get the paths of all files in the directory and store it in the list  "listOfFilepaths"
listOfFilepaths={}
def get_files_in_directory(path):
    count = 0
    for root, dirs, files in os.walk(path):
        if len(files)!=0:
            for file in files:
                print(root+'/'+file)
                count+=1
                listOfFilepaths[count]=(root+"/"+file)
		# print(root+'/'+file)
		# count+=1
    # DictionaryOfWords["filenames"]=listOfFilepaths
    Files["filenames"]=listOfFilepaths
    # for word in DictionaryOfWords:
    #     print word, DictionaryOfWords[word]
    # print "\n"
    # print listOfFilepaths
    # for file_path in listOfFilepaths:
	# 	print file_path
	

# Extract contents and process them.
def extractData(filename):
	# open filename as file
	with open(filename) as file:
		# extract the content in the file and store it in data
		data = "".join(line.rstrip() for line in file)
		# lower case the words
		data = data.lower()
		# Use BeautifulSoup to read xml format
		soup = BeautifulSoup(data, 'html.parser')
		# Exraxt the text from the respective tags
		try:
	    		title = soup.find("title").get_text()
		except AttributeError:
	    		title = ""
		try:
	    		text = soup.find("text").get_text()
		except AttributeError:
	    		text = ""
		# textContent stores the text of both the title and text tags.
		textContent = (title+text).strip()
		# Tokenize the text and store in listOfTextContent
		listOfTextContent = wordpunct_tokenize(textContent)
		# Remove stopwords from the list
		for word in listOfTextContent:
			if word not in stop_words:
				stemmedWords.append(porter.stem(word))
		# stemmedWords contains all the words(tokenized and stemmed) except stopwords

def pushToDict(fileno):
	# {{word: {fileno: frequency, fileno: frequency}}}
	index=0
	for word in stemmedWords:
		if word not in DictionaryOfWords:
			DictionaryOfWords[word] = {}
			DictionaryOfWords[word]["count"]=1
			DictionaryOfWords[word][fileno] = []
			DictionaryOfWords[word][fileno].append(1)
			DictionaryOfWords[word][fileno].append(index)
		else:
			DictionaryOfWords[word]["count"]+=1
			temp = DictionaryOfWords[word]
			if fileno in temp:
				# DictionaryOfWords[word][fileno]+=1
				DictionaryOfWords[word][fileno][0]+=1
				DictionaryOfWords[word][fileno].append(index)
			else:
				DictionaryOfWords[word][fileno] = []
				DictionaryOfWords[word][fileno].append(1)
				DictionaryOfWords[word][fileno].append(index)
		index=index+1

# main function
# argument(folder path) is given in the command line
path=sys.argv[1]
# Call get_files_in_directory function to get the list of all the paths of the files
get_files_in_directory(path)

with io.open('filePaths.json', 'w', encoding='utf8') as outfile:
    str_ = json.dumps(listOfFilepaths,
                      indent=4, sort_keys=True,
                      separators=(',', ': '), ensure_ascii=False)
    outfile.write(to_unicode(str_))

# Iterate through every file and extractData
for fileno in listOfFilepaths:
	print(listOfFilepaths[fileno])
	extractData(listOfFilepaths[fileno])
	pushToDict(fileno)
	stemmedWords=[]
	# print DictionaryOfWords

# Just for printing
# for word in DictionaryOfWords:
# 	print word, DictionaryOfWords[word]
# print "\n"

# Store in a json file
with open('data.json', 'w') as outfile:
    json.dump(DictionaryOfWords, outfile)
#    str_ = json.dumps(DictionaryOfWords,
#                      indent=4, sort_keys=True,
#                      separators=(',', ': '), ensure_ascii=False)
#    outfile.write(to_unicode(str_))
