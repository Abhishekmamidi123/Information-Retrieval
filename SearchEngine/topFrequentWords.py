import json
import io
try:
    to_unicode = unicode
except NameError:
    to_unicode = str

f = open('top_twenty_just_words.txt', 'w')
with open('word-frequency.json') as data_file:
    dictWords = json.load(data_file)

#print dictWords
length = len(dictWords)*0.2
#print length
topFrequentWordsList = []
topFrequentWordsList = sorted(dictWords, key=dictWords.get)[::-1][0:int(length)]

#print topFrequentWordsList

topFrequentWords = {}
count = 0
for x in topFrequentWordsList:
	topFrequentWords[count] = x
	f.write(x)
	f.write("\n")
	count+=1
f.close()			
# with io.open('topFrequentWords.json', 'w', encoding='utf8') as outfile:
#    str_ = json.dumps(topFrequentWords,
 #                     indent=4, sort_keys=True,
  #                    separators=(',', ': '), ensure_ascii=False)
   # outfile.write(to_unicode(str_))
#f.close()
