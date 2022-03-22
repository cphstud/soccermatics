#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 12:44:04 2022

@author: thor
"""

import pymongo
import numpy as np
import pandas as pd
import json
import Metrica_Viz as mviz
from matplotlib import pyplot as plt
from pymongo import UpdateOne
import pprint as pp

def get_distance(p, q):
    s_sq_difference = 0
    for p_i,q_i in zip(p,q):
        s_sq_difference += (p_i - q_i)**2
    distance = s_sq_difference**0.5
    return distance

def inside_trigon( s, a, b=(120,36), c=(120,44)):

    as_x = s[0]-a[0];
    as_y = s[1]-a[1];
    
    s_ab = (b[0]-a[0])*as_y-(b[1]-a[1])*as_x > 0;
    
    if ((c[0]-a[0])*as_y-(c[1]-a[1])*as_x > 0 == s_ab):
        return False;
    
    if (c[0]-b[0])*(s[1]-b[1])-(c[1]-b[1])*(s[0]-b[0]) > 0 != s_ab:
        return False;
    return True;

def area(x1, y1, x2, y2, x3, y3):
 
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1)
                + x3 * (y1 - y2)) / 2.0)
 
 

def isInside(pos,pos2):
    x1=pos[0]
    y1=pos[1]
    x=pos2[0]
    y=pos2[1]
    x2=120
    y2=44
    x3=120
    y3=36
 
    # Calculate area of triangle ABC
    A = area(x1, y1, x2, y2, x3, y3)
 
    # Calculate area of triangle PBC
    A1 = area(x, y, x2, y2, x3, y3)
     
    # Calculate area of triangle PAC
    A2 = area(x1, y1, x, y, x3, y3)
     
    # Calculate area of triangle PAB
    A3 = area(x1, y1, x2, y2, x, y)
     
    # Check if sum of A1, A2 and A3
    # is same as A
    if(A == A1 + A2 + A3):
        return True
    else:
        return False
    

def cleanDFNameP(df5):
    df5['player']=df5['player'].apply(lambda x: x.get('name'))
    df5['play_pattern']=df5['play_pattern'].apply(lambda x: x.get('name'))
    #df5['outcome']=df5['outcome'].apply(lambda x: x.get('name'))
    df5['position']=df5['position'].apply(lambda x: x.get('name'))
    df5['team']=df5['team'].apply(lambda x: x.get('name'))
    df5['technique']=df5['technique'].apply(lambda x: x.get('name'))
    df5['type']=df5['type'].apply(lambda x: x.get('name'))
    df5['body_part']=df5['body_part'].apply(lambda x: x.get('name'))
    df5['gender']=df5['gender'].apply(lambda x: x.get('name'))
    df5['pass_outcome']=df5['pass.outcome']
    df5['pass_length']=df5['pass.length']
    df5.drop('statsbomb_xg', inplace=True, axis=1)
    df5.drop('freeze_frame', inplace=True, axis=1)
    df5.drop('one_on_one', inplace=True, axis=1)
    df5.drop('redirect', inplace=True, axis=1)
    df5.drop('deflected', inplace=True, axis=1)
    df5.drop('follows_dribble', inplace=True, axis=1)
    df5.drop('saved_off_target', inplace=True, axis=1)
    df5.drop('saved_to_post', inplace=True, axis=1)


def cleanDFName(df5):
    df5['player']=df5['player'].apply(lambda x: x.get('name'))
    df5['play_pattern']=df5['play_pattern'].apply(lambda x: x.get('name'))
    df5['outcome']=df5['outcome'].apply(lambda x: x.get('name'))
    df5['position']=df5['position'].apply(lambda x: x.get('name'))
    df5['team']=df5['team'].apply(lambda x: x.get('name'))
    df5['technique']=df5['technique'].apply(lambda x: x.get('name'))
    df5['type']=df5['type'].apply(lambda x: x.get('name'))
    df5['body_part']=df5['body_part'].apply(lambda x: x.get('name'))
    df5['gender']=df5['gender'].apply(lambda x: x.get('name'))
    
    
    df5.drop('statsbomb_xg', inplace=True, axis=1)
    #df5.drop('freeze_frame', inplace=True, axis=1)
    df5.drop('one_on_one', inplace=True, axis=1)
    df5.drop('redirect', inplace=True, axis=1)
    df5.drop('deflected', inplace=True, axis=1)
    df5.drop('follows_dribble', inplace=True, axis=1)
    df5.drop('saved_off_target', inplace=True, axis=1)
    df5.drop('saved_to_post', inplace=True, axis=1)

def cleanDFID(df4):
    df4['player']=df4['player'].apply(lambda x: x.get('id'))
    df4['play_pattern']=df4['play_pattern'].apply(lambda x: x.get('id'))
    df4['outcome']=df4['outcome'].apply(lambda x: x.get('id'))
    df4['position']=df4['position'].apply(lambda x: x.get('id'))
    df4['team']=df4['team'].apply(lambda x: x.get('id'))
    df4['technique']=df4['technique'].apply(lambda x: x.get('id'))
    df4['type']=df4['type'].apply(lambda x: x.get('id'))
    df4['body_part']=df4['body_part'].apply(lambda x: x.get('id'))
    df4.drop('statsbomb_xg', inplace=True, axis=1)
    df4.drop('freeze_frame', inplace=True, axis=1)

def do_stats(df):
    pattern_counts = df["play_pattern"].value_counts()
    outcome_counts = df["outcome"].value_counts()
    pos_counts = df["position"].value_counts()
    tech_counts = df["technique"].value_counts()
    type_counts = df["type"].value_counts()
    body_counts = df["body_part"].value_counts()

def get_angle(shot):
    #handle the "wrong" y-axis
    x=120-shot[0]
    y=40-(shot[1])
    angle = np.arctan(7.32*x /(x**2 + y**2 - (7.32/2)**2))
    return np.degrees(angle)

def prepDFShot(df4):
    dfretVal=pd.concat(
            [df4['_id'], 
             df4['location'], 
             df4['timestamp'],
             df4['player'],
             df4['position'],
             df4['team'], 
             df4['under_pressure'], 
             df4['timestamp'],
             df4['gender'],
             df4['play_pattern'],
             df4.shot.apply(pd.Series)], axis=1
             )
    return dfretVal

def doCalc(row):
    print("CALLED ...\n\n")
    pp.pprint(f"ROW {row[0]}")
    playerpos=row['location']
    opponent_in_frame=[]
    mates_in_frame=[]
    num_of_players=[]
    for player in row['freeze_frame']:
        if (player['teammate']==False):
            opponent_in_frame.append(player)
        else:
            mates_in_frame.append(player)
    pcnt=0
    for player in opponent_in_frame:
        if isInside(playerpos,player['location']):
            pcnt+=1
    print(f"{row['player']} has {pcnt} in tri")
    p1={row['player']:pcnt}
    num_of_players.append(p1)
    
    for player in mates_in_frame:
        pcnt=0
        p1={}
        for opplayer in opponent_in_frame:
            if isInside(player['location'],opplayer['location']):
                pcnt+=1
        print(f"{player['player']} has {pcnt} in tri")
        #p1={player['player']:pcnt}
        num_of_players.append(p1)
      
        
  
    

#fh=open("DTU/02450Toolbox_Python/Data/allshotsLaLiga.json")
#data=json.load(fh)
client = pymongo.MongoClient("mongodb://127.0.0.1:27017/statsbomb?retryWrites=true&w=majority")
db=client.statsbomb
coll=db.get_collection("matches")
cursorF=coll.find({"type.name":"Shot", "gender.name":"female"})
dfF=pd.DataFrame(list(cursorF))
cursorM=coll.find({"type.name":"Shot", "gender.name":"male"}).limit(9000)
dfM=pd.DataFrame(list(cursorM))
frames=[dfF,dfM]
dfAll=pd.concat(frames)
dfAllPrep=prepDFShot(dfAll)
cleanDFName(dfAllPrep)
testDfAll=dfAllPrep.head(5)

testDfAllFreez=testDfAll['freeze_frame']
pp.pprint(testDfAllFreez[0])

oneShotFrame=testDfAllFreez[0]
testDfAll.apply(lambda row: doCalc(row), axis = 1)





cursorp=coll.find({"type.name":"Pass"})

dfpasses=pd.DataFrame(list(cursorp))
cleanDFNameP(dfpasses)

testdf=dfpasses.head(5)
onpass=testdf['pass']
dfpassesM=dfpasses[dfpasses['gender']=='male']

# passes group on player



df4=pd.DataFrame(list(cursor))
dft=df4.head(5)
df5=pd.concat([df4['_id'], df4['location'], df4['timestamp'],df4['player'],df4['position'],df4['team'], df4['under_pressure'], df4['timestamp'],df4['gender'],df4['play_pattern'],df4.shot.apply(pd.Series)], axis=1)
#print(row.get('dist'))
    #query="updateOne({'_id':'"+row.get('_id')+"'},{'$set': {'distance':"+str(row.get('dist'))+"}})"
    #query="{ updateOne : { \"filter\": { \"_id\" : \""+row.get('_id')+"\" }, \"update\" : {\"$set\": { \"distance\" : "+str(row.get('dist'))+ " }}}}"
    #query="{ updateOne : { \"filter\": { \"_id\" : \""+row.get('_id')+"\" }, \"update\" : {\"$set\": { \"distance\" : "+str(row.get('dist'))+ " }}}}"
    

dfpclean=pd.concat([dfpasses['_id'], dfpasses['location'], dfpasses['timestamp'],dfpasses['player'],dfpasses['position'],dfpasses['team'], dfpasses['under_pressure'], dfpasses['timestamp'],dfpasses['gender'],dfpasses['play_pattern'],dfpasses['pass'].apply(pd.Series)], axis=1)
cleanDFName(df5)
do_stats(df5)
outcome_counts = df5["outcome"].value_counts()
gender_counts = df5["gender"].value_counts()
df5['dist'] = df5.apply(lambda x: get_distance(x.location, x.end_location), axis=1)
df5['angle'] = df5.apply(lambda x: get_angle(x.location), axis=1)
players=df5['player'].value_counts()
#fig,ax = mviz.plot_pitch()
fig,ax=plt.subplots()
X=np.linspace(0,70,6)

ax.scatterplot(X,df4['dist'].loc[:5])
plt.show()

newdf=df4[['dist','angle','_id']]

updates=[]
for _, row in newdf.iterrows():
    updates.append(UpdateOne({ "_id" : "2a621cec-fbee-484c-8289-91c7e48e396c" }, {"$set": { "distance" : 23 }},upsert=True))
coll.bulk_write(updates) 
