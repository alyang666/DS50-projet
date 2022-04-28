import pandas as pd
import numpy as np
import heapq
import sys
import pymongo



def load_from_mongo():
    client = pymongo.MongoClient("mongodb+srv://jeremy:root@cluster0.5ei45.mongodb.net/database?retryWrites=true&w=majority")
    db = client.database
    collection = db['steam_games2']
    df= pd.DataFrame(list(collection.find()))
    del df['_id']
    return df



# Translate games' name to index
def name2idx(name):
    idx = steam[steam["name"]== name].index.tolist()[0]
    return idx

def get_score(name):
    game_index=name2idx(name)
    score = [0]*40789
    for i in range(len(tags[game_index])):
        for indexs in steam.index:
            if(indexs != game_index):
                for j in range(len(tags[indexs])):
                    if tags[game_index][i] == tags[indexs][j]:
                        score[indexs] = score[indexs]+1
    return score

def get_index(name, num):
    score=get_score(name)
    re1 = heapq.nlargest(num, score)
    print(re1)
    re2=[0]*num
    for i in range(len(re1)):    
        re2[i] = score.index(re1[i])
        if i>0 and re2[i] == re2[i-1]:
            score[re2[i]]=0
            re2[i] = score.index(re1[i])
    # print(re2)  
    return re1,re2

def recommend(name, num):
    re1,re2=get_index(name,num)
    print("Recommended games:")
    for i in range(len(re1)):
        name=steam.loc[re2[i],"name"]
        print("<{0}> with score:{1}\n".format(name,re1[i]))




steam = load_from_mongo()
# steam = pd.read_csv("D:\Code\DS50\datasets\steam_games2.csv",encoding = "ISO-8859-1")

steam = steam.iloc[0:,1:8]
steam = steam.drop(index = steam[(steam.types == "bundle")].index.tolist())
steam = steam.drop(index = steam[(steam.types == "sub")].index.tolist())
tags=[None]*40788

for indexs in steam.index:
    str = steam.loc[indexs,"popular_tags"]
    if isinstance(str,float):
        steam = steam.drop(index = indexs)
        indexs = indexs -1
    else:
        str = str.split(',')
        tags[indexs] = str

# Input from back-end nodejs
game_name = sys.argv[1]
num = int(sys.argv[2])

#print(recommend(game_name, num))
# Output to the backend
output = str(recommend(game_name, num))
sys.stdout.write(output)
sys.stdout.flush()



