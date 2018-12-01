# -*- coding: utf-8 -*-

import os
from pathlib import Path
directory=Path(os.getcwd())
data_folder = directory.parent
data_folder = data_folder/'data'
import pandas as pd
import numpy as np


df = pd.read_csv(data_folder/'pokemon_appears_US.csv', ',', engine='python')
if df.columns[0] == 'Unnamed: 0':
    df = df.drop([df.columns[0]],axis=1)
    
types = pd.read_csv(data_folder/'pokemon_list.csv', ',', engine='python')
if types.columns[0] == 'Unnamed: 0.1':
    types = types.drop([types.columns[0]],axis=1)

terrainTypesDict = {0: "Water", 1: "forest", 2: "forest", 3: "forest", 4: "forest", 5: "forest", 6: "shrublands", 7: "shrublands", 8: "savannas", 9: "savannas", 10: "grasslands", 11: "wetlands", 12: "croplands", 13: "urban",14: "cropland", 15: "ice", 16: "barren"}
df.replace({'terrainType': terrainTypesDict},  inplace=True)

dfFull=df.merge(types[['Pokemon No.', 'Type 1']], left_on='pokemonId', right_on='Pokemon No.', how='outer')

typesPokemon=pd.get_dummies(dfFull['Type 1'])
typesPokemon=typesPokemon.astype(bool)

terrainType=pd.get_dummies(dfFull['terrainType'])
terrainType=terrainType.astype(bool)

dfFull.drop(['Type 1','terrainType', 'Pokemon No.','continent'],axis=1,inplace=True)

dfFull[typesPokemon.columns]=typesPokemon
dfFull[terrainType.columns]=terrainType

dfFull=dfFull[~dfFull.isnull().any(axis=1)]
dfFull[['closeToWater','urban','suburban','midurban','rural']]=dfFull[['closeToWater','urban','suburban','midurban','rural']].astype(bool)
dfFull['weather']=dfFull['weather'].astype('str')
corr=dfFull.corr()