# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 10:14:44 2018

@author: Alex
"""

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
    df.loc[df.clean_water_crossings == 'no comment', 'water_class'] = 'no comment'
    df.loc[df.clean_water_crossings.isin(none_list), 'water_class'] = 'none'
    df.loc[df.clean_water_crossings.isin(easy_list), 'water_class'] = 'easy'
    df.loc[df.clean_water_crossings.isin(difficult_list), 'water_class'] = 'difficult'
    df.loc[df.clean_water_crossings.isin(impossible_list), 'water_class'] = 'impassable'

    return df

#%% Classify crossings
reports = classify_crossings(reports)


# Describe labels 
reports.clean_water_crossings.describe()
reports.water_class.describe()

# Definitely over samples impossible crossings but still lots of other reasons why people can't cross 
attempt_df = reports.loc[reports.attempt == 1]

#%% Label tricky/difficult data 
# List words like difficult
difficult_list = ['tricky','difficult','tough','hard']

# Make a dataframe of rows that contain the above words 
tricky_df = reports.loc[reports.clean_water_crossings.str.contains('|'.join(difficult_list)),'clean_water_crossings']

# Select random rows from this dataframe 
sample_rows = tricky_df.sample(100)

# Ask for input to asign
sample_rows = sample_rows.to_frame()
sample_rows.insert(loc = 1, column='water_class',value=0)

for idx, row in sample_rows.iterrows():
    print('\n' + row['clean_water_crossings']) 
    assignment = int(input('1 = no comment, 2 = none, 3 = easy, 4 = difficult, 5 = impassable. Pick class:\t'))
    class_list = ['no comment','none','easy','difficult','impassable']
    sample_rows.loc[idx,'water_class'] = class_list[assignment-1]
    reports.loc[idx,'water_class'] = class_list[assignment-1]
    
# Save the dataframe 


# Add it to the water_class column in reports dataframe 
    
#%% 
impassable_list = ['impassable','impossible']

# Make a dataframe of rows that contain the above words 
impassable_df = reports.loc[reports.clean_water_crossings.str.contains('|'.join(impassable_list)),'clean_water_crossings']


#%% Label impossible data 
