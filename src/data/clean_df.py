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

#%% Clean text data 
#Code adaptated from https://github.com/hundredblocks/concrete_NLP_tutorial/blob/master/NLP_notebook.ipynb
def standardize_text(df, text_field):
    # Prefix with r so that special characters aren't treated differently i.e. \n would be treated as \ and n rather than a new line
    # No comment for blank entries 
    df[text_field] = df[text_field].str.replace("(?<![\s\S])\xa0(?![\s\S])","no comment")
    #Remove words that are not relevant, such as “@” twitter mentions or urls
    df[text_field] = df[text_field].str.replace(r"http\S+", "")
    df[text_field] = df[text_field].str.replace(r"http", "")
    df[text_field] = df[text_field].str.replace(r"@\S+", "")
    df[text_field] = df[text_field].str.replace(r"@", "at")
    # Replace " and ' with inches and feet 
    df[text_field] = df[text_field].str.replace(r"\'", " feet")
    df[text_field] = df[text_field].str.replace(r"\"", " inches")
    # Replace digit-digit with digit to digit
    df[text_field] = df[text_field].str.replace("(?<=\d)-(?=\d)"," to ")
    df[text_field] = df[text_field].str.replace("(?<=[a-zA-Z]) -(?=\s[a-zA-Z])",". ")
    #Remove all irrelevant characters such as any non alphanumeric characters
    df[text_field] = df[text_field].str.replace("[^A-Za-z0-9]", " ")
    #Convert all characters to lowercase, in order to treat words such as “hello”, “Hello”, and “HELLO” the same
    df[text_field] = df[text_field].str.lower()
    # Remove trailing whitespace 
    df[text_field] = df[text_field].str.replace("\s+(?!\S)", "")

    return df

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
    

#%% Clean water crossings
    
# Create columns for standardized text and categorized text
reports.insert(loc=7,column='txtcleaned_water_crossings',value=reports['water_crossings'])
reports.insert(loc=8,column='water_class',value=0)

#%% Clean text 
reports = standardize_text(reports, "txtcleaned_water_crossings")
 
# Tokenize text 
space_tokenizer = RegexpTokenizer(r'\w+')
reports["water_tokens"] = reports["txtcleaned_water_crossings"].apply(space_tokenizer.tokenize)

# Look at most common crossing reports 
common_crossing_reports = reports['txtcleaned_water_crossings'].value_counts()




sum(reports.water_crossings.str.count('tough'))


#%% 
#Consider combining misspelled or alternately spelled words to a single representation (e.g. “cool”/”kewl”/”cooool”)

#Consider lemmatization (reduce words such as “am”, “are”, and “is” to a common form such as “be”)

#from nltk.stem.snowball import SnowballStemmer
#
#stemmer = SnowballStemmer("english")
#stemmer.stem('no issues')
# 
#from nltk.stem import WordNetLemmatizer
#
#lemmatizer = WordNetLemmatizer()
#
#lemmatizer.lemmatize('hoppable')


#%% Analyze peaks 

# Empty columns
reports.insert(loc=2,column='clean_peaks',value=reports['peaks'])
reports.insert(loc=3,column='peak_tokens',value=0)

# Make tokenizer
comma_space_tokenizer = RegexpTokenizer('\,\s', gaps=True)

# Clean the peaks column
reports = clean_peaks(reports, "clean_peaks")
reports["peak_tokens"] = reports["clean_peaks"].apply(comma_space_tokenizer.tokenize)

# Make an attempt column
reports['attempt'] = reports.peaks.str.find('attempt')>=0


#%% Extract state

# Make tokenizer, make state column, extract state, convert to string
state_tokenizer = RegexpTokenizer('NH|ME|VT|MA|RI|CT')
reports.insert(loc=3,column='state',value=0)
reports["state"] = reports["peaks"].apply(state_tokenizer.tokenize)
reports["state"] = reports["state"].apply(''.join)

# Correct duplicate states 
reports.state = reports.state.str.replace("NHNH","NH")
reports.state = reports.state.str.replace("CTCT","CT")
reports.state = reports.state.str.replace("MEME","ME")
reports.state = reports.state.str.replace("MAMA","MA")
reports.state = reports.state.str.replace("MARI","MA")

#%% Function for classifying water crossings
def classify_crossings(df):
    
    # None list 
    none_list = ['none','n a','none via this route','no crossings','na','no water crossings','none on this route']
    
    # Easy list 
    easy_list = ['no issue','no_issues','no problem','no problems','easy','not an issue','all easy','rock hoppable','rock hops','rock hopping','bridged','all bridged','none of note','minor','easy rock hops','all rock hoppable','frozen','easily rock hopped','easily crossed','all frozen']
    
    # Difficult list 
    difficult_list = ['']
    
    # Impassable list 
    impossible_list = ['']
    
    # Set classifications
    df.loc[df.txtcleaned_water_crossings == 'no comment', 'water_class'] = 'no comment'
    df.loc[df.txtcleaned_water_crossings.isin(none_list), 'water_class'] = 'none'
    df.loc[df.txtcleaned_water_crossings.isin(easy_list), 'water_class'] = 'easy'
    df.loc[df.txtcleaned_water_crossings.isin(difficult_list), 'water_class'] = 'difficult'
    df.loc[df.txtcleaned_water_crossings.isin(impossible_list), 'water_class'] = 'impassable'

    return df

#%% Classify crossings
reports = classify_crossings(reports)


# Describe labels 
reports.txtcleaned_water_crossings.describe()
reports.water_class.describe()

# Definitely over samples impossible crossings but still lots of other reasons why people can't cross 
attempt_df = reports.loc[reports.attempt == 1]

#%% Label tricky/difficult data 
# List words like difficult
difficult_list = ['tricky','difficult','tough','hard']

# Make a dataframe of rows that contain the above words 
tricky_df = reports.loc[reports.txtcleaned_water_crossings.str.contains('|'.join(difficult_list)),'txtcleaned_water_crossings']

# Select random rows from this dataframe 
sample_rows = tricky_df.sample(100)

# Ask for input to asign
sample_rows = sample_rows.to_frame()
sample_rows.insert(loc = 1, column='water_class',value=0)

for idx, row in sample_rows.iterrows():
    print('\n' + row['txtcleaned_water_crossings']) 
    assignment = int(input('1 = no comment, 2 = none, 3 = easy, 4 = difficult, 5 = impassable. Pick class:\t'))
    class_list = ['no comment','none','easy','difficult','impassable']
    sample_rows.loc[idx,'water_class'] = class_list[assignment-1]
    reports.loc[idx,'water_class'] = class_list[assignment-1]
    
# Save the dataframe 


# Add it to the water_class column in reports dataframe 
    
#%% 
impassable_list = ['impassable','impossible']

# Make a dataframe of rows that contain the above words 
impassable_df = reports.loc[reports.txtcleaned_water_crossings.str.contains('|'.join(impassable_list)),'txtcleaned_water_crossings']


#%% Label impossible data 



#%% Write dataframe 
os.chdir(r'C:\Users\Alex\Documents\GitHub\trail-conditions\data\interim')
reports.to_pickle('cleaned_reports')


