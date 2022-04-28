from quopri import encodestring
from tkinter import N
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import numpy as np
import sys,json,io
import pymongo


def load_from_mongo():
    client = pymongo.MongoClient("mongodb+srv://jeremy:root@cluster0.5ei45.mongodb.net/database?retryWrites=true&w=majority")
    db = client.database
    collection = db['steam_reviews_cum']
    df= pd.DataFrame(list(collection.find()))
    del df['_id']
    return df

def item(id):  
  return reviews.loc[reviews['app_id'] == id]['app_name'].tolist()[0]  #itemid to name

def recommend(item_id, num):
    print("Recommending " + str(num) + " products similar to " + item(item_id) + "...")   
    print("-------")
    idx = reviews[reviews["app_id"]== item_id].index.tolist()[0] #itemid to index
    similar_indices = cosine_similarities[idx].argsort()[::-1]  #sort the array in descending order and return the index
    
    for i in range(num): 
       print("Recommended: " + item(reviews["app_id"][similar_indices[i+1]]) +
             " (score:" +      str(cosine_similarities[idx][similar_indices[i+1]]) + ")")


# The encoding method must be modified or an error will be reported
# Because'gbk' codec can't encode some character
sys.stdout = io.TextIOWrapper(buffer=sys.stdout.buffer,encoding='utf8')


reviews = load_from_mongo()
# reviews = pd.read_csv('https://raw.githubusercontent.com/alyang666/DS50/main/datastes/steam_reviews_cum.csv')

# Input
item_id_in = int(sys.argv[1])
num_in = int(sys.argv[2])

tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(reviews['review_text'])
cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

# Output
output = str(recommend(item_id_in,num_in))
sys.stdout.write(output)
sys.stdout.flush()








