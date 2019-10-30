#%%
# %load ../usefulScritps/initialSetup_v3.py
# %load ../usefulScritps/initialSetup_v2.py
import pandas as pd
import datetime as dt
import numpy as np
import xlsxwriter as xlsx


f =  pd.read_csv(r'./data/Asset_LA.csv', low_memory=False)
f.drop_duplicates(subset='AssetID', keep='first', inplace= True)

try:
    f.KW_Load = f.KW_Load.str.replace(',','.').apply(float)
except:
    f.KW_Load = f.KW_Load.apply(float)
	


f.columns


cities = ['HORTOLANDIA (BMM)']
hasParentAsset = ~(f.Parent_Asset_ID.isna()) | ~(f.Parent_Asset_ID.isnull())
isInCity = f.City.isin(cities)
notDecommissioned = (f.Asset_Operational_Status.str.contains('Active'))
notRecycled = ~(f.Asset_Operational_Status.str.contains('Recy'))

# %%
f = f.loc[isInCity & notDecommissioned]

f.KW_Load =f.KW_Load.fillna(0)  

# %%
f.to_csv('assetsNlyte.csv')