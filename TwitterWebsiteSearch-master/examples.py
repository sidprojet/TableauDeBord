from TwitterWebsiteSearch import TwitterClient, SearchQuery
import json
import os
import pandas as pd

client = TwitterClient()
query = SearchQuery('légalisation #cannabis')
path = '/home/formationsid/Documents/M1SID/TableauDeBord/TwitterWebsiteSearch-master/donnees/'
#USER = 'R'
#OR #marijuana #France  '
#since:2016-01-01
count = 0
all_tweet = {}
for page in client.get_search_iterator(query):
    for tweet in page['tweets']:
        #if tweet['lang'] == 'en':
        tweet['entities'] = dict(tweet['entities'])
        all_tweet[count] = tweet
        count+=1
    
        if count%200 == 0:
            num_fichier = str(len(os.listdir(path)))
            with open(path+'_cannabis_fr' + num_fichier + '.json', 'a') as f:
                json.dump(all_tweet, f, ensure_ascii = False)
            all_tweet = {}
            

