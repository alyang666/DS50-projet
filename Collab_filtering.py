import pandas as pd
import numpy as np
import random
import sys
import pymongo
from collections import Counter

from sklearn.metrics.pairwise import pairwise_distances 


def load_from_mongo():
    client = pymongo.MongoClient("mongodb+srv://jeremy:root@cluster0.5ei45.mongodb.net/database?retryWrites=true&w=majority")
    db = client.database
    collection = db['steam-200k']
    df= pd.DataFrame(list(collection.find()))
    del df['_id']
    return df

def predict(ratings, similarity, type='user'):
    if type == 'user':
        mean_user_rating = ratings.mean(axis=1)
        #We use np.newaxis so that mean_user_rating has same format as ratings
        ratings_diff = (ratings - mean_user_rating[:, np.newaxis])
        pred = mean_user_rating[:, np.newaxis] + similarity.dot(ratings_diff) / np.array([np.abs(similarity).sum(axis=1)]).T
    elif type == 'item':
        pred = ratings.dot(similarity) / np.array([np.abs(similarity).sum(axis=1)])
    return pred


def find_diff(userid1,userid2):
    game1=clean_data[clean_data["userid"]==userid1]["gameIdx"].tolist()
    game2=clean_data[clean_data["userid"]==userid2]["gameIdx"].tolist()
    diff = set(game2).difference(set(game1))
    return diff  

def sort_game(game_diff,useridx,similar_indices,num):
    game_rating=[None]*len(game_diff)
    for i in range(len(game_diff)):
        game_rating[i]=user_game_interactions[similar_indices[0]][list(game_diff)[i]]
    game_rating=np.array(game_rating)
    sort=game_rating.argsort()[::-1]
    for i in range(num):        
        print(idx2game[list(game_diff)[sort[i]]])

def recommendation(userid,prediction,num):
    idx=user2idx[userid]
    similar_indices = user_prediction[idx].argsort()[::-1]
    userid2=idx2user[similar_indices[0]]
    game_diff=find_diff(userid,userid2)
    if len(game_diff)>=num:
        sort_game(game_diff,similar_indices[0],similar_indices,num)
    else:
        num=num-len(game_diff)
        userid2=idx2user[similar_indices[1]]
        game_diff=find_diff(userid,userid2)
        sort_game(game_diff,similar_indices[1],similar_indices,num)

# steam_data = pd.read_csv('D:\Code\DS50\datasets\steam-200k.csv\steam-200k.csv')
steam_data = load_from_mongo()

steam_data.isnull().values.any()

steam_data['Hours_Played'] = steam_data['hoursplayed'].astype('float32')

steam_data.loc[(steam_data['behavior'] == 'purchase') & (steam_data['hoursplayed'] == 1.0), 'Hours_Played'] = 0
steam_data['Hours_Played'] = steam_data['hoursplayed'].astype('float32')
steam_data.loc[(steam_data['behavior'] == 'purchase') & (steam_data['hoursplayed'] == 1.0), 'Hours_Played'] = 0
clean_data = steam_data.drop_duplicates(['userid', 'game'], keep = 'last').drop(['behavior', 'hoursplayed'], axis = 1)
clean_data = clean_data.sort_values(['userid', 'game', 'Hours_Played'])

n_users = len(clean_data.userid.unique())
n_games = len(clean_data.game.unique())
clean_data['rating'] = clean_data['Hours_Played']

for i in range(128804):
    if clean_data.iloc[i,2] > 100:
        clean_data.iloc[i,3]=5
    elif 50< clean_data.iloc[i,2] <= 100:
        clean_data.iloc[i,3]=4 
    elif 30< clean_data.iloc[i,2] <= 50:
        clean_data.iloc[i,3]=3 
    elif 10< clean_data.iloc[i,2] <= 30: 
        clean_data.iloc[i,3]=2 
    elif 1< clean_data.iloc[i,2] <= 10: 
        clean_data.iloc[i,3]=1 
    else:
        clean_data.iloc[i,3]=0

user_counter = Counter()
for user in clean_data.userid.tolist():
    user_counter[user] +=1

game_counter = Counter()
for game in clean_data.game.tolist():
    game_counter[game] += 1

# Create the dictionaries to convert user and games to idx and back
user2idx = {user: i for i, user in enumerate(clean_data.userid.unique())}
idx2user = {i : user for user, i in user2idx.items()}

game2idx = {game: i for i, game in enumerate(clean_data.game.unique())}
idx2game = {i: game for game, i in game2idx.items()}

user_idx = clean_data['userid'].apply(lambda x: user2idx[x]).values
game_idx = clean_data['gameIdx'] = clean_data['game'].apply(lambda x: game2idx[x]).values
rating = clean_data['rating'].values

# Using a sparse matrix will be more memory efficient and necessary for larger dataset, 
# but this works for now.
zero_matrix = np.zeros(shape = (n_users, n_games)) # Create a zero matrix
user_game_pref = zero_matrix.copy()
user_game_pref[user_idx, game_idx] = 1 # Fill the matrix will preferences (bought)

user_game_interactions = zero_matrix.copy()
# Fill the confidence with (hours played)
# Added 1 to the hours played so that we have min. confidence for games bought but not played.
user_game_interactions[user_idx, game_idx] = rating


user_similarity = pairwise_distances(user_game_interactions, metric='cosine')
item_similarity = pairwise_distances(user_game_interactions.T, metric='cosine')

user_prediction = predict(user_game_interactions, user_similarity, type='user')
item_prediction = predict(user_game_interactions, item_similarity, type='item')

# Create a random as index and find the userid with it
rand_idx = random.randint(1, 12393)
user_id_random = idx2user[rand_idx]
# print(user_id_random)
output = str(recommendation(user_id_random,user_prediction,8))
sys.stdout.write(output)
sys.stdout.flush()





