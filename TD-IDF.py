from quopri import encodestring
from tkinter import N
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import numpy as np
import pymysql
import sys,json,io



# 目前仍采用本地mysql数据库 待线上mongodb部署好后在修改
def load_from_mysql():
    conn = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        passwd="",
        db="steamtest",
        charset="utf8"
    )
    cursor = conn.cursor()
    cursor.execute('set autocommit=1')
    # sql = "delete from heart_2020_cleaned where BMI=94.85"
    sql = "SELECT app_id,app_name,GROUP_CONCAT(review_text) as 'review_cum' FROM dataset GROUP BY app_id,app_name;"
    cursor.execute(sql)
    dataframe = pd.read_sql(sql, conn)
    cursor.close()
    conn.close()
    return dataframe

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


reviews = load_from_mysql()

item_id_in = int(sys.argv[1])
num_in = int(sys.argv[2])
tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(reviews['review_cum'])
cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

output = str(recommend(item_id_in,num_in))
sys.stdout.write(output)
sys.stdout.flush()








