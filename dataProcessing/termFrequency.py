import operator 
import json
import preprocess as pre
from collections import Counter
from nltk.corpus import stopwords
import string

def termFrequency(geoBuilding, buildingFreq):
    punctuation = list(string.punctuation)
    stop = stopwords.words('english') + punctuation + ['rt', 'via']

    '''
    fname = 'Jets.json'
    with open(fname, 'r') as f:
        count_all = Counter()
        for line in f:
        	tweet = json.loads(line)
        	terms_stop = [term for term in pre.preprocess(tweet['text']) if term not in stop]
        	terms_only = [term for term in pre.preprocess(tweet['text'])
                  if term not in stop and
                  not term.startswith(('#', '@'))]
            terms_bigram = bigrams(terms_stop)
            #count_all.update(terms_bigram)
        # Print the first 5 most frequent words
        print(count_all.most_common(10))
    '''

    with open(geoBuilding, 'r') as f:
        tweet = json.load(f)
        count_all = Counter()
        building_type = []
        for data in tweet['features']:
            if data['buildings']:
                for type in data['buildings']:
                    building_type.append(type['type'])
                    count_all.update(building_type)
    with open(buildingFreq,'w') as freq:
        for term, count in count_all.most_common(10):
            print("{}: {}". format(term, count))
            freq.write("{}: {}". format(term, count))
            freq.write('\n')


