import os
query = 'rays of hope and sunshine'
result = os.popen("python 3_phraseQueries.py '" + str(query)  + "'").read()
print result
