# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 15:40:04 2018

@author: Alex

Exploratory analysis of snowshoe data 

"""

#%% Import packages 
import pandas as pd 
import os
from nltk.tokenize import RegexpTokenizer
import os
import matplotlib.pyplot as plt

#%% Read dataframe 
os.chdir(r'C:\Users\Alex\Documents\GitHub\trail-conditions\data\interim')
df = pd.read_pickle('df_for_snowshoe_classification')

#%% Figure setup
mng = plt.get_current_fig_manager()
mng.full_screen_toggle()
plt.show() 

#%% Hike prob
peak_snow_df = df.loc[df.month.isin([1,2,3])]
peak_prob = peak_snow_df[['peak','snowshoes']].groupby(['peak']).mean()

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
snowshoe_prob = df[['month','snowshoes']].groupby(['month']).mean()
snowshoe_prob.plot.bar()
plt.xlabel('Month',fontsize=12)
plt.ylabel('Probability of needing snowshoes',fontsize=12)
plt.title('Probability of needing snowshoes for each month',fontsize=20)
plt.legend('')
fig = plt.gcf()
fig.set_size_inches(10, 5, forward=True)
plt.ylim((0,1))
plt.tight_layout()
plt.savefig(r'C:\Users\Alex\Documents\GitHub\trail-conditions\reports\figures\prob_snowshoes_by_month.svg')

#%% Group by day of the week 
df['day'] = df['datetime'].dt.dayofweek
day_prob = df[['day','snowshoes']].groupby(['day']).mean()
day_prob.plot.bar()
plt.xlabel('Month',fontsize=12)
plt.ylabel('Probability of needing snowshoes',fontsize=12)
plt.title('Probability of needing snowshoes for each month',fontsize=20)
plt.legend('')
fig = plt.gcf()
fig.set_size_inches(10, 5, forward=True)
plt.ylim((0,1))
plt.tight_layout()
#plt.savefig(r'C:\Users\Alex\Documents\GitHub\trail-conditions\reports\figures\prob_snowshoes_by_month.svg')

#%% Group by day of the week 
df['year'] = df['datetime'].dt.year
year_prob = df[['year','snowshoes']].groupby(['year']).mean()
year_prob.plot.bar()
plt.xlabel('Month',fontsize=12)
plt.ylabel('Probability of needing snowshoes',fontsize=12)
plt.title('Probability of needing snowshoes for each month',fontsize=20)
plt.legend('')
fig = plt.gcf()
fig.set_size_inches(10, 5, forward=True)
plt.ylim((0,1))
plt.tight_layout()