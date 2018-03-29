from TwitterWebsiteSearch import TwitterClient, SearchQuery
import json
import os
import pandas as pd
from PIL import Image
from wordcloud import WordCloud
import numpy as np
from spacy.lang.fr.stop_words import STOP_WORDS as FR_ST
from spacy.lang.pt.stop_words import STOP_WORDS as PT_ST
from spacy.lang.nl.stop_words import STOP_WORDS as NL_ST
import datetime
from sklearn import preprocessing
from tqdm import tqdm

import plotly
plotly.tools.set_credentials_file(username='MrEon', api_key='7WED50dvW4vz4jkSsYbh')
import plotly.dashboard_objs as dashboard
import plotly.graph_objs as go
import plotly.plotly as py
### IMPORTER LES TWEETS

def sent2clean(sent):
    sent = sent.lower()
    sent = "".join([X if X.isalpha() else " " for X in sent])
    sent = " ".join(sent.split())
    sent = [word for word in sent.split() if word not in FR_ST and word not in PT_ST and word not in NL_ST]
    sent = " ".join(sent)
    return sent
        

### CREER LE DF pour les stocker et les traiter



def fill_df(path,df,rows = 0):
    directory = os.fsencode(path)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            with open(path+filename) as data_file:
                data = json.load(data_file)
                with tqdm(desc="Insertion dans la table...",total=len(data)) as ibar:
                    for v in data.values():
                        df.at[rows, "id"] = v["user"]["id_str"]
                        df.at[rows, "lang"] =  v["lang"]
                        df.at[rows, "date"] =  datetime.datetime.strftime(pd.to_datetime(v["created_at"]), "%Y-%m-%d")
                        df.at[rows, "texte"] = " ".join([word for word in v["text"].split() 
                                                        if 'http' not in word and word not in FR_ST and word not in PT_ST and word not in NL_ST])
                        df.at[rows, "hashtags"] =  v["entities"]["hashtags"]
                        df.at[rows, "user"] =  v["user"]["screen_name"]
                        df.at[rows, "nb_rt"] =  v["retweet_count"]
                        df.at[rows, "nb_like"] =  v["favorite_count"]
                        df.at[rows, "user_mentions"] = v["entities"]["user_mentions"]
                        rows+=1
                        ibar.update()
            continue
        else:
            continue
    df["texte"].apply(sent2clean)
    return df

def wordcloud(df, tags = True, lang = "fr"):
    print("Creating  Wordcloud for "+lang.capitalize())
    ### CREER un nuage de mots!
    # read the mask image
    weed_mask = np.array(Image.open("weed-icon.png"))
    STOP_WORD = FR_ST
    if lang == "pt" :
        STOP_WORD = PT_ST
    elif lang == "nl":
        STOP_WORD = NL_ST
    wc = WordCloud(collocations=False,background_color="white", stopwords = STOP_WORD,max_words=2000, mask=weed_mask)
    
    if tags:
        hashtags = [" ".join(row["hashtags"]) for index,row in df.iterrows() if row["lang"] == lang]
        hashtags = " ".join(hashtags)
        # generate word cloud
        wc.generate(hashtags)
        # store to file
        wc.to_file("#WC_WEED_"+lang+".png")
    texte = ["".join(row["texte"]) for index,row in df.iterrows() if row["lang"] == lang]
    texte = " ".join(texte)
    
    # generate word cloud
    wc.generate(texte)
    # store to file
    wc.to_file("WC_WEED_"+lang+".png")
    return wc



