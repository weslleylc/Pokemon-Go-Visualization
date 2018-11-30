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


dfFull=df.merge(types[['Pokemon No.', 'Type 1', 'Type 2']], left_on='pokemonId', right_on='Pokemon No.', how='outer')

columns=pd.get_dummies(dfFull['Type 1'])

terrainTypesDict = {0: "Water", 1: "forest", 2: "forest", 3: "forest", 4: "forest", 5: "forest", 6: "shrublands", 7: "shrublands", 8: "savannas", 9: "savannas", 10: "grasslands", 11: "wetlands", 12: "croplands", 13: "urban",14: "cropland", 15: "ice", 16: "barren"}
df.replace({'terrainType': terrainTypesDict},  inplace=True)
terrainType=pd.get_dummies(df['terrainType'])
columns=columns.astype(bool)
dfFull=dfFull[['pokemonId', 'latitude', 'longitude',
       'terrainType', 'closeToWater', 'city', 'continent', 'weather',
       'temperature', 'windSpeed', 'windBearing', 'pressure',
       'population_density', 'urban', 'suburban', 'midurban', 'rural']]

dfFull[columns.columns]=columns
dfFull[terrainType.columns]=terrainType
dfFull=dfFull[~dfFull.isnull().any(axis=1)]
dfFull['closeToWater']=dfFull['closeToWater'].astype(bool)

corr=dfFull.corr()
