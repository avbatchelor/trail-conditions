# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 18:42:12 2018

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
df = pd.read_pickle('df_for_snowshoe_classification')

#%% Separate out snowshoes var 
snowshoes = df.snowshoes.copy()

#%% One hot encoding 
dummy_df = df.copy()
dummy_df.drop(columns='snowshoes',inplace=True)
dummy_df["month"] = dummy_df["month"].astype('category')
dummy_df = pd.get_dummies(dummy_df)

#%% Split test and training data 
# Code adpated from: https://blog.myyellowroad.com/using-categorical-data-in-machine-learning-with-python-from-dummy-variables-to-deep-category-66041f734512
msk = np.random.rand(len(df)) < 0.8
x_train = dummy_df[msk].iloc[:,:]
x_test = dummy_df[~msk].iloc[:,:]
y_train = snowshoes[msk]
y_test = snowshoes[~msk]

#%% Baseline 1 - mean of y_train (i.e. overall probability of needing snowshoes)
y_pred = np.ones(len(y_test))*y_train.mean()
print(log_loss(y_test,y_pred))

#%% Baseline 2 - predict mean by month 
snowshoe_prob = df[['month','snowshoes']].groupby(['month']).mean()
test_month_list = df.month[~msk].tolist()
y_pred = snowshoe_prob.snowshoes[test_month_list]
print(log_loss(y_test,y_pred))

#%% Create models
l = LogisticRegression()
r = RandomForestClassifier(n_estimators=25,max_depth=10)

#%% Logistic regression 
l.fit(x_train,y_train)
y_pred = l.predict_proba(x_test)
print(log_loss(y_test,y_pred))

#%% Random forest
r.fit(x_train,y_train)
y_pred = r.predict_proba(x_test)
print(log_loss(y_test,y_pred))

#%% Hike prob
peak_snow_df = df.loc[df.month.isin([1,2,3])]
peak_prob = peak_snow_df[['peak','snowshoes']].groupby(['peak']).mean()

#%% Figure setup
mng = plt.get_current_fig_manager()
mng.full_screen_toggle()
plt.show() 

#%% Make snowshoes prob by peak figure 
plt.figure()
peak_prob.sort_values(by=['snowshoes'],inplace=True)
peak_prob.plot.bar()
fig = plt.gcf()
ax = plt.gca()
ax.legend_.remove()
fig.set_size_inches(10, 5, forward=True)
plt.xlabel('Mountain name',fontsize=12)
plt.ylabel('Probability of needing snowshoes',fontsize=12)
plt.legend('')
plt.title('Probability of needing snowshoes during Jan, Feb and March',fontsize=20)
plt.ylim((0,1))
plt.tight_layout()
plt.savefig(r'C:\Users\Alex\Documents\GitHub\trail-conditions\reports\figures\prob_snowshoes_by_peak.svg')

#%% 
snowshoe_prob.plot.bar()
plt.xlabel('Month',fontsize=12)
plt.ylabel('Probability of needing snowshoes',fontsize=12)
plt.title('Probability of needing snowshoes',fontsize=20)
plt.legend('')
fig.set_size_inches(10, 5, forward=True)
plt.ylim((0,1))
plt.tight_layout()
plt.savefig(r'C:\Users\Alex\Documents\GitHub\trail-conditions\reports\figures\prob_snowshoes_by_month.svg')
