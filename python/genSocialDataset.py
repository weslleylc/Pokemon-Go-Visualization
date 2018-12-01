#encoding:utf-8
import pandas as pd;
import numpy as np;
import matplotlib.pyplot as plt;
import seaborn as sns; sns.set()

import geopandas as gpd;	

class Income:
	counties = '';
	idManu = 0;
	income = 0.0;
	unemployment = 0.0;

dtIncome = pd.read_csv('./kaggle_income.csv', sep=",").set_index('id');
dtCities = pd.read_csv('./county_names.csv', sep=",").set_index('id');
dtUneplo = pd.read_csv('./unemployment_names.csv', sep=",");
dtPokemo = pd.read_csv('./pokemon_appears_US.csv', sep=",");
dtPokemo.dropna(inplace=True);

pokeCities = np.unique(dtPokemo['counties']);
icomCities = np.unique(dtIncome['County']);
manuCities = np.unique(dtCities['name']);

PN = [];
IM = [];
UN = [];
IN = [];
for pCity in pokeCities:
	iData = dtIncome[dtIncome['County'] == pCity]['Mean'];
	if (len(iData) > 0):
		income = np.mean(iData);
	else:
		income = 0;
	uneplo = np.mean(dtUneplo[dtUneplo['name'] == pCity]['rate']);
	idManu = int(np.mean(dtUneplo[dtUneplo['name'] == pCity]['id']));
	print(idManu);
	PN.append(pCity);
	IM.append(idManu);
	UN.append(uneplo);
	IN.append(income);
d = {'pokeCity':PN, 'idManu':IM, 'uneployment':UN, 'income':IN};
newData = pd.DataFrame(data = d);
newData.to_csv('./socialData.csv', sep=',');

