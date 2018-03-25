# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 11:32:51 2018

@author: Alex
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 10:48:31 2018

@author: Alex
"""

#%% Import packages 
import pandas as pd 
import os
from nltk.tokenize import RegexpTokenizer
import os

#%% Read in large dataframe
os.chdir('C:\\Users\\Alex\\Documents\\GitHub\\trail-conditions\\data\\raw')
reports = pd.read_pickle('all_reports')

#%% 
def clean_peaks(df,text_field):
    df[text_field] = df[text_field].str.replace(r"Mt. ", "")
    df[text_field] = df[text_field].str.replace(r"Mt ", "")
    df[text_field] = df[text_field].str.replace(r" Mountain", "")
    df[text_field] = df[text_field].str.replace(r"Mount ", "")
    # Remove state
    df[text_field] = df[text_field].str.replace("NH|ME|VT|MA|RI|CT", "")
    # Remove text in brackets 
    df[text_field] = df[text_field].str.replace("\(.+\)","")
    # Replace and with a comma
    df[text_field] = df[text_field].str.replace(" and ",",")
    # lowercase
    df[text_field] = df[text_field].str.lower()
    return df


#%% Analyze peaks 

# Empty columns
reports.insert(loc=2,column='clean_peaks',value=reports['peaks'])
reports.insert(loc=3,column='peak_tokens',value=0)

# Make tokenizer
comma_space_tokenizer = RegexpTokenizer('\,\s', gaps=True)

# Clean the peaks column
reports = clean_peaks(reports, "clean_peaks")
reports["peak_tokens"] = reports["clean_peaks"].apply(comma_space_tokenizer.tokenize)

#%% Make a snowshoes column
reports['snowshoes'] = reports.equipment.str.find('Snowshoes')>=0

#%% Expand out peaks 
# Code adapated from: https://stackoverflow.com/questions/32468402/how-to-explode-a-list-inside-a-dataframe-cell-into-separate-rows
reports.reset_index(inplace=True)
rows = []
_ = reports.apply(lambda row: [rows.append([row['entry_id'], pt, row['date_of_hike'], row['snowshoes'], row['comments']]) 
                         for pt in row.peak_tokens], axis=1)
column_list = ['entry_id','peak_tokens','date_of_hike','snowshoes','comments']
reports_new = pd.DataFrame(rows, columns=column_list).set_index(['entry_id', 'peak_tokens'])

#%% 

