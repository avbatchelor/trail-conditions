# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 09:58:05 2018

@author: Alex
"""

#%% Import modules 
import os
import glob
os.chdir('C:\\Users\\Alex\\Documents\\GitHub\\trail-conditions\\src\\data')
import trailscrape as ts
import pandas as pd
import numpy as np

#%% Make intermediate dataframes 
# cd to path for raw data 
raw_data_path = 'C:\\Users\\Alex\\Documents\\GitHub\\trail-conditions\\data\\raw\\'

# Loop through webpages and make dfs 
increment = 100
start_inds = np.arange(1,35000,increment)
for start_ind in start_inds:
    end_ind = start_ind + increment
    df = ts.make_df(start_ind,end_ind)
    filename = "trail_df_" + str(start_ind) + '_' + str(end_ind)
    os.chdir(raw_data_path)
    df.to_pickle(filename)

#%% Make large dataframe
df_list = []              
for file in glob.glob("trail*"):
   df_list.append(pd.read_pickle(file))
   big_df = pd.concat(df_list)
big_df.sort_index(inplace=True)
big_df.to_pickle('all_reports')

#%% Read in large dataframe
big_test_df = pd.read_pickle('all_reports')
