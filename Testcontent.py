import pandas as pd
import numpy as np
import heapq
import string
import sys

def recommend(game_id,num):
    gid=game_id+2000000  # locate the gameid in file.csv
    idx=steam[steam["gameid"]== gid].index.tolist()[0]
    id_list = []
    for i in range(num):
        index=idx+i+1
        gameid=steam.loc[index,"gameid"]
        gamescore=steam.loc[index,"score"]
        #print("<{0}> with score:{1}\n".format(gameid,gamescore))
        id_list.append(gameid)
    print(id_list)


steam = pd.read_csv("https://github.com/alyang666/DS50/blob/main/datastes/steam_id_score.csv")

game_id = int(sys.argv[1])
num = int(sys.argv[2])

output = recommend(game_id, num)
sys.stdout.write(output)

















