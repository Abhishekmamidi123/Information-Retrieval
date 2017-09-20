import os
import sys
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize, wordpunct_tokenize
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import cPickle as pickle
import json
# Make it work for Python 2+3 and with Unicode
import io
try:
    to_unicode = unicode
except NameError:
    to_unicode = str

Files = {}
listOfFilepaths={}
def get_files_in_directory(path):
    count = 0
    for root, dirs, files in os.walk(path):
        if len(files)!=0:
            for file in files:
                listOfFilepaths[count]=(root+"/"+file)
		print root+"/"+file
                count+=1
    print listOfFilepaths

path=sys.argv[1]
get_files_in_directory(path)
with io.open('filePaths.json', 'w', encoding='utf8') as outfile:
    str_ = json.dumps(listOfFilepaths,
                      indent=4, sort_keys=True,
                      separators=(',', ': '), ensure_ascii=False)
    outfile.write(to_unicode(str_))
