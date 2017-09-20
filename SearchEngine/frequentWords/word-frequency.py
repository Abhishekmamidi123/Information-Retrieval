import json
import io
try:
    to_unicode = unicode
except NameError:
    to_unicode = str

with open('data1.json') as data_file:
    DictionaryOfWords = json.load(data_file)

wordFrequency = {}
for word in DictionaryOfWords:
	if word!='filenames':
		wordFrequency[word] = DictionaryOfWords[word]['count']
with io.open('word-frequency.json', 'w', encoding='utf8') as outfile:
    str_ = json.dumps(wordFrequency,
                      indent=4, sort_keys=True,
                      separators=(',', ': '), ensure_ascii=False)
    outfile.write(to_unicode(str_))