#https://plot.ly/python/create-online-dashboard/
def bar_plot_dates(lang = "fr"):
    my_dboard = dashboard.Dashboard()
    my_dboard.get_preview()
    dates = [row["date"] for index,row in df.iterrows() if row["lang"] == lang]
    months, tweet_count = np.unique(dates,return_counts = True)
    
    data = [go.Bar(
                x=months,
                y=tweet_count
        )]
    fname= 'daily-barplot-'+lang
    py.iplot(data, filename=fname)
    
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
    
    tweet_ = ""
    mc_ = ""
    men_ = ""
    hash_ = ""
    cmen_ = ""
    cm_ = ""
    chash_ = ""

    with tqdm(desc="Writing insert instructions...", total=len(df)) as fbar:
        for i in range(len(df)):
            
            tweet_ += "INSERT INTO tweets VALUES ("+str(df.id[i])+", \'"+df.user[i]+"\', "+str(df.nb_rt[i])+", "+str(df.nb_like[i])+", "+str(df.date[i])+", \'"+df.lang[i]+"\')\n"
            
            mc_ += " ".join(["INSERT INTO motsCles VALUES ("+str(le_text.transform([word])[0])+", \'"+word+"\')\n" for word in df.texte[i].split(" ")])
            cm_ += " ".join(["INSERT INTO comp_motscles VALUES ("+str(df.id[i])+", "+str(le_text.transform([word])[0])+")\n" for word in df.texte[i].split(" ")])
            '''
            for word in df.texte[i].split(" "):
                #word = word.replace("#","").replace("@","")
                mc_ += "INSERT INTO motsCles VALUES ("+str(le_text.transform([word])[0])+", \'"+word+"\')\n"
                cm_ += "INSERT INTO comp_motscles VALUES ("+str(df.id[i])+", "+str(le_text.transform([word])[0])+")\n"
            '''
            
            if df.user_mentions[i]: 
                for men in df.user_mentions[i]:
                    men_ += "INSERT INTO mentionnees VALUES ("+str(men["id_str"])+", \'"+men["screen_name"]+"\')\n"
                    cmen_ += "INSERT INTO comp_mention VALUES ("+str(df.id[i])+", "+str(men["id_str"])+")\n"
            
            
            for hasht in df.hashtags[i]:
                hash_ += "INSERT INTO hashtag VALUES ("+str(le_hash.transform([hasht.capitalize()])[0])+", \'"+hasht+"\')\n"
                chash_ += "INSERT INTO comp_hashtag VALUES ("+str(df.id[i])+", "+str(le_hash.transform([hasht.capitalize()])[0])+")\n"
            
            fbar.update()
     
    t_tweet  = open("./inserts/tweets_insert.txt", "w").write(tweet_)
    tweet_ = ""
    
    t_motscles = open("./inserts/motcles_insert.txt","w").write(mc_)
    mc_ = ""

    t_mention = open("./inserts/mentions_insert.txt","w").write(men_)
    men_ = ""
    t_hash = open("./inserts/hashtags_insert.txt","w").write(hash_)
    hash_ = ""
    comp_mention = open("./inserts/comp_mention.txt","w").write(cmen_)
    cmen_ = ""
    comp_mots = open("./inserts/comp_motscles.txt","w").write(cm_)
    cm_ = ""
    comp_hash = open("./inserts/comp_hashtags.txt","w").write(chash_)
    chash_ = ""
    
def like_mean(lang = "fr"):
    return np.mean([row["nb_like"] for index,row in df.iterrows() if row["lang"] == lang])

def rt_mean(lang ="fr"):
    return np.mean([row["nb_rt"] for index,row in df.iterrows() if row["lang"] == lang])

def most_cited_person(lang = "fr", borne = 10):
    cited = [row["user_mentions"][0]["screen_name"] for index,row in df.iterrows() if row["lang"] == lang and row["user_mentions"]]
    cited, count = np.unique(cited, return_counts = True)
    c1 , c2 = (list(t) for t in zip(*sorted(zip(count, cited))))
    return c2[-borne:-1], c1[-borne:-1]

def most_used_word(lang = "fr", borne = 10):
    texte = ["".join(sent2clean(row["texte"])) for index,row in df.iterrows() if row["lang"] == lang]
    texte = " ".join(texte)
    words, count = np.unique(texte.lower().split(), return_counts = True)
    c1 , c2 = (list(t) for t in zip(*sorted(zip(count, words))))
    return c2[-borne:-1], c1[-borne:-1]


client = TwitterClient()

df = pd.DataFrame(columns=["id","lang", "date", "texte", "hashtags","user","nb_rt","nb_like","user_mentions"])
for lang in ["fr","pt","nl"]:
    path = './collecte/'+lang+'/'

    q = 'since:2010-01-01 lang:'+lang
    qu = ""
    if lang == "fr":
        qu = "cannabis "+q
    elif lang == "pt":
        qu = "canabis "+q
    elif lang == "nl":
        qu = "hennep "+q
        
    query = SearchQuery(qu)
    

    print("Variables set, lang = "+lang)
    
    count = 0
    all_tweet = {}
    for page in client.get_search_iterator(query):
        
        if not page or not page['tweets']:
            print('empty')
            continue
    
        for tweet in page['tweets']:
            all_tweet[count] = tweet
            count+=1
            if count%1000 == 0:
             	print(count, sep=' ', end=' ', flush=True)

    print("dumping twitter data into JSON")
    num_fichier = str(len(os.listdir(path)))
    with open(path+'_cannabis_'+lang + num_fichier + '.json', 'a') as f:
        json.dump(all_tweet, f, ensure_ascii = False)

    print("Data Collected")
    df = fill_df(path,df,len(df))

for lang in ["fr","pt","nl"]:    
    try:
        wordcloud(df, True, lang)
        print("WordCloud generated")
    except ValueError:
        print("Bad wording!")
    #bar_plot_dates(lang)
    print("\nMoyenne Likes:")
    print(lang+" "+str(like_mean(lang)))
    print("\nMoyenne de Retweets:")
    print(lang+" "+str(rt_mean(lang)))
    print("\nPersonnes les plus citées:")
    cited, count = most_cited_person(lang)
    print(lang+" "+str(cited)+" "+str(count))
    print("\nMots les plus utilisés:")
    print(most_used_word(lang, 20))
#write_inserts(df)

