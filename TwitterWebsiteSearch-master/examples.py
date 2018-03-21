from TwitterWebsiteSearch import TwitterClient, SearchQuery
import json
import os
import pandas as pd
from PIL import Image
from wordcloud import WordCloud
import numpy as np
from spacy.lang.fr.stop_words import STOP_WORDS
import datetime
from sklearn import preprocessing
from tqdm import tqdm

import plotly
plotly.tools.set_credentials_file(username='MrEon', api_key='7WED50dvW4vz4jkSsYbh')
import plotly.dashboard_objs as dashboard
import plotly.graph_objs as go
import plotly.plotly as py
### IMPORTER LES TWEETS


def set_var(lang = "fr"):
    query = SearchQuery('légalisation #cannabis  since:2010-01-01 lang:'+lang)
    path = './collecte/'+lang+'/'
    return lang,query,path


def collect_data(client, query, path, lang = "fr"):
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


def fill_df(path,df,rows = 0):
    hashtags = ""
    texte = ""
    
    directory = os.fsencode(path)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            with open(path+filename) as data_file:
                data = json.load(data_file)
                for v in data.values():
                    df.at[rows, "id"] = v["user"]["id_str"]
                    df.at[rows, "lang"] =  v["lang"]
                    df.at[rows, "date"] =  datetime.datetime.strftime(pd.to_datetime(v["created_at"]), "%Y-%m-%d")
                    df.at[rows, "texte"] = v["text"]
                    df.at[rows, "hashtags"] =  v["entities"]["hashtags"]
                    df.at[rows, "user"] =  v["user"]["screen_name"]
                    df.at[rows, "nb_rt"] =  v["retweet_count"]
                    df.at[rows, "nb_like"] =  v["favorite_count"]
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
    return df

def wordcloud(df, tags = True, lang = "fr"):
    ### CREER un nuage de mots!
    # read the mask image
    weed_mask = np.array(Image.open("weed-icon.png"))
    wc = WordCloud(collocations=False,background_color="white", stopwords = STOP_WORDS,max_words=2000, mask=weed_mask)
    
    if tags:
        hashtags = [" ".join(row["hashtags"]) for index,row in df.iterrows() if row["lang"] == lang]
        hashtags = " ".join(hashtags)
        # generate word cloud
        wc.generate(hashtags)
        # store to file
        wc.to_file("#WC_WEED_"+lang+".png")
    texte = [" ".join(row["texte"]) for index,row in df.iterrows() if row["lang"] == lang]
    texte = " ".join(texte)
    # generate word cloud
    wc.generate(texte)
    # store to file
    wc.to_file("WC_WEED_"+lang+".png")
    return wc



#https://plot.ly/python/create-online-dashboard/
def bar_plot_dates():
    my_dboard = dashboard.Dashboard()
    my_dboard.get_preview()
    
    months, tweet_count = np.unique(df.date,return_counts = True)
    
    data = [go.Bar(
                x=months,
                y=tweet_count
        )]
    
    py.iplot(data, filename='basic-bar')
    
def write_inserts(df):
    le_hash = preprocessing.LabelEncoder()
    le_text = preprocessing.LabelEncoder()
    
    a_hashtag = []
    for h in df.hashtags:
        a_hashtag.extend(h)
    a_hashtag = np.unique(a_hashtag)
    le_hash.fit([x.replace("#","").replace("@","").capitalize() for x in a_hashtag])
    
    text_list = np.unique([x.split(" ") for x in df.texte])
    word_list = []
    for l in text_list:
        word_list.extend(l)
    le_text.fit(word_list)
    
    t_tweet  = open("./inserts/tweets_insert.txt", "w")
    t_motscles = open("./inserts/motcles_insert.txt","w")
    t_mention = open("./inserts/mentions_insert.txt","w")
    t_hash = open("./inserts/hashtags_insert.txt","w")
    comp_mention = open("./inserts/comp_mention.txt","w")
    comp_mots = open("./inserts/comp_motscles.txt","w")
    comp_hash = open("./inserts/comp_hashtags.txt","w")
    with tqdm(desc="Writing insert instructions...", total=len(df)) as fbar:
        for i in range(len(df)):
            t_tweet.write("INSERT INTO tweets VALUES ("+str(df.id[i])+", "+df.user[i]+", "+str(df.nb_rt[i])+
                                            ", "+str(df.nb_like[i])+", "+str(df.date[i])+", "+df.lang[i]+")\n")
            a_text = df.texte[i].split(" ")
            for word in a_text:
                empty = []
                empty.append(word)
                #word = word.replace("#","").replace("@","")
                t_motscles.write("INSERT INTO motsCles VALUES ("+str(le_text.transform(empty)[0])+", "+word+")\n")
                comp_mots.write("INSERT INTO comp_motscles VALUES ("+str(df.id[i])+", "+str(le_text.transform(empty)[0])+")\n")
            
            if df.user_mentions[i]: 
                for men in df.user_mentions[i]:
                    t_mention.write("INSERT INTO mentionnees VALUES ("+str(men["id_str"])+", "+men["screen_name"]+")\n")
                    comp_mention.write("INSERT INTO comp_mention VALUES ("+str(df.id[i])+", "+str(men["id_str"])+")\n")
            for hasht in df.hashtags[i]:
                empty = []
                empty.append(hasht.capitalize())
                t_hash.write("INSERT INTO hashtag VALUES ("+str(le_hash.transform(empty)[0])+", "+hasht+")\n")
                comp_hash.write("INSERT INTO comp_hashtag VALUES ("+str(df.id[i])+", "+str(le_hash.transform(empty)[0])+")\n")
            fbar.update()
        
    t_tweet.close()
    t_motscles.close()
    t_mention.close()
    t_hash.close()
    comp_mention.close()
    comp_mots.close()
    comp_hash.close()
    
    
client = TwitterClient()
df = pd.DataFrame(columns=["id","lang", "date", "texte", "hashtags","user","nb_rt","nb_like","user_mentions"])
for l in ["fr","pt","nl"]:
    lang, query, path = set_var(l)
    collect_data(client, query, path)
    df = fill_df(path,df,len(df))
    wordcloud(df, False, lang)

write_inserts(df)