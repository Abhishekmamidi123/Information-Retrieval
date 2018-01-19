# Algorithm:
# To output generic summary for documents.

# Process:
# Get the file index of the input file for which summary is to be produced.
# Get the list of sentences of the file.
# Calculate the sentence similarities and thus the underlying graph for sentence ranking.
# Calculate the sentence ranking using degree centrality
# Dislplay the top 3 weighted sentences of the document as the summary. 


from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize, wordpunct_tokenize
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import nltk.data
import sys,os
import json
import math
import numpy as np

# Make it work for Python 2+3 and with Unicode
import io
try:
    to_unicode = unicode
except NameError:
    to_unicode = str


stop_words = set(stopwords.words('english'))
stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}']) # remove it if you need punctuation
porter = PorterStemmer()
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

sentenceList=[]
stemmedList=[]
n=0
def get_file_sentences_and_idf(filename):

	''' Get sentences from the document 
	    input: filename
	    output:sentenceList'''

	global sentenceList
	global stemmedList
	global n
	doc=open(filename,'r')

	# extract the content in the file and store it in data
	data = "".join(line.rstrip() for line in doc) 

	# lower case the words
	data = data.lower()                        	  

	# Use BeautifulSoup to read xml format
	soup = BeautifulSoup(data, 'html.parser')	

	# Extract the text from the respective tags  
	try:                                          
		text = soup.find("text").get_text()
	except AttributeError:
	    text = ""
	sentenceList=('\n'.join(tokenizer.tokenize(text))).split('\n')
	n = len(sentenceList)
	calculate_idf()


#get unique words of two sentences
def get_unique_words(sen1,sen2):

	''' Get unique words from the sentences
	    input: two sentences sen1, sen2
	    output:unique_list'''

	global sentenceList
	unique_list = list(set(sen1.split()).union(set(sen2.split())))
	return unique_list


#idf values for all the words in the doc
idf={}

#calculate idf			 
def calculate_idf():

	''' Calculate idf values for the words in the document
	    output:idf'''

	word_dict = {}
	global n
	for i in range(len(sentenceList)):
		lis = []
		lis = sentenceList[i].split()
		count = 0
		for word in lis:
			if word not in word_dict:
				word_dict[word] = []
			if i not in word_dict[word]:
				word_dict[word].append(i)
	for word in word_dict:
		idf[word] = math.log(float(n)/float(len(word_dict[word])),10)

#dictionary for similarities of every two sentences
sentence_similarities={}

#calculate sentence similarities using idf-cosine similarities
def calculate_similarities():

	''' Calculate sentence similarities
	    output:sentence_similarities'''

	global sentence_similarities
	for i in range(len(sentenceList)-1):
		for k in range(i+1,len(sentenceList)):
			unique_list = get_unique_words(sentenceList[i],sentenceList[k])
			sen1_list = sentenceList[i].split()
			sen2_list = sentenceList[k].split()
			vector1 = []
			vector2 = []
			for word in unique_list:
				if word in sen1_list:
					vector1.append(sen1_list.count(word))
				else:
					vector1.append(0)
				if word in sen2_list:
					vector2.append(sen2_list.count(word))
				else:
					vector2.append(0)

			# result_vector is the result of element-wise product of two sentence vectors
			result_vector = (np.asarray(vector1, dtype=np.float32)*np.asarray(vector2, dtype=np.float32)).tolist()
			numerator = 0
			tf_idf1=0
			tf_idf2=0
			for j in range(len(result_vector)):
				if result_vector[j]!=0:
					numerator+= (result_vector[j])*(idf[unique_list[j]]**2)
				if unique_list[j] in sen1_list:
					tf_idf1+= ( (sen1_list.count(unique_list[j])) * (idf[unique_list[j]]) )**2
				if unique_list[j] in sen2_list:
					tf_idf2+= ( (sen2_list.count(unique_list[j])) * (idf[unique_list[j]]) )**2
			denominator = ((math.sqrt(tf_idf1))*(math.sqrt(tf_idf2)))
			sentence_similarities[str(i)+" "+str(k)]=(float(numerator)/float(denominator))


# dictionary to store sentence weights
sentence_rank={}

# matrix to store all sentence to sentence mappings 
matrix={}				

# sentences whose weights are greater than the given threshold
valid_sentences=[]
def get_summary():

	''' Calculate degree centrality and thus the summary of the text
	    output:valid_sentences, matrix, "sentence_links.txt" '''

	global sentenceList,n
	global matrix
	global sentence_similarities
	global valid_sentences
	global sentence_rank
	key_max = max(sentence_similarities.keys(), key=(lambda k: sentence_similarities[k]))
	key_min = min(sentence_similarities.keys(), key=(lambda k: sentence_similarities[k]))
	threshold = float(sentence_similarities[key_max]+sentence_similarities[key_min])/float(2)
	# select the sentences with weights greater than the given threshold
	for i in sentence_similarities:
		if sentence_similarities[i]>threshold:
			nodes=[]
			nodes=i.split()
			valid_sentences.append(nodes)
		
	# fill the matrix with mappings according to similarities
	for i in range(n):
		for lis in valid_sentences:
			if str(i) in lis:
				if str(i) not in matrix:
					matrix[str(i)]=[]
				node = lis[(lis.index(str(i))+1)%2]
				if node not in matrix[str(i)]:
					matrix[str(i)].append(node)
				
	# write the matrix in the file 'sentence_links.txt'
	with open('sentence_links.txt','w') as f:
		for key in matrix:
			f.write(key)
			for i in matrix[key]:
				f.write(" "+i)
			f.write('\n')
		f.close()

	data = os.popen('python 5_pageRank.py sentence_links.txt 2').read()
	#print "\n","######## SUMMARY #######\n	"
	a=data.strip().split('\n')
	d=a[2:]
	d.sort()
	rank_list=[]
	summary = ''
	for i in d:
		summary+= sentenceList[int(i)].capitalize()
	#print "\n"
	print summary
	#print "\n"
	
path=sys.argv[1]
fileData=open('filePaths.json','r')
fileDict=json.load(fileData)
fileIndex = [k for k,v in fileDict.items() if v==path]
get_file_sentences_and_idf(path)
calculate_similarities()
get_summary()
