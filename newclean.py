#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 12:44:04 2022

@author: thor
"""
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
import pymongo
import numpy as np
import pandas as pd
import json
import Metrica_Viz as mviz
from FCPython import createPitch
from matplotlib import pyplot as plt
from pymongo import UpdateOne
import pprint as pp


def get_distance(p, q):
    s_sq_difference = 0
    for p_i,q_i in zip(p,q):
        s_sq_difference += (p_i - q_i)**2
    distance = s_sq_difference**0.5
    return distance

def area(x1, y1, x2, y2, x3, y3):
    cal_area=0
    cal_area=((0.5)*(x1*(y2-y3)+x2*(y3-y1)+x3*(y1-y2)))
    return abs(cal_area)

    '''
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1)
                + x3 * (y1 - y2)) / 2.0)
    '''
 
 

def isInside(pos,pos2):
    retVal=False
    print(f"pos {pos} and pos2 {pos2}")
    x1=pos[0]
    y1=pos[1]
    x=pos2[0]
    y=pos2[1]
    x2=120.0
    y2=44.0
    x3=120.0
    y3=36.0
 
    # Calculate area of triangle ABC
    print(f"call area area({x1},{y1},{x2},{y2},{x3},{y3})")
    A = area(x1, y1, x2, y2, x3, y3)
 
    # Calculate area of triangle PBC
    A1 = area(x, y, x2, y2, x3, y3)
     
    # Calculate area of triangle PAC
    A2 = area(x1, y1, x, y, x3, y3)
     
    # Calculate area of triangle PAB
    A3 = area(x1, y1, x2, y2, x, y)
     
    # Check if sum of A1, A2 and A3
    # is same as A
    sum=A1+A2+A3
    if(A == sum):
        retVal=True
    #else:
     #   return False
    print(f"returns {retVal} {A} sum {sum} on {A1} {A2} {A3} ")
    return retVal


def get_dist_pass(p1,p2,p3):
    d = np.abs(norm(np.cross(p2-p1, p1-p3)))/norm(p2-p1)


def get_angle(shot):
    #handle the "wrong" y-axis
    x=120-shot[0]
    y=40-(shot[1])
    angle = np.arctan(7.32*x /(x**2 + y**2 - (7.32/2)**2))
    return np.degrees(angle)

def to_meters(pos):
    a=pos[0]
    b=pos[1]
    sign=1
    # 30 skal blive til 90
    if a < 60:
        a=(abs(a-60))+60
    if b > 40:
        sign=-1
     
    x=abs(60-a)*0.9144 
    y=abs(40-b)*0.9144*sign 
    return (x,y)
    

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
    #fig,ax = createPitch(120,80,'yards','gray')
    fig, ax=mviz.plot_pitch(fak=1.5)
    p1={}
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
    pp.pprint(opponent_in_frame[0])
    col="yellow"
    name=row["player"]["name"]
    for oplayer in opponent_in_frame:
        #plot_frame(to_meters(playerpos),to_meters(oplayer['location']),ax,col,name,oplayer['player']['name'])
        plot_frame(to_meters(playerpos),to_meters(oplayer['location']),ax,col,name,"SOP")
        print(f"\t isInside({playerpos},{player['location']})")
        if isInside(playerpos,oplayer['location']):
            pcnt+=1
    print(f"Shooter {row['player']['name']} has {pcnt} in tri")
    #p1={row['player']:pcnt}
    num_of_players.append(p1)
    col="red"
    for player in mates_in_frame:
        pcnt=0
        p1={}
        for opplayer in opponent_in_frame:
            print(f"\t Others isInside({player['location']},{opplayer['location']})")
            if isInside(player['location'],opplayer['location']):
                pcnt+=1
        print(f"{player['player']} has {pcnt} in tri")
        #plot_frame(to_meters(player['location']),to_meters(opplayer['location']),ax,col,player['player']['name'],opplayer['player']['name'])
        #plot_frame(to_meters(player['location']),to_meters(opplayer['location']),ax,col,player['name'],opplayer['name'])
        plot_frame(to_meters(player['location']),to_meters(opplayer['location']),ax,col,player['player']['name'],"OP")
        
        #p1={player['player']:pcnt}
        num_of_players.append(p1)
        
def plot_frame(player,opp,ax,col,name1,name2):
    tcol="yellow"
    if name2 == "SOP":
        tcol="red"
    ax.plot(player[0],player[1],marker="o", markersize=9, markeredgecolor="blue", markerfacecolor=col) 
    ax.annotate(name1,player) 
    
    ax.plot(opp[0],opp[1],marker="o", markersize=6, markeredgecolor="blue", markerfacecolor="blue") 
    ax.annotate(name2,opp)
    ax.plot(*zip(player, to_meters((120,36)), to_meters((120,44)), player),  color=tcol)
        
  
#eters_per_yard = 0.9144 
  
    
#fh=open("DTU/02450Toolbox_Python/Data/allshotsLaLiga.json")
#data=json.load(fh)
client = pymongo.MongoClient("mongodb://127.0.0.1:27017/statsbomb?retryWrites=true&w=majority")
db=client.statsbomb
coll=db.get_collection("events")
cursorF=coll.find({"type.name":"Shot", "gender":"female"})
dfF=pd.DataFrame(list(cursorF))    

cursorM=coll.find({"type.name":"Shot", "gender":"male", "player.name":  {"$ne":"Lionel Andrés Messi Cuccittini"}}).limit(9000)
dfM=pd.DataFrame(list(cursorM))
frames=[dfF,dfM]
dfAll=pd.concat(frames)
dfAllPrep=prepDFShot(dfAll)
#ff=dfAllPrep.head()
#cleanDFNameImproved(dfAllPrep)
#cols=dfAllPrep.columns
testDfAll=dfAllPrep.head(3)

testDfAll.apply(lambda row: doCalc(row), axis = 1)

# plot the pitch