#!/usr/bin/env python3
"""
Created on Mon Feb  7 12:44:04 2022

@author: thor
"""


import numpy as np
import pandas as pd
import json
import Metrica_Viz as mviz

def get_distance(p, q):
    s_sq_difference = 0
    for p_i,q_i in zip(p,q):
        s_sq_difference += (p_i - q_i)**2
    distance = s_sq_difference**0.5
    return distance

def cleanDFName(df5):
    df5['player']=df5['player'].apply(lambda x: x.get('name'))
    df5['play_pattern']=df5['play_pattern'].apply(lambda x: x.get('name'))
    df5['outcome']=df5['outcome'].apply(lambda x: x.get('name'))
    df5['position']=df5['position'].apply(lambda x: x.get('name'))
    df5['team']=df5['team'].apply(lambda x: x.get('name'))
    df5['technique']=df5['technique'].apply(lambda x: x.get('name'))
    df5['type']=df5['type'].apply(lambda x: x.get('name'))
    df5['body_part']=df5['body_part'].apply(lambda x: x.get('name'))
    df5.drop('statsbomb_xg', inplace=True, axis=1)
    df5.drop('freeze_frame', inplace=True, axis=1)
    df5.drop('one_on_one', inplace=True, axis=1)
    df5.drop('redirect', inplace=True, axis=1)
    df5.drop('deflected', inplace=True, axis=1)
    df5.drop('follows_dribble', inplace=True, axis=1)
    df5.drop('saved_off_target', inplace=True, axis=1)
    df5.drop('saved_to_post', inplace=True, axis=1)

def cleanDFID(df5):
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
    pattern_counts = df5["play_pattern"].value_counts()
    outcome_counts = df5["outcome"].value_counts()
    pos_counts = df5["position"].value_counts()
    tech_counts = df5["technique"].value_counts()
    type_counts = df5["type"].value_counts()
    body_counts = df5["body_part"].value_counts()

#fh=open("DTU/02450Toolbox_Python/Data/allshotsLaLiga.json")
fh=open("resources/allshotsLaLiga.json")
data=json.load(fh)
df=pd.DataFrame(data)
df4=pd.concat([df['id'], df['location'], df['timestamp'],df['player'],df['position'],df['team'], df['under_pressure'],df['play_pattern'],df.shot.apply(pd.Series)], axis=1)


cleanDFName(df4)
do_stats(df4)
df4['dist'] = df4.apply(lambda x: get_distance(x.location, x.end_location), axis=1)
fig,ax = mviz.plot_pitch()
