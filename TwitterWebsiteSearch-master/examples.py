from TwitterWebsiteSearch import TwitterClient, SearchQuery
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud
import numpy as np
### IMPORTER LES TWEETS
client = TwitterClient()
query = SearchQuery('légalisation #cannabis  since:2016-01-01 lang:fr')
path = './collecte/France/'
#USER = 'R'
#OR #marijuana #France  '
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
    
### CREER LE DF pour les stocker et les traiter        
df = pd.DataFrame(columns=["lang", "date", "texte", "hashtags"])
directory = os.fsencode(path)

rows = 0
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".json"):
        with open(path+filename) as data_file:    
            data = json.load(data_file)
            for v in data.values():
                df.at[rows, "lang"] =  v["lang"]
                df.at[rows, "date"] =  v["created_at"]
                df.at[rows, "texte"] = v["text"]
                df.at[rows, "hashtags"] =  v["entities"]["hashtags"]
                rows+=1
        continue
    else:
        continue

### CREER un nuage de mots!


# Read the whole text.
text = df.hashtags.to_string(header=False,index=False)
text = text.replace(",", "")
text = text.replace("[","")
text = text.replace("]","")
text = text.replace("\n"," ")
text = text.replace("\r"," ")
text = text.replace("é","e")
for i in range(5):
    text = text.replace("  ", " ")
text = text.lower()
# read the mask image
weed_mask = np.array(Image.open("weed-icon.png"))

#stopwords = set(STOPWORDS)
#stopwords.add("said")

wc = WordCloud(background_color="white", max_words=2000, mask=weed_mask)
# generate word cloud
wc.generate(text)

# store to file
wc.to_file("WC_WEED.png")

# show
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.figure()
plt.imshow(weed_mask, cmap=plt.cm.gray, interpolation='bilinear')
plt.axis("off")
plt.show()

