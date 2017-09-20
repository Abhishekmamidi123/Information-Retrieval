import json
import io
try:
    to_unicode = unicode
except NameError:
    to_unicode = str

with open('data1.json') as data_file:
    DictionaryOfWords = json.load(data_file)

tfIdfDict = {}
for word in DictionaryOfWords:
	if word!='filenames':
		tfIdfDict[word] = {}
		Dict = DictionaryOfWords[word]
		for x in Dict:
			if x!='count':
				tfIdfDict[word][x] = Dict[x][0]
		tfIdfDict[word]['file_count'] = len(DictionaryOfWords[word])-1
		
with io.open('tf-idf_preprocess.json', 'w', encoding='utf8') as outfile:
    str_ = json.dumps(tfIdfDict,
                      indent=4, sort_keys=True,
                      separators=(',', ': '), ensure_ascii=False)
    outfile.write(to_unicode(str_))
