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

# argument(folder path) is given in the command line
path=sys.argv[1]
# Call get_files_in_directory function to get the list of all the paths of the files
get_files_in_directory(path)
