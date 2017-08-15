# Assignment:
# 1. Given a set of files with data in it.
# 2. A Query is given and the respective file_names should be displayed.

import os
import sys
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize, wordpunct_tokenize
from bs4 import BeautifulSoup
from nltk.corpus import stopwords


listOfFilepaths=[]
def get_files_in_directory(path):
	# count = 0
	# DictionaryOfWords[filepaths]={}
	for root, dirs, files in os.walk(path):
        	if len(files)!=0:
				for file in files:
					listOfFilepaths.append(root+"/"+file)
					count+=1
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
		# print data
		# print "abhi\n"
		# Use BeautifulSoup to read xml format
		soup = BeautifulSoup(data, 'html.parser')
		# print soup
		# print "shek\n"
		# Exraxt the text from the respective tags
		title = soup.find("title").get_text()
		text = soup.find("text").get_text()
		# textContent stores the text of both the title and text tags.
		textContent = (title+text).strip()
		# Tokenize the text and store in listOfTextContent
		listOfTextContent = wordpunct_tokenize(textContent)
		# Remove stopwords from the list
		for word in listOfTextContent:
			if word not in stop_words:
				stemmedWords.append(porter.stem(word))
		# print stemmedWords
		# print "\n\n\n"
		# stemmedWords contains all the words(tokenized and stemmed) except stopwords


def pushToDict(filename):
	# {{word: {filename: frequency, filename2: frequency}}}
	for word in stemmedWords:
		if word not in DictionaryOfWords:
			DictionaryOfWords[word] = {}
			DictionaryOfWords[word][filename] = 1
		else:
			temp = DictionaryOfWords[word]
			if filename in temp:
				DictionaryOfWords[word][filename]+=1
			else:
				DictionaryOfWords[word][filename] = 1



# argument(folder path) is given in the command line
path=sys.argv[1]
# Call get_files_in_directory function to get the list of all the paths of the files
get_files_in_directory(path)
print ""
# Iterate through every file and extractData
count=0
for filename in listOfFilepaths:
	# filename=listOfFilepaths[filePath]
	# print filename
	extractData(filename)
	pushToDict(count)
	count+=1
	print count
	

