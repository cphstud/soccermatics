import numpy as np
import pandas as pd

fh=open("resources/onegoal.json")
data=json.load(fh)
df=pd.DataFrame(data)

df4 = pd.concat([df['id'], df['location'], df['timestamp'],df['player'],df['position'],df['team'], df['under_pressure'],df['play_pattern'],df.shot.apply(pd.Series)], axis=1)
#df4['player'].apply(lambda x: x.get('id'))
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
