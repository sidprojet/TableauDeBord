from TwitterWebsiteSearch import TwitterClient, SearchQuery
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud
import numpy as np
from spacy.lang.fr.stop_words import STOP_WORDS
### IMPORTER LES TWEETS

lang = "fr"
client = TwitterClient()
query = SearchQuery('légalisation #cannabis  since:2016-01-01 lang:'+lang)
path = './collecte/'+lang+'/'
#USER = 'R'
#OR #marijuana #France  '
count = 0
all_tweet = {}
for page in client.get_search_iterator(query):
    for tweet in page['tweets']:
        all_tweet[count] = tweet
        count+=1
    
num_fichier = str(len(os.listdir(path)))
with open(path+'_cannabis_'+lang + num_fichier + '.json', 'a') as f:
    json.dump(all_tweet, f, ensure_ascii = False)


### CREER LE DF pour les stocker et les traiter
df = pd.DataFrame(columns=["lang", "date", "texte", "hashtags","urls","nb_rt","nb_(y)","user_mentions"])
directory = os.fsencode(path)


hashtags = ""
texte = ""
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
                df.at[rows, "urls"] =  v["entities"]["urls"]
                df.at[rows, "nb_rt"] =  v["retweet_count"]
                df.at[rows, "nb_(y)"] =  v["favorite_count"]
                df.at[rows, "user_mentions"] = v["entities"]["user_mentions"]
                for word in v["entities"]["hashtags"]:
                    hashtags += word.capitalize()
                    hashtags +=" "
                texte += v["text"].replace("#","").replace("@","")
                texte += " "
                rows+=1
        continue
    else:
        continue

### CREER un nuage de mots!
# read the mask image

weed_mask = np.array(Image.open("weed-icon.png"))

wc = WordCloud(collocations=False,background_color="white", stopwords = STOP_WORDS,max_words=2000, mask=weed_mask)
# generate word cloud
wc.generate(hashtags)

# store to file
wc.to_file("WC_WEED.png")


# generate word cloud
wc.generate(texte)

# store to file
wc.to_file("WC2_WEED.png")

# show
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.figure()
plt.imshow(weed_mask, cmap=plt.cm.gray, interpolation='bilinear')
plt.axis("off")
plt.show()

