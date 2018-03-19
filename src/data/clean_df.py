# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 10:48:31 2018

@author: Alex
"""

#%% Import packages 
import pandas as pd 
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
    return df

#%% Create columns for standardized text and categorized text
reports.insert(loc=7,column='txtcleaned_water_crossings',value=reports['water_crossings'])
reports.insert(loc=8,column='water_cat',value=0)
reports = standardize_text(reports, "txtcleaned_water_crossings")

#Tokenize your text by separating it into individual words

#Consider combining misspelled or alternately spelled words to a single representation (e.g. “cool”/”kewl”/”cooool”)

#Consider lemmatization (reduce words such as “am”, “are”, and “is” to a common form such as “be”)

#%% 
common_crossing_reports = reports['txtcleaned_water_crossings'].value_counts()

# no comment
# none | none. | n a | none via this route.  | no crossings | na
# no issues | no problems | no issues. | easy | not an issue | all easy | no problem | no problems.
# bridged | all bridged
# rock hoppable | rock hops | rock hopping




#%% 
from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer("english")
stemmer.stem('no issues')
 
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

lemmatizer.lemmatize('hoppable')





