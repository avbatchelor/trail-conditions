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
from sklearn import metrics

#%% Read dataframe 
os.chdir(r'C:\Users\Alex\Documents\GitHub\trail-conditions\data\interim')
df = pd.read_pickle('df_for_snowshoe_classification')
df.drop(columns = ['datetime'],inplace=True)

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

#%% Baseline 0 - most common class 
# For all the data 
snowshoe_freq = snowshoes.mean()

# For the training data 
y_pred = np.ones(len(y_test))*round(y_train.mean())
print(log_loss(y_test,y_pred))


#%% Baseline 1 - mean of y_train (i.e. overall probability of needing snowshoes)
y_pred = np.ones(len(y_test))*y_train.mean()
print(log_loss(y_test,y_pred))

#%% Baseline 2 - predict mean by month 
snowshoe_prob = df[['month','snowshoes'][msk]].groupby(['month']).mean()
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


#%% Measure performance
#def measure_model_performance(y_test,y_pred):
   
# Select probability and round
if y_pred.ndim == 2:
    y_comp = np.round(y_pred[:,1])
else:
    y_comp = np.round(y_pred)
    
 # Confusion matrix 
from confusion_matrix import compute_and_plot_confusion_matrix as cm
cm(y_test,y_comp,['0','1'])

# Accuracy score 
metrics.accuracy_score(y_test,y_comp)

#%% Make df to look at which classifications are hardest 
comp_df = df[~msk]
comp_df['prediction'] = y_pred[:,1]

#%% Plot weights 
weights = np.squeeze(l.coef_)
weights = weights.tolist()
weight_df = pd.DataFrame(weights,columns =['weight'])
weight_df['input_var'] = list(x_test)
weight_df.set_index('input_var',inplace=True)
weight_df.sort_values(by=['weight'],inplace=True)
weight_df.plot.bar()
#plt.figure()
#plt.bar(list(x_test),weights)
plt.xticks(rotation='vertical')
fig = plt.gcf()
fig.set_size_inches(10, 5, forward=True)
fig.ylabel('weight')

