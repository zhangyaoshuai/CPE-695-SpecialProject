import operator 
import json
import preprocess as pre
from collections import Counter
from nltk.corpus import stopwords
import string
from nltk import bigrams 
import vincent

punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via']

fname = 'stream_NewYork.json'
with open(fname, 'r') as f:
    count_all = Counter()
    for line in f:
    	tweet = json.loads(line)
    	terms_stop = [term for term in pre.preprocess(tweet['text']) if term not in stop]
    	terms_only = [term for term in pre.preprocess(tweet['text']) 
              if term not in stop and
              not term.startswith(('#', '@'))]
        terms_bigram = bigrams(terms_only) 
        count_all.update(terms_bigram)
    #Print the first 5 most frequent words
    #print(count_all.most_common(10))
word_freq = count_all.most_common(10)
labels, freq = zip(*word_freq)
data = {'data': freq, 'x': labels}
bar = vincent.Bar(data, iter_idx='x')
open('term_freq_newyork.json', 'w').close()
bar.to_json('term_freq_newyork.json')

