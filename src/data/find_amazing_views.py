# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 00:26:36 2018

@author: Alex
"""

#%% Import packages 
import pandas as pd 
import os
from nltk.tokenize import RegexpTokenizer
import os
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import log_loss
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

#%% Read dataframe 
os.chdir(r'C:\Users\Alex\Documents\GitHub\trail-conditions\data\interim')
df = pd.read_pickle('df_views')

#%% Clean comments column
# All lowercase
df.comments = df.comments.str.lower()
# Replace views with view
df.comments = df.comments.str.replace("views", "view")

#%% Find amazing views 
df.insert(loc=2,column='amazing_view',value=0)
df.loc[df.comments.str.contains('amazing view'),'amazing_view'] = 1
view_count = df[['peak','amazing_view']].groupby(['peak']).sum()
view_count.sort_values(by=['amazing_view'],inplace=True,ascending=False)
