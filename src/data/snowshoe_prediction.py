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
import matplotlib.pyplot as plt

#%% Function for cleaning peak column 
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
    # Replace apostophes 
    df[text_field] = df[text_field].str.replace("\'", "")
    #Remove all irrelevant characters such as any non alphanumeric characters
    df[text_field] = df[text_field].str.replace("[^a-z\s\,]", " ")
    # Remove trailing commas
    df[text_field] = df[text_field].str.replace("\,(?!\s+\S)", "")
    # remove multiple whitespaces 
    df[text_field] = df[text_field].str.replace("\s+", " ")
    # Remove trailing whitespace 
    df[text_field] = df[text_field].str.replace("\s+(?!\S)", "")
    # Remove preceding whitespace 
    df[text_field] = df[text_field].str.replace("(?<!\S)\s+", "")
    return df


#%% Analyze peaks 
os.chdir('C:\\Users\\Alex\\Documents\\GitHub\\trail-conditions\\data\\raw')
reports = pd.read_pickle('all_reports')

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

#%% Make a row for each peak 
# Code adapated from: https://stackoverflow.com/questions/32468402/how-to-explode-a-list-inside-a-dataframe-cell-into-separate-rows
reports.reset_index(inplace=True)
rows = []
_ = reports.apply(lambda row: [rows.append([row['entry_id'], pt, row['date_of_hike'], row['snowshoes'], row['comments']]) 
                         for pt in row.peak_tokens], axis=1)
column_list = ['entry_id','peak_tokens','date_of_hike','snowshoes','comments']
reports_new = pd.DataFrame(rows, columns=column_list).set_index(['entry_id', 'peak_tokens'])
reports_new.reset_index(inplace=True)

# Remove trailing whitespace 
reports_new['peak_tokens'] = reports_new['peak_tokens'].str.replace("\s+(?!\S)", "")

#%% Make a month column
reports_new['datetime'] = pd.to_datetime(reports_new.date_of_hike)
reports_new['month'] = reports_new['datetime'].dt.month

##%% 
#plt.show()
#snow_df = reports_new[['month','snowshoes']].copy()
#by_month = snow_df.groupby(snow_df.month).sum()
#by_month.plot()
#
##%%
#trail_df = reports_new[['peak_tokens','snowshoes']].copy()
#by_trail = trail_df.groupby(trail_df.peak_tokens).sum()
#by_trail.plot()
#
##%% Are all trails used equally in winter?
#trail_freq_df = reports_new[['peak_tokens','month','snowshoes']].copy()
#by_trail_freq = trail_freq_df.groupby(['month','peak_tokens']).sum()
#by_trail.plot()

#%% Get a list of the peaks
peak_list = reports_new[['peak_tokens','snowshoes']].groupby(['peak_tokens']).count()
peak_list.reset_index(inplace=True)

#%% Load 4000 footer mountain list and determine if a mountain is a four thousand footer, if so make sure that row has a standardized name for that mountain 
os.chdir(r'C:\Users\Alex\Documents\GitHub\trail-conditions\data\raw')
mtn_list = pd.read_csv("nh_48_list.csv")
mtn_list.mountain = mtn_list.mountain.str.lower()
# Replace apostophes 
mtn_list.mountain = mtn_list.mountain.str.replace("\'", "")
mtn_list["mtn_tokens"] = mtn_list.mountain
mtn_list["mtn_tokens"] = mtn_list["mtn_tokens"].apply(comma_space_tokenizer.tokenize)

# Insert 
reports_new.insert(loc=7,column='four_footer',value=0)
reports_new.insert(loc=8,column='clean_peak_names',value='')

for idx, mountain in mtn_list.mtn_tokens.iteritems():
    if len(mountain) == 1:
        # Look through peak_tokens in reports_new, 
        reports_new.loc[reports_new.peak_tokens.str.contains(''.join(mountain)),'four_footer'] = 1
        reports_new.loc[reports_new.peak_tokens.str.contains(''.join(mountain)),'clean_peak_names'] = ' '.join(mountain)
        
for idx, mountain in mtn_list.mtn_tokens.iteritems():
    if len(mountain) == 2:
        # Look through peak_tokens in reports_new, 
        reports_new.loc[(reports_new.peak_tokens.str.contains(''.join(mountain[0]))) & (reports_new.peak_tokens.str.contains(''.join(mountain[1]))),'four_footer'] = 1
        reports_new.loc[(reports_new.peak_tokens.str.contains(''.join(mountain[0]))) & (reports_new.peak_tokens.str.contains(''.join(mountain[1]))),'clean_peak_names'] = ' '.join(mountain)

#%% Get a new list of peaks to make sure there are only 48 
peak_list = class_df[['peak','snowshoes']].groupby(['peak']).count()

#%% Make a dataframe just for snowshoe classification 
class_df = reports_new[['clean_peak_names','month','snowshoes','four_footer']].copy()
class_df = class_df.loc[class_df.four_footer == 1]
class_df.drop(columns='four_footer',inplace=True)
class_df.rename(index=str, columns={"clean_peak_names": "peak"}, inplace=True)

# Save it 
os.chdir(r'C:\Users\Alex\Documents\GitHub\trail-conditions\data\interim')
class_df.to_pickle('df_for_snowshoe_classification')

#%% Make a dataframe for finding great views 



